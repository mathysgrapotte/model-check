
process HOMER_FIND_JASPAR_MOTIF {

    // the following is to handle both singularity and docker while using a biocontainer
    container "${ workflow.containerEngine == 'singularity' && !task.ext.singularity_pull_docker_container ?
        'https://depot.galaxyproject.org/singularity/homer:4.11--pl526hc9558a2_3' :
        'biocontainers/homer:4.11--pl526hc9558a2_3' }"                                                   // homer 4.11 and perl 5.26.2
    label "process_medium"
    tag "${id}"

    input:
    tuple val(id), val(filter_len), path(positve_set), path(negative_set)
    val jaspar_db

    output:
    //path( "*positive*.fasta" ), emit: positve_set
    stdout emit: standardout

    script:
    """
    echo bubba
    """

    stub:
    """
    findMotifs.pl ${positve_set} fasta tmp -fasta ${negative_set} -len ${filter_len} -norevopp -mcheck ${jaspar_db} -mknown ${jaspar_db}
    """
}
