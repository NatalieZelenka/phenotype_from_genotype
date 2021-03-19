from .. import fantom_tpm_clean as tpm
import pytest

@pytest.mark.skip
def test_meaning_of_hg19_in_label():
    """
    Check that the ids beginning hg38 account for the newly found ones mentioned in this paper:
    https://www.nature.com/articles/sdata2017107
    :return:
    """
    tpm_file = '../c06-combining/data/experiments/fantom/hg38_fair+new_CAGE_peaks_phase1and2_tpm_ann.osc.txt'
    all_cage_tpm = tpm.read_tpm(tpm_file, dtypes={'entrezgene_id': object})

    count_19 = 0
    count_38 = 0
    for id_ in all_cage_tpm.index:
        if id_[2:4] == '19':
            count_19 += 1
        if id_[2:4] == '38':
            count_38 += 1

    assert(round(count_38 / 500.0) * 500.0 == 8500)  # round to nearest 500
    assert(count_19 + count_38 == len(all_cage_tpm.index))

    return None


