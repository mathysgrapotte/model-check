
process CONVOLUTION_SCAN {

    container 'alessiovignoli3/model-check:dataload_training'
    label 'process_low'
    tag "${}"

    input:
    path fasta
    path hyperparameter
    path parameter

    output:
    path( "*positive*.fasta" ), emit: positve_set
    path( "*negative*.fasta" ), emit: negative_set
    stdout emit: standardout

    script:
    """
    launch_convolution_scan.py -i ${fasta} -hp ${hyperparameter} -p ${parameter} -o PLACEHOLDER_
    """

    stub:
    """
    launch_convolution_scan.py -i ${fasta} -hp ${hyperparameter} -p ${parameter} -o PLACEHOLDER_ --modules_version True
    """
}
