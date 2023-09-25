import sympy as sp
import unittest

from utils.list_to_polynomial import list_to_polynomial_set, list_to_polynomial


class TestPolynomialConversion(unittest.TestCase):

    def test_list_to_polynomial_set(self):
        # Test a simple case
        polynomials = [[[1, 2, 0, 1], [1, 2, 3, 4]],
                       [[2, 1, 0, 1], [0, 3, 1, 2.5]]]
        result = list_to_polynomial_set(polynomials)

        # Produce expected result
        x0, x1, x2 = sp.symbols('x0 x1 x2')
        expected = [4*x0*x1**2*x2**3 + x0*x1**2, x0**2*x1 + 2.5*x1**3*x2]

        # Compare
        self.assertEqual(result, expected)

        # Test case where monomials have different sizes
        polynomials = [[[1, 2, 0, 1], [1, 2, 3, 4]],
                       [[2, 1, 4], [0, 3, 2.5]]]
        with self.assertRaises(ValueError):
            list_to_polynomial_set(polynomials)

    def test_list_to_polynomial(self):
        # Simple case
        monomials = [[1, 2, 0, 1], [1, 2, 3, 4]]
        result = list_to_polynomial(monomials)

        # Produce expected result
        x0, x1, x2 = sp.symbols('x0 x1 x2')
        expected = 4*x0*x1**2*x2**3 + x0*x1**2

        # Compare
        self.assertEqual(result, expected)

        # Test case where degrees contain non-integer values
        monomials = [[1, 2, 0.5, 1.5], [1, 2, 3, 4]]
        with self.assertRaises(ValueError):
            list_to_polynomial(monomials)

        # Test case where monomials have different sizes
        monomials = [[1, 2, 1], [1, 2, 3, 4, 5]]
        with self.assertRaises(ValueError):
            list_to_polynomial(monomials)
