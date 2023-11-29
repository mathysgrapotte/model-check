
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
}