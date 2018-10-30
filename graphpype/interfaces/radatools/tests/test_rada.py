"""test rada"""
import os

from graphpype.interfaces.radatools.rada import CommRada

try:
    import neuropycon_data as nd

except ImportError:
    print("Error, could not find neuropycon_data")


data_path = os.path.join(nd.__path__[0], "data", "data_con")
# conmat_file = os.path.join(data_path, "Z_cor_mat_resid_ts.npy")
# coords_file = os.path.join(data_path, "ROI_MNI_coords-Atlas.txt")
# Z_list_file = os.path.join(data_path, "data_graph", "Z_List.txt")
Pajek_net_file = os.path.join(data_path, "data_graph", "Z_List.net")


def test_CommRada():
    comm_rada = CommRada()
    comm_rada.inputs.Pajek_net_file = Pajek_net_file
    comm_rada.inputs.optim_seq = "WS trfr 1"

    val = comm_rada.run().outputs

    assert os.path.exists(val.rada_lol_file)
    assert os.path.exists(val.rada_log_file)
    assert os.path.exists(val.lol_log_file)

    os.remove(val.rada_lol_file)
    os.remove(val.rada_log_file)
    os.remove(val.lol_log_file)


test_CommRada()
