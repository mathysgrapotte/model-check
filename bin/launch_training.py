#!/usr/bin/env python3

import argparse
from src.data.pytorch_loaders import fastaDataset
from src.learner.tune_trainer import MnnTrainer
from src.model.mnn_models import Net
from torch.utils.data import DataLoader
import sys
import ray
import numpy as np
import torch
from torch import nn
import torch.optim as optim
from ray import tune


def get_args():

	"get the arguments when using from the commandline"

	parser = argparse.ArgumentParser(description="This scripts loads a fasta file in the dataloder and then trains the model.")
	parser.add_argument("-i", "--infasta", type=str, required=True, metavar="FILE", help='The file path for the DNA sequences in fasta format.')
	parser.add_argument("-bs", "--batch_size", type=str, required=False, nargs='?', const='10,100', default='10,100', metavar="BATCH", help='The size of the batches in which the data are dived. Default 10,100. Meaninng all decades values are tested aka -> 10, 20 ,30,40 ecc .. up to 100. Ten values are taken equally interspaced between the values given.' )
	parser.add_argument("-x", "--shuffle", type=str, required=False, nargs='?', const='True', default='True', metavar='BOOL', help='The flag to tell or not to shuffle around data in th edtaloader. Default true.' )
	parser.add_argument("-sl", "--seq_len", type=int, required=False, nargs='?', const=100, default=100, metavar="LEN", help='Length in integer for the DNA seqs. Default 100.' )
	parser.add_argument("-e", "--epochs", type=int, required=False, nargs='?', const=10, default=10, metavar="EPOCH", help='The number of epochs for which the model have to be trained. Default 10.') 
	parser.add_argument("-fs", "--filter_size", type=str, required=False, nargs='?', const='2,20', default='2,20', metavar="RANGE", help='The convolution filter size to be tested. Default 2,20. Meaning value between 2,20 are tested.' ) 
	parser.add_argument("-olr", "--optimizer_lr", type=str, required=False, nargs='?', const='1e-4,0.01', default='1e-4,0.01', metavar="RANGE", help='The linear  rate value of the optimizer. Default 1e-4,o.o1. Meaning doing the tune.loguniform between those two values.')
	parser.add_argument("-ns", "--number_sample", type=int, required=False, nargs='?', const=15, default=15, metavar="EXPERIMENTS", help='The Ray tune.Tuner tune_config num_samples variable. Meaning the number of model training in parallel for each "step" of the Hyperparameter search. Default 15.')

	parser.add_argument("--modules_version", type=str, required=False, nargs='?', const='False', default='False', metavar='VERBOSE', help='auxiliary flag top check module version used byt this script.')

	args = parser.parse_args()
	return args


def main(data, Batch_size, Shuffle, seq_len, Epochs, filter_size, optimizer_lr, number_sample, modules_version='False'):

	if eval(modules_version):
		print('python :', sys.version, '\n',  'numpy :', np.__version__ , '\n', 'torch :', torch.__version__, '\n', 'ray :', ray.__version__)

	# load the fasta file using the pytorch fasta loader
	pytorch_loader = fastaDataset(data)
	train_set = DataLoader(pytorch_loader, batch_size=int(Batch_size.split(',')[1]), shuffle=Shuffle)
	
	# define the loss function
	loss_function = nn.MSELoss()

	# initiate the tune trainer
	mnn_trainer = MnnTrainer(train_loader=train_set, test_loader=train_set, loss_function=loss_function, epochs=Epochs, size=seq_len)

	# Creating the search space
	step = ( int(Batch_size.split(',')[1]) - int(Batch_size.split(',')[0]) ) / 9
	batch_ranges = [int( int(Batch_size.split(',')[0]) + i * step) for i in range(10)]
	config = {'filter_size':tune.sample_from(lambda _: np.random.randint( int(filter_size.split(',')[0]), int(filter_size.split(',')[1]) )),
              'learning_rate':tune.loguniform( float(optimizer_lr.split(',')[0]), float(optimizer_lr.split(',')[1]) ),
              'batch_size':tune.choice( batch_ranges )}

	# run a tune run
	dfs = mnn_trainer.tune(search_space=config, num_samples=number_sample)
	best_result = dfs.get_best_result(metric='accuracy', mode='max')
	checkpoint = best_result.checkpoint.to_dict()

	# save the best model and model architecture
	torch.save(mnn_trainer.model.state_dict(), 'best_model.pt')
	with open("architecture.txt", 'w') as arch_out:
		arch_out.write( str( mnn_trainer.model.get_hyper_parameters() ) )

	# printing accuracy of the best model
	print("printing accuracy of the best model")
	print(best_result.metrics)
	print("printing model")
	print(mnn_trainer.model)


if __name__ == "__main__":
	args = get_args()

	main(args.infasta, args.batch_size, args.shuffle, args.seq_len, args.epochs, args.filter_size, \
            args.optimizer_lr, args.number_sample, args.modules_version)
