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
    db                   = ''

    if ( params.skip_homer || params.input_fasta || !params.jaspar ) {
        completition_message = '\n# skipped jaspar download and formatting \n'

    } else {

        // get to motif file line level, because that is what is going to be downloaded, (each motif ID per line)
        // then appended to the same file all the motifs in the same line in the original motif file in the process
        jaspar_id_file       = Channel.fromPath( params.jaspar )
 	// this line gets filename and line num correctly making it the ID
        tmp_line_file        = jaspar_id_file.splitText( file: true ).map{
                                               it
                                                    -> [ ( it.baseName.split('\\.')[0..-2].join("_") + "_line" + it.baseName.split('\\.')[-1]  ),
                                                        it] }
        // this line now splits the files of already one line to get to a list of motifs etting rid of missing fields and empty lines
        motif_line           = tmp_line_file.splitCsv( elem: 1, strip: true ).map{ 
                                               it 
                                                    -> [ it[0], (it[1] - '') ] }.filter{ it[1] != [] }.map{
                                               it
                                                    -> [ it[0], it[1].join(" ")] }

        
        QUERY_JASPAR( motif_line )
        jaspar_pwm           = QUERY_JASPAR.out.jaspar_pwm
        completition_message = QUERY_JASPAR.out.standardout.filter{ it != '' }
        
        // transform jaspar output into homer readable one
        JASPAR_TO_HOMER( jaspar_pwm )
        db                   = JASPAR_TO_HOMER.out.homer_matrix
        JASPAR_TO_HOMER.out.standardout.first().view()
        
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
