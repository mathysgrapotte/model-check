/*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    IMPORT NF-CORE MODULES/SUBWORKFLOWS
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
*/

include { GENERATE_FASTA      } from '../modules/generate_fasta.nf'
include { GENERATE_FROM_FASTA } from '../modules/generate_from_fasta.nf'

/*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    RUN MAIN WORKFLOW
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
*/


workflow HANDLE_FASTA {

    main:

    // first create a channel for the base fasta file if necessary
    // this file is the one used to enrich on 
    // in case is missing an empty channel is created instead to comply with the input declaration of the GENERATE_FASTA process
    base_fasta = ''
    if ( params.generate_from_fasta  ) {
        base_fasta =  Channel.fromPath( params.generate_from_fasta )
    }

    fasta = ''
    if ( params.input_fasta ) {
        fasta = Channel.fromPath( params.input_fasta )

    } else if ( params.jaspar ) {
        jaspar_id_file = Channel.fromPath( params.jaspar )

	if ( params.generate_from_fasta ) {
		GENERATE_FROM_FASTA( jaspar_id_file, base_fasta, '-j' )
		fasta = GENERATE_FROM_FASTA.out.dna_fasta
		GENERATE_FROM_FASTA.out.standardout.view()
	} else {
        	GENERATE_FASTA( jaspar_id_file, '-j' )
        	fasta = GENERATE_FASTA.out.dna_fasta
       		GENERATE_FASTA.out.standardout.view()
	}

    } else if ( params.motif ) {
        motif_file =  Channel.fromPath( params.motif )

	if ( params.generate_from_fasta ) {
		GENERATE_FROM_FASTA( motif_file, base_fasta, '-m' )
                fasta = GENERATE_FROM_FASTA.out.dna_fasta
                GENERATE_FROM_FASTA.out.standardout.view()
	} else {
		GENERATE_FASTA( motif_file, '-m' )
        	fasta = GENERATE_FASTA.out.dna_fasta
        	GENERATE_FASTA.out.standardout.view()
	}

    } else {
        log.info("at least one of the following flags has to be given as input: input_fasta, jaspar, motif\nLook for more details about them in the nextflow.config")
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
