
process GENERATE_FROM_FASTA {

    container "alessiovignoli3/model-check:generate_fasta"
    label "process_low"
    tag "${dir_ID}"

    input:
    tuple val(motif_line_ID), val(fasta_ID), path(motif_file), path(base_fasta)
    val type_of_file_flag

    output:
    tuple val(motif_line_ID), val(fasta_ID), path("${dir_ID}/${prefix}"), emit: dna_dir
    stdout emit: standardout

    script:
    def args = task.ext.args ?: ""
    prefix   = task.ext.prefix ? task.ext.prefix : "generated.fasta"
    dir_ID   = motif_line_ID + "_" + fasta_ID
    """
    launch_fasta_generate.py ${type_of_file_flag} ${motif_file} -o ${prefix} -f ${base_fasta} ${args}
    mkdir ${dir_ID}
    mv  ${prefix}  ${dir_ID}
    """

    stub:
    def args = task.ext.args ?: ""
    prefix = task.ext.prefix ? task.ext.prefix : "generated.fasta"
    dir_ID   = motif_line_ID + "_" + fasta_ID
    """
    launch_fasta_generate.py ${type_of_file_flag} ${motif_file} -o ${prefix} -f ${base_fasta} ${args} --modules_version True
    mkdir ${dir_ID}
    mv  ${prefix}  ${dir_ID}
    """

}
