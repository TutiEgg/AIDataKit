""" ByteFileReader
This class is for reading out byte_files with structure ([id][value]...)
"""

import math
from io import BytesIO
import struct
import numpy as np
import math


def reverse_Bits(n, no_of_bits):
    result = 0
    for i in range(no_of_bits):
        result <<= 1
        result |= n & 1
        n >>= 1
    return result

class ByteFileReader():
    """
    This class is for reading out byte_files with structure [id][byte1][byte2]. First it will be checked if the ids in the dict corresponds to the ids
    in the byte-file. Then data of the byte-file will be read and interpreted like configuration in the dict
    """
    def __init__(self,
                 file_path,
                 dict_ids,
                 datatype_id,
                 use_time = False):
        """
        Initialization function
        Parameters
        ----------
        file_path : string
            path to file reltive or absolute
        dict_ids : dict
            dict_sensor_id = {'sensor0': dict_sensor_0_config,
                              'sensor1': dict_sensor_1_config,
            dict with sensor name and the id, also 'time' id is required when the time steps should be created
            dict_sensor_id = {'sensor0': dict_sensor_0_config, ...}
            dict_sensor_config = {'idx':       int : idx for the returned numpy array
                                  'name':      str : name of the data or sensor name
                                  'datatype':  str : [int16, uint16, int32 uint32] type of data, how the bytes should be
                                               interpreted
                                  'id1':       int : uint8 id value of the data in the binary
                                  'bytes':     int : num of bytes for the id
                                  'byteorder': list : int the list is specifies the bytepostion e.g. [3, ..] means,
                                               the third byte received (byte_3) have to be at position 0


        datatype_id : string
            datatype of the id ['uint8_t']
        """

        self.flag_use_time = use_time
        self.supported_datatypes_id = ['uint8_t']

        # check passing parameters
        if not datatype_id in self.supported_datatypes_id:
            raise ValueError("datatype of id not supported")

        if self.flag_use_time == True:
            if 'time' in dict_ids.keys():
                self.id_time = dict_ids['time']
            else:
                raise ValueError(" no time id provided in dict ids")
        else:
            self.id_time = -1


        self.file_path = file_path
        self.num_of_ids = len(dict_ids.keys())
        self.datatype_id = datatype_id
        self.dict_ids = dict_ids
        self.lst_all_ids = self._get_lst_all_ids()
        self.dict_id_to_key = self._get_dict_id_to_key() # id of data to the dict keys
        self.lst_dict_id_keys = list(self.dict_ids.keys()) # lst with all keys of the dict_ids
        self.dict_id_to_idx = self._get_dict_ids_to_idx()
        self.bytefile = self.read_file()
        #self.bytefile = self._check_byte_file()

        # get the raw data that was saved in the byte file
        self.structured_output_data_raw = self.get_structured_output_data_regarding_to_highest_sampling_rate()
        if self.flag_use_time:
            self.structured_output_data_time = self.get_structured_output_data_with_time()

    def _get_lst_all_ids(self):
        lst_all_ids = []
        for key in self.dict_ids.keys():
            id1 = self.dict_ids[key]['id1']#
            lst_all_ids.append(id1)
            if 'id2' in self.dict_ids[key].keys():
                id2 = self.dict_ids[key]['id2']
                lst_all_ids.append(id2)
        return lst_all_ids

    def _get_dict_id_to_key(self):
        dict_id_to_key = {}
        for key in self.dict_ids.keys():
            id1 = self.dict_ids[key]['id1']#
            dict_id_to_key.update({id1:key})
            if 'id2' in self.dict_ids[key].keys():
                id2 = self.dict_ids[key]['id2']
                dict_id_to_key.update({id2:key})

        return dict_id_to_key

    def _check_byte_file(self):
        """Check the bytefile for ids and removes the ids where the number of databytes doesnt fit"""
        print("check byte file")
        idx = 0
        counter_id = 0
        counter_amount_false_data = 0
        lst_new_bytes = []

        while(idx < (len(self.bytefile)-5)):
            current_byte = self._read_one_byte(idx)
            # check if the byte could be an id
            if current_byte in self.lst_all_ids:
                id = current_byte
                # check number of databytes for this id
                num_databytes = self.dict_ids[self.dict_id_to_key[id]]['bytes']
                # check if there comes also an id
                next_id = self._read_one_byte(idx + num_databytes + 1)

                if next_id in self.lst_all_ids:
                    # to correct ids in row is ok so data shpuld be okay and can be saved in the filtered data block
                    counter_id += 1
                    lst_new_bytes.append(id)
                    for i in range(1, num_databytes + 1):
                        data_byte = self._read_one_byte(idx + i)
                        lst_new_bytes.append(data_byte) #.to_bytes(1, byteorder='big'))
                    idx = idx + num_databytes
                else:
                    counter_amount_false_data += 1

            # up counting idx
            idx = idx + 1
            if (counter_id % 100000) == 0:
                print("counter found ids", counter_id)

            if idx >= len(self.bytefile):
                break

        new_byte_file = bytes(lst_new_bytes)
        print('\n## check bytefile is done ##')
        print('found {} ids with correct values'.format(counter_id))
        print('amount of corrupted data: {}'.format(counter_amount_false_data))
        print('\n\n')
        return new_byte_file

    def _get_lst_id1(self):
        """get a list with all id1 from dict ids"""
        lst_id1 = []
        for key in self.dict_ids.keys():
            lst_id1.append(self.dict_ids[key]['id1'])
        return lst_id1

    def _get_dict_ids_to_idx(self):
        """Returns a dict with the ids of the self.dict_ids as Keys and the idx for numpy array"""
        dict_ids_to_idx = {}
        lst_idx = []
        for key in self.dict_ids.keys():
            idx = self.dict_ids[key]['idx']
            id1 = self.dict_ids[key]['id1']
            id2 = None
            if idx not in lst_idx:
                lst_idx.append(idx)
            else:
                raise ValueError("the idx of the different sensor data have to be different. Check dict_ids!")
            if 'id2' in self.dict_ids[key].keys():
                id2 = self.dict_ids[key]['id2']
            else:
                id2 = None

            # check if there are all ids different
            if id1 not in dict_ids_to_idx.keys():
                dict_ids_to_idx.update({id1:idx})
            else:
                raise ValueError ("Ids have to be different")

            # check if there are all ids different
            if id2 is not None:
                if id2 not in dict_ids_to_idx.keys():
                    dict_ids_to_idx.update({id2: idx})
                else:
                    raise ValueError("Ids have to be different")

        return dict_ids_to_idx

    def read_file(self):
        """ read out the byte file and returns the raw byte file"""
        with open(self.file_path, "rb") as f:
            byte_file = f.read()
        return byte_file

    def _read_one_byte(self, byte_number):
        """ reads in one byte at the defined position"""
        byte_0 = struct.unpack_from('B', self.bytefile, byte_number)[0]
        return byte_0

    def get_value_from_bytes_list(self, id1, lst_bytes_values):
        """ Changes the order of the bytes like defined in the dict_ids and converts the bytes
        to the correct datatype """

        # convert list to bytes
        key = self.dict_id_to_key[id1] # get key in the dict of this id
        lst_byteorder = self.dict_ids[key]['byteorder']
        datatype = self.dict_ids[key]['datatype']
        value_uint = b''
        # put the bytes in the correct order like defined in the dict sensor config
        for i, byte in enumerate(lst_bytes_values):
            byte_num = lst_byteorder[i]
            value_uint += lst_bytes_values[byte_num].to_bytes(1,byteorder='big')

        ret_value = None
        if datatype == 'int16':
            ret_value = struct.unpack_from('>h', value_uint, 0)[0]

        elif datatype == 'uint16':
            ret_value = struct.unpack_from('>H', value_uint, 0)[0]

        elif datatype == 'int32':
            ret_value = struct.unpack_from('>i', value_uint, 0)[0]

        elif datatype == 'uint32':
            ret_value = struct.unpack_from('>I', value_uint, 0)[0]
        else:
            raise ValueError("Datatype not implemented yet")
        return ret_value

    def get_structured_output_data_regarding_to_highest_sampling_rate(self):
        """ Returns the structured output data. The data will be structured by id. The data with the different ids have
        most of the time different sampling rates, for time synchronization the id with the highest samplingrate
        is the reference for the time. The ids with lower sampling rate will have nan values at the timestamps where
        no data available
        Returns
        -------
        structured_output_data : numpy
            id_time   id_1    id_2  ...
            xx         inf      xx
            xx         xx       xx
            here the id_2 is the one with the highest sampling rate
        """
        print("start reading out the byte file and save it into numpy array ...")
        # create numpy array with nan values where the data can be inputed
        structured_output_data = np.full((self.num_of_ids, len(self.bytefile)), fill_value=np.nan)
        counter_of_every_id = np.zeros(self.num_of_ids)
        idx_bytefile = 0

        while (idx_bytefile < len(self.bytefile)-2):
            current_byte = self._read_one_byte(idx_bytefile)
            value_bytes = None
            if current_byte in self.lst_all_ids:
                id = current_byte
                num_databytes = self.dict_ids[self.dict_id_to_key[id]]['bytes']
                lst_bytes = []
                for i in range(1, num_databytes + 1):
                    data_byte = self.bytefile[idx_bytefile + i]
                    lst_bytes.append(data_byte)

                value_bytes = self.get_value_from_bytes_list(id, lst_bytes)
                idx_bytefile += num_databytes

            if value_bytes is not None:
                # convert the id of the sensor data to an idx which can be used later in the numpy array
                idx = self.dict_id_to_idx[id]

                # save at specified position (depending on the highest sampling rate)
                max_counter_id = counter_of_every_id.argmax() # get
                max_counter_ids = np.array(np.where(counter_of_every_id == np.amax(counter_of_every_id))) # get all the ids with the max value
                max_counter_value = math.ceil(counter_of_every_id[max_counter_id])
                if idx in max_counter_ids:
                    # save at the next row in that array
                    structured_output_data[idx, max_counter_value] = value_bytes
                else:
                    # save at the same row in the array for this id
                    structured_output_data[idx, max(max_counter_value - 1, 0)] = value_bytes
                counter_of_every_id[idx] = counter_of_every_id[idx] + 1

            # Update idx:
            status_percent = math.floor(100 * idx_bytefile / len(self.bytefile ))
            if status_percent > 0 and (status_percent % 10) == 0:
                print("{}% of bytes converted".format(status_percent))
            idx_bytefile += 1

        # cut the rest of the array away
        structured_output_data = structured_output_data[:,:max_counter_value]
        print("finished")
        return structured_output_data

    def get_structured_output_data_with_time(self):
        """ Add timestamps to every datapoint by using the highest sampling rate as reference"""
        # create time series for the data with the highest sampling rate
        idx_last_time_stamp = np.nanargmax(self.structured_output_data_raw[self.dict_id_to_idx[self.id_time]])
        last_time_stamp = self.structured_output_data_raw[self.dict_id_to_idx[self.id_time]][idx_last_time_stamp]

        # remove the values after the last time stamp from array
        structured_output_data = self.structured_output_data_raw[:, :(idx_last_time_stamp + 1)]

        # get all the time stamps for the data with the highest sampling rate
        if idx_last_time_stamp > 0:
            time_steps_highest_sample_rate = last_time_stamp / (idx_last_time_stamp)
        else:
            raise ValueError("divide by zero")

        timestamps_highest_sampling_rate = np.arange(0, last_time_stamp + time_steps_highest_sample_rate, time_steps_highest_sample_rate)

        # create an array with new time
        structured_output_data_wtime = structured_output_data
        structured_output_data_wtime[self.dict_id_to_idx[self.id_time]] = timestamps_highest_sampling_rate

        return structured_output_data_wtime

    def get_id_specific_data_wtime(self):
        """ This functions returns a list with data for every id with time, all arrays have different length
        (depending on the recorded sampling rate), the order is like the input of the sensor ids in the dict"""
        lst_data = []
        lst_data_without_nan = []

        for i in range(0, self.num_of_ids):
            if i != self.id_time:
                data = self.structured_output_data_time[[self.id_time, i], :]
                data__without_nan = data[:, ~np.isnan(data).any(axis=0)]  # remove all columns where a nan value is included
                lst_data.append(data)
                lst_data_without_nan.append(data__without_nan)

        return lst_data_without_nan

    def get_id_specific_data_with_sample_number(self):
        """This function returns a list with data for every id with the sample_number as reference and the value,
        so all arrays have different length"""
        lst_data = []
        lst_data_without_nan = []
        # add axis to the data
        data_points = np.arange(0, self.structured_output_data_raw.shape[1])
        data_points = data_points.reshape(1,data_points.shape[0])

        for i in range(0, self.num_of_ids):
            if i != self.id_time:
                data = self.structured_output_data_raw[[i],:]
                # concatenation of data points with the sensor data
                data_concatenate = np.concatenate((data_points, data))
                data__without_nan = data_concatenate[:, ~np.isnan(data).any(axis=0)]  # remove all columns where a nan value is included
                lst_data.append(data)
                lst_data_without_nan.append(data__without_nan)

        return lst_data_without_nan

    #############################
    # deprecated
    #############################
    def _check_id_ok(self, id, frame_number):
        """ Checks if the id is known and the order is correct before and after the id like in the
        configuration of the dict"""
        flag_unknown_id = 0
        flag_wrong_order = 0
        flag_wrong_start_id = 0

        if (id not in self.lst_2byte_datatype) and (id not in self.lst_2x2byte_datatype):
            print("found wrong id:{} in dataframe number {}".format(id, frame_number))
            flag_unknown_id = 1
        else:
            # check if related ids follow each other
            if id in self.lst_2x2byte_datatype_id1:
                frame_number = frame_number + 1
                id2, byte2, byte3 = self._read_id_and_bytes(frame_number)
                # check if id2 fits to id1
                if id2 is not None:
                    if self.dict_id_to_idx[id] != self.dict_id_to_idx[id2]:
                        print("After id1: {} follows wrong id2: {}".format(id, id2))
                        flag_wrong_order = 1

            # check if related id comes before
            elif id in self.lst_2x2byte_datatype_id2:
                if frame_number == 0:
                    flag_wrong_start_id = 1
                else:
                    # check id before
                    id1, byte2, byte3 = self._read_id_and_bytes(frame_number - 1)
                    # check if id2 fits to id1
                    if id1 is not None:
                        if self.dict_id_to_idx[id] != self.dict_id_to_idx[id1]:
                            print("After id1: {} follows wrong id2: {}".format(id1, id))
                            flag_wrong_order = 1

        return flag_unknown_id, flag_wrong_order, flag_wrong_start_id
    def _error_check_byte_file(self):
        """Check if there are any errors in the byte_file, the errors will be counte and printed out"""

        print("Start Error checking byte file ...")
        counter_unknown_ids = 0
        counter_wrong_id_order = 0
        counter_wrong_start_id = 0
        frame_number = 0

        for frame_number in range (0,self.number_of_data_frames):
            id1, byte0, byte1,byte2,byte3 = self._read_id_and_bytes(frame_number)
            flag_unknown_id, flag_wrong_order, flag_wrong_start_id = self._check_id_ok(id1,frame_number)

            if flag_unknown_id:
                counter_unknown_ids = counter_unknown_ids + 1
            if flag_wrong_order:
                counter_wrong_id_order = counter_wrong_id_order + 1
            if flag_wrong_start_id:
                counter_wrong_start_id = counter_wrong_start_id + 1

        # Results
        print("Found {} unknown ids".format(counter_unknown_ids))
        print("Found {} wrong id order".format(counter_wrong_id_order))
        print("Found {} wrong start id".format(counter_wrong_start_id))
        print("Finished error checking byte file")
    def _calculate_byte_size_data_frame(self):
        """calculate the size of a data frame (id + values)"""

        if self.datatype_id == 'uint8_t':
            size_id = struct.calcsize('B')
        else:
            raise ValueError("have to be implemented")

        size_data_value = self.num_of_bytes
        size = size_id + size_data_value
        return size
    def _get_lists_of_ids_for_datatype(self):
        """Returns lists with the ids for datatypes with different number of bytes"""
        lst_2byte_dataframe = []
        lst_2x2byte_dataframe = []
        lst_2x2byte_dataframe_id1 = []
        lst_2x2byte_dataframe_id2 = []
        lst_4byte_dataframe = []

        for key in self.dict_ids.keys():
            if (self.num_of_bytes == 2):
                # check datatype
                if self.dict_ids[key]['datatype'] in ['int16', 'uint16']:
                    lst_2byte_dataframe.append(self.dict_ids[key]['id1'])

                elif self.dict_ids[key]['datatype'] in ['int32', 'uint32']:
                    lst_2x2byte_dataframe.append(self.dict_ids[key]['id1'])
                    lst_2x2byte_dataframe.append(self.dict_ids[key]['id2'])
                    lst_2x2byte_dataframe_id1.append(self.dict_ids[key]['id1'])
                    lst_2x2byte_dataframe_id2.append(self.dict_ids[key]['id2'])

            elif self.num_of_bytes == 4:
                lst_4byte_dataframe.append(self.dict_ids[key]['id1'])

        return lst_2byte_dataframe,lst_2x2byte_dataframe,lst_2x2byte_dataframe_id1, lst_2x2byte_dataframe_id2, lst_4byte_dataframe
    def _read_id_and_bytes(self, frame_number):
        """ returns id (uint8) and the 2 bytes in raw byte format """
        try:
            byteorder = 'big'
            id = struct.unpack_from('B', self.bytefile, frame_number * self.size_data_frame)[0]  # unsigned char
            byte0 = self.bytefile[(frame_number * self.size_data_frame) + 1].to_bytes(1, byteorder=byteorder)
            byte1 = self.bytefile[(frame_number * self.size_data_frame) + 2].to_bytes(1, byteorder=byteorder)
            if self.num_of_bytes == 4:
                byte2 = self.bytefile[(frame_number * self.size_data_frame) + 3].to_bytes(1, byteorder=byteorder)
                byte3 = self.bytefile[(frame_number * self.size_data_frame) + 4].to_bytes(1, byteorder=byteorder)
            else:
                byte2 = None
                byte3 = None
        except:
            id = None
            byte0 = 0
            byte1 = 0

        return id, byte0, byte1, byte2, byte3
    def deprecated_get_structured_output_data_regarding_to_highest_sampling_rate(self):
        """ Returns the structured output data. The data will be structured by id. The data with the different ids have
        most of the time different sampling rates, for time synchronization the id with the highest samplingrate
        is the reference for the time. The ids with lower sampling rate will have nan values at the timestamps where
        no data available
        Returns
        -------
        structured_output_data : numpy
            id_time   id_1    id_2  ...
            xx         inf      xx
            xx         xx       xx
            here the id_2 is the one with the highest sampling rate
        """
        print("start reading out the byte file and save it into numpy array ...")
        # create numpy array with nan values where the data can be inputed
        structured_output_data = np.full((self.num_of_ids, self.number_of_data_frames), fill_value=np.nan)
        counter_of_every_id = np.zeros(self.num_of_ids)
        frame_number = 0
        idx = 0
        while (idx < (len(self.bytefile) - 5)):
            current_byte = self._read_one_byte(idx)

            if current_byte in self.lst_all_ids:
                id = current_byte
                num_databytes = self.dict_ids[self.dict_id_to_key[id]]['bytes']
                lst_bytes = []
                for i in range(1, num_databytes + 1):
                    data_byte = self._read_one_byte(idx + i)
                    lst_bytes.append(data_byte)
                idx = idx + num_databytes

            id1, byte0, byte1, byte2, byte3 = self._read_id_and_bytes(frame_number)

            # check if id is for 2 or 4 bytes
            value_bytes = 0
            if id1 in self.lst_2byte_datatype:
                value_bytes = self.get_value_from_bytes(id1, byte0, byte1)

            elif id1 in self.lst_2x2byte_datatype:
                frame_number = frame_number + 1
                id2, byte2, byte3 = self._read_id_and_bytes(frame_number)
                if id2 in self.lst_2x2byte_datatype:
                    value_bytes = self.get_value_from_bytes(id1, byte0, byte1, byte2, byte3)

            if id1 in self.lst_4byte_dataframe:
                value_bytes = self.get_value_from_bytes(id1, byte0, byte1, byte2, byte3)

            if value_bytes is not None:
                # convert the id of the sensor data to an idx which can be used later in the numpy array
                idx = self.dict_id_to_idx[id1]

                # save at specified position (depending on the highest sampling rate)
                max_counter_id = counter_of_every_id.argmax()  # get
                max_counter_ids = np.array(
                    np.where(counter_of_every_id == np.amax(counter_of_every_id)))  # get all the ids with the max value
                max_counter_value = math.ceil(counter_of_every_id[max_counter_id])
                if idx in max_counter_ids:
                    # save at the next row in that array
                    structured_output_data[idx, max_counter_value] = value_bytes
                else:
                    # save at the same row in the array for this id
                    structured_output_data[idx, max(max_counter_value - 1, 0)] = value_bytes
                counter_of_every_id[idx] = counter_of_every_id[idx] + 1

            frame_number = frame_number + 1
        # cut the rest of the array away
        structured_output_data = structured_output_data[:, :max_counter_value]
        print("finished")
        return structured_output_data



