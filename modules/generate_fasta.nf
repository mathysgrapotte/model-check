
process GENERATE_FASTA {

    container "alessiovignoli3/model-check:generate_fasta"
    label "process_low"
    tag "${motif_file}"

    input:
    tuple val(dir_ID), path(motif_file)
    val type_of_file_flag

    output:
    path "${dir_ID}", emit: dna_dir, type: 'dir'
    stdout emit: standardout  

    script:
    def args = task.ext.args ?: ""
    def prefix = task.ext.prefix ?: "generated.fasta"
    """
    launch_fasta_generate.py ${type_of_file_flag} ${motif_file} -o ${prefix} ${args} 
    mkdir ${dir_ID}
    mv  ${prefix}  ${dir_ID}
    """

    stub:
    def args = task.ext.args ?: ""
    def prefix = task.ext.prefix ?: "generated.fasta"
    """
    launch_fasta_generate.py ${type_of_file_flag} ${motif_file} -o ${prefix} ${args} --modules_version True
    mkdir ${dir_ID}
    mv  ${prefix}  ${dir_ID}
    """

}
