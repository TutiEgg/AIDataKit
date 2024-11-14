# Module fro preprocessing multidimensional array data
import numpy as np
from typing import Tuple
import random
import warnings

def get_random_cut(data: np.ndarray, cut_length: int, axis=0)->np.ndarray:
    """function to generate random cut out of np.ndarray on given axis

    Parameters
    ----------
    data : np.ndarray
        data to be cut
    cut_length : int
        length the resulting cut should be
    axis: int
        define where the cut should be done

    Returns
    -------
    np.array
        cutted data array
    """


    # check if data is np.array
    if not isinstance(data, np.ndarray):
        Warning('best use ndarray as input!')
        data = np.array(data)
    # get shape of data
    data_shape = data.shape
    if max(data_shape) <= cut_length :
        data = data[:]
        warnings.warn(f'can\'t produce cut for data with shape {data_shape}, with length {cut_length}\nData was passed through unchanged')
    else:  
        #make random cut -> index from where to start cut => max(data_shape)-1 -cut_length
        max_start_index = max(data_shape) - cut_length
        # draw random in between 0 and max_start_index
        start_index = np.random.randint(0,max_start_index)

        if axis == 0:
            data = data[start_index:start_index+cut_length]
        elif axis == 1:
            data = data[:,start_index:start_index+cut_length]
        elif axis == 2:
            data = data[:,:,start_index:start_index+cut_length]
        
        else:
            print("axis {} is not implemented".format(axis))

    return data


def add_relative_noise(data:np.ndarray, probability:float = 0.9, max_scale_factor:float = 1, axis:int = 0, modus:str = "std")->np.ndarray:
    """Scale np.ndarray relative to the standard deviasion of axis

    Parameters
    ----------
    data : np.ndarray
        data array to be scaled
    probability: float
        [0,1] Probability how often noise is added to the data signal
    max_scale_factor: float
        [0,x] max factor with which is the standard deviation of each axis scaled, under 1 is ok,
        over 1 it will be very noisy
    axis : int
        axis over which the standard deviation should be calculated
    
    Returns
    -------
    np.ndarray
        noisy data
    """
    # check if data is np.array
    if not isinstance(data, np.ndarray):
        Warning('best use ndarray as input!')
        data = np.array(data)

    if modus != "std":
        raise NotImplementedError('as for now only for std implemented... feel free to change')

    # get the scale factor of noise also randomly
    scale_factor = random.uniform(0, max_scale_factor)

    if random.uniform(0,1) < probability:
        data_random = (np.random.random(data.shape) - 0.5) * 2 # an array with same shape and random valus between [-1, 1]
        data_std = np.std(data, axis=axis)
        noise = data_random * data_std * scale_factor # scale std deviation by scale factor
        result_data_array = data + noise
    else:
        result_data_array = data
    
    return result_data_array


def random_peaks_in_signal(data:np.ndarray,probability=0.2, max_prob_error=0.01, scale_factor_max=5,axis=0):
    """
    This function is for adding random peaks in the signal depending on the scale factor,
    probability and the standard deviation
    Parameters
    ----------
    data : np.ndarray
        input data
    probability=0.2:
        probability that this augmentation is done
    max_prob_error : float
        the max probability that an peak is added at one specific point
    scale_factor_max : float
        this is the max scale factor for a peak
    axis: int
        axis along the standard deviation is computed

    Returns
    -------
    data_random_error : np.ndarray
        data + peaks

    """
    if random.uniform(0,1) < probability:
        # get random values between the specified max values
        prob_error = random.uniform(0, max_prob_error)
        scale_factor = random.uniform(0,scale_factor_max)
        data_std = np.mean(np.std(data, axis=axis))

        # create an array with some random values
        # The threshold if they are set to one are indicated by the probability defined before
        data_random_values = 2 * np.random.random(data.shape) - 0.5 # scale random value to [-1,1]

        # get the idx for the peaks
        data_idx_errors = np.random.random(data.shape)
        data_idx_errors[data_idx_errors < prob_error] = 1
        data_idx_errors[data_idx_errors < 1] = 0

        noise_values = data_idx_errors * data_random_values * scale_factor * data_std
        data_random_error = data + noise_values
    else:
        data_random_error = data

    return data_random_error


