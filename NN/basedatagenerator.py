import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict, Counter
from tqdm.auto import tqdm

import tensorflow.keras as keras
from scipy.fft import fft, rfft

from SWAI.IO.read_write_hdf5 import read_h5file_to_dict2
from SWAI.GLOBAL_KEYS.db_keys import *
from SWAI.IO.read_create_files import read_json_to_Dict
#from SWAI.DB.database import get_data_from_json
from SWAI.DSP.statistics import linearization, normalization

#from HUMMEL.ppm_kardanwelle.exploration.visualization_functions import *
keras.backend.clear_session()


class datagenerator(keras.utils.Sequence):
    """Generates data for Keras"""

    def __init__(self, list_IDs, database, batch_size=1, class_dict=None, data_aug=False,
                 shuffle=True, predload_ds_to_ram=False, path_h5_dataset=None, **kwargs):
        """
        .. todo:: More overview about needed and optional arguments. eg. dim
        Parameters
        ----------
        list_IDs
        database
        batch_size
        class_dict
        data_aug
        shuffle
        predload_ds_to_ram : bool
            If this parameter is true, all the data is first load to ram so it doesn't
             have to be loaded again and again during training

        dir_path_h5_dataset : str
            This is the path to the dir were the dataset is saved as h5 file
        kwargs
        """
        'parameter setup'
        self.data_aug = data_aug
        self.batch_size = batch_size
        self.list_IDs = list_IDs
        self.shuffle = shuffle
        self.dbjson = database.db #read_json_to_Dict(database)
        self.class_dict = class_dict
        self.list_IDs_temp = None  # Stores the current ID

        if 'model' in kwargs.keys():
            self.dim = kwargs['model']['inputshape']
            self.mode = kwargs['model']['mode']
            self.loss = kwargs["model"]["loss"]
            self.n_classes = kwargs['model']['n_classes']

            assert (len(self.class_dict.keys()) >= self.n_classes), "Not enough classes defined in class_dict!"
        if 'process_name' in kwargs:
            self.process_name = kwargs['process_name']

        #### preload ds
        self.d_preload_data = None
        self.predload_ds_to_ram = predload_ds_to_ram
        if self.predload_ds_to_ram:
            self._preload_data()

        ### load_ds
        self.path_h5_dataset = path_h5_dataset
        if path_h5_dataset is not None:
            print("load the saved h5 dataset file...")
            self.d_preload_data = read_h5file_to_dict2(self.path_h5_dataset)

        self.on_epoch_end()

    def __len__(self):
        'Denotes the number of batches per epoch'
        return int(np.floor(len(self.list_IDs) / self.batch_size))

    def __getitem__(self, index):
        'Generate one batch of data'
        # Generate indexes of the batch
        indexes = self.indexes[index * self.batch_size:(index + 1) * self.batch_size]

        # Find list of IDs
        self.list_IDs_temp = [self.list_IDs[k] for k in indexes]

        # Generate data
        X, y = self.__data_generation(self.list_IDs_temp)

        return X, y

    def on_epoch_end(self):
        'Updates indexes after each epoch'
        self.indexes = np.arange(len(self.list_IDs))
        if self.shuffle == True:
            np.random.shuffle(self.indexes)

    def _preload_data(self):
        """
        preloads the data into the RAM
        Returns
        -------

        """
        self.d_preload_data={}
        print("preload data to ram")
        for i, ID in enumerate(tqdm(self.list_IDs)):
            ID_info = ID.split('_')
            # label without underscore
            label = ID_info[0]
            nuID = '_'.join(ID_info[1:])  # nuID = not unique ID as label is missing
            obs_paths = []
            try:
                if "Observation" in self.dbjson[label][nuID].keys():
                    obs_paths += [self.dbjson[label][nuID]["Observation"]]
                else:
                    for dict in self.dbjson[label][nuID].values():
                        obs_paths += [dict["Observation"]]
            except:
                # the label name is maybe with underscore so use also the second value
                try:
                    label = '{}_{}'.format(ID_info[0],ID_info[1])
                    nuID = '_'.join(ID_info[2:])  # nuID = not unique ID as label is missing
                    if "Observation" in self.dbjson[label][nuID].keys():
                        obs_paths += [self.dbjson[label][nuID]["Observation"]]
                    else:
                        for dict in self.dbjson[label][nuID].values():
                            obs_paths += [dict["Observation"]]
                except:
                    print(ID)
                    raise KeyError("{}, {}".format(label, nuID))

            # load obs_path
            for obs_path in obs_paths:
                self.d_preload_data[obs_path] = self.load_obs(obs_path) # TODO: make sensor selection possible
    

    def __data_generation(self, list_IDs_temp):
        'Generates data containing batch_size samples'  # X : (n_samples, *dim, n_channels)
        # Initialization
        X = np.empty((self.batch_size, * self.dim))#, dtype=np.int16)
        y = np.empty((self.batch_size), dtype=int)

        # Load Data from json

        # Generate data
        for i, ID in enumerate(list_IDs_temp):
            # Store sample
            ID_info = ID.split('_')

            # label without underscore
            label = ID_info[0]

            nuID = '_'.join(ID_info[1:])  # nuID = not unique ID as label is missing
            obs_paths = []
            try:
                if "Observation" in self.dbjson[label][nuID].keys():
                    obs_paths += [self.dbjson[label][nuID]["Observation"]]
                else:
                    for dict in self.dbjson[label][nuID].values():
                        obs_paths += [dict["Observation"]]
            except:
                # the label name is maybe with underscore so use also the second value
                try:
                    label = '{}_{}'.format(ID_info[0],ID_info[1])
                    nuID = '_'.join(ID_info[2:])  # nuID = not unique ID as label is missing
                    if "Observation" in self.dbjson[label][nuID].keys():
                        obs_paths += [self.dbjson[label][nuID]["Observation"]]
                    else:
                        for dict in self.dbjson[label][nuID].values():
                            obs_paths += [dict["Observation"]]
                except:
                    print(ID)
                    raise KeyError("{}, {}".format(label, nuID))

            # load obs_path
            data = []
            if self.d_preload_data is not None:
                for obs_path in obs_paths:
                    data += [self.d_preload_data[obs_path]]
            else: # load from memory
                for obs_path in obs_paths:
                    data += [self.load_obs(obs_path)]


            # augmentation and preprocessing
            obs = self.process(data)


            try:
                obs_re = obs.reshape(self.dim)
                X[i, ] = obs_re
            except:
                print("Shape of the oberservation after preprocessing:", obs.shape)
                raise ValueError("Error for file {}, {}, {} \n shape of model required {}".format(ID, label, nuID, self.dim))
            y[i] = self.class_dict[label]

        if self.loss["name"] == "categorical_crossentropy":
            y = keras.utils.to_categorical(y, num_classes=self.n_classes)
        return X, y

    def load_obs(self, obs_path, flag_init):
        """
        ..todo:: Insert Code to load obs_path here

        Returns
        -------
        data :
        flag_init: bool
            if flag is True

        """
        assert True, ' Overwrite this function'
        return 0

    def process(self, data):
        """
         ..todo:: Do some Augmentation and Preprocessing here. Final data should be stored to 'obs'

        Returns
        -------
        obs :

        """
        assert True, ' Overwrite this function'
        return 0
    
    def load_all_data_to_dict(self):
        """
        this functions is for laoding all the data to an dict so one can create a ds before
        """
        d_data = {}
        print("preload data to ram")
        for i, ID in enumerate(tqdm(self.list_IDs)):
            ID_info = ID.split('_')
            # label without underscore
            label = ID_info[0]
            nuID = '_'.join(ID_info[1:])  # nuID = not unique ID as label is missing
            try:
                obs_path = self.dbjson[label][nuID]["Observation"]
            except:
                # the label name is maybe with underscore so use also the second value
                try:
                    label = '{}_{}'.format(ID_info[0], ID_info[1])
                    nuID = '_'.join(ID_info[2:])  # nuID = not unique ID as label is missing
                    obs_path = self.dbjson[label][nuID]["Observation"]
                except:
                    print(ID)
                    raise KeyError("{}, {}".format(label, nuID))
            # load obs_path
            d_data[obs_path] ={}
            d_data[obs_path]['data'] = self.load_obs(obs_path)
        return d_data
    


