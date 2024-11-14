import numpy as np
import copy

import pickle

class SensorDataBase:
    """ This is the Base Class for Different Sensor Data. The class should 
    contain all general functions that can be used by different sensortypes"""
    def __init__(self,
                sensorname,
                ):
        """
        Parameters
        ----------
        sensorname : str
            name of the Sensor
        """
        self.sensorname = sensorname


    def flatten_of_data(self, l_data):
        """
        If data is in format like [[1,2,3],[1,2,3],None,[1,2]...]
        This function will flatten the data
        --> this function is only for list in list
        """
        # todo make it faster
        flat_list = []
        if type(l_data) == list: 
            for sublist in l_data:
                if type(sublist) == list:
                    for item in sublist:
                        flat_list.append(item)
                else:
                    flat_list.append(sublist)
            return flat_list
        else:
            return l_data

    def remove_none_values(self, data):
        """ Removes the none values of the data in a flatten list
        to do , for all shapes
        """
        np_data = np.array(data)
        np_data = np_data[np.where(np_data != None)[0]]
        return np_data
    
    
    def dump_as_pickle(self, data,target_dir):
        """todo"""
        filehandler = open(target_dir, "wb")
        pickle.dump(data, filehandler)
        filehandler.close()

    def get_data_of_pickel(self, file_path):
        """todo"""
        file = open(file_path, 'rb')
        object_file = pickle.load(file)
        file.close()
        return object_file



        
    