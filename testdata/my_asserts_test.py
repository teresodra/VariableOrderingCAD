import unittest
from testdata.my_asserts import dict_equal
from testdata.my_asserts import deep_list_equals


class TestDeepDictEquality(unittest.TestCase):

    def test_dicts_equal(self):
        dict1 = {
            'key1': [[1, 2], [3, 4]],
            'key2': {'subkey': 'value'},
        }
        dict2 = {
            'key1': [[1, 2], [3, 4]],
            'key2': {'subkey': 'value'},
        }
        self.assertTrue(dict_equal(dict1, dict2))

    def test_dicts_not_equal_1(self):
        dict1 = {
            'key1': [[1, 2], [3, 4]],
            'key2': {'subkey': 'value'},
        }
        dict2 = {
            'key1': [[1, 2], [3, 4]],
            'key2': {'subkey': 'different_value'},
        }
        self.assertFalse(dict_equal(dict1, dict2))

    def test_dicts_not_equal_2(self):
        dict1 = {
            'key1': [[1, 2], [3, 4]],
            'key2': {'subkey': 'value'},
        }
        dict2 = {
            'key1': [[1, 3], [3, 4]],
            'key2': {'subkey': 'value'},
        }
        self.assertFalse(dict_equal(dict1, dict2))


class TestDeepListEquals(unittest.TestCase):
    def test_equal_nested_lists(self):
        list1 = [1, [2, [3, 4]], 5]
        list2 = [1, [2, [3, 4]], 5]
        self.assertTrue(deep_list_equals(list1, list2))

    def test_different_nested_lists(self):
        list3 = [1, [2, [3, 4]], 5]
        list4 = [1, [2, [3, 4]], 6]
        self.assertFalse(deep_list_equals(list3, list4))

    def test_nested_lists_with_different_lengths(self):
        list5 = [1, [2, [3, 4]], 5]
        list6 = [1, [2, [3, 4, 5]], 5]
        self.assertFalse(deep_list_equals(list5, list6))

    def test_empty_nested_lists(self):
        list7 = []
        list8 = []
        self.assertTrue(deep_list_equals(list7, list8))

    def test_nested_lists_with_different_order(self):
        list9 = [1, [2, [3, 4]], 5]
        list10 = [1, [2, [4, 3]], 5]
        self.assertFalse(deep_list_equals(list9, list10))
