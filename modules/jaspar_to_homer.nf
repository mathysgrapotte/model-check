
process  JASPAR_TO_HOMER {

    container "luisas/python:bio3" 
    label 'process_medium'
    tag "${jaspar_pwm_file}"

    input:
    path jaspar_pwm_file

    output:
    //path "*.pt", emit: best_model
    stdout emit: standardout

    script:
    def args = task.ext.args ?: ''
    """
    echo bubba
    """

    stub:
    """
    #pwm2homer.py -i ${jaspar_pwm_file} -o tmp -f jaspar --modules_version
    """

}