# ---------------------------------------------------------------------------------------------------------------------
# Just for test
def byte_file_reader_test():
    dict_sensor_id = {'time': 2,
                      'sensor1': 25,
                      'sensor2': 7,
                      'sensor3': 9,
                      'sensor4': 0
                      }

    dict_sensor_data_1 = {'datatype' : 'uint32',
                          'endian': 'little',
                          'id1':0x75,
                          'id2':0x7A}


    byte_file_reader = ByteFileReader(file_path = 'test.bin',
                                      num_of_ids = 5,
                                      dict_ids=dict_sensor_id,
                                      datatype_id='uint8_t',
                                      datatype_data='int16_t')

    data = byte_file_reader.get_id_specific_data()
    print(data)

def create_dummy_byte_file():
    # config
    num_of_ids = 30
    num_samples = 1000

    ### creating bytes file ###
    ids = np.int8(np.random.randint(0, num_of_ids, (num_samples,)))
    msb = np.int8(np.random.randint(0, 255, (num_samples,)))
    lsb = np.int8(np.random.randint(0, 255, (num_samples,)))

    bytes_array = np.concatenate((ids, msb, lsb), axis=-1)
    bytes_array = np.stack((ids, msb, lsb), axis=-1)
    bytes_array_flatten = np.ndarray.flatten(bytes_array)

    write_byte = BytesIO(bytes_array_flatten)
    with open("test.bin", "wb") as f:
        f.write(write_byte.getbuffer())

if __name__ =='__main__':
    create_dummy_byte_file()
    byte_file_reader_test()