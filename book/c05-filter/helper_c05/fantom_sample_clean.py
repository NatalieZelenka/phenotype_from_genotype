import pandas as pd
from myst_nb import glue
import numpy as np
import logging
import re
import time
import os
import datetime


def clean_donor(desc_str):
    if 'donor' in str(desc_str):
        donor_id = desc_str.split('donor')[-1].strip()
        if len(donor_id) == 1:
            cleaned_donor = np.nan
        else:
            cleaned_donor = 'FANTOM-donor-' + donor_id
    else:
        cleaned_donor = np.nan
    return cleaned_donor


def clean_dev_stage(dev_str):
    dev_str = str(dev_str).lower()
    if 'adult' in dev_str:
        cleaned_dev_stage = 'adult'
    elif 'fetus' in dev_str:
        cleaned_dev_stage = 'fetus'
    else:
        cleaned_dev_stage = np.nan
    return cleaned_dev_stage


def month_to_year(number_str, fetus=False, sig_figs=2):
    months_in_year = 12.0
    if fetus:
        max_months_preg = 9.0
        assert (float(number_str) <= max_months_preg)
        return round(-(max_months_preg - float(number_str)) / float(months_in_year), sig_figs)
    else:
        return round(float(number_str) / float(months_in_year), sig_figs)


def week_to_year(number_str, fetus=False, sig_figs=2):
    weeks_year = 52.0
    if fetus:
        max_weeks_preg = 40.5
        assert (float(number_str) <= max_weeks_preg)
        return round(-(max_weeks_preg - float(number_str)) / float(weeks_year), sig_figs)
    else:
        return round(float(number_str) / float(weeks_year), sig_figs)


def clean_age_exact(dev_str, age_str):
    # Clean based on development string:
    o_dev_str = str(dev_str)
    dev_str = str(dev_str).lower()
    dev_str = dev_str.replace(' old', '')
    dev_str = dev_str.replace('years', 'year')
    dev_str = dev_str.replace('weeks', 'week')

    if ('-' in dev_str) or (',' in dev_str):
        cleaned_age_exact = np.nan
    elif 'year' in dev_str:
        if 'adult' in dev_str:
            cleaned_age_exact = dev_str.replace('year adult', '').strip()
        elif 'infant' in dev_str:
            cleaned_age_exact = dev_str.replace('year infant', '').strip()
        else:
            cleaned_age_exact = dev_str.replace('year', '').strip()
    elif 'week' in dev_str:
        cleaned_age_exact = week_to_year(dev_str.strip().replace('week fetus', ''), fetus=True)
    else:
        cleaned_age_exact = np.nan
    cleaned_age_exact = float(cleaned_age_exact)

    # Clean based on age string:
    o_age_str = str(age_str)
    age_str = str(age_str).lower()
    age_str = age_str.replace(' old', '')
    age_str = age_str.replace('months', 'month')
    age_str = age_str.replace('years', 'year')
    age_str = age_str.replace('year', '').strip()
    age_str = age_str.replace('weeks', 'week')
    if ('week' in age_str) and ('embryo' in age_str):
        cleaned_age_age = week_to_year(age_str.replace('week', '').replace('embryo', '').strip(), fetus=True)
    elif ('month' in age_str) and not ('embryo' in age_str):
        cleaned_age_age = month_to_year(re.match(r'\d+', age_str).group(), fetus=False)
    elif ('month' in age_str) and ('embryo' in age_str):
        cleaned_age_age = month_to_year(re.match(r'\d+', age_str).group(), fetus=True)
    else:
        cleaned_age_age = np.nan
    cleaned_age_age = float(cleaned_age_age)


    # Check if they agree (use dev string by default)
    if (not np.isnan(cleaned_age_exact)) and (not np.isnan(cleaned_age_age)):
        assert (cleaned_age_exact == cleaned_age_age)
    if np.isnan(cleaned_age_exact) and (not np.isnan(cleaned_age_age)):
        cleaned_age_exact = cleaned_age_age
        logging.info(
            f'Age string ({o_age_str}) contained info not in dev string ({o_dev_str}). Age string info used. instead')

    return cleaned_age_exact


def clean_age_range(dev_str):
    dev_str = str(dev_str).lower()
    dev_str = dev_str.replace(' old', '')
    dev_str = dev_str.replace('years', 'year')
    dev_str = dev_str.replace('weeks', 'week')
    dev_str = dev_str.replace('year adult', '')
    dev_str = dev_str.replace('year infant', '')

    if ('-' in dev_str):
        if 'week' in dev_str:
            num1, num2 = dev_str.replace('week fetus', '').strip().split('-')
            cleaned_age_range = [week_to_year(num2), week_to_year(num1)]
        else:
            cleaned_age_range = dev_str.strip().split('-')
        cleaned_age_range = [float(cleaned_age_range[0]), float(cleaned_age_range[1])]
    elif (',' in dev_str):
        age_range = [dev_str.split(',')[0], dev_str.split(',')[-1]]
        cleaned_age_range = [float(age_range[0].strip()), float(age_range[1].strip())]
    else:
        cleaned_age_range = np.nan

    if isinstance(cleaned_age_range, list):
        return [min(cleaned_age_range), max(cleaned_age_range)]
    else:
        return cleaned_age_range


