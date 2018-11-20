import os
import shutil
from graphpype.nodes.modularity import (ComputeNetList, ComputeNodeRoles)

try:
    import neuropycon_data as nd

except ImportError:
    print("neuropycon_data not installed")


data_path = os.path.join(nd.__path__[0], "data", "data_con")
conmat_file = os.path.join(data_path, "Z_cor_mat_resid_ts.npy")
coords_file = os.path.join(data_path, "ROI_MNI_coords-Atlas.txt")
Z_list_file = os.path.join(data_path, "data_graph", "Z_List.txt")
Pajek_net_file = os.path.join(data_path, "data_graph", "Z_List.net")
lol_file = os.path.join(data_path, "data_graph", "Z_List.lol")

tmp_dir = "/tmp/test_graphpype"
if os.path.exists(tmp_dir):
    shutil.rmtree(tmp_dir)

os.makedirs(tmp_dir)
os.chdir(tmp_dir)


def test_compute_net_list():
    """ test ComputeNetList"""
    compute_net_list = ComputeNetList()
    compute_net_list.inputs.Z_cor_mat_file = conmat_file

    val = compute_net_list.run().outputs
    print(val)
    assert os.path.exists(val.net_List_file)
    os.remove(val.net_List_file)


def test_compute_node_roles():
    """ test ComputeNodeRoles"""
    compute_node_roles = ComputeNodeRoles()
    compute_node_roles.inputs.rada_lol_file = lol_file
    compute_node_roles.inputs.Pajek_net_file = Pajek_net_file

    val = compute_node_roles.run().outputs
    print(val)
    assert os.path.exists(val.node_roles_file)
    assert os.path.exists(val.all_Z_com_degree_file)
    assert os.path.exists(val.all_participation_coeff_file)

    os.remove(val.node_roles_file)
    os.remove(val.all_Z_com_degree_file)
    os.remove(val.all_participation_coeff_file)