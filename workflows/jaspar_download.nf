/*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    IMPORT NF-CORE MODULES/SUBWORKFLOWS
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
*/

include { QUERY_JASPAR    } from '../modules/query_jaspar.nf'
include { JASPAR_TO_HOMER } from '../modules/jaspar_to_homer.nf'

/*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    RUN MAIN WORKFLOW
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
*/


workflow JASPAR_DOWNLOAD {

    main:


    completition_message = ''
    db = ''

    if ( params.skip_homer || params.input_fasta ) {
        completition_message = '\n# skipped homer for verifying motif learnt by model\n'

    } else {

        // get to motif id level, because that is what is going to be downloaded
        jaspar_id_file       = Channel.fromPath( params.jaspar )
        motif_id             = jaspar_id_file.splitCsv( strip: true ).flatten().filter{ it != '' }

        QUERY_JASPAR( motif_id )
        jaspar_pwm          = QUERY_JASPAR.out.jaspar_pwm
        completition_message = QUERY_JASPAR.out.standardout.filter{ it != '' }

        // transform jaspaer output into homer readable one
        JASPAR_TO_HOMER( jaspar_pwm )
        JASPAR_TO_HOMER.out.standardout.view()

    }


    emit:

    db
    completition_message

}


/*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    THE END
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
*/
