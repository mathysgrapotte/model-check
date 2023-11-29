#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Convert a PWM matrix to a custom homer motif matrices

Auteur : Mathys Grapotte, Christophe Vroland and Charles Lecellier
Date : 07/13/2023
"""

__authors__ = ("Mathys Grapotte", "Christophe Vroland", "Charles Lecellier")
__date__ = '07/13/2023'
__email__ = ("mathysgrapotte@gmail.com", 'christophe@cvroland.com', "charles.lecellier@igmm.cnrs.fr")
__status__ = 'Prototype'
__version__ = "0.0.1"


import argparse
from Bio import motifs
from Bio.motifs import jaspar
import numpy as np
import pandas as pd
"""import multiprocessing
try:
    cpus = multiprocessing.cpu_count()
except NotImplementedError:
    cpus = 2   # arbitrary default

from typing import IO, List
"""
def getHomerLogOdd(
    motif:motifs.Motif,
    mismatch:int=0,
    eps:float=0.01,
    *args, 
    **kwargs) -> float:    
    """
    Calculate the log-odds score for a motif using a modified Homer seq2profile.pl algorithm.

    Parameters
    ----------
    motif : Bio.motifs.Motif
        The motif for which to calculate the log-odds score.
    mismatch : int, optional
        The number of worst mismatches to consider (default is 0).
    eps : float, optional
        A small constant to be lower than a perfect match (default is 0.01).

    Returns
    -------
    float
        The calculated log-odds score.
    """
    # it's a more universal version of homer seq2profile.pl. 
    # the idea is to get the score of the best sequence possible where the worst mismatches are done.
    pssm=motif.pssm
    # XXX: homer use "log" and not log2, the score is different, the PSSM compute by biopython is better.
    pssmArray=np.asarray([pssm[c] for c in pssm.alphabet])
    maxOnNtPssmArray=np.max(pssmArray, axis=0)
    if mismatch > 0 :
        minOnNtPssmArray=np.min(pssmArray, axis=0)
        worstMismatchScore=maxOnNtPssmArray-minOnNtPssmArray
        worstMismatchIdx=np.argsort(worstMismatchScore)[-mismatch:]
        maxOnNtPssmArray[worstMismatchIdx]=minOnNtPssmArray[worstMismatchIdx]
    score=np.sum(maxOnNtPssmArray)-eps
    return score

def getLogOddThresholdFpr(
    motif:motifs.Motif,
    pValue:float=0.05,
    precision:int=10 ** 3,
    *args, 
    **kwargs) -> float:
    """
    Calculate the log-odds threshold using the false positive rate (FPR) method.

    Parameters
    ----------
    motif : Bio.motifs.Motif
        The motif for which to calculate the threshold.
    pValue : float, optional
        The desired p-value (default is 0.05).
    precision : int, optional
        The precision parameter for threshold calculation (default is 10^3).

    Returns
    -------
    float
        The calculated log-odds threshold.
    """
    pssm=motif.pssm
    return pssm.distribution(motif.background, precision=precision).threshold_fpr(pValue)

def getLogOddThresholdFnr(
    motif: motifs.Motif,
    pValue: float = 0.05,
    precision: int = 10 ** 3,
    *args, 
    **kwargs) -> float:
    """
    Calculate the log-odds threshold using the false negative rate (FNR) method.

    Parameters
    ----------
    motif : Bio.motifs.Motif
        The motif for which to calculate the threshold.
    pValue : float, optional
        The desired p-value (default is 0.05).
    precision : int, optional
        The precision parameter for threshold calculation (default is 10^3).

    Returns
    -------
    float
        The calculated log-odds threshold.
    """
    pssm=motif.pssm
    return pssm.distribution(motif.background, precision=precision).threshold_fnr(pValue)

def getLogOddThresholdBalanced(
    motif: motifs.Motif,
    pValue: float = 0.05,
    precision: int = 10 ** 3,
    *args, 
    **kwargs) -> float:
    """
    Calculate the log-odds threshold using the balanced method.

    Parameters
    ----------
    motif : Bio.motifs.Motif
        The motif for which to calculate the threshold.
    pValue : float, optional
        The desired p-value (default is 0.05).
    precision : int, optional
        The precision parameter for threshold calculation (default is 10^3).

    Returns
    -------
    float
        The calculated log-odds threshold.
    """
    pssm=motif.pssm
    return pssm.distribution(motif.background, precision=precision).threshold_balanced(pValue)

def getLogOddThresholdPatser(
    motif: motifs.Motif,
    precision: int = 10 ** 3,
    *args, 
    **kwargs) -> float:
    """
    Calculate the log-odds threshold using the Patser method.

    Parameters
    ----------
    motif : Bio.motifs.Motif
        The motif for which to calculate the threshold.
    precision : int, optional
        The precision parameter for threshold calculation (default is 10^3).

    Returns
    -------
    float
        The calculated log-odds threshold.
    """
    pssm=motif.pssm
    return pssm.distribution(motif.background, precision=precision).threshold_patser()

_switchCaseMethod={
    "homer":getHomerLogOdd,
    "fpr":getLogOddThresholdFpr,
    "fnr":getLogOddThresholdFnr,
    "balanced":getLogOddThresholdBalanced,
    "patser":getLogOddThresholdPatser,
}

def getLogOddThreshold(
    motif: motifs.Motif,
    method: str = "fpr",
    *args, 
    **kwargs) -> float:
    """
    Calculate the log-odds threshold using the specified method.

    Parameters
    ----------
    motif : Bio.motifs.Motif
        The motif for which to calculate the threshold.
    method : str, optional
        The method to use for threshold calculation (default is "fpr").
    *args : list, optional
        Additional positional arguments for the threshold calculation function.
    **kwargs : dict, optional
        Additional keyword arguments for the threshold calculation function.

    Returns
    -------
    float
        The calculated log-odds threshold.
    """
    return _switchCaseMethod[method](motif, *args, **kwargs)



def getLogOddThresholdList(
    motifList: List[motifs.Motif],
    method: str = "fpr",
    *args, 
    **kwargs) -> List[float]:
    """
    Calculate a list of log-odds thresholds for a list of motifs using the specified method.

    Parameters
    ----------
    motifList : List[Bio.motifs.Motif]
        The list of motifs for which to calculate the thresholds.
    method : str, optional
        The method to use for threshold calculation (default is "fpr").
    *args : list, optional
        Additional positional arguments for the threshold calculation function.
    **kwargs : dict, optional
        Additional keyword arguments for the threshold calculation function.

    Returns
    -------
    List[float]
        A list of calculated log-odds thresholds.
    """
    #pool=multiprocessing.Pool(cpus)
    #asyncThresholdList=[pool.apply_async(getLogOddThreshold, args=(motifList[i], *args),kwds={"method":method, **kwargs}) for i in range(len(motifList))]
    #thresholdList=[ar.get() for ar in asyncThresholdList]
    thresholdList = []
    for i in range(len(motifList)):
        thresholdList[i]=getLogOddThreshold(motifList[i], method=method, *args, **kwargs)
    return thresholdList


def readMotifFile(handle:IO, format:str="MINIMAL")->list[motifs.Motif]:
    """
    Read motifs from a file.

    Parameters
    ----------if eval(modules_version):
                print('python :', sys.version, '\n',  'numpy :', np.__version__)
    handle : IO
        The file handle to read from.
    format : str, optional
        The format of the input file. Default is "MINIMAL".
        Supported formats: 'AlignAce', 'ClusterBuster', 'XMS', 'MEME', 'MINIMAL', 'MAST', 'TRANSFAC', 'pfm-four-columns', 'pfm-four-rows', 'pfm', 'jaspar', 'sites'.

    Returns
    -------
    List[Bio.motifs.Motif]
        A list of motifs read from the file.
    """
    motifList:list[motifs.Motif]=motifs.parse(handle, format)
    return motifList

def setPseudoCounts(motifList: List[motifs.Motif]):
    """
    Set pseudocounts for a list of motifs.

    Parameters
    ----------
    motifList : List[Bio.motifs.Motif]
        The list of motifs for which to set pseudocounts.
    """
    for motif in motifList :
        motif.pseudocounts=jaspar.calculate_pseudocounts(motif)
    
def setBackground(motifList: List[motifs.Motif], background):
    """
    Set background for a list of motifs.

    Parameters
    ----------
    motifList : List[Bio.motifs.Motif]
        The list of motifs for which to set the background.
    background : dict
        The background dictionary.
    """
    for m in motifList :
        m.background=background


def setLogOddThreshold(
    motifList: List[motifs.Motif],
    thresholdList: List[float]):
    """
    Set log-odds thresholds for a list of motifs.

    Parameters
    ----------
    motifList : List[Bio.motifs.Motif]
        The list of motifs for which to set the log-odds thresholds.
    thresholdList : List[float]
        The list of log-odds thresholds to set.
    """
    for m,t in zip(motifList,thresholdList) :
        m.logOddThreshold=t

def motif2homerString(motif:motifs.Motif):
    if not hasattr(motif, "logOddThreshold"):
        motif.logOddThreshold=getHomerLogOdd(motif)
    headerRepr=">{consensus}\t{motifName}\t{logOddThreshold}\n".format(consensus=motif.degenerate_consensus, motifName=motif.name, logOddThreshold=motif.logOddThreshold)
    pwmDict=motif.pwm
    pwm=np.asarray([pwmDict[a] for a in motif.alphabet]).T
    matrixRepr=pd.DataFrame(pwm).to_csv(header=None, index=None, sep="\t")
    homerRepr=headerRepr+matrixRepr
    return homerRepr

def motifList2homerString(motifList:list[motifs.Motif]):
    return "".join([motif2homerString(motif) for motif in motifList])

def parseArgs() -> argparse.Namespace:
    """
    Parse command-line arguments.

    Returns
    -------
    argparse.Namespace
        An object containing the parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(description="Calculate log-odds thresholds for motifs and generate Homer format output.")

    parser.add_argument("-i", "--input", type=argparse.FileType("r"), default='-', help="Input motif file (default: stdin)")
    parser.add_argument("-o", "--output", type=argparse.FileType("w"), default='-', help="Output Homer format file (default: stdout)")
    parser.add_argument("-f", "--format", default="MINIMAL", choices=["AlignAce", "ClusterBuster", "XMS", "MEME", "MINIMAL", "MAST", "TRANSFAC", "pfm-four-columns", "pfm-four-rows", "pfm", "jaspar", "sites"], help="Input motif file format (default: MINIMAL)")
    parser.add_argument("-b", "--background", type=str, help="Background file path")
    parser.add_argument("-m", "--method", default="fpr", choices=["homer", "fpr", "fnr", "balanced", "patser"], help="Threshold calculation method (default: fpr)")
    parser.add_argument("--mismatch", type=int, default=0, help="Number of worst mismatches to consider (default: 0, homer)")
    parser.add_argument("--eps", type=float, default=0.01, help="A small constant subtracted to the score (default: 0.01, homer)")
    parser.add_argument("--pValue", type=float, default=0.05, help="Desired p-value for threshold calculation (default: 0.05)")
    parser.add_argument("--precision", type=int, default=10 ** 3, help="Precision parameter for threshold calculation (default: 1000)")
    parser.add_argument("--modules_version", type=str, required=False, nargs='?', const='False', default='False', metavar='VERBOSE', help='auxiliary flag top check module version used byt this script.')

    return parser.parse_args()

