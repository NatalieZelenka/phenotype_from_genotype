import os
import numpy
import sys
from Bio import SeqIO
import argparse

def parser():
    # ---------------------------------
    # PARSE ARGUMENTS AND SETUP LOGGING
    # ---------------------------------
    # Parse arguments:
    p = argparse.ArgumentParser(description='Get list of uniprot KB ids from CAFA fasta file')
    p.add_argument(
    	'indir',
        metavar='INDIR',
        type=str,  # decided not to use argparse.FileType('r') as it leaves file open
        help=f"Path to the targets input fasta file directory",
        )

    p.add_argument(
    	'outfile',
        type=str,
        help='Path to output file.',
        )

    p.add_argument(
    	'--species',
        type=int,
        default=9606, # human
        help='Path to output file.',
        )

    return p


def run(arguments=None):
	"""
	Get list of uniprot KB ids to load into the website and get the mapping
	"""
    if args is None:
        args = parser().parse_args(sys.argv[1:])

	fasta_file = os.path.join(args.indir,f"target.{args.species}.fasta")
	fasta = SeqIO.parse(open(fasta_file),'fasta')

	uniprotKBIDlist = []
	CAFATargets = {}
	for fasta in FASTAsequences:
		CAFAid, sequence = fasta.id, fasta.seq
		uniprotKBid =  fasta.description.split(' ')[1]
		uniprotKBIDlist.append(uniprotKBid)
	uniprotKBIDlist = list(set(uniprotKBIDlist))

	with open(args.outfile,'w') as f:
		for uniprotKBid in uniprotKBIDlist:
			f.write(uniprotKBid + '\n')

if __name__ == "__main__":
    run()

