import sympy as sp
from typing import List, Union


def list_to_polynomial_set(polynomials: List[List[List[Union[float, int]]]]
                           ) -> List[sp.Expr]:
    """
    Create a set of polynomials from a list of lists of monomials,
    where each monomial is represented as [degrees, coefficient].

    Args:
    - polynomials (list of lists of lists): List of lists of monomials,
    where each monomial is represented as [degrees, coefficient].

    Returns:
    - list of sympy expression: List of the polynomials expressions.
    """

    # Check that all monomial have the same size
    monomial_lengths = set(len(monomial) for monomials in polynomials
                           for monomial in monomials)
    if len(monomial_lengths) != 1:
        raise ValueError("All monomials must have the same size.")

    return [list_to_polynomial(monomials) for monomials in polynomials]


def list_to_polynomial(monomials: List[List[Union[float, int]]]
                       ) -> sp.Expr:
    """
    Create a polynomial from a list of monomials,
    where each monomial is represented as [degrees, coefficient].

    Args:
    - monomials (list of lists): List of monomials,
    where each monomial is represented as [degrees, coefficient].

    Returns:
    - sympy expression: The polynomial expression.
    """

    # Check that all degrees are integers
    for *degrees, _ in monomials:
        if not all(isinstance(deg, int) for deg in degrees):
            raise ValueError("Degrees must be integers.")

    # Check that all monomial have the same size
    monomial_lengths = set(len(monomial) for monomial in monomials)
    if len(monomial_lengths) != 1:
        raise ValueError("All monomials must have the same size.")

    # Make sure the list of monomials is not empty
    if monomials == []:
        return 0

    # Compute the number of variables
    num_variables = len(monomials[0]) - 1

    # Create symbolic variables in a loop and store them in a list
    variables = [sp.symbols(f'x{i}') for i in range(num_variables)]

    polynomial = sum(coefficient * sp.prod(var**degree
                     for var, degree in zip(variables, degrees))
                     for *degrees, coefficient in monomials)

    return polynomial


# Example usage:
if __name__ == "__main__":

    # List of monomials, each represented as [degrees, coefficient]
    monomials = [[1, 2, 0, 1.5], [1, 2, 3, 4]]

    # Create the polynomial
    polynomial = list_to_polynomial(monomials)

    # Print the polynomial
    print("Polynomial:", polynomial)
