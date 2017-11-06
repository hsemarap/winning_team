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

def get_matches(dir_name):
    """Get all matches in directory."""
    matches = []
    files = []
    num_files = 10
    # num_files = 1
    for f in itertools.islice(os.listdir(dir_name), num_files):
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
    matches = get_matches(season_dir)

    for i, match in enumerate(matches):
        print(batsman_total(match, 'BB McCullum'))
        print(batsman_num_balls(match, 'BB McCullum'))
        print(batsman_strike_rate(match, 'BB McCullum'))

def test_season_2_with_season_1_stats():
    """
    """
    season1_dir = './raw-data/ipl/season-1-2008'
    season2_dir = './raw-data/ipl/season-2-2009'
    season1_matches = get_matches(season1_dir)
    season2_matches = get_matches(season2_dir)
    match1 = season2_matches[0]
    fs = match1.features(season1_matches)
    print(fs)

if __name__ == '__main__':
    print('Winning Team: ML on IPL\n')
    # test_matrix_save()
    # test_parse_yaml()

    # test_reading_files()
    test_season_2_with_season_1_stats()
