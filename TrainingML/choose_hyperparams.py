
import pickle

from config.ml_models import all_models
from config.hyperparameters_grid import grid
from sklearn.model_selection import GridSearchCV
from utils.yaml_tools import write_yaml_to_file
from utils.find_filename import find_dataset_filename
from utils.find_filename import find_hyperparams_filename


def k_folds_ml(x_train, y_train, model, random_state=0):
    """
    Train the desired model.

    The hyperparameters of the models are chosen using 5-fold cross validation.
    """
    current_classifier = all_models[model]
    current_grid = grid[model]
    rf_cv = GridSearchCV(estimator=current_classifier(),
                         param_grid=current_grid,
                         cv=5,
                         verbose=10  # to get updates
                         )
    rf_cv.fit(x_train, y_train)
    return rf_cv.best_params_


def choose_hyperparams(model_name, paradigm, training_quality):
    """Given a ml_model and a method, a file with the hyperparameters
    chosen by cross validation is created"""
    this_dataset_file = find_dataset_filename('Train', dataset_quality=training_quality)
    with open(this_dataset_file, 'rb') as f:
        dataset = pickle.load(f)
    hyperparams = k_folds_ml(dataset['features'], dataset['labels'], model=model_name)
    print(hyperparams)
    hyperparams_filename = find_hyperparams_filename(model_name, paradigm, training_quality)
    print('new hyperparams_filename', hyperparams_filename)
    write_yaml_to_file(hyperparams, hyperparams_filename)