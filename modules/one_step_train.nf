
process ONE_STEP_TRAIN {

    container 'alessiovignoli3/model-check:dataload_training'
    label 'process_low'
    tag "${fasta}"

    input:
    tuple val(dir_ID), path(fasta)

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
    launch_check_training.py -i tmp -bs 1,10 --modules_version True 
    """

}
