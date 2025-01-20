import numpy as np

# array = np.array(range(10))

# def pick(array, *indices):
#     if len(indices) != len(array.shape):
#         raise ValueError("Wrong number of indexes. Expected " + str(len(array.shape)) + " indexes, got " + str(len(indices)) + ".")
    
#     indices = np.mod(indices, array.shape)
#     return array[indices]


# for i in range(-15,15):
#     print(pick(array, i))
    
    
array = np.zeros((2,10))
array2 = np.zeros((10,2))

print(array[0])
print(array2[0])