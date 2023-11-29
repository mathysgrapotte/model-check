
process  JASPAR_TO_HOMER {

    container "alessiovignoli3/model-check:pwm2homer" 
    label 'process_low'
    tag "${jaspar_pwm_file}"

    input:
    path jaspar_pwm_file

    output:
    path "${out_name}", emit: homer_matrix
    stdout emit: standardout

    script:
    out_name = "${jaspar_pwm_file.baseName}.homer"
    """
    pwm2homer.py -i ${jaspar_pwm_file} -o ${out_name} -f jaspar 
    """

    stub:
    out_name = "${jaspar_pwm_file.baseName}.homer"
    """
    pwm2homer.py -i ${jaspar_pwm_file} -o ${out_name} -f jaspar --modules_version True
    """

}
