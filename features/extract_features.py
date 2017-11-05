#!/usr/bin/python3

import numpy as np
import scipy.io as sio
import yaml
import pprint
from batsman_features import *
import itertools

def test_matrix_save():
    """Test how to save a matrix in the MATLAB format.
    """
    xs = [range(1, 4), range(5, 8)]
    a = np.matrix(xs)
    print(a)
    sio.savemat('dummy-matrix.mat', {'a': a})

def parse_yaml(yaml_file):
    """Return YAML data from yaml_file.
    """
    with open(yaml_file, 'r') as stream:
        try:
            data = yaml.load(stream)
            # pprint.pprint(data)
            return data
        except yaml.YAMLError as exc:
            print(exc)

def test_parse_yaml():
    """Test parsing a YAML file.
    """
    f = "./raw-data/test-data/3-overs-335982.yaml"
    parse_yaml(f)

def test_reading_files():
    import os
    season_dir = './raw-data/ipl/season-4-2011'
    matches = []
    files = []
    for f in itertools.islice(os.listdir(season_dir), 4):
        # TODO: No idea why the test fails.
        # if os.path.isfile(os.path.abspath(f)):
        #     print (f)
        print(f)
        files.append(f)
        x = Match(parse_yaml(os.path.join(season_dir, f)))
        matches.append(x)

    for i, match in enumerate(matches):
        print(files[i])
        print(batsman_total(match, 'BB McCullum'))
        print(batsman_num_balls(match, 'BB McCullum'))
        print(batsman_average(match, 'BB McCullum'))

if __name__ == '__main__':
    print('Winning Team: ML on IPL\n')
    # test_matrix_save()
    # test_parse_yaml()

    test_reading_files()
