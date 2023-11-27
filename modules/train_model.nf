
process TRAIN_MODEL {

    container 'alessiovignoli3/model-check:dataload_training'
    label 'process_medium_high'
    tag "${fasta}"

    input:
    path fasta

    output:
    path "*.pt", emit: best_model
    path "train_statistics.txt", emit: statistics
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
