/*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    IMPORT NF-CORE MODULES/SUBWORKFLOWS
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
*/

include { CONVOLUTION_SCAN        } from '../modules/convolution_scan.nf'
include { HOMER_FIND_MOTIF        } from '../modules/homer_find_motif.nf'
include { HOMER_FIND_JASPAR_MOTIF } from '../modules/homer_find_jaspar_motif.nf'

/*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    RUN MAIN WORKFLOW
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
*/


workflow VERIFY_TRAINED {

    take:

    input_fasta
    model_architecture                     // hyperparameters
    trained_model                          // parameters
    jaspar_db


    main:


    completition_message = ''
    
    if ( params.skip_homer || params.input_fasta ) {
        completition_message = '\n# skipped homer for verifying motif learnt by model\n'

    } else {
        CONVOLUTION_SCAN( input_fasta, model_architecture, trained_model )
        completition_message = CONVOLUTION_SCAN.out.standardout


	// pair the positive set with the negative one using the motif and convolution filter number as key
        // also retrieving the filter length from the file name
        posive_set           = CONVOLUTION_SCAN.out.positve_set.flatten().map{ 
                                             it 
                                                   -> [ ("${it.baseName}".split('_')[0] + '_' + "${it.baseName}".split('_')[-2]), \
                                                      "${it.baseName}".split('_')[-1], \
                                                      it ] }
        negative_set         = CONVOLUTION_SCAN.out.negative_set.flatten().map{ 
                                             it
                                                   -> [ ("${it.baseName}".split('_')[0] + '_' + "${it.baseName}".split('_')[-2]), \
                                                      "${it.baseName}".split('_')[-1], \
                                                      it ] }
	paired_sets          = posive_set.combine( negative_set, by:[0, 1] )


        // Handle the case when there is no jaspar db in input
	if ( params.jaspar ) {
		HOMER_FIND_JASPAR_MOTIF( paired_sets, jaspar_db )
		completition_message.concat( HOMER_FIND_JASPAR_MOTIF.out.standardout )
	} else {
		HOMER_FIND_MOTIF( paired_sets )
		completition_message.concat( HOMER_FIND_MOTIF.out.standardout ).view()
	}
    
    }


    emit:

    completition_message

}


/*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    THE END
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
*/ 
