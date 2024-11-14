import json

import pandas as pd
import os
import ujson
import h5py
import numpy as np
import pickle
import csv
from SWAI.Util import modify_datatypes as md
from tkinter.filedialog import asksaveasfilename
from datetime import datetime


def read_json_to_DataFrame(path_to_file):
    assert path_to_file.endswith('.json'), 'File is no Json format!'

    with open(path_to_file, 'r') as file:
        data_dict = ujson.load(file)
    df = pd.DataFrame(data_dict)
    return df


def read_json_to_Dict(path_to_file):
    """
    Reading Data from .json and returning any datatype used in this specific json-file

    :param path_to_file: string: jsonfile to be read
    :return: format used in Json-file (dict)
    """
    assert path_to_file.endswith('.json'), 'File is no Json format!'

    with open(path_to_file, 'r') as file:
        data_dict = ujson.load(file)

    # df = pd.DataFrame(data_dict)

    return data_dict


def read_CSV_File_to_dict(path_to_file, start=0, end=None):
    data_dict = dict()
    with open(path_to_file, 'r') as fp:
        index = 0
        for line in fp:
            clean_line = line.rstrip("\n")  # Delete \n from all Strings
            if (start <= index and end is None) or (start <= index <= end):
                value_split = clean_line.split(",")
                data_dict[value_split[0]] = value_split[1:]  # Get every value from 1 to last
            elif index > end:
                break
            index += 1
    return data_dict


def read_CSV_File_to_df(path_to_file, start=0, row_amount=None):
    return pd.read_csv(path_to_file, skiprows=start, nrows=row_amount)


def read_universal_File_(path_to_file):
    pass


def get_info_of_CSV_File(path, start, end, string_to_search):
    """
    This function is searching for a string to read from
    (1.column = information_label, 2.Column = information_content)

    Parameters
    ----------
    path:               path to the file
    start:              startrow of csv_file (starting point to read)
    end:                endrow of csv_file  (end point to stop reading)
    string_to_search:    information you want to read

    Returns
    -------

    """
    df = read_CSV_File_to_df(path, start, end)
    col_one = df.values
    for label_info in col_one:
        if str(label_info[0]) == string_to_search:
            return str(label_info[1])
    return "[ERROR] no string with: " + string_to_search + " was found!"


def split_csv_file(path, path_output):
    df = read_CSV_File_to_df(path, start=21)
    column_dict = md.dataframe_to_Dictionary(df)
    for split in column_dict:
        origin_file_name = os.path.basename(os.path.normpath(path))
        splitted_file_name = str(split) + "_" + origin_file_name[:-3] + "json"

        path_splitted_file = os.path.join(path_output, splitted_file_name)
        create_Data_file_and_path(column_dict[split], path_splitted_file)


def read_hdf5_file(filepath):
    """
    Reads a hdf5 file and return a dict with numpy arrays. If there is an annotation saved in the hdf5 file it will be treated
    as dict not as numpy
    Parameters
    ----------
    filepath    path to the hdf5 file

    Returns
    -------
    dict with all the value of the hdf5 file

    """
    f_h5py = h5py.File(filepath, 'r')
    lst_keys = list(f_h5py.keys())
    dict_data = dict()
    dict_anno = dict()

    for key in lst_keys:
        # read the meta data into a dict
        if key == "Annotation":
            for num, anno_key in enumerate(f_h5py[key].attrs.keys()):
                dict_anno[anno_key] = f_h5py["Annotation"].attrs[anno_key]
        # save the data as numpy array
        else:
            dict_data[key] = np.array(f_h5py[key][:])

    dict_data["Annotation"] = dict_anno

    return dict_data


def read_npy_file(file_path_obs):
    """
        Reads a npy file (Observation) and an Annotation.json File from the given Dir-path.
        Returns a dict with numpy arrays.
        Parameters
        ----------
        filepath    path to the npy file

        Returns
        -------
        dict with all the value of the npy file

        """
    anno_file_name = os.path.join(os.path.split(file_path_obs)[0], "annotation.json")
    data_npy = np.load(file_path_obs)
    with open(anno_file_name) as anno_file:
        ann_dict_json = json.load(anno_file)
    dict_data = dict()
    dict_data["Annotation"] = ann_dict_json
    dict_data["Data"] = data_npy

    return dict_data


