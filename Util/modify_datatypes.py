import numpy as np
import copy
from itertools import chain
import os
import shutil
from bisect import bisect_left
import re
import functools

# Reformat object =====================================================================================================
def dataframe_to_Dictionary(df):
    column_name_list = df.columns.tolist()
    data_dict = dict()
    if len(column_name_list) == 2:
        x = df[column_name_list[0]].tolist()
        y = df[column_name_list[1]].tolist()

        data_dict = dict(zip(x, y))
    else:
        # returns a dicitonary of Channels and each Channel_dict has another dictionary with key:value (time:value) data
        # Start at second column (1), because the first one is always the time_col
        for col_index in range(1, len(column_name_list)):
            # Get a list out of this column
            chan_list = df[column_name_list[col_index]].tolist()
            # Check if the first entry of the list is a label
            if isinstance(column_name_list[0], str):
                time_list = df[column_name_list[0]].tolist()
                value_list = df[column_name_list[col_index]].tolist()
                content_dict = dict(zip(time_list, value_list))

                data_dict[column_name_list[col_index]] = content_dict
            else:
                raise ValueError("[ERROR] The first position: (Type" + str(type(chan_list[0])) + ") " + str(chan_list[
                                                                                                                0]) + " of the Dataframe isnt a string_label, check the dataframe given to the function: dataframe_to_Dictionary")
    return data_dict


def dataframe_to_Dictionary_wo_timestamp(df):
    column_name_list = df.columns.tolist()

    y = df[column_name_list[0]].tolist()
    x = list(range(-500000, 500000, 8))
    x = [number / 1000 for number in x]
    y = list(filter(lambda a: a >= 1.34, y))

    data_dict = dict(zip(x, y))
    return data_dict


def dataframe_transpose(df):
    df_transposed = df.T
    return df_transposed


def get_list_of_dict_out_of_dataframe(df):
    """
    returns a list of dictionarys.
    every dictionary is one column of data. Key=column

    Parameters
    ----------
    df

    Returns
    -------

    """


def convert_AnyList_to_intList(any_list):
    return list(map(int, any_list))


def convert_AnyList_to_stringList(any_list):
    return list(map(str, any_list))


def convert_listOfDict_to_nestedDict(content, key=None):
    ret_dict = dict()
    for idx, val in enumerate(content):
        if key:
            ret_dict[key] = val
        else:
            ret_dict[idx] = val
    return ret_dict


# Modify Dictionary ===================================================================================================

def check_correct_format(content):
    def correct_type(content):
        # TODO: correct_type(content) es müssen noch die list_indexe gelöscht werden.
        new_dict = dict()
        if isinstance(content, dict):
            for k, v in content.items():
                if isinstance(v, list):
                    for idx, val in enumerate(v):
                        append_to_dict(new_dict, k, correct_type(val))
                else:
                    append_to_dict(new_dict, k, correct_type(v))

        elif isinstance(content, list):
            # list into dict
            for idx_con, val_con in enumerate(content):
                append_to_dict(new_dict, idx_con, correct_type(val_con))
        # if value = np.ndarray -------------------------------------------------------------------------------
        elif isinstance(content, np.ndarray):
            print("numpay-array: ", content)
            return correct_type(content.tolist())
        else:
            return content
        return new_dict

    return correct_type(content)


def append_to_dict(data_dict, key, value):
    """
    Adds new key:value to or appends a value to an already existing key to dictionary

    If key not in data_dict => create new key:value
    If key IS in data_dict => append value to existing key
    Parameters
    ----------
    data_dict   Dictionary to append to
    key         key to append
    value       value to append

    Returns
    -------

    """

    if key not in data_dict:
        print(key)
        data_dict[key] = value
    else:
        # merge 2 dict to one dict (data_dict[key] with value)
        if isinstance(data_dict[key], dict) and isinstance(value, dict):
            data_dict[key].update(value)
        # merge none_dict with none_dict to list
        elif not isinstance(data_dict[key], dict) and not isinstance(value, dict):
            data_dict[key] = [data_dict[key], value]

    return data_dict


def get_subDict(data_dict):
    return_list = []
    for key in data_dict:
        return_list.append(data_dict[key])
    return return_list


def create_dict_of_2_lists(key_list, value_list):
    return dict(zip(key_list, value_list))


