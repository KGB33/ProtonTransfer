import unittest
from Formulas import *


class TestDistance(unittest.TestCase):

    def test_one_dimensional_input(self):
        self.assertEqual(5, distance([0], [5]))

    def test_really_big_dimensional_input(self):
        self.assertEqual(500, distance([0 for _ in range(0, 10000)], [5 for _ in range(0, 10000)]))

    def test_different_dimensions_least_square(self):
        self.assertEqual(5, distance([3, 4, 5], [0, 0], zero_fill=False))
        self.assertEqual(5, distance([0, 0], [3, 4, 5], zero_fill=False))

    def test_different_dimensions_zero_fill(self):
        self.assertEqual(7, distance([2, 3, 6], [0, 0], zero_fill=True))
        self.assertEqual(7, distance([0, 0], [2, 3, 6], zero_fill=True))

    def test_negative_coords(self):
        self.assertEqual(500, distance([0 for _ in range(0, 10000)], [-5 for _ in range(0, 10000)]))


if __name__ == '__main__':
    unittest.main()
