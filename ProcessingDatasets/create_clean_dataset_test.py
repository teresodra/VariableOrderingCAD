import os
import unittest
import tempfile

from .create_clean_dataset import (cleaning_dataset, penalize_timing,
                                   penalize_cells, is_float, is_int)
from utils.find_filename import find_dataset_filename


class TestCleaningDataset(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for testing
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        # Clean up the temporary directory
        os.rmdir(self.temp_dir)

    def test_cleaning_dataset_file_created(self):
        # Run your cleaning_dataset function
        cleaning_dataset()

        # Check if the file 'clean_dataset_filename' exists
        # in the temp directory
        clean_dataset_file_path = find_dataset_filename('clean')
        self.assertTrue(os.path.exists(clean_dataset_file_path))


class TestCleaningDatasetFunctions(unittest.TestCase):
    def test_penalize_timing(self):
        self.assertAlmostEqual(penalize_timing("Over 30"), 60.0)
        self.assertAlmostEqual(penalize_timing("15"), 15.0)
        self.assertAlmostEqual(penalize_timing("-5"), -5.0)
        self.assertAlmostEqual(penalize_timing("7.5"), 7.5)

    def test_penalize_cells(self):
        cells = [1, 2, "Over 30", "10", -5, "20"]
        penalized_cells = penalize_cells(cells)
        self.assertEqual(penalized_cells, [1, 2, 40, 10, -5, 20])

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
