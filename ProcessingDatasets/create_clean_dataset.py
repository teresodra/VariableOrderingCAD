"""This file contains a function that given the raw dataset containing
the sets of polynomials and its timings for each order, creates a dataset
containing a set of unique features and its class"""

import json
import pickle
from typing import List, Union

from ProcessingDatasets.replicating_Dorians_features import extract_features
from ProcessingDatasets.dataset_manipulation import remove_notunique_features
from utils.find_filename import find_dataset_filename, find_other_filename
from sklearn.preprocessing import MinMaxScaler, StandardScaler


def normalise_features(names, features, normalization='standarised', nvar=3):

    # Check there is one name for every feature
    if len(names) != len(features[0]):
        raise ValueError("There should be a name for each feature")
    n = len(names)
    nfeatures = n//nvar
    ninstances = len(features)

    # Check that the names are the same for all the variables
    if n % nvar != 0:
        raise ValueError("The names should be the same for all variables")
    for i in range(nfeatures):
        values = set(names[j*nfeatures+i][:-14] for j in range(nvar))
        # After -14 information relevant to the variable should be different
        if len(values) != 1:
            raise ValueError("The names should be the same for all variables")

    # Separate by features
    by_features = [list(row) for row in zip(*features)]

    # Put the related features together
    related_features = []
    for i in range(nfeatures):
        related_features.append([feature for j in range(nvar)
                                 for feature in by_features[j*nfeatures+i]])

    # Transpose
    transposed_features = [list(row) for row in zip(*related_features)]

    if normalization == 'scaled':
        # Min-max scaling
        normaliser = MinMaxScaler()
    elif normalization == 'standarised':
        # Standardization
        normaliser = StandardScaler()

    normalised_feature = normaliser.fit_transform(transposed_features)

    # Transpose back
    normalised_related_features = [list(row) for row
                                   in zip(*normalised_feature)]

    # Break them into the ones for each variable
    normalised_by_features = []
    for j in range(nvar):
        for i in range(nfeatures):
            normalised_by_features.append(
                normalised_related_features[i][j*ninstances:(j+1)*ninstances])

    # Transpose back
    normalised_features = [list(row) for row
                           in zip(*normalised_by_features)]

    return normalised_features


def cleaning_dataset(normalization: str = 'scaled'):
    """
    Clean and process the dataset.

    This function performs several cleaning and processing steps
    on the dataset and saves the cleaned dataset to a new file.

    Args:
    - normalization: The normalization method.
        Allowed values: "scaled" or "standarised".

    Returns:
    - None
    """
    # Find unclean and clean dataset filenames
    dataset_filename = find_dataset_filename('unclean')
    clean_dataset_filename = find_dataset_filename('clean')

    # Load the unclean dataset
    with open(dataset_filename, 'rb') as f:
        dataset = pickle.load(f)

    # Extract features and keep only the unique ones
    my_dataset = extract_features(dataset)
    clean_dataset = dict()
    clean_dataset['names'], clean_dataset['features'] = \
        remove_notunique_features(my_dataset['names'], my_dataset['features'])
    print(len(clean_dataset['features']), len(clean_dataset['features'][0]))

    clean_dataset['features'] = normalise_features(clean_dataset['names'],
                                                   clean_dataset['features'],
                                                   normalization)
    print(len(clean_dataset['features']), len(clean_dataset['features'][0]))

    print("features in biased", len(my_dataset['features'][0]))

    # Save names of unique features to a file
    unique_features_filename = find_other_filename("unique_features")
    with open(unique_features_filename, 'w') as unique_features_file:
        json.dump(clean_dataset['names'], unique_features_file)

    # Clean timings and cells
    print(type(my_dataset['timings'][0][0]))
    clean_dataset['timings'] = \
        [[penalise_timing(timing_ordering)
         for timing_ordering in timings_problem]
         for timings_problem in my_dataset['timings']]
    clean_dataset['cells'] = \
        [penalise_cells(cells_problem)
         for cells_problem in my_dataset['cells']]

    # Copy other keys from the original dataset
    for key in my_dataset:
        if key not in clean_dataset:
            clean_dataset[key] = my_dataset[key]

    # Save the cleaned dataset
    with open(clean_dataset_filename, 'wb') as clean_dataset_file:
        pickle.dump(clean_dataset, clean_dataset_file)


def penalise_timing(timing_str: str, penalization: float = 2) -> float:
    """
    Convert a timing string to a numerical value with optional penalization.

    Args:
    - timing_str (str): The input timing string.
    - penalization (float, optional): A penalization factor. Default is 2.

    Returns:
    - float: The converted timing value with penalization if needed.
    """
    if not is_float(timing_str):
        return penalization * float(timing_str[5:])
    return float(timing_str)


def penalise_cells(cells: List[Union[int, str]],
                   penalization: int = 2) -> List[Union[int, float]]:
    """
    Convert a list of cells to integers with optional penalization.

    Args:
    - cells (List[Union[int, str]]): The input list of cells
    containing integers or strings.
    - penalization (int, optional): A penalization factor. Default is 2.

    Returns:
    - List[Union[int, float]]: The converted list of integers
    with penalization applied if needed.
    """
    int_cells = [int(cell) if is_int(cell) else cell for cell in cells]
    max_cells = max([cell for cell in int_cells
                     if isinstance(cell, int)], default=0)
    penalization_cells = [cell if isinstance(cell, int)
                          else penalization * max_cells for cell in int_cells]
    return penalization_cells


def is_float(input_str: str) -> bool:
    """
    Check if a string can be converted to a floating-point number.

    Args:
    - input_str (str): The input string.

    Returns:
    - bool: True if the string can be converted to a float, False otherwise.
    """
    try:
        float(input_str)
        return True
    except ValueError:
        return False
    # float_pattern = r'^[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?$'
    # return re.match(float_pattern, input_str) is not None


def is_int(input_str: str) -> bool:
    """
    Check if a string can be converted to an integer.

    Args:
    - input_str (str): The input string.

    Returns:
    - bool: True if the string can be converted to an int, False otherwise.
    """
    try:
        int(input_str)
        return True
    except ValueError:
        return False
    # if type(input_str) != str:
    #     return False
    # int_pattern = r'^[-+]?\d+$'
    # return re.match(int_pattern, input_str) is not None
