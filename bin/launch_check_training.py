#!/usr/bin/env python3

import argparse
from src.data.pytorch_loaders import fastaDataset
from src.learner.tune_trainer import Trainer 
from src.model.mnn_models import Net
from torch.utils.data import DataLoader
import sys
import numpy as np


def get_args():

	"get the arguments when using from the commandline"

	parser = argparse.ArgumentParser(description="This scripts loads a fasta file in the dataloder and then tries to do a testing train run of th emodel.")
	parser.add_argument("-i", "--infasta", type=str, required=True, metavar="FILE", help='The file path for the DNA sequences in fasta format.')
	parser.add_argument("-bs", "--batch_size", type=int, required=False, nargs='?', const=100, default=100, metavar="BATCH", help='The size of the batches in which the data are dived. Default 100.' )
	parser.add_argument("-x", "--shuffle", type=str, required=False, nargs='?', const='True', default='True', metavar='BOOL', help='The flag to tell or not to shuffle around data in th edtaloader. Default true.' )
	parser.add_argument("-sl", "--seq_len", type=int, required=False, nargs='?', const=100, default=100, metavar="LEN", help='Length in integer for the DNA seqs. Default 100.' )
	parser.add_argument("-olr", "--optimizer_lr", type=float, required=False, nargs='?', const=0.01, default=0.01, metavar="FLOAT", help='The linear  rate value of the optimizer. Default o.o1')
	parser.add_argument("-om", "--optimizer_momentum", type=float, required=False, nargs='?', const=0.5, default=0.5, metavar="FLOAT", help='The momentum value used by SGD optimizer. Default o.5')
	parser.add_argument("--modules_version", type=str, required=False, nargs='?', const='False', default='False', metavar='VERBOSE', help='auxiliary flag top check module version used byt this script.')

	args = parser.parse_args()
	return args


def main(data, batch_size, shuffle, seq_len, optimizer_lr, optimizer_momentum, modules_versionn='False'):

	print(data, batch_size, shuffle, seq_len, optimizer_lr, optimizer_momentum, modules_versionn)



if __name__ == "__main__":
	args = get_args()

	main(args.infasta, args.batch_size, args.shuffle, args.seq_len, args.optimizer_lr, args.optimizer_momentum, args.modules_version)
	
