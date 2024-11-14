"""
handling hdf5 files, save data with annotation, load the data,...
"""

import h5py
import os
import numpy as np
import ast


def save_dict_to_h5_file(d_data:dict, save_path, output_data_type = np.int32):
    """
    creates a dataset for every key of dict and safes all together in a h5 file
    The data have to be marked by Key 'data' other stuff are saved as attributes for the dataset
    e.g.:

    d_data { sensor_1 : { 'data':           [1,2,3,...] # have to be numpy array
                          'sample_rate':    192000
                          'sensortype':     'xy'
                        }
             sensor_2
             ...
            }
    Parameters
    ----------
    d_data : dict
        data which should be saved in h5 file
    save_path : string
        path where the data should be saved wiht ending .h5
    output_data_type: np.dtype
        format in which the data should be saved. The smallest possible --> saves memory and speeds everything up
        todo: get this value as list or integrated in the dict --> can selct for every dataset    
    """

    if type(d_data) != dict:
        raise ValueError("Provide dict as input data")

    # create file
    target_dir = os.path.dirname(save_path) 
    if not os.path.isdir(target_dir):
        raise ValueError("target dir does not exist: {}".format(target_dir))
    
    with h5py.File(save_path, 'w') as hf:
        # save the datasets inside
        for key in d_data.keys():
            # data
            np_data = d_data[key]['data'].astype(output_data_type)
            ds = hf.create_dataset(name = key, data = np_data)

            # attributes
            for key2 in d_data[key].keys():
                # to do check datatypes
                if key2 != 'data':
                    # cant be any objects 
                    ds.attrs[key2] = str(d_data[key][key2])



def read_h5file_to_dict(path):
    """
    reads a h5 file and returns data in dict format like it was saved
    Parameters
    ----------
    path: str
        path to the h5 file
    
    Returns
    -------
    d_data:dict
        e.g.
        d_data { sensor_1 : { 'data':           [1,2,3,...] # have to be numpy array
                            'sample_rate':    192000
                            'sensortype':     'xy'
                            }
                sensor_2
                ...
                }
    """
    hf = h5py.File(path, 'r')
    l_keys = list(hf.keys())
    d_data = {}
    for key in l_keys:
        # data
        d_data[key] = {'data': np.array(hf.get(key))}

        # add attributes as seprate keys 
        l_attrbs = list(hf.get(key).attrs.items())
        for attrb in l_attrbs:
            d_data[key][attrb[0]] = attrb[1]
    hf.close()
    return d_data


def read_h5file_to_dict2(path):
    """
    reads a h5 file and returns a dict
    There will be no meta data read out
    Parameters
    ----------
    path: str
        path to the h5 file
    
    Returns
    -------
    d_data:dict
        e.g.
        d_data { key_1 :[1,2,3,...] # have to be numpy array
                 key_2
                 ...
                }
    """
    hf = h5py.File(path, 'r')
    l_keys = list(hf.keys())
    d_data = {}
    for key in l_keys:
        # data
        d_data[key] = np.array(hf.get(key))

    hf.close()
    return d_data



def get_key_data_h5file(l_keys, path):
    """
    reads out specific keys of the h5 file
    Parameters
    ----------
    l_keys : list
        list which contains keys that should be read out from the file
    path: str
        path to the h5 file
    
    returns: d_data
    e.g.
    d_data { sensor_1 : { 'data':           [1,2,3,...] # have to be numpy array
                          'sample_rate':    192000
                          'sensortype':     'xy'
                        }
             sensor_2
             ...
            }
    """
    hf = h5py.File(path, 'r')
    l_keys_h5 = list(hf.keys())
    d_data = {}
    for key in l_keys_h5:
        if key in l_keys:
            # data
            d_data[key]={'data': np.array(hf.get(key))}

            # add attributes as seprate keys 
            l_attrbs = list(hf.get(key).attrs.items())
            for attrb in l_attrbs:
                d_data[key][attrb[0]] = attrb[1]
    hf.close()
    return d_data

