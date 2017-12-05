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
        print(f)
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
        # print(batsman_strike_rate(match, 'BB McCullum'))

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

def write_all_feature_matrices(matrices, file_name_template, starting_season):
    start_index = starting_season
    for matrix in matrices:
        write_feature_matrix(matrix, file_name_template % start_index)
        start_index += 1

def get_all_season_matches(league):
    """Return matches for all seasons."""
    season1_dir = './raw-data/{}/season-1-2008'.format(league)
    season2_dir = './raw-data/{}/season-2-2009'.format(league)
    season3_dir = './raw-data/{}/season-3-2010'.format(league)
    season4_dir = './raw-data/{}/season-4-2011'.format(league)
    season5_dir = './raw-data/{}/season-5-2012'.format(league)
    season6_dir = './raw-data/{}/season-6-2013'.format(league)
    season7_dir = './raw-data/{}/season-7-2014'.format(league)
    season8_dir = './raw-data/{}/season-8-2015'.format(league)
    season9_dir = './raw-data/{}/season-9-2016'.format(league)
    season10_dir = './raw-data/{}/season-10-2017'.format(league)

    season_dir = './raw-data/{}/'.format(league)

    # num_files = 20
    num_files = None
    if league == 'ipl':
        all_seasons = [season1_dir, season2_dir, season3_dir, season4_dir,
                       season5_dir, season6_dir, season7_dir, season8_dir,
                       season9_dir, season10_dir]
        all_season_matches = [get_matches(f, num_files) for f in all_seasons]
    else:
        all_matches = get_matches(season_dir, num_files)
        # Percentage of initial matches that we will use to calculate stats
        # for later matches but not for training or testing.
        perc_ignored_initial_matches = 10/100
        total_matches = len(all_matches)
        num_ignored_initial_matches = int(perc_ignored_initial_matches * total_matches)
        num_ignored_initial_matches = num_ignored_initial_matches if num_ignored_initial_matches > 10 else 10
        all_season_matches = [all_matches[:num_ignored_initial_matches],
                              all_matches[num_ignored_initial_matches:]]
    return all_season_matches

def get_current_and_past_season_matches(all_season_matches, starting_season = 2, ending_season = 4):
    """Return per-season list of matches (past list, current list).

    past list: list of season matches from 1 to starting_season - 1.
    current list: list of season matches from starting_season to ending_season."""
    # Non-inclusive
    past_season_matches = all_season_matches[:starting_season-1]
    current_season_matches = all_season_matches[starting_season-1:ending_season]

    assert len(past_season_matches) == starting_season - 1
    assert len(current_season_matches) == ending_season - starting_season + 1
    return (past_season_matches, current_season_matches)

def rolling_stats_respect_structure(xs, stat_fn, past):
    """Get rolling stats returning the same list-of-lists structure as xs.

    For example, if xs is a list of season matches, then the output will have
    stats for each match but in the same list of lists structure. """
    mmxs = rolling_stats(xs,
                         lambda s, past_ss: (rolling_stats(s, stat_fn, concat(past_ss))),
                         past)
    return mmxs

def generate_and_write_season_matrices(starting_season, ending_season, all_season_matches, stat_fn, file_name_template):
    """Generate rolling stats for each season and write to files."""
    (past_season_matches, current_season_matches) = get_current_and_past_season_matches(all_season_matches,
        starting_season, ending_season)
    matrices = rolling_stats_respect_structure(
        current_season_matches,
        stat_fn,
        past_season_matches)
    write_all_feature_matrices(matrices, file_name_template, starting_season)

def generate_stats_for(targets, league = 'ipl'):
    """Generic function to get different datasets based on target."""
    all_season_matches = get_all_season_matches(league)
    if league == 'ipl':
        stats_dir = 'extracted-stats/'
        starting_season = 2
        ending_season = 10
    else:
        stats_dir = 'extracted-stats/' + league + '/'
        starting_season = 2
        ending_season = 2
    for target in targets:
        if target == 'strike rates alone':
            generate_and_write_season_matrices(2, 4, all_season_matches,
                                               strike_rate_features_fn,
                                               stats_dir + 'season%d-alone-rolling-stats.mat')
        elif target == 'averages 2-4':
            generate_and_write_season_matrices(2, 4, all_season_matches,
                                               average_features_fn,
                                               stats_dir + 'season%d-alone-average.mat')
        if target == 'strike rates all seasons':
            generate_and_write_season_matrices(starting_season, ending_season, all_season_matches,
                                               strike_rate_features_fn,
                                               stats_dir + 'season%d-alone-strike-rate.mat')
        elif target == 'averages all seasons':
            generate_and_write_season_matrices(starting_season, ending_season, all_season_matches,
                                               average_features_fn,
                                               stats_dir + 'season%d-alone-average.mat')
        elif target == 'batting average + strike rate all seasons':
            generate_and_write_season_matrices(starting_season, ending_season, all_season_matches,
                                               batting_average_plus_strike_rate_features_fn,
                                               stats_dir + 'season%d-alone-batting-average-plus-strike-rate.mat')
        elif target == 'bowling economy all seasons':
            generate_and_write_season_matrices(starting_season, ending_season, all_season_matches,
                                               bowling_economy_features_fn,
                                               stats_dir + 'season%d-alone-bowling-economy.mat')
        elif target == 'bowling strike rate all seasons':
            generate_and_write_season_matrices(starting_season, ending_season, all_season_matches,
                                               bowling_strike_rate_features_fn,
                                               stats_dir + 'season%d-alone-bowling-strike-rate.mat')
        elif target == 'bowling average + strike rate + economy all seasons':
            generate_and_write_season_matrices(starting_season, ending_season, all_season_matches,
                                               bowling_average_plus_strike_rate_plus_economy_features_fn,
                                               stats_dir + 'season%d-alone-bowling-average-plus-strike-rate-plus-economy.mat')
        elif target == 'team win rate all seasons':
            generate_and_write_season_matrices(starting_season, ending_season, all_season_matches,
                                               team_win_rate_features_fn,
                                               stats_dir + 'season%d-alone-team-win-rate.mat')
        elif target == 'team net run rate all seasons':
            generate_and_write_season_matrices(starting_season, ending_season, all_season_matches,
                                               team_net_run_rate_features_fn,
                                               stats_dir + 'season%d-alone-team-net-run-rate.mat')

if __name__ == '__main__':
    print('Winning Team: ML on IPL\n')
    # test_matrix_save()
    # test_parse_yaml()

    # test_reading_files()
    targets = [
        'strike rates all seasons',
        'averages all seasons',
        'bowling economy all seasons',
        'bowling strike rate all seasons',
        'team win rate all seasons',
        'team net run rate all seasons',
         'batting average + strike rate all seasons',
         'bowling average + strike rate + economy all seasons'
               ]
    # generate_stats_for(targets)
    generate_stats_for(targets, 'bbl')
