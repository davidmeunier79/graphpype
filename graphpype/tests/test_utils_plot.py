
"""test over plots (with matplotlib)"""

import os
import numpy as np

from graphpype.utils_plot import (plot_cormat)

# test if neuropycon_data package and data are available

tmp_dir  = "/tmp/test_graphpype"
nb_nodes = 100

def test_plot_cormat():
    """
    test plot_cormat
    """

    try:
        os.makedirs(tmp_dir)
    except OSError:
        print("dir {} already exists".format(tmp_dir))
        
    cor_mat = np.random.rand(nb_nodes,nb_nodes)
    
    plot_file = os.path.join(tmp_dir,"test_plot_cormat.png")
    
    print (cor_mat.shape)
    
    plot_cormat(plot_file, cor_mat = cor_mat)
