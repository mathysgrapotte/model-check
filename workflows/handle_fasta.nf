/*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    IMPORT NF-CORE MODULES/SUBWORKFLOWS
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
*/

include { GENERATE_FASTA } from '../modules/generate_fasta.nf'

/*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    RUN MAIN WORKFLOW
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
*/


workflow HANDLE_FASTA {

    main:

    fasta = ''
    if ( params.input_fasta ) {
        fasta = Channel.fromPath( params.input_fasta )

    } else if ( params.jaspar_id ) {
        jaspar_id_file = Channel.fromPath( params.jaspar_id )
        GENERATE_FASTA( jaspar_id_file, '-j' )
        fasta = GENERATE_FASTA.out.dna_fasta
        GENERATE_FASTA.out.standardout.view()

    } else if ( params.motif ) {
        motif_file =  Channel.fromPath( params.motif )
        GENERATE_FASTA( motif_file, '-m' )
	fasta = GENERATE_FASTA.out.dna_fasta
	GENERATE_FASTA.out.standardout.view()

    } else {
        log.info("at least one of the following flags has to be given as input: input_fasta, jaspar_id, motif\nLook for more details about them in the nextflow.config")
        exit 1

    }


    emit:

    fasta

}


/*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    THE END
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
*/
