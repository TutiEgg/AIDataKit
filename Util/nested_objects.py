import pandas as pd
import os
# Functions for Nested Objects ========================================================================================

def get_type_nested_obj(obj_to_check):
    def type_spec_iterable(obj, name):
        tps = set(type_spec(e) for e in obj)
        if len(tps) == 1:
            return name + "<" + next(iter(tps)) + ">"
        else:
            return name + "<?>"

    def type_spec_dict(obj):
        tps = set((type_spec(k), type_spec(v)) for (k, v) in obj.items())
        keytypes = set(k for (k, v) in tps)
        valtypes = set(v for (k, v) in tps)
        kt = next(iter(keytypes)) if len(keytypes) == 1 else "?"
        vt = next(iter(valtypes)) if len(valtypes) == 1 else "?"
        return "dict<%s,%s>" % (kt, vt)

    def type_spec_tuple(obj):
        return "tuple<" + ", ".join(type_spec(e) for e in obj) + ">"

    def type_spec(obj):
        t = type(obj)
        res = {
            int: "int",
            str: "str",
            bool: "bool",
            float: "float",
            type(None): "(none)",
            list: lambda o: type_spec_iterable(o, 'list'),
            set: lambda o: type_spec_iterable(o, 'set'),
            dict: type_spec_dict,
            tuple: type_spec_tuple,
        }.get(t, lambda o: type(o).__name__)
        return res if type(res) is str else res(obj)

    return type_spec(obj_to_check)


def get_path_of_key_value(dict_obj, key_value_list):
    # Clear lists
    path_list = list()
    path = list()

    # Function to find path to key and value
    def _find_path_to_key_value(dict_obj, key_value, i=None):
        for k, v in dict_obj.items():
            # add key to path
            path.append(k)

            # if all(x in key_value for x in [k, v]): #If k and v are in key_value_list
            if str(k) in key_value.keys():
                if v == key_value[k]:  # if v.
                    path_string = os.path.join(*path, v)
                    path_list.append(path_string)
            else:
                if isinstance(v, dict):
                    # continue searching
                    _find_path_to_key_value(v, key_value, i)
                if isinstance(v, list):
                    # search through list of dictionaries
                    for i, item in enumerate(v):
                        # add the index of list that item dict is part of, to path
                        path.append(i)
                        if isinstance(item, dict):
                            # continue searching in item dict
                            _find_path_to_key_value(item, key_value, i)
                        # if reached here, the last added index was incorrect, so removed
                        path.pop()

            # remove the key added in the first line
            if path != []:
                path.pop()

    # Get Path to key_value
    _find_path_to_key_value(dict_obj, key_value_list)
    return path_list


def get_path_and_value_of_nested_dict(dict_obj, key):
    new_dict = dict()
    path = list()

    # Function to the path and the value of a key in a nested dictionary
    def _find_path_and_content(dict_obj, label_list, i=None):
        for k, v in dict_obj.items():
            # add key to path
            path.append(k)
            if isinstance(v, dict):
                # continue searching
                _find_path_and_content(v, label_list, i)
            if isinstance(v, list):
                # search through list of dictionaries
                for i, item in enumerate(v):
                    # add the index of list that item dict is part of, to path
                    path.append(i)
                    if isinstance(item, dict):
                        # continue searching in item dict
                        _find_path_and_content(item, label_list, i)
                    # if reached here, the last added index was incorrect, so removed
                    path.pop()
            if k in label_list:
                path_string = os.path.join(*path[1:])
                new_dict[path_string] = v

            # remove the key added in the first line
            if path != []:
                path.pop()

    _find_path_and_content(dict_obj, key)
    return new_dict


def get_dict_of_keys_in_nestedDict(nested_dictionary, keyname_list, key_list):
    for key, value in nested_dictionary.items():

        if str(key) in keyname_list:
            new_dict = dict()
            new_dict[key] = value
            key_list.append(new_dict)

        else:
            if isinstance(value, dict):
                key_list = get_dict_of_keys_in_nestedDict(nested_dictionary=value, keyname_list=keyname_list,
                                                          key_list=key_list)
            else:
                break

    return key_list


def get_path_to_key_in_dict(nested_dictionary, keyname, path_list):
    for key, value in nested_dictionary.items():
        if str(key) == keyname:
            break
        else:
            if isinstance(value, dict):
                path_list.append(key)
                path_list = get_path_to_key_in_dict(nested_dictionary=value, keyname=keyname, path_list=path_list)
                break
            else:
                break
    return path_list


def get_all_Values_in_nested_dict(value_dict, new_value):
    for key, value in value_dict.items():
        if isinstance(value, dict):
            get_all_Values_in_nested_dict(value_dict=value, new_value=new_value)
        else:
            new_value.append(value)
    return new_value


def get_all_Values_in_nested_dict_with_except(value_dict, new_value, except_list):
    for key, value in value_dict.items():
        if isinstance(value, dict):
            get_all_Values_in_nested_dict_with_except(value_dict=value, new_value=new_value,
                                                      except_list=except_list)
        else:
            if value not in except_list:
                new_value.append(value)
    return new_value


def get_all_Json_Values_in_nested_dict(value_dict, new_value):
    for key, value in value_dict.items():
        if isinstance(value, dict):
            get_all_Json_Values_in_nested_dict(value_dict=value, new_value=new_value)
        else:
            if str(value).endswith(".json"):
                new_value.append(value)
    return new_value


def flatten_dict(data_dict):
    """
        Flatten a nested dict. New Keywords are: key1_key2_...

    Parameters
    ----------
    data_dict : nested dictionarry

    Returns
    -------
    dict
        dictionarry with depth of one
    """
    flattened = pd.json_normalize(data_dict, sep='_')
    flattened = flattened.to_dict(orient='records')[0]
    return flattened