def main():
    # get arguments of the cli
    args = parseArgs()
    input=args.input
    format=args.format
    output=args.output
    backgroundFilePath=args.background
    method=args.method
    mismatch=args.mismatch
    eps=args.eps
    pValue=args.pValue
    precision=args.precision
    """# read motifs from input (stdin or file)
    motifList = readMotifFile(input, format=format)
    # set pseudocounts to avoid issues
    setPseudoCounts(motifList)
    # set background if given
    if backgroundFilePath is not None :
        # with `sep=r"\s+|\t"` we can read tab separated file produce by getBackground.py and space separated file produce by MEME fasta-get-markov. We need to skip comment line.
        background=pd.read_csv(backgroundFilePath, sep=r"\s+|\t", engine="python", header=None, index_col=0, comment='#')[1].to_dict()
        setBackground(motifList,background)
    # compute logOffThreshold et set on motifs
    thresholdList=getLogOddThresholdList(
        motifList,
        method=method,
        mismatch=mismatch,
        eps=eps,
        pValue=pValue,
        precision=precision,
    )
    setLogOddThreshold(motifList, thresholdList)
    # print homer format into output (stdout or file)
    homerString = motifList2homerString(motifList)
    output.write(homerString)
    output.flush()
    """
    # print dependencies version
    if eval(modules_version):
        import Bio
        import sys
        print('python :', sys.version, '\n',  'numpy :', np.__version__, '\n', 'pandas :', pd.__version__, '\n', 'Bio :', Bio.__version__) 
    
if __name__ == "__main__":
    main()
