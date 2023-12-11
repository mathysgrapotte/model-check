
process GENERATE_FROM_FASTA {

    container "alessiovignoli3/model-check:generate_fasta"
    label "process_low"
    tag "${motif_file}"

    input:
    tuple val(dir_ID), path(motif_file), path(base_fasta)
    val type_of_file_flag

    output:
    tuple val(dir_ID), path("${dir_ID}/${prefix}"), emit: dna_dir
    stdout emit: standardout

    script:
    def args = task.ext.args ?: ""
    prefix = task.ext.prefix ? task.ext.prefix : "generated.fasta"
    """
    launch_fasta_generate.py ${type_of_file_flag} ${motif_file} -o ${prefix} -f ${base_fasta} ${args}
    mkdir ${dir_ID}
    mv  ${prefix}  ${dir_ID}
    """

    stub:
    def args = task.ext.args ?: ""
    prefix = task.ext.prefix ? task.ext.prefix : "generated.fasta"
    """
    launch_fasta_generate.py ${type_of_file_flag} ${motif_file} -o ${prefix} -f ${base_fasta} ${args} --modules_version True
    mkdir ${dir_ID}
    mv  ${prefix}  ${dir_ID}
    """

}
