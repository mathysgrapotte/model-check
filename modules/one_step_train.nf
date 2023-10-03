
process ONE_STEP_TRAIN {

    container 'clearlinux/numpy-mp:latest'
    label 'process_low'
    tag "${fasta}"

    input:
    path fasta

    output:
    stdout emit: standardout

    script:
    def args = task.ext.args ?: ''
    """
    echo 'bubba' 
    """

    stub:
    """
    launch_check_training.py -i ${fasta} -bs 3 
    echo 'bubba'
    """

}
