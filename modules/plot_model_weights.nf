
process PLOT_MODEL_WEIGHTS {

    // the outdir has to be the one the user specify plus stuff that makes it run unique
    publishDir (
        path: "${params.outdir}/${workflow.runName}_" + "${workflow.start}".replaceAll('[-:]', '_').split('\\.')[0] +  "/${dir_ID}",
        mode: "${params.publish_dir_mode}",
        overwrite: true
    )
    container 'alessiovignoli3/model-check:dataload_training'
    label 'process_low'
    tag "${dir_ID}"

    input:
    tuple val(motif_line_ID), val(fasta_ID), path(architecture), path(best_model)

    output:
    path "*.png", emit: weights_plots  
    stdout emit: standardout

    script:
    dir_ID   = motif_line_ID
    if ( fasta_ID != '') {
        dir_ID = motif_line_ID + "_" + fasta_ID
    }
    """
    launch_plot_model_weights.py -hp ${architecture} -p ${best_model} -o ${dir_ID}
    """

    stub:
    dir_ID   = motif_line_ID
    if ( fasta_ID != '') {
        dir_ID = motif_line_ID + "_" + fasta_ID
    }
    """
    #!/usr/bin/env python3
     
    import sys
    import torch

    # print module versions and a fake image 
    print('python :', sys.version, '\\n', 'torch :', torch.__version__)

    with open('placeholder.png', 'w') as PNG:
        PNG.write('Hello world, you have run stub-run mode. no plot here, go home.')
    """
}
