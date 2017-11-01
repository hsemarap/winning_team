#!/usr/bin/python3

import numpy as np
import scipy.io as sio

def test_matrix_save():
    """Test how to save a matrix in the MATLAB format.
    """
    xs = [range(1, 4), range(5, 8)]
    a = np.matrix(xs)
    print(a)
    sio.savemat('dummy-matrix.mat', {'a': a})

if __name__ == '__main__':
    print('Winning Team: ML on IPL\n')
    test_matrix_save()
