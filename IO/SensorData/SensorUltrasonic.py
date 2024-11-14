import numpy as np

import scipy.io.wavfile as wavf

from SWAI.IO.SensorData.SensorDataBase import SensorDataBase

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