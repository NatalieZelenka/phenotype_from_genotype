import numpy as np
import pandas as pd


def week_to_year(number_str):
    max_weeks_preg = 40.5
    assert(float(number_str) <= max_weeks_preg)
    weeks_year = 52
    sig_figs = 3
    return -round((max_weeks_preg-float(number_str))/float(weeks_year), sig_figs)


class MapsHDBR:
    sex = {
        '46, XX': 'F',
        '46, XY': 'M',
        'unknown': np.nan,
        '46, xx': 'F',
        '46, xy': 'M',
    }

    age = {
        'Carnegie Stage 13': week_to_year(6),  #Carnegie Stage 13 is 6 weeks (gestational age)
        'Carnegie Stage 14': week_to_year(7),
        'Carnegie Stage 15': week_to_year(7),
        'Carnegie Stage 16': week_to_year(8),
        'Carnegie Stage 17': week_to_year(8),
        'Carnegie Stage 18': week_to_year(9),
        'Carnegie Stage 19': week_to_year(9),
        'Carnegie Stage 20': week_to_year(10),
        'Carnegie Stage 21': week_to_year(10),
        'Carnegie Stage 22': week_to_year(10),
        'Carnegie Stage 23': week_to_year(10),
        'Late 8 post conception weeks': week_to_year(10),
        '9 post conception weeks': week_to_year(11),
        '10 post conception weeks': week_to_year(12),
        '11 post conception weeks': week_to_year(13),
        '12 post conception weeks': week_to_year(14),
        '13 post conception weeks': week_to_year(15),
        '14 post conception weeks': week_to_year(16),
        '15 post conception weeks': week_to_year(17),
        '16 post conception weeks': week_to_year(18),
        '17 post conception weeks': week_to_year(19),
        '18 post conception weeks': week_to_year(20),
        '19 post conception weeks': week_to_year(21),
        '20 post conception weeks': week_to_year(22)
    }


def clean_sex(sex_str):
    if sex_str == 'female':
        cleaned_sex = 'F'
    elif sex_str == 'male':
        cleaned_sex = 'M'
    else:
        cleaned_sex = np.nan
    return cleaned_sex


def clean_techrep(techrep_str, exp):
    if type(techrep_str) == str:
        cleaned_techrep = exp+'-T' + techrep_str.replace('group','').strip().zfill(3)
    else:
        cleaned_techrep = np.nan
    return cleaned_techrep


def clean_tissue(tissue):
    if type(tissue) == str:
        cleaned_tissue = tissue
        assert('UBERON' in cleaned_tissue)
    elif tissue is None:
        cleaned_tissue = np.nan
    else:
        cleaned_tissue = tissue.iloc[0]  # There are multiple mapping, just choose the first.
        assert('UBERON' in cleaned_tissue)
    return cleaned_tissue