def clean_sex(sex):
    nan_value = 'unlabeled'
    m = 'male'
    f = 'female'
    mixed = 'mixed'
    sex_dict = {'female': f, 'unknown': nan_value, 'male': m, 'M': m, 'F': f, 'mixed': mixed, 'nan': nan_value}
    try:
        sex_cleaned = sex_dict[sex]
    except:
        logging.info(f'Sex string "{sex}" could not be identified, converted to {nan_value}')
        sex_cleaned = nan_value
    return sex_cleaned


def get_sample_type(cat_str, desc_str):
    """
    Extract information about remaining (after removal of cell lines, fractionations, and time series) sample categories: tissues are divided into pool and donor types."""
    if cat_str == 'tissues':
        if 'pool' in desc_str:
            sample_type = 'tissues - pool'
        else:
            sample_type = 'tissues - donor'
    elif cat_str == 'primary cells':
        sample_type = 'primary cells'
    else:
        sample_type = np.nan
    return sample_type


def col_name_to_tech_rep(long_id):
    fantom_sample_accession = 'FF:' + long_id.split('.')[3]

    if 'tech_rep' in long_id:
        number = long_id.split('tech_rep')[-1][0]  # first character after 'tech_rep' (e.g. "1" or "2")
        fantom_sample_accession = fantom_sample_accession + '_tech_rep' + number
    elif ('rep2' in long_id) and ('11227-116C3' in fantom_sample_accession):
        logging.info(f"{fantom_sample_accession} has typo in long header name. Manually fixing in rep_info.")
        fantom_sample_accession = fantom_sample_accession + '_tech_rep2'
        number = 2
    else:
        number = None

    return fantom_sample_accession, number


def calc_has_tech_rep(long_id, ff):
    has_tech_rep = ('tech_rep' in long_id) or (('rep2' in long_id) and ('11227-116C3' in ff))
    return has_tech_rep


def get_tech_bio_reps(header, samples_info):
    """
    Extract information about which samples are technical and biological reps from TPM header.
    """
    category = 'Characteristics [Category]'
    wrong_accession = '11227-116C3'

    rep_info = []
    tech_rep_counter = 0
    bio_rep_counter = 0
    for col_name in header[6:]:
        fantom_sample_accession = 'FF:' + col_name.split('.')[3]
        has_tech_rep = calc_has_tech_rep(col_name, fantom_sample_accession)
        if has_tech_rep:
            fantom_sample_accession, number = col_name_to_tech_rep(col_name)
            if number == '1':
                tech_rep_counter += 1
            tech_rep_id = 'FANTOM-T' + str(tech_rep_counter).zfill(3)
        else:
            tech_rep_id = None

        if ('biol_rep' in col_name) or ('biol_%20rep' in col_name) or ('donor' in col_name):
            number = re.search(r"(donor)*(biol_rep)*(\d)", col_name).group(3)
            # number = col_name.split('biol_rep')[-1][0]  # first character after 'bio_rep' (e.g. "1" or "2")
            if number == '1':  # new sample with a bio rep
                bio_rep_counter += 1
            bio_rep_id = 'FANTOM-B' + str(bio_rep_counter).zfill(3)
        else:
            bio_rep_id = None

        # Check for any other 'reps' - for some reason regex was not working as expected.
        type_ = samples_info.loc[fantom_sample_accession.split('_')[0], category]
        if ('tech' not in col_name) and ('biol' not in col_name) \
                and ('rep' in col_name) and not ('strep' in col_name) and (type_ in ['primary cells', 'tissues']):
            assert(wrong_accession in fantom_sample_accession)

        rep_info.append([fantom_sample_accession, tech_rep_id, bio_rep_id])

    rep_info = pd.DataFrame(rep_info, columns=['Sample ID', 'Tech Rep ID', 'Bio Rep ID'])
    rep_info.set_index('Sample ID', inplace=True)

    return rep_info


