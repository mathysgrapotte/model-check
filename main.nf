#!/usr/bin/env nextflow
/*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    model-check
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
*/

nextflow.enable.dsl = 2

/*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    NAMED WORKFLOW FOR PIPELINE
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
*/

include { HANDLE_FASTA    } from './workflows/handle_fasta.nf'
include { JASPAR_DOWNLOAD } from './workflows/jaspar_download.nf'
include { CHECK_TRAINABLE } from './workflows/check_trainable.nf'
include { TRAIN           } from './workflows/train.nf'
include { VERIFY_TRAINED  } from './workflows/verify_trained.nf'
include { PLOT_MODEL} from './workflows/plot_model.nf'

/*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    RUN ALL WORKFLOWS
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
*/


workflow {

    // TODO make a nicer print of the filename
    // TODO write all parameters flags to log file
	
    HANDLE_FASTA()
    fasta          = HANDLE_FASTA.out.fasta
    fasta_message  = HANDLE_FASTA.out.completition_message 
    fasta_message.view()
    
    JASPAR_DOWNLOAD()
    jaspar_db      = JASPAR_DOWNLOAD.out.db
    jaspar_message = JASPAR_DOWNLOAD.out.completition_message
    jaspar_message.view()
    
    CHECK_TRAINABLE( fasta )
    check_message  = CHECK_TRAINABLE.out.message
    check_message.view()

    TRAIN( fasta, check_message )
    train_message  = TRAIN.out.message
    architecture   = TRAIN.out.architecture
    trained_model  = TRAIN.out.trained_model
    train_message.view()

    VERIFY_TRAINED( jaspar_db )
    verify_message = VERIFY_TRAINED.out.completition_message
    verify_message.view()    

    PLOT_MODEL( architecture, trained_model )

}

workflow.onComplete {
    println "# best model parameter file          : ${params.outdir}/model/best_model.pt "
    println "# model architecture dictionary file : ${params.outdir}/model/architecture.txt"
}

/*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    THE END
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
*/
