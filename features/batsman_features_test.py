import unittest
from batsman_features import *
from extract_features import parse_yaml

class TestBatsmenFeatures(unittest.TestCase):
    """
    Our basic test class
    """
    def setUp(self):
        yaml_file = "./raw-data/test-data/3-overs-335982.yaml"
        self.yaml_data = parse_yaml(yaml_file)

    def test_runs_off_ball(self):
        self.assertEqual(120, 120)

    def test_get_ball(self):
        self.assertEqual(get_ball(self.yaml_data),
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

if __name__ == '__main__':
    unittest.main()
