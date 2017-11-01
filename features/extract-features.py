#!/usr/bin/python3

import numpy as np
import scipy.io as sio
import yaml
import pprint

def test_matrix_save():
    """Test how to save a matrix in the MATLAB format.
    """
    xs = [range(1, 4), range(5, 8)]
    a = np.matrix(xs)
    print(a)
    sio.savemat('dummy-matrix.mat', {'a': a})

def parse_yaml(yaml_file):
    """
    """
    with open(yaml_file, 'r') as stream:
        try:
            data = yaml.load(stream)
            pprint.pprint(data)
        except yaml.YAMLError as exc:
            print(exc)

def test_parse_yaml():
    """Test parsing a YAML file.
    """
    f = "./raw-data/test-data/3-overs-335982.yaml"
    parse_yaml(f)

if __name__ == '__main__':
    print('Winning Team: ML on IPL\n')
    # test_matrix_save()
    test_parse_yaml()