def get_key_data_h5file_list(l_keys, path):
    """
    reads out specific keys of the h5 file
    Parameters
    ----------
    l_keys : list
        list which contains keys that should be read out from the file
    path: str
        path to the h5 file
    
    returns: d_data
    e.g.
    d_data { sensor_1 : { 'data':           [1,2,3,...] # have to be numpy array
                          'sample_rate':    192000
                          'sensortype':     'xy'
                        }
             sensor_2
             ...
            }
    """
    hf = h5py.File(path, 'r')
    l_keys_h5 = list(hf.keys())
    l_data = []
    for key in l_keys_h5:
        if key in l_keys:
            # data
            l_data.append(np.array(hf.get(key)))

    hf.close()
    return l_data

def get_keys_of_h5_file(path):
    """
    Returns all the keys (Datatsets) of an h5 file
    Parameters
    ----------
    path: str
        path to the h5 file
    
    Returns
    -------
    l_keys_h5: list
        list with keys in the h5 file
    """
    hf = h5py.File(path, 'r')
    l_keys_h5 = list(hf.keys())
    hf.close()
    
    return l_keys_h5


def save_data_in_hdf5_format(save_dir, file_name, dict_data, dict_anno=None):
    """
    This function is for saving data in the hdf5 file format with an annotation file
    Parameters
    ----------
    save_dir : str
        dir to the saving directory
    file_name : str
        name of the file (without extension)
    dict_data : dict
        dict includes the data which should be saved:
        e.g. {"data_name_1" : 'data' : [1,2,3,4,...],...
                              'anno' : 'label' : 'label1',....
              "data_name_2" : ....
              ...}
        optional:
        the anno key is optional
    dict_anno : dict
        dict which is for example for general annotations or dict with all the annotations:
        e.g. { 'name_sensor1' : dict_annotation-sensor_1,
                ...
        }
    """

    file_name = "{}.hdf5".format(file_name)
    saving_path = os.path.join(save_dir, file_name)

    f_hdf5 = h5py.File(saving_path, "w")

    # create dataset in the hdf5 file for every data point with annotation data
    for num, key in enumerate(dict_data.keys()):
        np_values = np.array(dict_data[key]['data'])
        shape = np_values.shape
        dataset = f_hdf5.create_dataset(key, shape, data=np_values)
        if 'anno' in dict_data[key].keys():
            dataset.attrs['anno'] = str(dict_data[key]['anno'])

    # General Annotation file for all data in the hdf5 file
    if dict_anno is not None:
        str_anno = str(dict_anno) # convert dict into str for easier saving in hdf5 file format
        # add Annotation data with dummy value to add there metadata as annotation data
        data_annotation = f_hdf5.create_dataset("annotation", (1,), dtype='i', data=1)
        # Add one attribute to this dataset with the metadata, the string of the annotation dict
        data_annotation.attrs['dict_annotation'] = str_anno

    f_hdf5.close()


def save_single_data_in_hdf5_format(save_dir, file_name, data, dict_anno=None):
    """
    This function is for saving data in the hdf5 file format with an annotation file
    Parameters
    ----------
    save_dir : str
        dir to the saving directory
    file_name : str
        name of the file (without extension)
    dict_data : dict
        dict includes the data which should be saved:
        e.g. {"data_name_1" : 'data' : [1,2,3,4,...],...
                              'anno' : 'label' : 'label1',....
              "data_name_2" : ....
              ...}
        optional:
        the anno key is optional
    dict_anno : dict
        dict which is for example for general annotations or dict with all the annotations:
        e.g. { 'name_sensor1' : dict_annotation-sensor_1,
                ...
        }
    """

    file_name = "{}.hdf5".format(file_name)
    saving_path = os.path.join(save_dir, file_name)

    f_hdf5 = h5py.File(saving_path, "w")

    # create dataset in the hdf5 file for every data point with annotation data
    np_values = np.array(data)
    shape = np_values.shape
    dataset = f_hdf5.create_dataset('data', shape, data=np_values)
    
    # General Annotation file for all data in the hdf5 file
    if dict_anno is not None:
        str_anno = str(dict_anno) # convert dict into str for easier saving in hdf5 file format
        # add Annotation data with dummy value to add there metadata as annotation data
        data_annotation = f_hdf5.create_dataset("annotation", (1,), dtype='i', data=1)
        # Add one attribute to this dataset with the metadata, the string of the annotation dict
        data_annotation.attrs['dict_annotation'] = str_anno

    f_hdf5.close()