def update_sample_info_labels(samples_info, rep_info):
    """
    Fantom accessions (e.g. FF:12225-129F2) are unique per physical sample, not per CAGE peak measurement.
    Technical replicates have the same Fantom accession. This is a problem because I often use them for mapping.
    This changes the sameples_info dataframe to use identifiers FF:12225-129F2_tech_rep1 and FF:12225-129F2_tech_rep2, to make it easier to map.
    And also returns a mapping (dict) between these.
    """

    tech_reps = rep_info.dropna(axis=0, subset=['Tech Rep ID'], how='all')['Tech Rep ID']
    nrow_a = samples_info.shape[0]

    # works by copying rows for the samples with tech reps (new ids), then removing old sample id rows:
    to_drop = set([])
    for new_ff in tech_reps.index:
        ff = new_ff.split('_')[0]

        assert(len(new_ff.split('_')) > 1)

        if ff in samples_info.index:
            samples_info.loc[new_ff] = samples_info.loc[ff].copy()
            to_drop.add(ff)

    nrow_b = samples_info.shape[0]
    samples_info.drop(index=list(to_drop), inplace=True)
    nrow_c = samples_info.shape[0]

    assert (nrow_b - nrow_a == 2 * len(to_drop))  # 2 tech reps for those FFs that have one
    assert (nrow_c - nrow_a == len(to_drop))

    return samples_info


def clean_samples_info(samples_info, rep_info):
    """
    Adds new columns to samples_info for cleaned versions of columns.
    """
    samples_info['Donor ID'] = samples_info['Charateristics [description]'].apply(clean_donor)
    #     samples_info['Age (years)'] = samples_info['Characteristics [Developmental stage]'].apply(clean_age_exact)
    samples_info['Age (years)'] = np.vectorize(clean_age_exact)(samples_info['Characteristics [Developmental stage]'],
                                                                samples_info['Characteristics [Age]'])
    samples_info['Age range (years)'] = samples_info['Characteristics [Developmental stage]'].apply(clean_age_range)
    samples_info['Developmental Stage'] = samples_info['Characteristics [Developmental stage]'].apply(clean_dev_stage)
    samples_info['Sex'] = samples_info['Characteristics [Sex]'].apply(clean_sex)
    samples_info['Sample Type'] = np.vectorize(get_sample_type)(samples_info['Characteristics [Category]'],
                                                                samples_info['Charateristics [description]'])
    samples_info['Tech Rep ID'] = rep_info.loc[samples_info.index, 'Tech Rep ID']
    samples_info['Bio Rep ID'] = rep_info.loc[samples_info.index, 'Bio Rep ID']

    collab_tidy = {
        'FANTOM5 OSC CORE (contact: Al Forrest)': 'FANTOM5 core, OSC, RIKEN',  # OSC = Riken Omics Science Centre
        'Peter Heutink': 'DZNE, Germany',  # DZNE = German Center for Neurodegenerative Diseases
        'Christine Wells (University of Queensland)': 'University of Queensland',
        'Michael Rehli (University of Regensberg)': 'University of Regensberg',
        'Matched_genome_OSC(contact:Al Forrest)': 'Matched genome, OSC, RIKEN',
        'Claudio Schneider LNCIB': 'LNCIB, Italy',
        'Mitsuhiro Ohshima (Nihon University School of Dentistry)': 'Nihon University',
        'Alessandro Bonetti': 'CLST, RIKEN',
        'Lennartsson': 'Karolinska Institutet',
        'Splicing (contact: Al Forrest)': 'Splicing, OSC, RIKEN',
    }
    samples_info['Characteristics [Collaboration]'] = samples_info['Characteristics [Collaboration]'].map(collab_tidy)
    samples_info.loc['FF:10027-101D9', 'Age (years)'] = np.nan
    samples_info.loc['FF:10027-101D9', 'Age range (years)'] = np.nan

    # Checks and glue:
    assert (len(samples_info.dropna(subset=['Age (years)', 'Age range (years)'], how='all')[
                    ['Age (years)', 'Age range (years)']].isnull().sum(
        axis=1).unique()) == 1)  # Have only age range OR age

    num_bio_rep_samples = (len(samples_info['Bio Rep ID'].unique()) - 1)
    glue('num_bio_rep_samples', num_bio_rep_samples, display=False)
    logging.info(f"There are {num_bio_rep_samples} remaining in data set")

    num_tech_rep_samples = len(samples_info['Tech Rep ID'].unique()) - 1
    logging.info(f"There are {num_tech_rep_samples} remaining in data set")
    glue('num_tech_rep_samples', num_tech_rep_samples, display=False)

    age_ranged = len(samples_info['Age range (years)'].dropna())
    glue('age_ranged', age_ranged, display=False)

    return samples_info


def read_CAGE_header():
    """
    Read in header of CAKE peaks expression file, containing measurement info
    """
    header = pd.read_csv('../c06-combining/data/experiments/fantom/hg38_fair+new_CAGE_peaks_phase1and2_tpm_ann.osc.txt',
                         delimiter='\t', comment='#', dtype={'entrezgene_id': object}, nrows=0)
    header = pd.Series(header.columns[1:])
    return header


