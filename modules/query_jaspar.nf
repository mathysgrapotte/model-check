
process QUERY_JASPAR {

    container "python@sha256:9b009a025fa0c270a1617086d74bde1f7015fdcb8a8447aca14ec0de78d99f74" // Python 3.10 slim-bullseye
    label "process_low"

    input:
    path jaspar_motif

    output:
    //path "*", emit: dna_fasta
    stdout emit: standardout

    script:
    """
    echo bubba
    """

    stub:
    //def args = task.ext.args ?: ""
    //def prefix = task.ext.prefix ?: "generated.fasta"
    """
    echo ${jaspar_motif}
    """

}
