
process CONVOLUTION_SCAN {

    container 'alessiovignoli3/model-check:dataload_training'
    label 'process_low'
    tag "${dir_ID}"

    input:
    tuple val(dir_ID), path(fasta), path(hyperparameter), path(parameter)

    output:
    path( "*positive*.fasta" ), emit: positve_set
    path( "*negative*.fasta" ), emit: negative_set
    stdout emit: standardout

    script:
    """
    # the output prefix is appended with 2 _ for splitting reason later in the pipeline
    launch_convolution_scan.py -i ${fasta} -hp ${hyperparameter} -p ${parameter} -o "${dir_ID}__"
    """

    stub:
    """
    # the output prefix is appended with 2 _ for splitting reason later in the pipeline
    launch_convolution_scan.py -i ${fasta} -hp ${hyperparameter} -p ${parameter} -o "${dir_ID}__" --modules_version True
    """
}
