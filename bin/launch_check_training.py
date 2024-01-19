#!/usr/bin/env python3

import argparse
from src.data.pytorch_loaders import fastaDataset
from src.learner.tune_trainer import Trainer 
from src.model.mnn_models import Net
from torch.utils.data import DataLoader
import sys
import ray
import numpy 
import torch
from torch import nn
import torch.optim as optim

def get_args():

	"get the arguments when using from the commandline"

	parser = argparse.ArgumentParser(description="This scripts loads a fasta file in the dataloder and then tries to do a testing train run of th emodel.")
	parser.add_argument("-i", "--infasta", type=str, required=True, metavar="FILE", help='The file path for the DNA sequences in fasta format.')
	parser.add_argument("-bs", "--batch_size", type=str, required=False, nargs='?', const='10,100', default='10,100', metavar="BATCH", help='The size of the batches in which the data are dived. Default 10,100. Meaninng .t the right value will be used aka 100.' )
	parser.add_argument("-x", "--shuffle", type=str, required=False, nargs='?', const='True', default='True', metavar='BOOL', help='The flag to tell or not to shuffle around data in th edtaloader. Default true.' )
	parser.add_argument("-sl", "--seq_len", type=int, required=False, nargs='?', const=100, default=100, metavar="LEN", help='Length in integer for the DNA seqs. Default 100.' )
	parser.add_argument("--modules_version", type=str, required=False, nargs='?', const='False', default='False', metavar='VERBOSE', help='auxiliary flag top check module version used byt this script.')

	args = parser.parse_args()
	return args


def main(data, Batch_size, Shuffle, seq_len, modules_version='False', with_seed=True):

	if with_seed:
		# set the seed for reproducibility
		seed = 42
		torch.manual_seed(seed)
		torch.cuda.manual_seed(seed)
		torch.cuda.manual_seed_all(seed)
		torch.backends.cudnn.deterministic = True
		torch.backends.cudnn.benchmark = False
		numpy.random.seed(seed)
		numpy.random.RandomState(seed)
	
	if eval(modules_version):
                print('python :', sys.version, '\n',  'numpy :', numpy.__version__ , '\n', 'torch :', torch.__version__, '\n', 'ray :', ray.__version__)

	# load the fasta file using the pytorch fasta loader
	pytorch_loader = fastaDataset(data)
	train_set = DataLoader(pytorch_loader, batch_size=int(Batch_size.split(',')[1]), shuffle=Shuffle)
	
	# check if we can access the first batch
	for batch_idx, (data, target, sequence_names) in enumerate(train_set):
		if data.shape == torch.Size([int(Batch_size.split(',')[1]), 4, seq_len]) and target.shape == torch.Size([ int(Batch_size.split(',')[1]) ]) and len(sequence_names) == int(Batch_size.split(',')[1]):
			print("Data is loaded correctly")
			break
		else:
			print("Data batched does not have the expected size. given :", data.shape, 'expected :', [ int(Batch_size.split(',')[1]) , 4, seq_len])
			raise TypeError("Data not loaded correctly")

	
	# define the loss function
	loss_function = nn.MSELoss()
	
	# define the model
	model = Net(filter_size=4, size=seq_len)

	# define the optimizer
	optimizer = optim.SGD(model.parameters(), lr=0.01, momentum=0.5)

	# initiate the tune trainer
	tune_trainer = Trainer(train_set, train_set, loss_function)
	

	# make sure that the model is training (i.e. the weights are changing) after running a tune_trainer.train() call
	# compare the weights before and after training
	weights_before = str(list(model.parameters())[0])
	tune_trainer.train(model=model, optimizer=optimizer)
	weights_after = str(list(model.parameters())[0])
	if weights_before == weights_after:
		print('Weights have not updated, model is not training')
		raise TypeError("Model not training")
	else:
		print('Model is traininable, weights are changing')
	

	# run a testing run from the tune_trainer
	print(tune_trainer.test_regression(model=model, data_loader=train_set))


if __name__ == "__main__":
	args = get_args()

	main(args.infasta, args.batch_size, args.shuffle, args.seq_len, args.modules_version)
	
