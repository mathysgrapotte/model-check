
process PLOT_MODEL_WEIGHTS {

    publishDir path: "${params.outdir}/${dir_ID}", mode: "${params.publish_dir_mode}", overwrite: true
    container 'alessiovignoli3/model-check:dataload_training'
    label 'process_low'
    tag "${dir_ID}"

    input:
    tuple val(dir_ID), path(architecture), path(best_model)

    output:
    path "*.png", emit: weights_plots  
    stdout emit: standardout

    script:
    """
    launch_plot_model_weights.py -hp ${architecture} -p ${best_model} -o ${dir_ID}
    """

    stub:
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
