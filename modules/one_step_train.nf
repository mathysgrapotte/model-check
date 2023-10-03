
process ONE_STEP_TRAIN {

    container 'alessiovignoli3/model-check:ray_torch_sklearn'
    label 'process_low'
    tag "${fasta}"

    input:
    path fasta

    output:
    stdout emit: standardout

    script:
    def args = task.ext.args ?: ''
    """
    launch_check_training.py -i ${fasta} ${args}
    """

    stub:
    // first reduce the input sequernces to 10 in total so that is faster to run
    """
    awk '/^>/{n++;if(n<=10){print}} n>10{exit} !/^>/'  ${fasta} > tmp
    launch_check_training.py -i tmp -bs 3 --modules_version True 
    """

}