# Modify List =========================================================================================================
def check_duplicates_in_list(list_to_check):
    """
    Check if List has duplicates

    :param list_to_check: List
    """
    seen = set()
    for item in list_to_check:
        if item in seen:
            print("Duplicate: ", item)
        else:
            seen.add(item)
    return seen


def delete_duplicates_in_list(unclean_list):
    """
    Delete duplicates of List

    :param list: List
    """
    # Deletes Empty list in unclean_list
    unclean_list = [x for x in unclean_list if x]
    new_list = list()

    for content in unclean_list:
        if content not in new_list and content != None:
            new_list.append(content)
    return new_list


def flat_list(list_to_flat):
    return list(chain.from_iterable(list_to_flat))


def get_closest_value(list_to_check, value_number):
    """
    Assumes list_to_check is sorted. Returns closest value to value_number.

    If two numbers are equally close, return the smallest number.

    >>> get_closest_value([1,2,4,5,6],4)

    """
    # Using bisect is way faster the longer the list is
    pos = bisect_left(list_to_check, value_number)

    if pos == 0:
        return list_to_check[0]
    if pos == len(list_to_check):
        return list_to_check[-1]
    before = list_to_check[pos - 1]
    after = list_to_check[pos]
    if after - value_number < value_number - before:
        return after
    else:
        return before


# Modify Folder =======================================================================================================
def delete_all_in_Folder(path):
    """
    Delete every Content in Folder

    :param path: Path to Folder
    """
    for files in os.listdir(path):
        path = os.path.join(path, files)
        try:
            shutil.rmtree(path)
        except OSError:
            os.remove(path)


def delete_complete_Folder(path):
    """
    Delete Folder and Content

    :param path: Path to Folder
    """
    shutil.rmtree(path)


def getAbsolutePathToFolder(origin_Folder):
    """
    Get Absolute_Path of an Origin_Folder above and returns it

    :param origin_Folder:   The Name of the Folder you want the Absolute_Path of
    :return:                the Absolute Path of this Folder
    """

    origin = False
    path = os.path.dirname(os.path.abspath(__file__))
    while not origin:
        try:
            stripped_path = os.path.basename(os.path.normpath(path))
            if stripped_path == origin_Folder:
                return path
            else:
                path = os.path.abspath(os.path.join(path, '..'))
        except:
            print("No Origin Folder called: ", origin_Folder, " found")


def get_directory_structure(rootdir):
    """
    Creates a nested dictionary that represents the folder structure of rootdir
    without the Root_Folder (only Content)

    :param rootdir: Path to folder structure
    """
    dir = {}
    rootdir = rootdir.rstrip(os.sep)
    start = rootdir.rfind(os.sep) + 1  # So it doesnt include the Root_Folder
    for path, dirs, files in os.walk(rootdir):
        folders = path[start:].split(os.sep)
        subdir = dict.fromkeys(files)
        parent = functools.reduce(dict.get, folders[:-1], dir)
        parent[folders[-1]] = subdir
    return dir


# Modify String =======================================================================================================
def create_string(*args):  # Same as split_ID
    """
    Creates a Path with all Parameters (args)

    The order in which the values are passed is important

    :param variable number of parameters which will put into one String
    :return Path as a String
    """
    pathToFile = ""
    for arg in args:
        pathToFile += arg
    return pathToFile


def split_string(idString):
    """
    splits a string on indicators

    :param idString:    the String which is getting split
    :return:            returns a list of part_strings of idString

    >>> stringToSplit = "part1_part2_part3.dataFormat"
    >>> split_string(stringToSplit)
    ['part1', 'part2', 'part3', 'dataFormat']
    """
    return re.split("[_.]", idString)


def split_string_custom(idString, custom_indicator_string):
    """
    splits a string on custom indicators

    Parameters
    ----------
    idString:                   the String which is getting split
    custom_indicator_string:    a string with all custom indicators

    Returns
    -------
    list of strings

    >>> stringToSplit = "dict<part2,part3>nothing<.dataFormat>"
    >>> custom_indi = "<,>"
    >>> split_string_custom(stringToSplit, custom_indi)
    ['dict', 'part2', 'part3', 'nothing', '.dataFormat', '']

    """
    return re.split("[{}]".format(custom_indicator_string), idString)


def split_path(path):
    new_path = os.path.normpath(path)  # Normalize path to proper string
    return new_path.split(os.sep)