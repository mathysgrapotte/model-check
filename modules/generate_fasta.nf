
process GENERATE_FASTA {

    container "alessiovignoli3/model-check:generate_fasta"
    label "process_low"
    tag "${dir_ID}"

    input:
    tuple val(dir_ID), path(motif_file)
    val type_of_file_flag

    output:
    // the following has an addtional value that is empty to unify to the number of values in the generate_from_fasta output
    tuple val(dir_ID), val(''), path("${dir_ID}/${prefix}"), emit: dna_dir
    stdout emit: standardout  

    script:
    def args = task.ext.args ?: ""
    prefix = task.ext.prefix ?: "generated.fasta"
    """
    launch_fasta_generate.py ${type_of_file_flag} ${motif_file} -o ${prefix} ${args} 
    mkdir ${dir_ID}
    mv  ${prefix}  ${dir_ID}
    """

    stub:
    def args = task.ext.args ?: ""
    prefix = task.ext.prefix ?: "generated.fasta"
    """
    launch_fasta_generate.py ${type_of_file_flag} ${motif_file} -o ${prefix} ${args} --modules_version True
    mkdir ${dir_ID}
    mv  ${prefix}  ${dir_ID}
    """

}
