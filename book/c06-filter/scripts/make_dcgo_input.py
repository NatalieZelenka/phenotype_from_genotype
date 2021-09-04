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
    p = argparse.ArgumentParser(description='Create DcGO input')
    p.add_argument(
    	'targets_file',
        type=str,  # decided not to use argparse.FileType('r') as it leaves file open
        help=f"Path to the targets input fasta file directory",
        )

    p.add_argument(
    	'supfam_file',
        type=str,  # decided not to use argparse.FileType('r') as it leaves file open
        help=f"Path to the supfam domains file",
        )

    p.add_argument(
    	'uniprot_map',
        type=str,  # decided not to use argparse.FileType('r') as it leaves file open
        help=f"Path to the uniprotkb mapping",
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

	#Load in uniprotKB id to ENSP id mapping
	uniprotkb_to_ensp = {}
	with open(args.uniprot_map) as f:
		for i, line in enumerate(f):
			if i==0: #skip header
				continue
			line = line.strip().split('\t')
			uniprotkb_to_ensp[line[0]] = line[1]

	fasta_file = os.path.join(args.indir,f"target.{args.species}.fasta")
	fastas = SeqIO.parse(open(fasta_file),'fasta')

	cafa_targets = {}
	for fasta in fastas:
		cafa_id, sequence = fasta.id, fasta.seq
		uniprotkb_id =  fasta.description.split(' ')[1]

		if uniprotkb_id in uniprotkb_to_ensp.keys():
			ensp_id = uniprotkbid_to_enspid[uniprotkb_id]
			line = [cafa_id, uniprotkb_id, ensp_id,[]]
			cafa_targets[ensp_id] = line
		else:
			#cannot map
			continue

	#Load in SUPERFAMILY file
	supfam_file = os.path.join(args.supfam_file)
	with open(supfam_file) as f:
		for line in f:
			if line[0] == '#':
				continue

			line = line.strip().split('\t')
			if line[0] == 'Genome ID':
				header = line
				print header
				continue 
			ensp_id = line[1]
			sf_id = line[5]
			if ensp_id in cafa_targets.keys():
				cafa_targets[ensp_id][3].append(sf_id)

	with open(args.outfile,'wb') as f:
		for ensp_id in cafa_targets.keys():
			cafa_id, uniprotkb_id, _, domain_list = cafa_targets[ensp_id]
			if len(domain_list) == 0:
				continue
			domains = ','.join(domain_list)
			line = '\t'.join([cafa_id, domains]) + '\n'
			f.write(line)

if __name__ == "__main__":
    run()
