
process GENERATE_FASTA {

    container "alessiovignoli3/model-check:generate_fasta"
    label "process_low"

    input:
    path motif_file
    val type_of_file_flag

    output:
    path "*", emit: dna_fasta
    stdout emit: standardout  

    script:
    def args = task.ext.args ?: ""
    def prefix = task.ext.prefix ?: "generated.fasta"
    """
    launch_fasta_generate.py ${type_of_file_flag} ${motif_file} -o ${prefix} ${args} 
    """

    stub:
    def args = task.ext.args ?: ""
    def prefix = task.ext.prefix ?: "generated.fasta"
    """
    launch_fasta_generate.py ${type_of_file_flag} ${motif_file} -o ${prefix} ${args} --modules_version True
    touch tmp
    """

}
