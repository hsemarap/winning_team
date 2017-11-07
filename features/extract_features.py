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
    if num_files is None:
        num_files = len(os.listdir(dir_name))
    for f in os.listdir(dir_name)[:num_files]:
        try:
            x = Match(parse_yaml(os.path.join(dir_name, f)), f)
            matches.append(x)
        except:
            print('Error processing file', f)
    return matches

def test_reading_files():
    season_dir = './raw-data/ipl/season-4-2011'
    matches = get_matches(season_dir, None)

    for i, match in enumerate(matches):
        print(batsman_total(match, 'BB McCullum'))
        print(batsman_num_balls(match, 'BB McCullum'))
        print(batsman_strike_rate(match, 'BB McCullum'))

def rolling_stats(xs, fn, initial_past = []):
    """Get value of fn for each element with previous elements as additional input.
    """
    past = initial_past
    result = []
    for x in xs:
        result.append(fn(x, past))
        past.append(x)
    return result

def write_feature_matrix(mxs, path):
    """Write feature matrix mxs as MATLAB training set and label set.
    """
    matrix = []
    outcome_vector = []
    for fs in mxs:
        outcome = fs[-1]
        fs = fs[:-1]
        matrix.append(fs)
        outcome_vector.append(outcome)
    readable_output_file = path + '.readable'
    mat_file = path
    # print(matrix)
    # print(outcome_vector)
    with open(readable_output_file, 'w+') as rf:
        rf.write(str(matrix))
        rf.write('\n')
        rf.write(str(outcome_vector))
    sio.savemat(mat_file,
                {'X': matrix, 'y': outcome_vector})

def concat(xs):
    return list(itertools.chain(*xs))

def generate_stats():
    season1_dir = './raw-data/ipl/season-1-2008'
    season2_dir = './raw-data/ipl/season-2-2009'
    season3_dir = './raw-data/ipl/season-3-2010'
    season4_dir = './raw-data/ipl/season-4-2011'
    season5_dir = './raw-data/ipl/season-5-2012'
    season6_dir = './raw-data/ipl/season-6-2013'
    season7_dir = './raw-data/ipl/season-7-2014'
    season8_dir = './raw-data/ipl/season-8-2015'
    season9_dir = './raw-data/ipl/season-9-2016'
    season10_dir = './raw-data/ipl/season-10-2017'

    num_files = None
    # num_files = 10
    season1_matches = get_matches(season1_dir, num_files)

    later_seasons = [season2_dir, season3_dir, season4_dir]
    # num_files = 1
    num_files = None
    per_season_matches = [get_matches(f, num_files) for f in later_seasons]

    later_matches = concat(per_season_matches)
    # last = 1
    last = len(later_matches)

    # mxs = rolling_stats(later_matches[:last], lambda x, xs: x.features(xs), season1_matches)
    mmxs = rolling_stats(per_season_matches,
                         lambda s, past_ss: (rolling_stats(s[:last], lambda x, xs: x.features(xs), concat(past_ss))),
                         [season1_matches])
    for i, matrix in enumerate(mmxs):
        write_feature_matrix(matrix, 'extracted-stats/season%d-alone-rolling-stats.mat' % (i + 2))

if __name__ == '__main__':
    print('Winning Team: ML on IPL\n')
    # test_matrix_save()
    # test_parse_yaml()

    # test_reading_files()
    generate_stats()
