import numpy as np


# ----------------------------------------------------------------------------- periodic array indexing

def index(array, *indices):
    if len(indices) != len(array.shape):
        raise ValueError("Wrong number of indexes. Expected " + str(len(array.shape)) + " indexes, got " + str(len(indices)) + ".")
    
    indices = np.mod(indices, array.shape)
    return array[indices]


