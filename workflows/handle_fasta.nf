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
        base_fasta =  Channel.fromPath( params.generate_from_fasta ).map{ it -> [ it.baseName, it ]}
    }




    // the folowing variables act as switches or have different behavior in case 
    // the generation of the fasta is not needed
    fasta                = ''
    completition_message = "\n# fasta file used for the training can be found at  : ${params.outdir}"


    if ( params.input_fasta ) {
        fasta = Channel.fromPath( params.input_fasta ).map{ it -> [ it.baseName, it ] }
        completition_message = "\n# fasta file used for the training   : ${params.input_fasta}\n"



    } else if ( params.jaspar ) {

        // Read the file line by line and create as many files as there are lines, each file containing one line from the original.
        // the only tricky part is creating a unique name containing the source file and line#num_line in it  
        tmp_line_file   = Channel.fromPath( params.jaspar ).splitText( file: true ).map{
                                               it
                                                    -> [ ( it.baseName.split('\\.')[0..-2].join("_") + "_line" + it.baseName.split('\\.')[-1]  ), 
                                                        it] }
        // this line filter the content of the files of already one line getting rid of missing field and empty lines ecc..
        // just to end up to what was there before: a tuple with ID and one_file_path
        jaspar_id_file  = tmp_line_file.splitCsv( elem: 1, strip: true ).map{
                                               it
                                                    -> [ it[0], (it[1] - '') ] }.filter{ it[1] != [] }.collectFile() { 
                                               it
                                                    -> [ "${it[0]}.txt", it[1].join(",") + '\n']}.map{ it -> [ it.baseName, it ]}

	
	if ( params.generate_from_fasta ) {
                
                // to make the next process execute the correct number of times base_fasta has to be adde to the tuple created above
                tmp_input_files = jaspar_id_file.combine( base_fasta )

                // and the filename of the base fasta added as auxiliary ID for later on usage
                input_files     = tmp_input_files.map{ it -> [ it[0], it[2], it[1], it[3] ]}

                GENERATE_FROM_FASTA( input_files, '-j' )
                fasta = GENERATE_FROM_FASTA.out.dna_dir
                GENERATE_FROM_FASTA.out.standardout.view()
	} else {
        	GENERATE_FASTA( jaspar_id_file, '-j' )
        	fasta = GENERATE_FASTA.out.dna_dir
       		GENERATE_FASTA.out.standardout.view()
	}
        


    } else if ( params.motif ) {
       
        // the description of the following lines of code are just above
        tmp_line_file  =  Channel.fromPath( params.motif ).splitText( file: true ).map{
                                               it
                                                    -> [ ( it.baseName.split('\\.')[0..-2].join("_") + "_line" + it.baseName.split('\\.')[-1]  ),
                                                        it] }
        motif_file     =  tmp_line_file.splitCsv( elem: 1, strip: true ).map{
                                               it
                                                    -> [ it[0], (it[1] - '') ] }.filter{ it[1] != [] }.collectFile() {   
                                               it
                                                    -> [ "${it[0]}.txt", it[1].join(",") + '\n']}.map{ it -> [ it.baseName, it ]}


	if ( params.generate_from_fasta ) {

                tmp_input_files = motif_file.combine( base_fasta )
                input_files     = tmp_input_files.map{ it -> [ it[0], it[2], it[1], it[3] ]}

		GENERATE_FROM_FASTA( input_files, '-m' )
                fasta = GENERATE_FROM_FASTA.out.dna_dir
                GENERATE_FROM_FASTA.out.standardout.view()
	} else {
		GENERATE_FASTA( motif_file, '-m' )
        	fasta = GENERATE_FASTA.out.dna_dir
        	GENERATE_FASTA.out.standardout.view()
	}


    } else {
        log.info("at least one of the following flags has to be given as input: input_fasta, jaspar, motif\nLook for more details about them in the nextflow.config")
        exit 1
    }



    emit:

    fasta
    completition_message

}


/*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    THE END
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
*/
