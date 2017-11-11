import unittest
from extract_features import *

class TestExtractFeatures(unittest.TestCase):
    def setUp(self):
        pass

    def test_rolling_stats(self):
        xs = list(range(1, 5))
        ans = rolling_stats(xs, lambda y, ys: y - sum(ys))
        self.assertEqual(ans, [1, 1, 0, -2])

    def test_concat(self):
        self.assertEqual(concat([[1, 2], [3, 4]]), [1, 2, 3, 4])

    def test_rolling_stats_respect_structure(self):
        self.assertEqual(rolling_stats_respect_structure(
            [[5, 6, 7], [8]],
            lambda x, xs: x + sum(xs),
            [[1, 2], [3, 4]]),
            [[15, 21, 28], [36]])

if __name__ == '__main__':
    unittest.main()
