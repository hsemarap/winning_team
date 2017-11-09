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

    def test_batsman_strike_rate(self):
        self.assertAlmostEqual(batsman_strike_rate(self.match, 'R Dravid'), 100 * 2/3)
        self.assertAlmostEqual(batsman_strike_rate(self.match, 'BB McCullum'), 100 * 23/14)
        self.assertAlmostEqual(batsman_strike_rate(self.match, 'Foo'), default_strike_rate)

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

    def test_first_batting_side_won(self):
        self.assertEqual(self.match.first_batting_side_won(), True)

    def test_match_features(self):
        output = self.match.features([self.match])
        x = default_strike_rate
        expected = [0.0, 164.28571428571428, x, x,
                    x, x, x, x, x, x, x,
                    66.66666666666667, 10.0, 20.0, 100.0,
                    x, x, x, x, x, x, x,
                    1]
        print(output, expected)
        for o, e in zip(output, expected):
            self.assertAlmostEqual(o, e)

    def test_get_player_stats_dict(self):
        matches = [self.match, self.match2]
        d = get_player_stats_dict(matches)
        self.assertEqual(d['BB McCullum']['total runs'], 23)
        self.assertEqual(d['BB McCullum']['total balls'], 14)
        self.assertEqual(d['JR Hopes']['total runs'], 14)
        self.assertEqual(d['JR Hopes']['total balls'], 8)
        self.assertEqual(d['BB McCullum']['matches played'], 1)

    def test_batsman_num_matches(self):
        matches = [self.match, self.match2]
        d = get_player_stats_dict(matches)
        self.assertEqual(batsman_num_matches(d, 'BB McCullum'), 1)
        self.assertEqual(batsman_num_matches(d, 'Foo'), 0)

    def test_batsman_average(self):
        matches = [self.match, self.match2]
        d = get_player_stats_dict(matches)
        self.assertEqual(batsman_average(d, 'BB McCullum'), 23)
        self.assertEqual(batsman_average(d, 'Foo'), default_average)

if __name__ == '__main__':
    unittest.main()