def get_category_info(samples_info):
    """
    Glues (using myst_glue) information about the samples categories for use in thesis.
    """
    categories = samples_info['Characteristics [Category]'].value_counts()
    for category, freq in categories.iteritems():
        name_num_samps = category.replace(' ', '-') + '-num-samps'
        name_ex_id = category.replace(' ', '-') + '-ex-id'
        name_ex_desc = category.replace(' ', '-') + '-ex-desc'

        example = samples_info[samples_info['Characteristics [Category]'] == category].iloc[
            5]  # examples chosen (row 5) so that they contain anything too weird/not yet explained.

        glue(name_num_samps, freq, display=False)
        glue(name_ex_id, example.name, display=False)
        glue(name_ex_desc, example['Charateristics [description]'], display=False)


def read_samples_info():
    """
    Reads in FANTOM5 human samples files and checks that all samples are human.
    """
    samples_info_file_loc = '../c06-combining/data/experiments/fantom/fantom_humanSamples2.0.csv'
    samples_info = pd.read_csv(samples_info_file_loc, index_col=1)
    assert (len(samples_info['Chracteristics [Species]'].unique()) == 1)
    assert (samples_info['Chracteristics [Species]'].unique()[0] == 'Human (Homo sapiens)')
    get_category_info(samples_info)

    return samples_info


def restrict_samples(samples_info):
    """
    Restricts samples from Human Sample Info file to tissues and primary cells.
    """
    samples_info = samples_info[samples_info['Characteristics [Category]'].isin(['tissues', 'primary cells'])]
    glue("fantom-primary-tissue-samples", samples_info.shape[0], display=False)
    return samples_info


def long_ids_to_restricted_samples(samples_info, header):
    """
    Takes already restricted list of samples... Returns:
    - list of kept header IDs (long IDs) to read in from the expression file.
    - dictionary mapping from long header IDs to augmented Fantom accession IDs, e.g. "FF:10063-101H9_tech_rep1"
    """
    index_label = '00Annotation'  # not in header
    long_ids_to_new_ff = {index_label: index_label}
    long_ids_to_keep = [index_label]

    first_sample_index = 6
    for i, long_id in enumerate(header):
        if i < first_sample_index:  # not sample IDs, other column names (eg. "short_description", "uniprotgene_id")
            long_ids_to_new_ff[long_id] = long_id
            long_ids_to_keep.append(long_id)
        else:  # long sample ids e..g. "tpm.293SLAM%20rinderpest%20infection%2c%2012hr%2c%20biol_rep1.CNhs14413.13547-145I1.hg38.nobarcode"

            ff = 'FF:' + long_id.split('.')[3]  # original FF accession number, e.g. FF:10063-101H9

            has_tech_rep = calc_has_tech_rep(long_id, ff)
            if has_tech_rep:
                ff, _ = col_name_to_tech_rep(long_id)

            if ff in samples_info.index:
                long_ids_to_keep.append(long_id)
                long_ids_to_new_ff[long_id] = ff

    try:
        assert(len(long_ids_to_keep) == len(long_ids_to_new_ff))
    except AssertionError:
        logging.error(f"Error in calcuating `long_ids_to_keep` {len(long_ids_to_keep)} "
                      f"and `long_ids_to_new_ff` {len(long_ids_to_new_ff)}")
    try:
        assert(len(long_ids_to_new_ff) < len(header))
    except AssertionError:
        logging.error(f"Error in calculating `long_ids_to_new_ff` {len(long_ids_to_new_ff)} "
                      f"longer than `header` {len(header)}")

    try:
        # Samples info should be shorter due to lack of extra col info
        assert(samples_info.shape[0] + first_sample_index + 1 == len(long_ids_to_keep))
    except AssertionError:
        logging.error(f"Error in calculating `long_ids_to_keep` {len(long_ids_to_keep)} "
                      f"wrong size compared to `samples_info` {len(samples_info)}")

    return long_ids_to_keep, long_ids_to_new_ff


def save_sample_cleaned(df, file_path, over_write=False):
    """
    :param df: Pandas dataframe: samples info file.
    :param file_path: path to file
    :param over_write: if True, over-write existing file
    :return:
    """
    if (not os.path.exists(file_path)) or over_write:
        f = open(file_path, 'a')
        f.write(f"# Cleaned samples file. Created by {os.path.split(__file__)[1]} at"
                f" {datetime.datetime.now().strftime('%d/%m/%y, %H:%M:%S')}\n")
        df.to_csv(f, sep='\t')
        f.close()
    return None
