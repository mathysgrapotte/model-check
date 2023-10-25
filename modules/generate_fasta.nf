
process GENERATE_FASTA {

    container "alessiovignoli3/model-check:generate_fasta"
    label "process_low"

    output:
    path "*", emit: dna_fasta
    stdout emit: standardout  

    script:
    def args = task.ext.args ?: ""
    def prefix = task.ext.prefix ?: "ENCODED"
    """
    launch_fasta_generate.py -o ${prefix} ${args} 
    """

    stub:
    def prefix = task.ext.prefix ?: "ENCODED"
    """
    #launch_fasta_generate.py -o ${prefix} -sl 100 -m aattttttttttttaa -t 5 -u 0 -ns 5 --modules_version True
    launch_fasta_generate.py -o ${prefix} -sl 100 -m bubba -j BUBBA
    """

}
