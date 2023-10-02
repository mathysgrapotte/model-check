#!/usr/bin/env python3

import argparse
from src.data.generate_fasta import GenerateSingleFixedMotifDataset
import sys
import numpy as np

def get_args():

	"get the arguments when using from the commandline"

	parser = argparse.ArgumentParser(description="This script generates DNA sequence from a given starting motif.")
	parser.add_argument("-o", "--out_name", type=str, required=True, metavar="FILE", help='The file path for the generated DNBA sequences in fasta format.' )
	parser.add_argument("-sl", "--seq_len", type=int, required=False, nargs='?', const=100, default=100, metavar="LEN", help='Length in integer for the DNA seqs to be created. Default 100 (aa).' )
	parser.add_argument("-m", "--motif", type=str, required=False, nargs='?', const='aattttttttttttaa', default='aattttttttttttaa', metavar="SEQ", help='The motif sequence that is used to generate the DNA sequences for the positive set. default aattttttttttttaa .')
	parser.add_argument("-t", "--motif_tag", type=int, required=False, nargs='?', const=5, default=5, metavar="LEN", help='TODO write description' )
	parser.add_argument("-u", "--non_motif_tag", type=int, required=False, nargs='?', const=0, default=0, metavar="LEN", help='TODO write description' )
	parser.add_argument("-ns", "--num_seq", type=int, required=False, nargs='?', const=1000, default=1000, metavar="TOT", help='The total number of DNA sequences the script generates. Default 1k.')
	parser.add_argument("-p", "--motif_start", type=int, required=False, nargs='?', const=None, default=None, metavar="POS", help='If the start parameter is set to an integer, the motif starting input position is the said integer. Note : the user is responsible for inputing an integer, and for making sure that the motif is not out of bounds.')
	parser.add_argument("--modules_version", type=str, required=False, nargs='?', const='False', default='False', metavar='VERBOSE', help='auxiliary flag top check module version used byt this script.')

	args = parser.parse_args()
	return args


def main(out_name, seq_len, motif, motif_tag, non_motif_tag, num_seq, motif_start, modules_version='False'):

	# Generating DNA sequences
	singleFixedMotifDataset = GenerateSingleFixedMotifDataset(seq_len, motif, motif_tag, non_motif_tag, num_seq, motif_start)

	# write the fasta file
	singleFixedMotifDataset.write_fasta(out_name)

	# Printing if necessary the module versions
	if eval(modules_version):
		print('python :', sys.version, '\n',  'numpy :', np.__version__)  #, '\n', 'torch :', torch.version)


if __name__ == "__main__":
	args = get_args()

	main(args.out_name, args.seq_len, args.motif, args.motif_tag, args.non_motif_tag, args.num_seq, args.motif_start, args.modules_version)
