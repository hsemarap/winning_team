#!/usr/bin/python3

import numpy as np
import scipy.io as sio
import yaml
import pprint
from batsman_features import *
import itertools
import os

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

def get_matches(dir_name, num_files):
    """Get all matches in directory.
    If num_files is None, get all files."""
    matches = []
    files = []
    if num_files is None:
        num_files = len(os.listdir(dir_name))
    for f in os.listdir(dir_name)[:num_files]:
    # for f in [os.listdir(dir_name)[6]]:
    # for f in os.listdir(dir_name):
        # TODO: No idea why the test fails.
        # if os.path.isfile(os.path.abspath(f)):
        #     print (f)
        print(f)
        files.append(f)
        x = Match(parse_yaml(os.path.join(dir_name, f)), f)
        matches.append(x)
    return matches

def test_reading_files():
    season_dir = './raw-data/ipl/season-4-2011'
    matches = get_matches(season_dir, None)

    for i, match in enumerate(matches):
        print(batsman_total(match, 'BB McCullum'))
        print(batsman_num_balls(match, 'BB McCullum'))
        print(batsman_strike_rate(match, 'BB McCullum'))

def test_season_2_with_season_1_stats():
    season1_dir = './raw-data/ipl/season-1-2008'
    season2_dir = './raw-data/ipl/season-2-2009'
    num_files = None
    season1_matches = get_matches(season1_dir, num_files)
    # num_files = 1
    num_files = None
    season2_matches = get_matches(season2_dir, num_files)
    # last = 1
    last = len(season2_matches)
    matrix = []
    outcome_vector = []
    for match in season2_matches[:last]:
        fs = match.features(season1_matches)
        outcome = fs[-1]
        fs = fs[:-1]
        matrix.append(fs)
        outcome_vector.append(outcome)
    print(matrix)
    print(outcome_vector)
    sio.savemat('extracted-stats/season2-wrt-season1.mat',
                {'X': matrix, 'y': outcome_vector})

if __name__ == '__main__':
    print('Winning Team: ML on IPL\n')
    # test_matrix_save()
    # test_parse_yaml()

    # test_reading_files()
    test_season_2_with_season_1_stats()
