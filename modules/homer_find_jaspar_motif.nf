
process HOMER_FIND_JASPAR_MOTIF {

    // the following is to handle both singularity and docker while using a biocontainer
    container "${ workflow.containerEngine == 'singularity' && !task.ext.singularity_pull_docker_container ?
        'https://depot.galaxyproject.org/singularity/homer:4.11--pl526hc9558a2_3' :
        'biocontainers/homer:4.11--pl526hc9558a2_3' }"                                                   // homer 4.11 and perl 5.26.2
    publishDir path: "${params.outdir}/${dir_ID}/filter_${filter_num}", mode: "${params.publish_dir_mode}", overwrite: true
    label "process_medium"
    tag "${dir_ID}-${filter_num}"

    input:
    tuple val(dir_ID), val(filter_num), val(filter_len), path(positve_set), path(negative_set), path(jaspar_db)

    output:
    path( "homerResults" ),type: 'dir', emit: positve_set
    stdout emit: standardout

    script:
    """
    findMotifs.pl ${positve_set} fasta . -fasta ${negative_set} -len ${filter_len} -norevopp -mcheck ${jaspar_db} -mknown ${jaspar_db}
    """

    stub:
    """
    # print versions
    perl -X --version | grep 'This is perl'
    echo 'homer version (10-24-2019)'

    # create the expected dirs and outputs
    mkdir -p homerResults
    """
}
