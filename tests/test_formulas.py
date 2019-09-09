import unittest
from ProtonTransfer import (
    weight_function,
    projected_donor_acceptor_ratio,
    normalization_factor,
)
import numpy as np


class TestWeightFunction(unittest.TestCase):
    def test_x_geq_one(self):
        self.assertEqual(0, weight_function(10))
        self.assertEqual(0, weight_function(1))

    def test_x_less_than_zero(self):
        self.assertEqual(1, weight_function(-0.0000001))
        self.assertEqual(1, weight_function(-10))

    def test_x_eq_zero(self):
        self.assertEqual(1, weight_function(0))

    def test_x_geq_zero_and_x_less_than_one(self):
        self.assertEqual(0.500000000, weight_function(0.50))
        self.assertEqual(0.103515625, weight_function(0.75))
        self.assertEqual(0.896484375, weight_function(0.25))

    def test_x_one_third(self):
        result = weight_function(1 / 3)
        expected = 0.7901234568
        self.assertAlmostEqual(expected, result)

    def test_x_random_floats(self):
        x1, x2, x3 = 0.4666923675, 0.7422350280, 0.7462493491
        r1, r2, r3 = weight_function(x1), weight_function(x2), weight_function(x3)
        e1, e2, e3 = 0.562267, 0.111874, 0.107511
        self.assertAlmostEqual(e1, r1, places=6)
        self.assertAlmostEqual(e2, r2, places=6)
        self.assertAlmostEqual(e3, r3, places=6)


class TestProjectedDonorAcceptorRatio(unittest.TestCase):
    def test_pmj_one(self):
        donor_coords = np.asarray([1, 1, 1])
        hydrogen_coords = np.asarray([2, 2, 2])
        acceptor_coords = np.asarray([3, 3, 3])
        result = projected_donor_acceptor_ratio(
            acceptor_coords, hydrogen_coords, donor_coords
        )
        expected = 0.50
        self.assertAlmostEqual(expected, result)

    def test_pmj_two(self):
        donor_coords = np.asarray([3, -1, -7])
        hydrogen_coords = np.asarray([10, 2, -3])
        acceptor_coords = np.asarray([5, -2, -9])
        result = projected_donor_acceptor_ratio(
            acceptor_coords, hydrogen_coords, donor_coords
        )
        expected = 1 / 3
        self.assertAlmostEqual(expected, result)


class TestNormalizationFactor(unittest.TestCase):
    def test_norm_factor_one(self):
        donor_coords = np.asarray([3, -1, -7])
        hydrogen_coords = (
            np.asarray([1000, 1000, 1000]),
            np.asarray([2, 2, 2]),
            np.asarray([2, -4, 7]),
        )
        acceptor_coords = (
            np.asarray([5, -2, -9]),
            np.asarray([3, 3, 3]),
            np.asarray([1, 1, 1]),
        )
        result = normalization_factor(acceptor_coords, hydrogen_coords, donor_coords)
        expected = 4.014550763343388
        self.assertAlmostEqual(expected, result)

    def test_norm_factor_two(self):
        donor_coords = np.asarray([3, -1, -7])
        hydrogen_coords = (
            np.asarray([10, 2, -3]),
            np.asarray([2, 2, 2]),
            np.asarray([2, -4, 7]),
        )
        acceptor_coords = (
            np.asarray([5, -2, -9]),
            np.asarray([3, 3, 3]),
            np.asarray([1, 1, 1]),
        )
        result = normalization_factor(acceptor_coords, hydrogen_coords, donor_coords)
        expected = 5.191090746609785
        self.assertAlmostEqual(expected, result)


if __name__ == "__main__":
    unittest.main()
