import unittest
from extract_features import *

class TestExtractFeatures(unittest.TestCase):
    def setUp(self):
        pass

    def test_rolling_stats(self):
        xs = list(range(1, 5))
        ans = rolling_stats(xs, lambda y, ys: y - sum(ys))
        self.assertEqual(ans, [1, 1, 0, -2])

if __name__ == '__main__':
    unittest.main()
