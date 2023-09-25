import os
# import pickle
import unittest
import tempfile

from ProcessingDatasets.create_clean_dataset import (normalise_features,
                                                     cleaning_dataset,
                                                     penalise_timing,
                                                     penalise_cells,
                                                     is_float,
                                                     is_int)
from utils.find_filename import find_dataset_filename, find_other_filename
# from testdata.my_asserts import dict_equal


class TestNormalisingFeatures(unittest.TestCase):

    def test_normalise_features(self):
        # Create simple example
        features = [[1, 3, 6, 7, 9, 11],
                    [2, 4, 5, 8, 10, 12]]
        names = ['a_0_in_monomials',
                 'b_0_in_monomials',
                 'a_1_in_monomials',
                 'b_1_in_monomials',
                 'a_2_in_monomials',
                 'b_2_in_monomials']
        result = normalise_features(names, features)

        # Create the expected output
        expected = [[-1.3619698352243594,
                     -1.3619698352243594,
                     0.15132998169159548,
                     -0.15132998169159548,
                     1.0593098718411684,
                     1.0593098718411684],
                    [-1.0593098718411684,
                     -1.0593098718411684,
                     -0.15132998169159548,
                     0.15132998169159548,
                     1.3619698352243594,
                     1.3619698352243594]]
        self.assertEqual(result, expected)


class TestCleaningDataset(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for testing
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        # Clean up the temporary directory
        os.rmdir(self.temp_dir)

    def test_files_created(self):
        # Run your cleaning_dataset function
        cleaning_dataset()

        # Check if the file 'unique_features_filename' exists
        # in the temp directory
        unique_features_filename = find_other_filename("unique_features")
        self.assertTrue(os.path.exists(unique_features_filename))

        # Check if the file 'clean_dataset_filename' exists
        # in the temp directory
        clean_dataset_filename = find_dataset_filename('clean')
        self.assertTrue(os.path.exists(clean_dataset_filename))

    ###
    # Test commented out because it modifies the environment,
    # maybe I can retrieve the original file and upload it after
    # finishing, but the original file is too big for GitHub
    ###
    # def test_correct_run(self):
    #     # Test correct execution

    #     # Get the mock unclean and clean dataset
    #     mock_unclean_filename = os.path.join(os.path.dirname(__file__),
    #                                          '..', 'testdata',
    #                                          "mock_unclean_dataset.txt")
    #     with open(mock_unclean_filename, 'rb') as mock_unclean_file:
    #         mock_unclean_dataset = pickle.load(mock_unclean_file)
    #     mock_clean_filename = os.path.join(os.path.dirname(__file__),
    #                                        '..', 'testdata',
    #                                        "mock_clean_dataset.txt")
    #     with open(mock_clean_filename, 'rb') as mock_clean_file:
    #         mock_clean_dataset = pickle.load(mock_clean_file)

    #     # Upload the mock unclean dataset
    #     # to the temp directory
    #     print(self.temp_dir)
    #     unclean_dataset_filename = find_dataset_filename('unclean')
    #     with open(unclean_dataset_filename, 'wb') as unclean_file:
    #         pickle.dump(mock_unclean_dataset, unclean_file)

    #     # Run your cleaning_dataset function
    #     cleaning_dataset()

    #     # Retrieve the createed clean dataset
    #     clean_dataset_filename = find_dataset_filename('clean')
    #     with open(clean_dataset_filename, 'rb') as clean_dataset_file:
    #         clean_dataset = pickle.load(clean_dataset_file)
    #     self.assertTrue(dict_equal(mock_clean_dataset, clean_dataset))


class TestCleaningDatasetFunctions(unittest.TestCase):

    def test_penalise_timing(self):
        
        self.assertAlmostEqual(penalise_timing("Over 30"), 60.0)
        self.assertAlmostEqual(penalise_timing("15"), 15.0)
        self.assertAlmostEqual(penalise_timing("-5"), -5.0)
        self.assertAlmostEqual(penalise_timing("7.5"), 7.5)

    def test_penalise_cells_1(self):

        cells = [1, 2, "Over 30", "10", -5, "20"]
        penalised_cells = penalise_cells(cells)
        self.assertEqual(penalised_cells, [1, 2, 40, 10, -5, 20])

    def test_penalise_cells_2(self):

        cells = [1, 25, "Over 30", "10", -5, "20"]
        penalised_cells = penalise_cells(cells)
        self.assertEqual(penalised_cells, [1, 25, 50, 10, -5, 20])

    def test_is_float(self):

        self.assertTrue(is_float("3.14"))
        self.assertTrue(is_float("0.0"))
        self.assertTrue(is_float("-2.5"))
        self.assertFalse(is_float("abc"))
        self.assertFalse(is_float("12a.5"))

    def test_is_int(self):

        self.assertTrue(is_int("42"))
        self.assertTrue(is_int("0"))
        self.assertTrue(is_int("-10"))
        self.assertFalse(is_int("3.14"))
        self.assertFalse(is_int("abc"))


if __name__ == '__main__':
    unittest.main()
