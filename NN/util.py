import os
import json
import pickle
import numpy as np

def convert_generator_to_lists(generator, ids=False):
    """
        Convert a datagenerator into two lists.
        One containing the observation, the other containing the true labels.
        Add corresponding list of uid to output.

    Parameters
    ----------
    generator : datagenerator
        First dimension of each element in generator has to contain batches
    ids : bool
        Set to True if id list desired

    Returns
    -------
    tuple of numpy arrays, optional list of strings as third elemt of tuple
    """
    obs_list = list()
    label_list = list()
    ids_list = list()

    for batch in generator:
        batch_len = batch[0].shape[0]
        for obs_num in range(batch_len):
            obs = batch[0][obs_num]
            obs_label = batch[1][obs_num]
            obs_list.append(obs)
            label_list.append(obs_label)
            ids_list.append(generator.list_IDs_temp[obs_num])

    x = np.array(obs_list)
    y = np.array(label_list)
    if ids == True:
        return x, y, ids_list
    return x, y


def get_best_ckpt(log_dir):
    """ moved to SWAI.NN.store_model.py
    """
    assert False, 'Function was moved to SWAI.NN.store_model'


def get_parameters(log_dir):
    """
    Get dict of stored parameters used to train a model

    Parameters
    ----------
    log_dir : str or Path : path to directory where log files are stored

    Returns
    -------
    parameters : dict : dict of all stored parameters from training set up
    """
    parameter_path = os.path.join(log_dir, 'params.json')
    with open(parameter_path, 'r') as file:
        parameters = json.load(file)
    return parameters


def get_parameters_pickle(log_dir):
    """
    Get dict of stored parameters used to train a model

    Parameters
    ----------
    log_dir : str or Path : path to directory where log files are stored

    Returns
    -------
    parameters : dict : dict of all stored parameters from training set up
    """
    parameter_path = os.path.join(log_dir, 'params.pickle')
    with open(parameter_path, 'rb') as file:
        parameters = pickle.load(file)
    return parameters