def mirror_data_at_mean_value(data,probability=0.5, axis=0):
    """
    Mirrors the data at the mean value of the signal
    Parameters
    ----------
    data : np.ndarray
        input data
    probability: probability that the signal is mirrored

    Returns
    -------
    mirrored signal
    """
    if random.uniform(0,1) < probability:
        mean_axis = np.mean(data, axis=axis)
        data_mirrored = (-1 * (data - mean_axis)) + mean_axis
    else:
        data_mirrored = data

    return data_mirrored

def exchange_two_axis(data, axis1, axis2, probabilty=0.3):
    """
    exchange two axis in vibration data if it is sensefull, no information the direction
    Parameters
    ----------
    data
    axis1
    axis2
    probability

    Returns
    -------

    """
    if random.uniform(0,1) < probabilty:
        temp_axis1 = np.copy(data[:, axis1])
        data[:, axis1] = data[:, axis2]
        data[:, axis2] = temp_axis1

    return data


def min_max_scale_data(data: np.ndarray, feature_range = (0,1), axis: int=None) -> np.ndarray:
    """scales data to a given range (scales whole dat -> or over an axis!!!)
    use axis = 0 to scale each column (feature vector)

    Parameters
    ----------
    data : np.ndarray
        
    feature_range : tuple, optional
        range to scale data to, by default (0,1)

    axis : int, optional
        axis to scale data to, by default None (means it scales over complete data!)

    Returns
    -------
    np.ndarray
        scaled data
    """
    X = data+ 1e-15
    X_std = (X - X.min(axis=axis)) / (X.max(axis=axis) - X.min(axis=axis))
    X_scaled = X_std * (max(feature_range) - min(feature_range)) + min(feature_range)
    return X_scaled


def log_scale_data(data: np.ndarray) -> np.ndarray:
    """log scale data, input have to be positive

    Parameters
    ----------
    data : np.ndarray

    Returns
    -------
    np.ndarray
        
    """
    X = data + 1 # np.abs(np.min(data))*2 # offset data by adding double the abs of the total min of array
    # -> no negative and no extrem small values near 0 which behave strange 
    X_scaled = np.log(X)
    return X_scaled


def min_max_log_scale(data:np.ndarray, feature_range:tuple = (0,1), axis: int =None) -> np.ndarray:
    """wrapper function to combined log + minmax scaling of multidimenional array 
    -> first apply log_scale_data
    -> than apply min_max_scale_data to result

    Parameters
    ----------
    data : np.ndarray
        
    feature_range : tuple, optional
        range to scale data to, by default (0,1)

    axis : int, optional
        axis to scale data to, by default None (means it scales over complete data!), by default None

    Returns
    -------
    np.ndarray
        
    """
    l_scaled_data = log_scale_data(data)
    mm_scaled_data = min_max_scale_data(l_scaled_data, feature_range=feature_range, axis=axis)
    return mm_scaled_data


def add_random_offset_relative_to(data:np.ndarray, percentage:float=0.1, reference:str ="std", axis:int = None)->np.ndarray:
    """adds an offset to an data array, relative to the chosen reference e.g. std (standard deviation), mean, median...

    Parameters
    ----------
    data : np.ndarray
        
    percentage : float, optional
        percentage of the reference value to add to, by default 0.1

    reference : str, optional
        the value the offset should be referenced to, by default "std"
    
    axis: int, optional
        the axis, the referenceshould be taken from, default None

    Returns
    -------
    np.ndarray
        
    """
    if reference != "std":
        raise NotImplementedError("Currently only std is implemented!")
    else:    
        # calc std of data
        std = np.std(data, axis=axis)
        return data + (std*percentage * np.random.randint(-100,100, size=(data.shape))/100)

def cut_stectrum_byindx(spectrum: np.ndarray, offsets: Tuple[int,int], window_dim: Tuple[int,int])->np.ndarray:
    """function to cut a 2d_spectrogram (along both axis) (like a slice of an image)

    Parameters
    ----------
    spectrum : np.ndarray
        contains full spectrogram [freqs, times, values]
    offsets : Tuple[int,int]
        (freqs offset from origin, time offset from origin) both as indices!!!
    window_dim : Tuple[int,int]
        (window width in freq axis, window width in time axis) both as indices!!!
        -> if you would like to cut to the end, need to put in the length of the respective axis.

    Returns
    -------
    np.ndarray
        cut spectrogram
    """
    return (spectrum[0][offsets[0]:offsets[0]+window_dim[0]], spectrum[1][offsets[1]:offsets[1]+window_dim[1]], spectrum[2][offsets[0]:offsets[0]+window_dim[0], offsets[1]:offsets[1]+window_dim[1]])

