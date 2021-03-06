import unittest
from batsman_features import *
from extract_features import parse_yaml
from pprint import pprint

class TestBatsmenFeatures(unittest.TestCase):
    """
    Our basic test class
    """
    @classmethod
    def setUpClass(cls):
        yaml_file = "./raw-data/test-data/3-overs-335982.yaml"
        yaml_file2 = "./raw-data/test-data/3-overs-335983.yaml"
        cls.yaml_data = parse_yaml(yaml_file)
        cls.match = Match(cls.yaml_data, yaml_file)
        cls.match2 = Match(parse_yaml(yaml_file2), yaml_file2)
        cls.ball_1_point_2 = {
            'batsman': 'BB '
            'McCullum',
            'bowler': 'Z Khan',
            'non_striker': 'SC '
            'Ganguly',
            'runs': {
                'batsman': 4,
                'extras': 0,
                'total': 4
            }
        }
        cls.ball_2_point_2 = {
            'batsman': 'V Kohli',
            'bowler': 'AB Dinda',
            'non_striker': 'W '
            'Jaffer',
            'runs': {
                'batsman': 0,
                'extras': 0,
                'total': 0
            },
            'wicket': {
                'kind': 'bowled',
                'player_out': 'V '
                'Kohli'
            }
        }

    def setUp(self):
        pass

    def assertAlmostEqualLists(self, outputList, expectedList):
        """Assert that the given lists are element-wise almost equal."""
        self.assertEqual(len(outputList), len(expectedList))
        # print(outputList, expectedList)
        for o, e in zip(outputList, expectedList):
            self.assertAlmostEqual(o, e)

    def test_flatten_list_of_dicts(self):
        self.assertEqual(flatten_list_of_dicts([{1: 2}, {2: 3}]),
                         {1: 2, 2: 3})

    def test_flatten_yaml_dict(self):
        flat_innings = self.match.match_details['innings']
        self.assertEqual(flat_innings['1st innings']['deliveries'][1.2],
                         self.ball_1_point_2)
        self.assertEqual(flat_innings['2nd innings']['deliveries'][2.2],
                         self.ball_2_point_2)

    def test_runs_off_ball(self):
        self.assertEqual(120, 120)

    def test_get_first_ball(self):
        self.assertEqual(self.match.get_ball('1st innings',
                                             0.1),
                         {
                             'batsman': 'SC Ganguly',
                             'bowler': 'P Kumar',
                             'extras': {
                                 'legbyes': 1
                             },
                            'non_striker': 'BB '
                             'McCullum',
                             'runs': {
                                 'batsman': 0,
                                 'extras': 1,
                                 'total': 1
                             }
                        })

    def test_runs_off_ball(self):
        ball = self.match.get_ball('1st innings', 1.2)
        self.assertEqual(runs_off_ball(ball['batsman'], ball), 4)
        self.assertEqual(runs_off_ball(ball['non_striker'], ball), 0)

    def test_batsman_total(self):
        self.assertEqual(batsman_total(self.match, 'R Dravid'), 2)
        self.assertEqual(batsman_total(self.match, 'BB McCullum'), 23)

    def test_batsman_num_balls(self):
        self.assertEqual(batsman_num_balls(self.match, 'R Dravid'), 3)
        self.assertEqual(batsman_num_balls(self.match, 'BB McCullum'), 14)

    # def test_batsman_strike_rate(self):
    #     self.assertAlmostEqual(batsman_strike_rate(self.match, 'R Dravid'), 100 * 2/3)
    #     self.assertAlmostEqual(batsman_strike_rate(self.match, 'BB McCullum'), 100 * 23/14)
    #     self.assertAlmostEqual(batsman_strike_rate(self.match, 'Foo'), default_strike_rate)

    def test_overall_strike_rate(self):
        self.assertAlmostEqual(batsman_overall_strike_rate(
            get_player_stats_dict([self.match]), 'R Dravid'), 100 * 2/3)
        self.assertAlmostEqual(batsman_overall_strike_rate(
            get_player_stats_dict([self.match]), 'BB McCullum'), 100 * 23/14)
        self.assertAlmostEqual(batsman_overall_strike_rate(
            get_player_stats_dict([self.match]), 'Foo'), default_strike_rate)

    def test_unique_everseen(self):
        self.assertEqual(list(unique_everseen("aabbcedeeeb")),
                         ['a', 'b', 'c', 'e', 'd'])

    def test_get_players(self):
        self.assertEqual(list(self.match.get_first_batting_side_players()),
                         ['SC Ganguly', 'BB McCullum', 'AB Dinda', 'I Sharma'])
        self.assertEqual(list(self.match.get_second_batting_side_players()),
                         ['R Dravid', 'W Jaffer', 'V Kohli', 'JH Kallis', 'P Kumar', 'Z Khan'])

    def test_winner(self):
        self.assertEqual(self.match.winner(), 'Kolkata Knight Riders')

    def test_first_batting_side(self):
        self.assertEqual(self.match.first_batting_side(),
                         'Kolkata Knight Riders')

    def test_second_batting_side(self):
        self.assertEqual(self.match.second_batting_side(),
                         'Royal Challengers Bangalore')

    def test_first_batting_side_won(self):
        self.assertEqual(self.match.first_batting_side_won(), True)

    def test_match_features_strike_rate(self):
        output = strike_rate_features_fn(self.match, [self.match])
        x = default_strike_rate
        expected = [0.0, 164.28571428571428, x, x,
                    x, x, x, x, x, x, x,
                    66.66666666666667, 10.0, 20.0, 100.0,
                    x, x, x, x, x, x, x,
                    1]
        self.assertAlmostEqualLists(output, expected)

    def test_match_features(self):
        output = average_features_fn(self.match, [self.match])
        x = default_average
        expected = [0.0, 23.0, x, x,
                    x, x, x, x, x, x, x,
                    2.0, 1.0, 1.0, 1.0,
                    x, x, x, x, x, x, x,
                    1]
        self.assertAlmostEqualLists(output, expected)

    def test_get_player_stats_dict(self):
        matches = [self.match, self.match2]
        d = get_player_stats_dict(matches)
        self.assertEqual(d['BB McCullum']['total runs'], 23)
        self.assertEqual(d['BB McCullum']['total balls'], 14)
        self.assertEqual(d['JR Hopes']['total runs'], 14)
        self.assertEqual(d['JR Hopes']['total balls'], 8)
        self.assertEqual(d['BB McCullum']['batsman matches played'], 1)

    def test_batsman_num_matches(self):
        matches = [self.match, self.match2]
        d = get_player_stats_dict(matches)
        self.assertEqual(batsman_num_matches(d, 'BB McCullum'), 1)
        self.assertEqual(batsman_num_matches(d, 'Foo'), 0)

    def test_bowler_num_matches(self):
        matches = [self.match, self.match2]
        d = get_player_stats_dict(matches)
        self.assertEqual(bowler_num_matches(d, 'MS Gony'), 1)
        self.assertEqual(bowler_num_matches(d, 'Foo'), 0)

    def test_batsman_average(self):
        matches = [self.match, self.match2]
        d = get_player_stats_dict(matches)
        self.assertEqual(batsman_average(d, 'BB McCullum'), 23)
        self.assertEqual(batsman_average(d, 'Foo'), default_average)

    def test_batsman_average_plus_strike_rate(self):
        matches = [self.match, self.match2]
        d = get_player_stats_dict(matches)
        self.assertEqual(batsman_average_plus_strike_rate(d, 'Foo'), default_average_plus_strike_rate)
        self.assertEqual(batsman_average_plus_strike_rate(d, 'BB McCullum'), 23 + 100 * 23/14)

    def test_team_strike_rates(self):
        matches = [self.match]
        d = get_player_stats_dict(matches)
        team1 = self.match.get_first_batting_side_players()
        team2 = self.match.get_second_batting_side_players()
        x = default_strike_rate
        expected = [x] * 11
        expected[0] = 0.0
        expected[1] = 23 * 100 / 14
        self.assertAlmostEqualLists(self.match.team_strike_rates(d, team1),
                                    expected)
        # No wickets taken.
        expected = [x] * 11
        expected[0] = 100 * 2 / 3
        expected[1] = 100 * 1 / 10
        expected[2] = 100 * 1 / 5
        expected[3] = 100 * 1 / 1
        self.assertAlmostEqualLists(self.match.team_strike_rates(d, team2),
                                    expected)

    def test_team_averages(self):
        matches = [self.match]
        d = get_player_stats_dict(matches)
        team1 = self.match.get_first_batting_side_players()
        team2 = self.match.get_second_batting_side_players()
        x = default_average
        expected = [x] * 11
        expected[0] = 0.0
        expected[1] = 23.0
        self.assertAlmostEqualLists(self.match.team_averages(d, team1),
                                    expected)
        # No wickets taken.
        expected = [x] * 11
        expected[0] = 2
        expected[1] = 1
        expected[2] = 1
        expected[3] = 1
        self.assertAlmostEqualLists(self.match.team_averages(d, team2),
                                    expected)

    def test_team_average_plus_strike_rate(self):
        matches = [self.match]
        d = get_player_stats_dict(matches)
        team1 = self.match.get_first_batting_side_players()
        team2 = self.match.get_second_batting_side_players()
        x = default_average_plus_strike_rate
        expected = [x] * 11
        expected[0] = 0.0
        expected[1] = 23 + 100 * 23/14
        self.assertAlmostEqualLists(self.match.team_batting_average_plus_strike_rate(d, team1),
                                    expected)
        expected = [x] * 11
        expected[0] = 2 + 100 * 2 / 3
        expected[1] = 1 + 100 * 1 / 10
        expected[2] = 1 + 100 * 1 / 5
        expected[3] = 1 + 100 * 1 / 1
        self.assertAlmostEqualLists(self.match.team_batting_average_plus_strike_rate(d, team2),
                                    expected)

    def test_bowler_economy(self):
        matches = [self.match, self.match2]
        d = get_player_stats_dict(matches)
        self.assertEqual(bowler_economy(d, 'JDP Oram'), 10.0)
        self.assertEqual(bowler_economy(d, 'Foo'), default_bowling_economy)

    def test_bowler_average(self):
        matches = [self.match, self.match2]
        d = get_player_stats_dict(matches)
        pprint(d)
        self.assertEqual(bowler_average(d, 'JDP Oram'), default_bowling_average)
        self.assertEqual(bowler_average(d, 'AB Dinda'), 6.0)
        self.assertEqual(bowler_average(d, 'Foo'), default_bowling_average)

    def test_bowler_strike_rate(self):
        matches = [self.match, self.match2]
        d = get_player_stats_dict(matches)
        self.assertEqual(bowler_strike_rate(d, 'Foo'), default_bowling_strike_rate)
        self.assertEqual(bowler_strike_rate(d, 'I Sharma'), 6.0)
        self.assertEqual(bowler_strike_rate(d, 'AB Dinda'), 13.0)
        self.assertEqual(bowler_strike_rate(d, 'B Lee'), 13.0)

    def test_bowler_average_plus_strike_rate_plus_economy(self):
        matches = [self.match, self.match2]
        d = get_player_stats_dict(matches)
        self.assertEqual(bowler_average_plus_strike_rate_plus_economy(d, 'Foo'),
                         default_bowling_average_plus_strike_rate_plus_economy)
        self.assertEqual(bowler_average_plus_strike_rate_plus_economy(d, 'JDP Oram'), 10.0 + default_bowling_average + default_bowling_strike_rate)
        self.assertEqual(bowler_average_plus_strike_rate_plus_economy(d, 'I Sharma'), 5.0 + 6.0 + 5.0)
        self.assertEqual(bowler_average_plus_strike_rate_plus_economy(d, 'AB Dinda'), 6.0 + 13.0 + 3.0)
        self.assertEqual(bowler_average_plus_strike_rate_plus_economy(d, 'B Lee'), 12.0 + 13.0 + 6.0)

    def test_team_bowling_economies(self):
        matches = [self.match]
        d = get_player_stats_dict(matches)
        team1 = self.match.get_first_batting_side_players()
        team2 = self.match.get_second_batting_side_players()
        x = default_bowling_economy
        expected = [x] * 11
        expected[2] = 3.0
        expected[3] = 5.0
        self.assertAlmostEqualLists(self.match.team_bowling_economies(d, team1),
                                    expected)
        # No wickets taken.
        expected = [x] * 11
        expected[4] = 4.5
        expected[5] = 18.0
        self.assertAlmostEqualLists(self.match.team_bowling_economies(d, team2),
                                    expected)

    def test_team_bowling_average_plus_strike_rate_plus_economy(self):
        matches = [self.match]
        d = get_player_stats_dict(matches)
        team1 = self.match.get_first_batting_side_players()
        team2 = self.match.get_second_batting_side_players()
        x = default_bowling_average_plus_strike_rate_plus_economy
        expected = [x] * 11
        expected[2] = 6.0 + 3.0 + 13
        expected[3] = 5.0 + 6.0 + 5.0
        self.assertAlmostEqualLists(self.match.team_bowling_average_plus_strike_rate_plus_economy(d, team1),
                                    expected)
        expected = [x] * 11
        expected[4] = default_bowling_average + default_bowling_strike_rate + 4.5
        expected[5] = default_bowling_average + default_bowling_strike_rate + 18
        self.assertAlmostEqualLists(self.match.team_bowling_average_plus_strike_rate_plus_economy(d, team2),
                                    expected)

    def test_team_bowling_strike_rates(self):
        matches = [self.match]
        d = get_player_stats_dict(matches)
        team1 = self.match.get_first_batting_side_players()
        team2 = self.match.get_second_batting_side_players()
        x = default_bowling_strike_rate
        expected = [x] * 11
        expected[2] = 13.0
        expected[3] = 6.0
        self.assertAlmostEqualLists(self.match.team_bowling_strike_rates(d, team1),
                                    expected)
        # No wickets taken.
        expected = [x] * 11
        self.assertAlmostEqualLists(self.match.team_bowling_strike_rates(d, team2),
                                    expected)

    def test_team_win_rate(self):
        matches = [self.match, self.match2]
        d = get_player_stats_dict(matches)
        team1 = self.match.get_first_batting_side_players()
        team2 = self.match.get_second_batting_side_players()
        x = default_win_rate
        self.assertEqual(self.match.team_win_rate(d, 'Foo'), [default_win_rate])
        self.assertEqual(self.match.team_win_rate(d, 'Kolkata Knight Riders'), [1])
        self.assertEqual(self.match.team_win_rate(d, 'Royal Challengers Bangalore'), [0])
        self.assertEqual(self.match.team_win_rate(d, 'Kings XI Punjab'), [0])
        self.assertEqual(self.match.team_win_rate(d, 'Chennai Super Kings'), [1])

    def test_team_net_run_rate(self):
        matches = [self.match, self.match2]
        d = get_player_stats_dict(matches)
        x = default_net_run_rate
        self.assertEqual(self.match.team_net_run_rate(d, 'Foo'), [default_net_run_rate])
        self.assertEqual(self.match.team_net_run_rate(d, 'Kolkata Knight Riders'), [27/3 - 11/3])
        self.assertEqual(self.match.team_net_run_rate(d, 'Royal Challengers Bangalore'), [11/3 - 27/3])
        self.assertEqual(self.match.team_net_run_rate(d, 'Kings XI Punjab'), [0])
        self.assertEqual(self.match.team_net_run_rate(d, 'Chennai Super Kings'), [0])

    def test_get_team_features(self):
        matches = [self.match, self.match2]
        d = get_player_stats_dict(matches)
        output = self.match.get_team_features(Match.team_win_rate, matches)
        self.assertEqual(output, [1.0, 0.0, 1])
        output = self.match2.get_team_features(Match.team_win_rate, matches)
        self.assertEqual(output, [1.0, 0.0, 1])

if __name__ == '__main__':
    unittest.main()
