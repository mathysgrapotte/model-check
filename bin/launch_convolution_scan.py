#!/usr/bin/env python3

import argparse
from src.motif_discovery.homer_convolution_scan import MnnHomerForegroundBackgroundSetup

# read the hyper parameters from the file, where they are stored in a dictionary manner such as : {'filter_size': [3, 5, 7], 'size': 101}
def read_dictionary_from_file(path):
    """
    Reads a dictionary from a file

    @param path: the path to the file containing the dictionary

    @return: the dictionary
    """
    with open(path, 'r') as f:
        d = eval(f.read())
    return d

def get_args():
    parser = argparse.ArgumentParser(description="This scripts loads a fasta file and a model, then scans the sequences with the model and outputs the foreground and background for homer analysis depending on convolution hits")
    parser.add_argument("-i", "--infasta", type=str, required=True, metavar="FILE", help='The file path for the DNA sequences in fasta format.')
    parser.add_argument("-hp", "--hyper_params", type=str, required=True, metavar="FILE", help='The file path for the hyper parameters of the model.')
    parser.add_argument("-p", "--params", type=str, required=True, metavar="FILE", help='The file path for the parameters of the model.')
    parser.add_argument("-o", "--output", type=str, required=False, metavar="FILE", default="output/", help='The file path for the output folder.')
    args = parser.parse_args()
    return args

def main(hyper_params, params, infasta , output):
    # initialize the homer foreground background setup class
    hyper_params = read_dictionary_from_file(hyper_params)
    homer_foreground_background_setup = MnnHomerForegroundBackgroundSetup(hyper_params, params, infasta)
    homer_foreground_background_setup.scan_for_all_modules_and_save(output)

if __name__ == "__main__":
	
    args = get_args()
    
    main(args.hyper_params, args.params, args.infasta, args.output)