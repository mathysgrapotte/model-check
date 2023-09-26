
process GENERATE_FASTA {

    container 'numpy'

    output:
    stdout emit: standardout  

    script:
    def args = task.ext.args ?: ''
    def prefix = task.ext.prefix ?: "ENCODED"
    """
    launch_fasta_generate.py -o ${prefix} ${args} 
    """

    stub:
    def args = task.ext.args ?: ''
    def prefix = task.ext.prefix ?: "ENCODED"
    """
    echo -o ${prefix} ${args}
    """

}
