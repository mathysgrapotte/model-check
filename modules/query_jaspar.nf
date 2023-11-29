
process QUERY_JASPAR {

    container "alessiovignoli3/tango-project@sha256:57013bf372b519245608c95fd60a38f9e5d65775aaf18c2d711031818c1a145e"     // bash5.0.17 with awk and wget
    label "process_low"
    tag "${jaspar_motif_id}"

    input:
    val jaspar_motif_id

    output:
    path "*.jaspar", emit: jaspar_pwm, optional: true
    stdout emit: standardout

    script:
    """
    # preventing wget to send error message on not found id
    wget -q -O  motif_${jaspar_motif_id}.jaspar https://jaspar.elixir.no/api/v1//matrix/${jaspar_motif_id}/?format=jaspar  || [[ \$? == 8 ]]

    # if no id was found there will be no output file so a message can be sent to user
    if ! [ -s motif_${jaspar_motif_id}.jaspar ]
    then
        echo "###  WARNING   motif ID not found : ${jaspar_motif_id} "
        rm motif_${jaspar_motif_id}.jaspar
    else
        exit 0                                          ## exiting with no error
    fi
    """

    stub:
    """
    # preventing wget to send error message on not found id
    wget -q -O  motif_${jaspar_motif_id}.jaspar https://jaspar.elixir.no/api/v1//matrix/${jaspar_motif_id}/?format=jaspar  || [[ \$? == 8 ]]
    
    # if no id was found there will be no output file so a message can be sent to user
    if ! [ -s motif_${jaspar_motif_id}.jaspar ]
    then
        echo "###  WARNING   motif ID not found : ${jaspar_motif_id} "
        rm motif_${jaspar_motif_id}.jaspar
    else
        exit 0                                          ## exiting with no error
    fi
    """

}