def read_hdf5_file(file_path):
    """

    Parameters
    ----------
    file_path

    Returns
    -------

    """
    f_h5py = h5py.File(file_path, 'r')
    lst_keys_datasets = list(f_h5py.keys())
    dict_data = dict()
    dict_anno = dict()

    for key in lst_keys_datasets:
        # read the meta data into a dict
        if key == "annotation":
           str_anno = f_h5py["annotation"].attrs['dict_annotation']
           dict_anno = ast.literal_eval(str_anno) # convert the stringformat back to dict

        else:
            dict_hdf5 = {'data': np.array(f_h5py[key])}
            if 'anno' in f_h5py[key].attrs.keys():
                str_anno = f_h5py[key].attrs['anno']
                dict_anno = ast.literal_eval(str_anno)  # convert the stringformat back to dict
                dict_hdf5.update({'anno': dict_anno})
            dict_data[key] = dict_hdf5

    dict_data["annotation"] = dict_anno
    return dict_data

def func1_test():
    save_dir = ''
    file_name = 'test'
    data = np.array([1, 2])
    dict_anno_label_1 = {'name': 'sensor1', 'label': 'used'}
    dict_anno_general = {'name': 'test1', 'label': 'lalala'}

    dict_sensor_1 = {'data': data,
                     'anno': dict_anno_label_1 }

    dict_sensor_2 = {'data': data}

    dict_data = {'sensor1': dict_sensor_1,
                 'sensor2': dict_sensor_2}

    # test saving file
    save_data_in_hdf5_format(save_dir, file_name, dict_data, dict_anno_general)

    # test opening file
    dict_data = read_hdf5_file('test.hdf5')
    print(dict_data)


if __name__ == '__main__':
    func1_test()
    #func2_test()


###################################
# old
def func2_test():
    save_dir = ''
    file_name = 'test'
    data = np.array([[1, 2], [3, 4]])
    dict_data = {'data1': data, 'data2': data}
    dict_anno_label_1 = {'name': 'sensor1', 'label': 'used'}
    dict_anno_label_2 = {'name': 'sensor2', 'label': 'healthy'}

    dict_anno = {'anno_sensor1': dict_anno_label_1,
                 'anno_sensor2': dict_anno_label_2}

    # test saving file
    old_save_data_in_hdf5_format(save_dir, file_name, dict_data, dict_anno)

    # test opening file
    dict_data = old_read_hdf5_file('test.hdf5')
    print(dict_data)

def old_save_data_in_hdf5_format(save_dir, file_name, dict_data, dict_anno=None):
    """
    This function is for saving data in teh hdf5 file format with an annotation file
    Parameters
    ----------
    save_dir : str
        dir to the saving directory
    file_name : str
        name of the file (without extension)
    dict_data : dict
        dict includes the data which should be saved:
        e.g. {"data_name_1" : [1,2,3,4,...],
              "data_name_2" : [[1,2],...],
              ...}
    dict_anno : dict
        dict which includes all the annotations:
        e.g. { 'name_sensor1' : dict_annotation-sensor_1,
                ...
        }

    """
    file_name = "{}.hdf5".format(file_name)
    saving_path = os.path.join(save_dir, file_name)

    f_hdf5 = h5py.File(saving_path, "w")

    # create dataset in the hdf5 file for every data point in the data dict
    for num,key in enumerate(dict_data.keys()):
        np_values = dict_data[key]
        shape = np_values.shape
        f_hdf5.create_dataset(key, shape, dtype='i', data=np_values)

    str_anno = str(dict_anno) # convert dict into str for easier saving in hdf5 file format
    # add Annotation data with dummy value to add there metadata as annotation data
    data_annotation = f_hdf5.create_dataset("annotation", (1,), dtype='i', data=1)
    # Add one attribute to this dataset with the metadata, the string of the annotation dict
    data_annotation.attrs['dict_annotation'] = str_anno

    f_hdf5.close()


def old_read_hdf5_file(file_path):
    """

    Parameters
    ----------
    file_path

    Returns
    -------

    """
    f_h5py = h5py.File(file_path, 'r')
    lst_keys_datasets = list(f_h5py.keys())
    dict_data = dict()
    dict_anno = dict()

    for key in lst_keys_datasets:
        # read the meta data into a dict
        if key == "annotation":
           str_anno = f_h5py["annotation"].attrs['dict_annotation']
           dict_anno = ast.literal_eval(str_anno) # convert the stringformat back to dict

        else:
            dict_data[key] = np.array(f_h5py[key][:])

    dict_data["annotation"] = dict_anno
    return dict_data
