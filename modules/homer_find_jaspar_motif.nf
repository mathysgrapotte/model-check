
process HOMER_FIND_JASPAR_MOTIF {

    container 'mgibio/homer@sha256:8a71ac97e2c862d84842a4c9d52a49aa7804790952c286f3219d411b6fce7b4f'   // 
    label "process_medium"
    tag "${id}"

    input:
    tuple val(id), path(positve_set), path(negative_set)
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
    echo ${id} ${positve_set} ${negative_set} ${jaspar_db}
    """
}
