#!/usr/bin/env python3

import argparse
import torch
from src.model.mnn_models import BlockNet, Net

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
    parser.add_argument("-hp", "--hyper_params", type=str, required=True, metavar="FILE", help='The file path for the hyper parameters of the model.')
    parser.add_argument("-p", "--params", type=str, required=True, metavar="FILE", help='The file path for the parameters of the model.')
    parser.add_argument("-o", "--output", type=str, required=False, metavar="FILE", default="output/", help='The file path for the output folder.')
    args = parser.parse_args()
    return args

def main(hyper_params, params, output):
    # initialize the homer foreground background setup class
    hyper_params = read_dictionary_from_file(hyper_params)
    model = Net()
    model.build_model(hyper_params)
    model.load_state_dict(torch.load(params))
    model.save_all_convolution_weight_logo(output)
    model.save_all_modules_linear_weights(output)


if __name__ == "__main__":
	
    args = get_args()
    
    main(args.hyper_params, args.params, args.output)