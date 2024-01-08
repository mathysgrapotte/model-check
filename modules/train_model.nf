
process TRAIN_MODEL {

    publishDir path: "${params.outdir}/${dir_ID}", mode: "${params.publish_dir_mode}", overwrite: true
    container 'alessiovignoli3/model-check:dataload_training'
    label 'process_medium_high'
    tag "${dir_ID}"

    input:
    tuple val(dir_ID), path(fasta)
    val passed_check                         // used just to enforce dependency from the check train step

    output:
    tuple val(dir_ID), path("*.pt"), emit: best_model
    tuple val(dir_ID), path("train_statistics.txt"), emit: statistics
    tuple val(dir_ID), path("architecture.txt"), emit: architecture
    stdout emit: standardout

    script:
    def args = task.ext.args ?: ''
    """
    launch_training.py -i ${fasta} ${args} 1>train_statistics.txt
    """

    stub:
    """
    launch_training.py -i ${fasta} -e 2 --modules_version True 1>train_statistics.txt
    head -n 4 train_statistics.txt 
    """

}
