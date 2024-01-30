
process HOMER_FIND_MOTIF {

    // the following is to handle both singularity and docker while using a biocontainer
    container "${ workflow.containerEngine == 'singularity' && !task.ext.singularity_pull_docker_container ?
        'https://depot.galaxyproject.org/singularity/homer:4.11--pl526hc9558a2_3' :
        'quay.io/biocontainers/homer:4.11--pl526hc9558a2_3' }"                                                   // homer 4.11 and perl 5.26.2
    
    // the outdir has to be the one the user specify plus stuff that makes it run unique
    publishDir (
        path: ( "${params.outdir}/${workflow.runName}_" + "${workflow.start}".replaceAll('[-:]', '_').split('\\.')[0] +  "/${dir_ID}/filter_${filter_num}"),
        mode: "${params.publish_dir_mode}",
        overwrite: true 
    )
    label "process_medium"
    tag "${dir_ID}-${filter_num}"

    input:
    tuple val(motif_line_ID), val(fasta_ID), val(filter_num), val(filter_len), path(positve_set), path(negative_set)

    output:
    path( "homerResults.html" ), emit: positve_set
    stdout emit: standardout

    script:
    dir_ID   = motif_line_ID
    if ( fasta_ID != '') {
        dir_ID = motif_line_ID + "_" + fasta_ID 
    }
    """
    findMotifs.pl ${positve_set} fasta . -fasta ${negative_set} -len ${filter_len}
    """

    stub:
    dir_ID   = motif_line_ID
    if ( fasta_ID != '') {
        dir_ID = motif_line_ID + "_" + fasta_ID 
    }
    """
    # print versions 
    perl -X --version | grep 'This is perl'
    echo homer version (10-24-2019)

    # create the expected dirs and outputs
    mkdir -p homerResults
    """
}