def cut_spectrum_byvalue(spectrum: np.ndarray, offsets: Tuple[float,float], window_dim: Tuple[float,float])->np.ndarray:
    """function to cut a 2d_spectrogram (along both axis) (like a slice of an image)

    Parameters
    ----------
    spectrum : np.ndarray
        contains full spectrogram [freqs, times, values]
    offsets : Tuple[float,float]
        (freqs offset from origin, time offset from origin) both as values!!!
    window_dim : Tuple[float,float]
        (window width in freq axis, window width in time axis) both as values!!!
        
    Returns
    -------
    np.ndarray
        cut spectrogram
    """
    # find the fitting index for both values:
    freq_offset_indx = np.argmax(spectrum[0]>=offsets[0])
    time_offset_indx = np.argmax(spectrum[1]>=offsets[1])
    print(f'calculated indx values for offsets {freq_offset_indx=} {time_offset_indx=}')
    freq_sampling_rate = spectrum[0][1]-spectrum[0][0]
    freq_window_width_as_indx = int(window_dim[0] / freq_sampling_rate)
    print('calculated freq rate and window as index')
    time_sampling_rate = spectrum[1][1] - spectrum[1][0]
    time_window_width_as_indx = int(  window_dim[1] / time_sampling_rate) 
    print(f'calculated time rate and window indx {freq_window_width_as_indx=} {time_window_width_as_indx=}')
    return cut_stectrum_byindx(spectrum, (freq_offset_indx, time_offset_indx), (freq_window_width_as_indx, time_window_width_as_indx))

def cut_spectrum_by_abs_values(spectrum: np.ndarray, freq_bin: Tuple[float,float], time_bin: Tuple[float,float])->np.ndarray:
    """function to cut a 2d_spectrogram (along both axis) (like a slice of an image)

    Parameters
    ----------
    spectrum : np.ndarray
        contains full spectrogram [freqs, times, values]
    freq_bin : Tuple[float,float]
        (freqs to start cut, freq to end cut) both as values!!!
    time_bin : Tuple[float,float]
        (time to start cut, time to end cut) both as values!!!
        
    Returns
    -------
    np.ndarray
        cut spectrogram
    """
    # find fitting indexes for values: 
    freq_start_indx = np.argmax(spectrum[0]>=freq_bin[0])
    freq_end_indx = np.argmax(spectrum[0]>=freq_bin[1])
    time_start_indx = np.argmax(spectrum[1]>=time_bin[0])
    time_end_indx = np.argmax(spectrum[1]>=time_bin[1])
    return (spectrum[0][freq_start_indx:freq_end_indx], spectrum[1][time_start_indx:time_end_indx],spectrum[2][freq_start_indx:freq_end_indx, time_start_indx:time_end_indx])


def moving_average(data: np.ndarray, kernel_size:int = 100):
    """ This functions calculates the moving average over a 1D signal"""
    kernel = np.ones(kernel_size) / kernel_size
    data_ma = np.convolve(data, kernel)
    return data_ma


def weighted_moving_average(data: np.ndarray, kernel:np.ndarray = None):
    """ This functions calculates the weighted moving average over a 1D signal"""
    kernel = np.array([1,1,1,1,1,2,2,2,2,3,3,3,4,4,5,4,4,3,3,3,2,2,2,2,1,1,1,1,1])
    kernel = kernel/kernel.sum()
    data_ma = np.convolve(data, kernel)
    return data_ma


def ts_sum_i16(array):
    """ Multidimensional Timeseries Summation - Vibration

    Reducing multidimensional data into single dimension.
    Removing mean from each axis and than summin along all axis.

    Good use for Vibration data to get a singeldimensional array and remove varianz by rotation.

    Parameters
    ----------
    array : np.ndarray
        input array

    Returns
    -------
    preproc : np.ndarray
        resulting array
    """
    #preproc = np.sum(np.abs(np.subtract(array, np.mean(array, axis=1)[:, None])), axis=0, dtype=np.int16)[:, None]
    preproc = np.sum((np.subtract(array, np.mean(array, axis=1)[:, None])), axis=0, dtype=np.int16)[:, None]
    return preproc