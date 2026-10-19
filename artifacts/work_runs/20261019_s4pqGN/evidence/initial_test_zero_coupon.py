"""Tests use the "quoted annual effective yield decimal" convention."""

import math
import unittest

from zero_coupon import price_annual


class PriceAnnualTests(unittest.TestCase):
    def test_reference_price(self):
        self.assertAlmostEqual(price_annual(100, 0.05, 2), 90.7029478458,
                               places=10)

    def test_zero_cases(self):
        self.assertEqual(price_annual(0, 0.05, 2), 0)
        self.assertEqual(price_annual(100, 0, 2), 100)
        self.assertEqual(price_annual(100, 0.05, 0), 100)
        self.assertEqual(price_annual(0, 0, 0), 0)

    def test_negative_valid_yield(self):
        self.assertAlmostEqual(price_annual(100, -0.5, 2), 400)

    def test_fractional_years(self):
        self.assertAlmostEqual(price_annual(100, 0.21, 0.5), 100 / 1.1)

    def test_invalid_domains(self):
        for args in ((-1, 0.05, 2), (100, 0.05, -1),
                     (100, -1, 2), (100, -1.1, 2),
                     (0, -1, 0)):
            with self.subTest(args=args), self.assertRaises(ValueError):
                price_annual(*args)

    def test_nonfinite_inputs(self):
        for index in range(3):
            for value in (math.nan, math.inf, -math.inf):
                args = [100, 0.05, 2]
                args[index] = value
                with self.subTest(index=index, value=value):
                    with self.assertRaises(ValueError):
                        price_annual(*args)


if __name__ == "__main__":
    unittest.main()
