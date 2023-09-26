#!/usr/bin/env python3

import argparse

def get_args():

	"get the arguments when using from the commandline"

	parser = argparse.ArgumentParser(description="This script generates DNA sequence from a given starting motif.")
	parser.add_argument("-o", "--out_name", type=str, required=True, metavar="FILE", help='The file path for the generated DNBA sequences in fasta format.' )
	parser.add_argument("-sl", "--seq_len", type=int, required=False, nargs='?', const=100, default=100, metavar="LEN", help='Length in integer for the DNA seqs to be created. Default 100 (aa).' )
	parser.add_argument("-m", "--motif", type=str, required=False, nargs='?', const='aattttttttttttaa', default='aattttttttttttaa', metavar="SEQ", help='The motif sequence that is used to generate the DNA sequences for the positive set. default aattttttttttttaa .')
	parser.add_argument("-t", "--motif_tag", type=int, required=False, nargs='?', const=5, default=5, metavar="LEN", help='TODO write description' )
	parser.add_argument("-u", "--non_motif_tag", type=int, required=False, nargs='?', const=0, default=0, metavar="LEN", help='TODO write description' )

	args = parser.parse_args()
	return args


def main(out_name, seq_len, motif, motif_tag, non_motif_tag):
	print(out_name, seq_len, motif, motif_tag, non_motif_tag)


if __name__ == "__main__":
	args = get_args()

	main(args.out_name, args.seq_len, args.motif, args.motif_tag, args.non_motif_tag)
