
process GENERATE_FROM_FASTA {

    container "alessiovignoli3/model-check:generate_fasta"
    label "process_low"

    input:
    path motif_file
    path base_fasta
    val type_of_file_flag

    output:
    path "*", emit: dna_fasta
    stdout emit: standardout

    script:
    def args = task.ext.args ?: ""
    def prefix = task.ext.prefix ?: "generated.fasta"
    """
    launch_fasta_generate.py ${type_of_file_flag} ${motif_file} -o ${prefix} -f ${base_fasta} ${args}
    """

    stub:
    def args = task.ext.args ?: ""
    def prefix = task.ext.prefix ?: "generated.fasta"
    """
    launch_fasta_generate.py ${type_of_file_flag} ${motif_file} -o ${prefix} -f ${base_fasta} ${args} --modules_version True
    """

}