class datagenerator_AE(keras.utils.Sequence):
    """Generates data for Keras"""

    def __init__(self, list_IDs, database, batch_size=1, data_aug=False,
                 shuffle=True, **kwargs):
        'parameter setup'
        self.dim = kwargs['model']['inputshape']
        self.mode = kwargs['model']['mode']  # .. deprecated:: use process_name?
        self.loss = kwargs["model"]["loss"]
        self.process_name = kwargs['process_name']

        self.data_aug = data_aug
        self.batch_size = batch_size
        self.list_IDs = list_IDs
        self.shuffle = shuffle
        self.dbjson = database.db  # read_json_to_Dict(database)

        self.on_epoch_end()

    def __len__(self):
        'Denotes the number of batches per epoch'
        return int(np.floor(len(self.list_IDs) / self.batch_size))

    def __getitem__(self, index):
        'Generate one batch of data'
        # Generate indexes of the batch
        indexes = self.indexes[index * self.batch_size:(index + 1) * self.batch_size]

        # Find list of IDs
        list_IDs_temp = [self.list_IDs[k] for k in indexes]

        # Generate data
        X = self.__data_generation(list_IDs_temp)

        return X, X

    def on_epoch_end(self):
        'Updates indexes after each epoch'
        self.indexes = np.arange(len(self.list_IDs))
        if self.shuffle == True:
            np.random.shuffle(self.indexes)

    def __data_generation(self, list_IDs_temp):
        'Generates data containing batch_size samples'  # X : (n_samples, *dim)
        # Initialization
        X = np.empty((self.batch_size, * self.dim))

        # Load Data from json

        # Generate data
        for i, ID in enumerate(list_IDs_temp):
            # Store sample
            ID_info = ID.split('_')

            # label without underscore
            label = ID_info[0]
            nuID = '_'.join(ID_info[1:])  # nuID = not unique ID as label is missing
            try:
                obs_path = self.dbjson[label][nuID]["Observation"]
            except:
                # the label name is maybe with underscore so use also the second value
                try:
                    label = '{}_{}'.format(ID_info[0], ID_info[1])
                    nuID = '_'.join(ID_info[2:])  # nuID = not unique ID as label is missing
                    obs_path = self.dbjson[label][nuID]["Observation"]
                except:
                    print(ID)
                    raise KeyError("{}, {}".format(label, nuID))

            # load obs_path
            data = self.load_obs(obs_path)

            # augmentation and preprocessing
            obs = self.process(data)

            try:
                obs_re = obs.reshape(self.dim)
                X[i, ] = obs_re
            except:
                print("Shape of the oberservation after preprocessing:", obs.shape)
                raise ValueError("Error for file {}, {}, {} \n shape of model required {}".format(ID, label,
                                                                                                  nuID, self.dim))

        return X

    def load_obs(self, obs_path):
        """
        ..todo:: Insert Code to load obs_path here

        Returns
        -------
        data :

        """
        assert True, ' Overwrite this function'
        return 0

    def process(self, data):
        """
         ..todo:: Do some Augmentation and Preprocessing here. Final data should be stored to 'obs'

        Returns
        -------
        obs :

        """
        assert True, ' Overwrite this function'
        return 0