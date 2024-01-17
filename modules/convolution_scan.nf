
process CONVOLUTION_SCAN {

    container 'alessiovignoli3/model-check:dataload_training'
    label 'process_low'
    tag "${dir_ID}"

    input:
    tuple val(motif_line_ID), val(fasta_ID), path(fasta), path(hyperparameter), path(parameter)

    output:
    tuple val(motif_line_ID), val(fasta_ID), path( "*positive*.fasta" ), emit: positve_set
    tuple val(motif_line_ID), val(fasta_ID), path( "*negative*.fasta" ), emit: negative_set
    stdout emit: standardout

    script:
    dir_ID   = motif_line_ID + "_" + fasta_ID
    """
    # the output prefix is appended with 2 _ for splitting reason later in the pipeline
    launch_convolution_scan.py -i ${fasta} -hp ${hyperparameter} -p ${parameter} -o "${dir_ID}-"
    """

    stub:
    dir_ID   = motif_line_ID + "_" + fasta_ID
    """
    # the output prefix is appended with 2 _ for splitting reason later in the pipeline
    launch_convolution_scan.py -i ${fasta} -hp ${hyperparameter} -p ${parameter} -o "${dir_ID}-" --modules_version True
    """
}
