'''Compares whether two dictionaries containing
nested lists/dictionaries are equal'''

import numpy as np


def dict_equal(dict1, dict2):

    # Check if the keys in both dictionaries match
    if set(dict1.keys()) != set(dict2.keys()):
        return False

    # Recursively compare the values
    for key in dict1.keys():
        value1 = dict1[key]
        value2 = dict2[key]

        # If the values are dictionaries, recursively compare them
        if isinstance(value1, dict) and isinstance(value2, dict):
            if not dict_equal(value1, value2):
                return False

        # If both elements are lists, recursively compare them
        if isinstance(value1, list) and isinstance(value2, list):
            if not deep_list_equals(value1, value2):
                return False

        # If both elements are nparrays, compare them
        if isinstance(value1, np.ndarray) and isinstance(value2, np.ndarray):
            return np.array_equal(value1, value2)

        # For other types, use the default comparison
        else:
            if value1 != value2:
                return False
    return True


def deep_list_equals(list1, list2):
    """
    Test whether two nested lists are equal.

    Args:
    - list1 (list): The first nested list.
    - list2 (list): The second nested list.

    Returns:
    - bool: True if the nested lists are equal, False otherwise.
    """
    # Check if the lengths of the lists are the same
    if len(list1) != len(list2):
        return False

    # Iterate through the elements of the lists
    for elem1, elem2 in zip(list1, list2):

        # If both elements are lists, recursively compare them
        if isinstance(elem1, list) and isinstance(elem2, list):
            if not deep_list_equals(elem1, elem2):
                return False

        # If both elements are nparrays, compare them
        if isinstance(elem1, np.ndarray) and isinstance(elem2, np.ndarray):
            return np.array_equal(elem1, elem2)

        # For other types, use the default comparison
        else:
            if elem1 != elem2:
                return False

    return True
