import pandas as pd
from myst_nb import glue
import logging


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


def read_and_clean_tpm(tpm_file):
    """
    Reads orginal FANTOM human CAGE peaks file
    """
    # TODO: Use to restrict protein-centric expression as read in file
    # TODO: Save protein centric expression file
    # TODO: Rename transcript tpm to CAGE tpm

    transcript_tpm = pd.read_csv(
        tpm_file,
        delimiter='\t', comment='#', dtype={'entrezgene_id': object})
    transcript_tpm.drop([0], axis='index', inplace=True)
    transcript_tpm.set_index('00Annotation', inplace=True)

    sep_in_col = ' '  # In expression file, multiple values in a column are separated by a space.

    n_peaks = transcript_tpm.shape[0]  # Total number of CAGE peaks in FANTOM5 data set
    glue("total_F5_peaks", n_peaks, display=False)

    transcript_tpm.dropna(axis=0, subset=['uniprot_id'], inplace=True)
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
