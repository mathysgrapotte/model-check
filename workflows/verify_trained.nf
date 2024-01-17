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
        
    if ( params.skip_homer ) {
        completition_message = '\n# skipped homer for verifying motif learnt by model\n'

    } else {

        // pair together the right elements of each channel
        model          = model_architecture.combine( trained_model, by: [0,1] )
        matched_imputs = input_fasta.combine( model, by: [0,1] )


        CONVOLUTION_SCAN( matched_imputs )
        completition_message = CONVOLUTION_SCAN.out.standardout

        // reformatting the channel to have the ids associated each with one file, instead with a list of files produced by the process
        reformatted_positive = CONVOLUTION_SCAN.out.positve_set.transpose()
        reformatted_negative = CONVOLUTION_SCAN.out.negative_set.transpose()

	// pair the positive set with the negative one using the motif file line, fasta filename and convolution filter number as key
        // also retrieving the filter length and the motif file line from the output file name
        posive_set           = reformatted_positive.map{ 
                                             it 
                                                   -> [ it[0], \
                                                      it[1], \
                                                      "${it[2]}".split("\\.")[-2].split('_')[-2], \
                                                      "${it[2]}".split("\\.")[-2].split('_')[-1], \
                                                      it[2] ] }
        negative_set         = reformatted_negative.map{ 
                                             it
                                                   -> [ it[0], \
                                                      it[1], \
                                                      "${it[2]}".split("\\.")[-2].split('_')[-2], \
                                                      "${it[2]}".split("\\.")[-2].split('_')[-1], \
                                                      it[2] ] }
	paired_sets          = posive_set.combine( negative_set, by:[0, 1, 2, 3] )
        
        
        // Handle the case when there is no jaspar db in input
	if ( params.jaspar ) {
                
                // pair also the correct jaspar pwm downloaded with his corresponding trained model sets
                homer_inputs = paired_sets.combine( jaspar_db, by: 0 )

    
		HOMER_FIND_JASPAR_MOTIF( homer_inputs )
		completition_message.concat( HOMER_FIND_JASPAR_MOTIF.out.standardout )

	} else {
		HOMER_FIND_MOTIF( paired_sets )
		completition_message.concat( HOMER_FIND_MOTIF.out.standardout )
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
