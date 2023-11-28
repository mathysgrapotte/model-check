#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Request Jaspar and write motif database for a species in the output.

Auteur : Mathys Grapotte, Christophe Vroland and Charles Lecellier
Date : 06/22/2023
"""

__authors__ = ("Mathys Grapotte", "Christophe Vroland", "Charles Lecellier")
__date__ = '06/22/2023'
__email__ = ("mathysgrapotte@gmail.com", 'christophe@cvroland.com', "charles.lecellier@igmm.cnrs.fr")
__status__ = 'Prototype'
__version__ = "0.0.1"

import sys
import argparse
import re
import requests

from typing import Generator, Sequence, Optional, Dict, Any
API_URL="https://jaspar.genereg.net/api/v1/"

def getJsonRestRequest(
    url:str, 
    params:Optional[Dict[str, Any]] =None,
    nbTry:int=3
)->Dict:    
    """
    Send a GET request to the specified URL and return the JSON response.

    Parameters:
        url (str): The URL to send the GET request to.
        params (Optional[Dict[str, str]]): Optional parameters to include in the request.
        nbTry (int): Number of times to retry the request in case of failure.

    Returns:
        Dict: The JSON response as a dictionary

    Raises:
        requests.exceptions.RequestException: If the request fails after the maximum number of attempts.
    """
    error=None
    for tryCount in range (nbTry):
        try:
            restResponse=requests.get(url, params=params)
            jsonResponse=restResponse.json()
            return jsonResponse
        except Exception as e: 
            error=e
            print("get json fail for {} and params {}, retry ({}/{}).".format(url, params, tryCount+1, nbTry+1), file=sys.stderr)
    raise error

def removeHeaderMeme(matrixTxt:str)->str:
    """
    Remove the header from a MEME format motif matrix.

    Parameters
    ----------
    matrixTxt : str
        String representation of the motif matrix in MEME format.

    Returns
    -------
    str
        String representation of the motif matrix without the header.

    """
    matrixStartPattern=r"^MOTIF"
    match=re.search(matrixStartPattern, matrixTxt, re.MULTILINE)
    if match is not None:
        matrixTxt=matrixTxt[match.start():]
    return matrixTxt


def getMotifMatrix(
    motifId: str, 
    outputFormat: str = "jaspar", 
    apiUrl: str = API_URL, 
    removeHeader: bool = False
) -> str:    
    """
    Retrieve the motif matrix for a given motif ID.

    Parameters
    ----------
    motifId : str
        Identifier of the motif.
    outputFormat : str, optional
        Format of the motif matrix, by default "jaspar".
    apiUrl : str, optional
        URL of the API, by default API_URL.
    removeHeader : bool, optional
        Whether to remove the header from the matrix (only for MEME format), by default False.

    Returns
    -------
    str
        String representation of the motif matrix.

    """
    restRequest="{apiUrl}matrix/{motifId}/".format(apiUrl=apiUrl, motifId=motifId)
    restResponse=requests.get(restRequest, params={"format":outputFormat})
    matrixTxt=restResponse.text
    if removeHeader:
        if outputFormat=="meme":
            matrixTxt=removeHeaderMeme(matrixTxt)
    return matrixTxt

def getMotifs(
    collection:str = None,
    name:str=None,
    taxGroup:str=None,
    taxId:str=None,
    tfClass:str=None,
    tfFamily:str=None,
    dataType:str=None,
    version:str=None,
    release:str=None,
    outputFormat: str = "jaspar", 
    cat:bool=False,
    apiUrl: str = API_URL
) -> Generator[str, None, None]:
    """
    Retrieve motifs in the JASPAR database.

    Parameters
    ----------
    page : str, optional
        A page number within the paginated result set.
    page_size : str, optional
        Number of results to return per page.
    search : str, optional
        A search term.
    order : str, optional
        Which field to use when ordering the results.
    collection : str, optional
        JASPAR Collection name. For example: CORE or CNE.
    name : str, optional
        Search by TF name (case-sensitive). For example: SMAD3
    tax_group : str, optional
        Taxonomic group. For example: Vertebrates
    tax_id : str, optional
        Taxa ID. For example: 9606 for Human & 10090 for Mus musculus. Multiple IDs can be added separated by commas (e.g. tax_id=9606,10090).
    tf_class : str, optional
        Transcription factor class. For example: Zipper-Type
    tf_family : str, optional
        Transcription factor family. For example: SMAD factors
    data_type : str, optional
        Type of data/experiment. For example: ChIP-seq, PBM, SELEX etc.
    version : str, optional
        If set to latest, return latest version
    release : str, optional
        Access a specific release of JASPAR. Available releases are: 2014, 2016, 2018, 2020 and 2022. If blank, the query will provide data from the latest release.
    outputFormat: str, optional
        Format of the output, by default "jaspar". Available formats are : "json", "jsonp", "jaspar", "meme", "transfac", "pfm" and "yaml" 
    cat: bool, optional
        remove the header of the first motif.
    apiUrl: str, optional
        URL of the API, by default API_URL.

    Yields
    ------
    str
        String representation of a motif matrix.

    """
    restRequest="{apiUrl}matrix/".format(apiUrl=apiUrl)
    params={}
    if collection is not None: params["collection"]=collection
    if name is not None: params["name"]=name
    if taxGroup is not None: params["tax_group"]=taxGroup
    if taxId is not None: params["tax_id"]=taxId
    if tfClass is not None: params["tf_class"]=tfClass
    if tfFamily is not None: params["tf_family"]=tfFamily
    if dataType is not None: params["data_type"]=dataType
    if version is not None: params["version"]=version
    if release is not None: params["release"]=release
    try :
        jsonResponse=getJsonRestRequest(restRequest, params=params, nbTry=3)
    except :
        print("didn't manage to get JSON from {} for parameters {}".format(restRequest, params), file=sys.stderr)
        return
    notFirstMatrix=cat
    while restRequest is not None :
        #read and request next
        for motif in jsonResponse["results"]:
            motifMatrix=getMotifMatrix(motif["matrix_id"], outputFormat=outputFormat, apiUrl=apiUrl, removeHeader=notFirstMatrix)
            notFirstMatrix=True
            yield motifMatrix
        restRequest=jsonResponse["next"] 
        if restRequest is not None : 
            try :
                jsonResponse=getJsonRestRequest(restRequest, nbTry=3)
            except :
                print("didn't manage to get JSON from {}".format(restRequest), file=sys.stderr)
                pass
            

def parseArgs() -> argparse.Namespace:
    """
    Parse command-line arguments.

    Returns
    -------
    argparse.Namespace
        Parsed command-line arguments.

    """
    parser = argparse.ArgumentParser(description="""Write the JASPAR motif database in to stdOut
    """)
    parser.add_argument("-c", "--collection", type=str, default=None,help="JASPAR Collection name. For example: CORE or CNE.")
    parser.add_argument("-n", "--name", type=str, default=None,help="Search by TF name (case-sensitive). For example: SMAD3")
    parser.add_argument("-g", "--taxGroup", type=str, default=None,help="Taxonomic group. For example: Vertebrates")
    parser.add_argument("-i", "--taxId", type=str, default=None,help="Taxa ID. For example: 9606 for Human & 10090 for Mus musculus. Multiple IDs can be added separated by commas (e.g. tax_id=9606,10090).")
    parser.add_argument("-C", "--tfClass", type=str, default=None,help="Transcription factor class. For example: Zipper-Type")
    parser.add_argument("-F", "--tfFamily", type=str, default=None,help="Transcription factor family. For example: SMAD factors")
    parser.add_argument("-t","--dataType", type=str, default=None,help="Type of data/experiment. For example: ChIP-seq, PBM, SELEX etc.")
    parser.add_argument("-V", "--version", type=str, default=None,help="If set to latest, return latest version")
    parser.add_argument("-r", "--release", type=str, default=None,help="Access a specific release of JASPAR. Available releases are: 2014, 2016, 2018, 2020 and 2022. If blank, the query will provide data from the latest release.")
    parser.add_argument("-f", "--outputFormat", type=str, default="jaspar", help="Format of the output, by default \"jaspar\". Available formats are : \"json\", \"jsonp\", \"jaspar\", \"meme\", \"transfac\", \"pfm\" and \"yaml\" ") #bed not supported
    parser.add_argument("-a", "--cat", action="store_true", help="Use this option if you want to use the output to complete an existing file. It will remove the header of the first matrix")
    parser.add_argument("-u", "--apiUrl", type=str, default=API_URL, help="API URL. Use 'https://jaspar2020.genereg.net/api/v1/' if you want to get access to POLII collection.")
    return parser.parse_args()

def main():
    args = parseArgs()
    collection=args.collection
    name=args.name
    taxGroup=args.taxGroup
    taxId=args.taxId
    tfClass=args.tfClass
    tfFamily=args.tfFamily
    dataType=args.dataType
    version=args.version
    release=args.release
    outputFormat=args.outputFormat
    cat=args.cat
    apiUrl=args.apiUrl
    motifMatrixTxtGenerator=getMotifs(
        collection=collection,
        name=name,
        taxGroup=taxGroup,
        taxId=taxId,
        tfClass=tfClass,
        tfFamily=tfFamily,
        dataType=dataType,
        version=version,
        release=release,
        outputFormat=outputFormat,
        cat=cat,
        apiUrl=apiUrl
    )
    for matrixTxt in motifMatrixTxtGenerator :
        print(matrixTxt)

if __name__ == '__main__':
    main()
