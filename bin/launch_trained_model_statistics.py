#!/usr/bin/env python3

import argparse
import torch
import matplotlib.pyplot as plt
from src.model.mnn_models import BlockNet, Net
from src.data.pytorch_loaders import fastaDataset
from torch.utils.data import DataLoader

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
    parser = argparse.ArgumentParser(description="This scripts loads a fasta file and a model, then scans the sequences with the model to generate some statistics.")
    parser.add_argument("-hp", "--hyper_params", type=str, required=True, metavar="FILE", help='The file path for the hyper parameters of the model.')
    parser.add_argument("-p", "--params", type=str, required=True, metavar="FILE", help='The file path for the parameters of the model.')
    parser.add_argument("-i", "--infasta", type=str, required=True, metavar="FILE", help='The file path for the DNA sequences in fasta format.')
    parser.add_argument("-o", "--output", type=str, required=False, metavar="FILE", default="", help='The file path for the output folder.')
    args = parser.parse_args()
    return args

def main(hyper_params, params, infasta, output_path):
    # initialize the homer foreground background setup class
    hyper_params = read_dictionary_from_file(hyper_params)
    model = Net()
    model.build_model(hyper_params)
    model.load_state_dict(torch.load(params))

    # load the data in the pytorch loader
    pytorch_loader = fastaDataset(infasta)
    train_set = DataLoader(pytorch_loader, batch_size=100, shuffle=True)

    # apply the model on the train set then store the labels and the predictions in two lists
    labels = []
    predictions = []
    for batch_idx, (data, target, sequence_names) in enumerate(train_set):
        output = model(data.float())
        labels.extend(target.tolist())
        predictions.extend(output.tolist())

    print("done!")

    # sample 1000 points from the labels and the predictions
    labels = labels[:1000]
    predictions = predictions[:1000]

    print("done sampling")

    # plot the predictions vs the labels in a scatter plot, with 300 dpi, corret labels and title
    plt.scatter(labels, predictions)
    plt.xlabel("Labels")
    plt.ylabel("Predictions")
    plt.title("Predictions vs Labels")
    plt.savefig(output_path + "predictions_vs_labels.png")
    plt.close()

if __name__ == "__main__":
	
    args = get_args()
    
    main(args.hyper_params, args.params, args.infasta, args.output)