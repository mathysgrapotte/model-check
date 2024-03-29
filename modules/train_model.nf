
process TRAIN_MODEL {

    // the outdir has to be the one the user specify plus stuff that makes it run unique
    publishDir (
        path: "${params.outdir}/${workflow.runName}_" + "${workflow.start}".replaceAll('[-:]', '_').split('\\.')[0] +  "/${dir_ID}",
        mode: "${params.publish_dir_mode}", 
        overwrite: true 
    )
    container 'alessiovignoli3/model-check:dataload_training'
    label 'process_medium_high'
    tag "${dir_ID}"

    input:
    tuple val(motif_line_ID), val(fasta_ID), path(fasta)
    val passed_check                         // used just to enforce dependency from the check train step

    output:
    tuple val(motif_line_ID), val(fasta_ID), path("*.pt"), emit: best_model
    tuple val(motif_line_ID), val(fasta_ID), path("train_statistics.txt"), emit: statistics
    tuple val(motif_line_ID), val(fasta_ID), path("architecture.txt"), emit: architecture
    stdout emit: standardout

    script:
    def args = task.ext.args ?: ''
    dir_ID   = motif_line_ID 
    if ( fasta_ID != '') {
        dir_ID = motif_line_ID + "_" + fasta_ID
    }
    """
    launch_training.py -i ${fasta} ${args} 1>train_statistics.txt
    """

    stub:
    dir_ID   = motif_line_ID
    if ( fasta_ID != '') {
        dir_ID = motif_line_ID + "_" + fasta_ID
    }
    """
    launch_training.py -i ${fasta} -e 2 --modules_version True 1>train_statistics.txt
    head -n 4 train_statistics.txt 
    """

}
