
process QUERY_JASPAR {

    container "alessiovignoli3/tango-project@sha256:57013bf372b519245608c95fd60a38f9e5d65775aaf18c2d711031818c1a145e"     // bash5.0.17 with awk and wget
    label "process_low"
    tag "${dir_ID}"

    input:
    tuple val(dir_ID), val(jaspar_motif_id)

    output:
    tuple val(dir_ID), path("*.jaspar"), emit: jaspar_pwm, optional: true
    stdout emit: standardout

    script:
    """
    touch ${dir_ID}.jaspar
    
    for motif_id in ${jaspar_motif_id}
    do
    
        # preventing wget to send error message on not found id
        wget -q -O tmp_\$motif_id https://jaspar.elixir.no/api/v1//matrix/\$motif_id/?format=jaspar  || [[ \$? == 8 ]]
        
        # if no id was found there will be no output file so a message can be sent to user
        if ! [ -s tmp_\$motif_id ] 
            then
                echo "###  WARNING   motif ID not found : " \$motif_id
            else
                cat tmp_\$motif_id >> ${dir_ID}.jaspar
                rm tmp_\$motif_id
        fi
    done

    # if no id was found there will be no output file so a message can be sent to user
    if ! [ -s ${dir_ID}.jaspar ]
    then
        echo "###  WARNING   no motif ID was found for this line -> ${dir_ID}"
        rm ${dir_ID}.jaspar
    else
        exit 0                                          ## exiting with no error
    fi
    """

    stub:
    """
    touch ${dir_ID}.jaspar

    for motif_id in ${jaspar_motif_id}
    do

        # preventing wget to send error message on not found id
        wget -q -O tmp_\$motif_id https://jaspar.elixir.no/api/v1//matrix/\$motif_id/?format=jaspar  || [[ \$? == 8 ]]
        
        # if no id was found there will be no output file so a message can be sent to user
        if ! [ -s tmp_\$motif_id ]
            then
                echo "###  WARNING   motif ID not found : " \$motif_id
            else
                cat tmp_\$motif_id >> ${dir_ID}.jaspar
                rm tmp_\$motif_id
        fi
    done
    
    # if no id was found there will be no output file so a message can be sent to user
    if ! [ -s ${dir_ID}.jaspar ]
    then
        echo "###  WARNING   no motif ID was found for this line -> ${dir_ID}"
        rm ${dir_ID}.jaspar
    else
        exit 0                                          ## exiting with no error
    fi
    """

}
