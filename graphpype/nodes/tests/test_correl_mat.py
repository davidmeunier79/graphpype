import os

from graphpype.nodes.correl_mat import (ExtractTS, IntersectMask,
                                        ExtractMeanTS)

try:
    import neuropycon_data as nd

except ImportError:
    print("neuropycon_data not installed")

data_path = os.path.join(nd.__path__[0], "data", "data_nii")
img_file = os.path.join(data_path, "sub-test_task-rs_bold.nii")
gm_mask_file = os.path.join(data_path, "sub-test_mask-anatGM.nii")
wm_mask_file = os.path.join(data_path, "sub-test_mask-anatWM.nii")
indexed_mask_file = os.path.join(data_path, "Atlas", "indexed_mask-Atlas.nii")


def test_extract_ts():
    """ test ExtractTS"""
    extra_ts = ExtractTS()
    extra_ts.inputs.indexed_rois_file = indexed_mask_file
    extra_ts.inputs.file_4D = img_file

    val = extra_ts.run().outputs
    print(val)
    assert os.path.exists(val.mean_masked_ts_file)
    os.remove(val.mean_masked_ts_file)


def test_intersect_mask():
    """test IntersectMask"""
    intersect_mask = IntersectMask()
    intersect_mask.inputs.indexed_rois_file = indexed_mask_file
    intersect_mask.inputs.filter_mask_file = gm_mask_file

    val = intersect_mask.run().outputs
    print(val)
    assert os.path.exists(val.filtered_indexed_rois_file)
    os.remove(val.filtered_indexed_rois_file)


def test_extract_mean_ts():
    """test ExtractMeanTS"""
    extract_mean_ts = ExtractMeanTS()
    extract_mean_ts.inputs.file_4D = img_file
    extract_mean_ts.inputs.mask_file = wm_mask_file
    extract_mean_ts.inputs.suffix = "wm"

    val = extract_mean_ts.run().outputs
    print(val)
    assert os.path.exists(val.mean_masked_ts_file)
    os.remove(val.mean_masked_ts_file)
    # TODO raise Error if incompatible images


# test_extract_ts()
# test_intersect_mask()
test_extract_mean_ts()
