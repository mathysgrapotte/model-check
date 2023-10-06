
process TRAIN_MODEL {

    container 'alessiovignoli3/model-check:ray_torch_sklearn'
    label 'process_medium_high'
    tag "${fasta}"

    input:
    path fasta

    output:
    stdout emit: standardout

    script:
    def args = task.ext.args ?: ''
    """
    launch_training.py -i ${fasta} ${args}
    """

    stub:
    // first reduce the input sequernces to 10 in total so that is faster to run
    """
    awk '/^>/{n++;if(n<=10){print}} n>10{exit} !/^>/'  ${fasta} > tmp
    launch_training.py -i tmp -bs 1,10 -e 1 --modules_version True
    """

}
