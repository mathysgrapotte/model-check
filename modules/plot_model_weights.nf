
process PLOT_MODEL_WEIGHTS {

    container 'alessiovignoli3/model-check:dataload_training'
    label 'process_low'

    input:
    path architecture
    path best_model

    output:
    path "*.png", emit: weights_plots  

    script:
    """
    launch_plot_model_weights.py -hp ${architecture} -p ${best_model} -o ''
    """

    stub:
    """
    #!/usr/bin/env python3
   
    # print module versions and a fake image 
    print('python :', sys.version, '\n', 'torch :', torch.__version__)

    with open('placeholder.png', 'w') as PNG:
        PNG.write('Hello world, you have run stub-run mode. no plot here, go home.')
    """
}
