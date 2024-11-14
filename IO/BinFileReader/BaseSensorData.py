import numpy as np
import copy
import scipy.io.wavfile as wavf
import pickle

class SensorDataBase:
    def __init__(self,
                sensorname,
                ):
        """
        Parameters
        ----------
        data : list
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
        for sublist in l_data:
            if type(sublist) == list:
                for item in sublist:
                    flat_list.append(item)
            else:
                flat_list.append(sublist)
        return flat_list

    def remove_none_values(self, data):
        """ Removes the none values of the data"""
        np_data = np.array(data)
        np_data = np_data[np.where(np_data != None)[0]]
        return np_data
    
    def dump_as_pickle(self, data, target_dir):
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



class SensorDataUltrasonic(SensorDataBase):
    def __init__(self, sensorname):
       super().__init__( sensorname)


    def convert_data_to_list():
       raise NotImplementedError

    def create_wave_file():
       raise NotImplementedError

    def correct_msb_error(self, l_ultrasonic_data):
        """ This funktion is to adapt the ultrasonic values when their is a 
        transmission problem of the ultrasonic values and the MSB of the data is corrupted
        For questions got to lambert or neuried """
    
        for i, elem in enumerate(l_ultrasonic_data):
            if type(elem) is list:
                for j, value in enumerate(elem):
                    if value < -1073741824: 
                        value += 2147483648
                    elif value > 1073741824:
                        value -= 2147483648 
                    l_ultrasonic_data[i][j] = value
        return l_ultrasonic_data

    def convert_to_wav_file(np_data, file_path='out.wav', sample_rate=192000):
        """converts data to a wave file which can bes aved somewhere
        Parameters
        ----------
        np_data : np.array
            one dimensional data of microfone or something like this
        file_path: string
            path where the file should be saved
        sample_rate: int
            sample rate of the the data. This is nedded for the conversion into wav file
        
        Returns
        -------
        """
        # create wave file
        wavf.write(file_path, sample_rate, np_data.astype(np.int32))
        print("saved .wav file to: {}".format(file_path))





class SensorDataTime(SensorDataBase):
    def __init__(self,  sensorname):
      super().__init__( sensorname)
    
    def check_datarates():
        pass

    def calc_abs_timestamps(self, l_timestamps, n_bytes_timestamp = 4):
        """ This functions calculates the timestamps by searching the timestamps in the list between the None values
         Based on the number of None values between two timestamps, it can be calculated at which time the 
         individual package arrived.
         
        Parameters
        ----------
        l_data : list
            list with the absolute timestamps [None, Noen,..., 21100,None,...]
        n_bytes_timestamp: int
            Number of bytes of the timestamp --> for calculation of timeroverflow

        Returns
        -------
        np_abs_time: np.array
            np array with all the abs tiemstamps inside
        l_steps: list
            steps between the packages --> coudl varriate because of low resolution timestamps
        
        """
        max_timer_value = 2**(n_bytes_timestamp*8) - 1


        np_timestamps = np.array(l_timestamps)
                
        np_idx_timestamps = np.where(np_timestamps != None)[0] # get idx where timestamps are in the list

        if np_idx_timestamps.shape[0] < 2:
            raise ValueError("There are less then 2 timestamps in the data, so no time")

        # create the relative timestamps
        np_abs_time = copy.deepcopy(np_timestamps)
        np_abs_time[0] = 0 # set first element to zero
        l_steps = []

        # For approximate the time until the first timestamp, approximate it by the scoond
        recieved_pkgs = np_idx_timestamps[1] - np_idx_timestamps[0]
        elapsed_time = np_timestamps[np_idx_timestamps[1]] - np_timestamps[np_idx_timestamps[0]]
        time_step = elapsed_time / recieved_pkgs
        for j in range(1, np_idx_timestamps[0]+1):
                np_abs_time[j] = np_abs_time[(j-1)] + time_step

        # for all the other timesteps
        for i in range(0, len(np_idx_timestamps)-1):
            recieved_pkgs = 0
            recieved_pkgs = np_idx_timestamps[i+1] - np_idx_timestamps[i]

            # calculated elapsed time
            if np_timestamps[np_idx_timestamps[i+1]] > np_timestamps[np_idx_timestamps[i]]:
                elapsed_time = np_timestamps[np_idx_timestamps[i+1]] - np_timestamps[np_idx_timestamps[i]]
            
            else:
                # overflow of the timer signal
                elapsed_time = max_timer_value - np_timestamps[np_idx_timestamps[i]]
                elapsed_time += np_timestamps[np_idx_timestamps[i + 1]] - 0

            time_step = elapsed_time / recieved_pkgs
            l_steps.append(time_step)
            # put the timesteps into the list
            for j in range(1, recieved_pkgs+1):
                np_abs_time[np_idx_timestamps[i] + j] = np_abs_time[np_idx_timestamps[i] + (j-1)] + time_step

        # for the rest of the data after the last timestamp
        for i in range(np_idx_timestamps[-1], len(np_abs_time)):
            if i >= 1:
                np_abs_time[i] = np_abs_time[i-1] + time_step
        
        return np_abs_time, l_steps
        
    