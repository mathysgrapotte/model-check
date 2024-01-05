
process HOMER_FIND_MOTIF {

    // the following is to handle both singularity and docker while using a biocontainer
    container "${ workflow.containerEngine == 'singularity' && !task.ext.singularity_pull_docker_container ?
        'https://depot.galaxyproject.org/singularity/homer:4.11--pl526hc9558a2_3' :
        'quay.io/biocontainers/homer:4.11--pl526hc9558a2_3' }"                                                   // homer 4.11 and perl 5.26.2
    label "process_medium"
    tag "${dir_ID}-${filter_num}"

    input:
    tuple val(dir_ID), val(filter_num), val(filter_len), path(positve_set), path(negative_set)

    output:
    //path( "*positive*.fasta" ), emit: positve_set
    stdout emit: standardout

    script:
    """
    findMotifs.pl ${positve_set} fasta tmp -fasta ${negative_set} -len ${filter_len}
    """

    stub:
    """
    # print versions 
    perl -X --version | grep 'This is perl'
    echo homer version (10-24-2019)

    # create the expected dirs and outputs
    mkdir -p tmp/homerResults
    """
}
