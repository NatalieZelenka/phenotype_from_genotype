import pandas as pd
from myst_nb import glue
import logging
import time
import numpy as np
import datetime
import os

def get_dtypes(header):
    dtypes = {'00Annotation': object}
    for i, header_item in enumerate(header):
        if i < 6:
            dtypes[header_item] = object
        else:
            dtypes[header_item] = np.float64
    return dtypes


def get_cage_stats(transcript_tpm):
    # How many CAGE peaks map to multiple HGNC id genes?
    hgnc_id_duplicates = transcript_tpm[transcript_tpm['hgnc_id'].str.contains(' ', na=False)].shape[0]
    logging.info(f"There are {hgnc_id_duplicates} CAGE peaks that map to multiple HGNC ids (genes)")
    glue("hgnc_id_duplicates", hgnc_id_duplicates, display=False)

    entrezgene_id_duplicates = transcript_tpm[transcript_tpm['entrezgene_id'].str.contains(' ', na=False)].shape[0]
    logging.info(f"There are {entrezgene_id_duplicates} CAGE peaks that map to multiple Entrezgene ids")
    glue("entrezgene_id_duplicates", entrezgene_id_duplicates, display=False)

    total_gene_id_duplicates = transcript_tpm[(
                transcript_tpm['hgnc_id'].str.contains(' ', na=False) |
                transcript_tpm['entrezgene_id'].str.contains(' ', na=False))].shape[0]
    logging.info(f"There are {total_gene_id_duplicates} CAGE peaks that map to multiple genes (HGNC or entrezgene IDs)")
    glue("total_gene_id_duplicates", total_gene_id_duplicates, display=False)


def read_tpm(tpm_file, long_ids_to_keep=None, long_ids_to_new_ff=None, dtypes=None):
    start = time.time()

    transcript_tpm = pd.read_csv(
        tpm_file,
        delimiter='\t', comment='#', dtype=dtypes,
        usecols=long_ids_to_keep,
    )
    transcript_tpm.drop([0], axis='index', inplace=True)
    transcript_tpm.set_index('00Annotation', inplace=True)
    if long_ids_to_new_ff:
        transcript_tpm.rename(columns=long_ids_to_new_ff, inplace=True)

    end = time.time()
    logging.info(f"Read file in {end-start} seconds")

    return transcript_tpm


def remove_non_proteins(transcript_tpm):
    transcript_tpm.dropna(axis=0, subset=['uniprot_id'], inplace=True)
    return transcript_tpm


def read_and_clean_tpm(tpm_file, long_ids_to_keep, long_ids_to_new_ff, dtypes):
    """
    Reads orginal FANTOM human CAGE peaks file
    """
    # TODO: Save protein centric expression file
    # TODO: Rename transcript tpm to CAGE tpm?

    transcript_tpm = read_tpm(tpm_file, long_ids_to_keep, long_ids_to_new_ff, dtypes)
    sep_in_col = ' '  # In expression file, multiple values in a column are separated by a space.
    n_peaks = transcript_tpm.shape[0]  # Total number of CAGE peaks in FANTOM5 data set
    glue("total_F5_peaks", n_peaks, display=False)

    transcript_tpm = remove_non_proteins(transcript_tpm)
    n_peaks_protein = transcript_tpm.shape[0]  # Number of peaks which are protein-coding (as mapped by FANTOM)
    glue("has_protein_F5_peaks", n_peaks_protein, display=False)

    transcript_tpm['uniprot_list'] = transcript_tpm['uniprot_id'].str.split(sep_in_col)

    get_cage_stats(transcript_tpm)

    # Remove gene duplicates per CAGE TSS (due to overlapping CAGE TSS)
    transcript_tpm = transcript_tpm[
        ~(transcript_tpm['hgnc_id'].str.contains(' ', na=False) |
          transcript_tpm['entrezgene_id'].str.contains(' ', na=False))
    ]

    n_peaks_single_gene = transcript_tpm.shape[0]  # Number of peaks which are protein-coding (as mapped by FANTOM)
    glue("single_gene_F5_peaks", n_peaks_single_gene, display=False)

    return transcript_tpm


def get_protein_tpm(transcript_tpm):
    """
    Turns cage-peak centric tpm into protein-centric tpm

    """
    # Create expression by protein (uniprot ID), rather than by transcript
    protein_tpm = transcript_tpm.explode('uniprot_list').groupby(['uniprot_list', 'entrezgene_id', 'hgnc_id']).sum()
    protein_tpm.reset_index(level=['hgnc_id', 'entrezgene_id'], inplace=True)
    protein_tpm.rename_axis(index='uniprot_id')
    # Every protein ID should have at least one gene ID
    assert (protein_tpm[protein_tpm['entrezgene_id'].isna()].shape[0] == 0)
    assert (protein_tpm[protein_tpm['hgnc_id'].isna()].shape[0] == 0)

    glue("protein_expression_total", protein_tpm.shape[0], display=False)
    protein_tpm.head()

    rows_left_multiple_genes = protein_tpm[protein_tpm.index.duplicated(keep=False)].shape[0]
    logging.info(f"Number of remaining rows that map to multiple genes: {rows_left_multiple_genes}")
    glue("rows_left_multiple_genes", rows_left_multiple_genes, display=False)

    proteins_multiple_genes = len(protein_tpm[protein_tpm.index.duplicated(keep=False)].index.unique())
    logging.info(f"Number of proteins that map to multiple genes: {proteins_multiple_genes}")
    glue("proteins_multiple_genes", proteins_multiple_genes, display=False)

    protein_tpm[protein_tpm.index.duplicated(keep=False)].head()

    protein_tpm = protein_tpm[~protein_tpm.index.duplicated(keep=False)]
    assert (protein_tpm.shape[0] == len(protein_tpm.index.unique()))
    glue("unique_proteins", protein_tpm.shape[0], display=False)

    return protein_tpm


def save_protein_tpm(df, file_path, over_write=False):
    """
    :param df: Pandas dataframe: protein tpm file.
    :param  path to file
    :param over_write: if True, over-write existing file
    :return:
    """
    if (not os.path.exists(file_path)) or over_write:
        f = open(file_path, 'a')
        f.write(f"# Protein-centric TPM. Created by {os.path.split(__file__)[1]} at"
                f" {datetime.datetime.now().strftime('%d/%m/%y, %H:%M:%S')}\n")
        df.to_csv(f, sep='\t')
        f.close()
    return None


def save_long_ids(long_ids_to_new_ff, file_path, over_write=False):
    """
    :param long_ids_to_new_ff: dictionary of mappings between long ids and new FF accessions (including tech rep info)
    :param file_path: path to file
    :param over_write: if True, over-write existing file
    :return:
    """
    if (not os.path.exists(file_path)) or over_write:
        accessions_to_keep = [x[0] for x in pd.Series(long_ids_to_new_ff.values()).str.split('_') if x[0][:2] == 'FF']
        with open(file_path, 'w') as f:
            f.write(f"# List of FF accessions (old - no rep info) to keep. Created by {os.path.split(__file__)[1]} at"
                    f" {datetime.datetime.now().strftime('%d/%m/%y, %H:%M:%S')}\n")
            for accession in accessions_to_keep:
                f.write(accession + '\n')
    return None