def read_hterm_log(file_path):
    """ Reading a signal from a hterm savefile

    Data in savefile should be saved as Values separated by ',' or '\n'.
    Files can be .log or .txt.
    Data has to be 1-Dimensional.

    Parameters
    ----------
    file_path : string, path
        Path to file

    Returns
    -------
    content : np.array
        Signal as numpyarray.
    """
    with open(file_path, 'r') as file:
        content = file.read()
        if ',' in content:
            content = content.split(',')
        else:
            content = content.split('\n')
        content = [int(x) for x in content]
        return np.array(content)

def read_excel_to_df(file_path):
    df = pd.read_excel(file_path).fillna('')
    return df

# Create File on Path =================================================================================================

def create_CSV_file(header_list, data_list, path):
    """

    Parameters
    ----------
    header_list:    List of headers
    data_list:      List of data (same length as headerlist) 2 dim, each nested list contains data of one column
    path:           Path where to save the file

    Returns
    -------

    """

    with open(path, 'w', encoding='UTF8') as f:
        writer = csv.writer(f)

        # write the header
        writer.writerow(header_list)

        # write data
        for i in range(len(data_list[0])):
            row = list()
            for j in range(len(header_list)):
                row.append(data_list[j][i])
            writer.writerow(row)

        # write the data
        # writer.writerow(data_list)


def create_Data_file(content, path):
    """
    Create a new Data_file

    :param content: DataFrame with all datas
    :param path: The Path were the file should be created
    """

    if isinstance(content, pd.DataFrame):
        contentToWrite = content.to_dict()
    else:
        contentToWrite = content

    with open(path, "w") as outfile:
        ujson.dump(contentToWrite, outfile)


def create_Data_file_and_path(content, path):
    """
    Create a new Data_file

    :param content: DataFrame with all datas
    :param path: The Path were the file should be created
    """

    if isinstance(content, pd.DataFrame):
        contentToWrite = content.to_dict()
    else:
        contentToWrite = content
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as outfile:
        ujson.dump(contentToWrite, outfile)


def create_path_to_file(*args):  # Hardcoded for one systemtype only
    """
    Creates a Path with all Parameters (args)

    The order in which the values are passed is important

    :param variable number of parameters which will put into one String
    :return Path as a String
    """
    pathToFile = ""
    for arg in args:
        pathToFile += arg + "\\"
    if pathToFile.endswith("\\"):
        pathToFile = pathToFile[:-1]
    return pathToFile


def dump_as_pickel(data,target_dir,file_name):
    """
    Dumps data as pickle (.obj) file at the specified target dir with file_name
    Parameters
    ----------
    data : any
        some kind of data
    target_dir : path
        path to the target directory
    file_name : str

    Returns
    -------

    """
    file_name += '.obj'
    file_path = os.path.join(target_dir,file_name)
    filehandler = open(file_path, "wb")
    pickle.dump(data, filehandler)
    filehandler.close()


def get_data_of_pickel(file_path):
    """
    read pickle file and return the data
    Parameters
    ----------
    file_path : path to the pickle file

    Returns
    -------
    data : data of the pickle file
    """
    file = open(file_path, 'rb')
    object_file = pickle.load(file)
    file.close()
    return object_file


def create_one_csv_of_all_and_transpose_data():
    # TODO: put this Function into another file
    path = r"C:\Users\Praktikant Software\Desktop\Data of Temperature and Pressure\Pressure data\new_machine_1cyc(machine_02)\healthy_CH1_01.csv"
    path_folder = r""  # path to folder with all files
    path_output = r""  # path to output_folder

    list_files = os.listdir(path_output)
    for file in list_files:
        df = read_CSV_File_to_df(os.path.join(path_output, file))
        df_transposed = md.dataframe_transpose(df)


def get_file_save_path_by_tk(initial_dirpath=None, filename=None, timestamp=False):
    """
    This function is for getting save name for image file
    Parameters
    ----------
    initial_dirpath : str
        initial path which will be opened in the explorer
    filename : str
        give a default filename to the file
    timestamp : bool
        if true the name will start with timestamp and date

    Returns
    -------
    filename_save : str
        file_path for saving the file

    """

    files = [('images (*.png)', '*.png')]
    intial_dir = r"C:"
    if initial_dirpath:
        intial_dir = initial_dirpath

    if filename is None:
        filename = ""

    if timestamp == True:
        date = datetime.today().strftime('%Y_%m_%d')
        now = datetime.now()
        current_time = now.strftime("%Hh_%Mm_%Ss")
        name = date + '_' + current_time
        filename = name + "_" + filename

    filename_save = asksaveasfilename(initialdir=intial_dir,
                                      filetypes=files,
                                      defaultextension=files,
                                      initialfile=filename)
    return filename_save