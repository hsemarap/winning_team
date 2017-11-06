import unittest
from batsman_features import *
from extract_features import parse_yaml

class TestBatsmenFeatures(unittest.TestCase):
    """
    Our basic test class
    """
    @classmethod
    def setUpClass(cls):
        yaml_file = "./raw-data/test-data/3-overs-335982.yaml"
        cls.yaml_data = parse_yaml(yaml_file)
        cls.match = Match(cls.yaml_data)
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
        self.assertAlmostEqual(batsman_strike_rate(self.match, 'Foo'), 0)

    def test_overall_strike_rate(self):
        self.assertAlmostEqual(batsman_overall_strike_rate(
                [self.match], 'R Dravid'), 100 * 2/3)
        self.assertAlmostEqual(batsman_overall_strike_rate(
                [self.match], 'BB McCullum'), 100 * 23/14)
        self.assertAlmostEqual(batsman_overall_strike_rate(
                [self.match], 'Foo'), 0)

    def test_unique_everseen(self):
        self.assertEqual(list(unique_everseen("aabbcedeeeb")),
                         ['a', 'b', 'c', 'e', 'd'])

if __name__ == '__main__':
    unittest.main()
