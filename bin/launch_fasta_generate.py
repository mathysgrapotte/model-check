#!/usr/bin/env python3

import argparse
from src.data.generate_fasta import GenerateSingleFixedMotifDataset
from src.data.generate_fasta import GenerateSingleJasparMotifDataset
import sys
import numpy as np
from csv import reader

def get_args():

	"get the arguments when using from the commandline"

	parser = argparse.ArgumentParser(description="This script generates DNA sequence from a given starting motif.")

	# Create a group so the following flags follow XOR logic, aka mutually exclusive.

	group = parser.add_mutually_exclusive_group(required=True)
	group.add_argument("-m", "--motif", type=str, metavar="FILE", help='The csv file containing the motif/s sequence/s that is/are used to generate the DNA sequences for the positive set. Based on the ammount of elemnts in the file either the single or multi class is called. if one motif is present then   GenerateSingleFixedMotifDataset  is called otherwise   GenerateMultiple*  is called. One between this and the following flag are mandatory. They are mutually exclusive.')
	group.add_argument("-j", "--jaspar", type=str, metavar="FILE", help='The csv file containing the JASPAR id/s  used to generate the DNA sequences for the positive set. Based on the ammount of elemnts in the file either the single or multi class is called. (like above). One between this and the above flag are mandatory')
	
	parser.add_argument("-o", "--out_name", type=str, required=True, metavar="FILE", help='The file path for the generated DNA sequences in fasta format.' )
	parser.add_argument("-f", "--base_fasta", type=str, required=False, nargs='?', const=None, default=None, metavar="FILE", help='The fasta file to use as a base for the enrichment of mitifs. If this flag is given with a valid path it is going to be used instead of generating random DNA sequences. Default None, aka enrich random DNA seq.')
	parser.add_argument("-sl", "--seq_len", type=int, required=False, nargs='?', const=100, default=100, metavar="LEN", help='Length in integer for the DNA seqs to be created. Default 100.' )
	parser.add_argument("-t", "--motif_tag", type=int, required=False, nargs='?', const=5, default=5, metavar="LEN", help='TODO write description' )
	parser.add_argument("-u", "--non_motif_tag", type=int, required=False, nargs='?', const=0, default=0, metavar="LEN", help='TODO write description' )
	parser.add_argument("-ns", "--num_seq", type=int, required=False, nargs='?', const=1000, default=1000, metavar="TOT", help='The total number of DNA sequences the script generates. Default 1k.')
	parser.add_argument("-p", "--motif_start", type=int, required=False, nargs='?', const=None, default=None, metavar="POS", help='If the start parameter is set to an integer, the motif starting input position is the said integer. Note : the user is responsible for inputing an integer, and for making sure that the motif is not out of bounds.')
	parser.add_argument("--modules_version", type=str, required=False, nargs='?', const='False', default='False', metavar='VERBOSE', help='auxiliary flag top check module version used byt this script.')

	args = parser.parse_args()
	return args


# Helper function to retrieve all fields ina csv file

def fromCSVtoList(file_path):

	elements = []

	with open(file_path, newline='') as csvfile:
		parsed_line = reader(csvfile)
		for row in parsed_line:
			elements.extend([elem.strip() for elem in row if elem.strip()])
	return elements



def main(motif, jaspar, out_name, base_fasta, seq_len, motif_tag, non_motif_tag, num_seq, motif_start, modules_version='False'):
	#print(motif, jaspar, out_name, base_fasta, seq_len, motif_tag, non_motif_tag, num_seq, motif_start, modules_version)

	# Decide what class to call based on wether the input is jaspar id or directly motifs
	dataset = None
	if jaspar:
		jaspar_id = fromCSVtoList(jaspar)
		
		# If there are more than one id then the multi version of the class is called
		if len(jaspar_id) == 1:
			dataset = GenerateSingleJasparMotifDataset(seq_len, jaspar_id[0])
			dataset.generate_dataset(num_seq, motif_start, base_fasta)
		else:
			# TODO Put here your multi class using jaspar
			raise SystemError('not implemented the multi class using jaspar ids')

	else:
		motif_id = fromCSVtoList(motif)
		
		# If there are more than one id then the multi version of the class is called
		if len(motif_id) == 1:
			dataset = GenerateSingleFixedMotifDataset(seq_len, motif_id[0])
			dataset.generate_dataset(motif_tag, non_motif_tag, num_seq, motif_start, base_fasta)
		else:
			# TODO Put here your multi class using jaspar
			raise SystemError('not implemented the multi class using jaspar ids')

	# write the fasta file
	dataset.write_fasta(out_name)


	# Printing if necessary the module versions
	if eval(modules_version):
		print('python :', sys.version, '\n',  'numpy :', np.__version__)  #, '\n', 'torch :', torch.version)



if __name__ == "__main__":
	args = get_args()

	main(args.motif, args.jaspar, args.out_name, args.base_fasta, args.seq_len, args.motif_tag, args.non_motif_tag, \
		 args.num_seq, args.motif_start, args.modules_version)
