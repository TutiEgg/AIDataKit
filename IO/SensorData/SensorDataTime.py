import numpy as np
import copy

from SWAI.IO.SensorData.SensorDataBase import SensorDataBase


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
        for j in range(1, np_idx_timestamps[0] + 1):
            np_abs_time[j] = np_abs_time[(j-1)] + time_step

        # for all the other timesteps
        for i in range(0, len(np_idx_timestamps)-  1):
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
        
        #np_abs_time = np.around(np_abs_time,decimals=3)

        return np_abs_time, l_steps