
process QUERY_JASPAR {

    container "alessiovignoli3/model-check:jaspar_api"  // Python 3.10 slim-bullseye + corepai-cli 1.0.9
    label "process_low"
    tag "${jaspar_motif_id}"

    input:
    val jaspar_motif_id

    output:
    path "*.jaspar", emit: jaspar_pwm
    stdout emit: standardout

    script:
    """
    coreapi get https://jaspar.elixir.no/api/v1/docs/ > tmp

    # preventing coreapi to send error message on not found id
    coreapi action matrix read -p matrix_id=${jaspar_motif_id} 1>motif_${jaspar_motif_id}.jaspar || [[ \$? == 1 ]]

    # if no id was found the file first line contains the error message
    if [[ \$( head -n 1 motif_${jaspar_motif_id}.jaspar | grep 'Error') ]] ;
    then
        echo "###  WARNING   motif ID not found : ${jaspar_motif_id} "
    else
        exit 0                                          ## exiting with no error
    fi
    """

    stub:
    """
    coreapi get https://jaspar.elixir.no/api/v1/docs/ > tmp

    # preventing coreapi to send error message on not found id 
    coreapi action matrix read -p matrix_id=${jaspar_motif_id} 1>motif_${jaspar_motif_id}.jaspar || [[ \$? == 1 ]]  

    # if no id was found the file first line contains the error message 
    if [[ \$( head -n 1 motif_${jaspar_motif_id}.jaspar | grep 'Error') ]] ; 
    then
        echo "###  WARNING   motif ID not found : ${jaspar_motif_id} "
    else
        exit 0                                          ## exiting with no error
    fi
    """

}
