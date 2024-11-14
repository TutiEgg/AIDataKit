from scipy import signal
import numpy as np
import statistics


def downsample_df(df, value, start_value=0):
    """

    Parameters
    ----------
    df :
    value : int : factor by which samplenumber of signal is reduced
    start_value :

    Returns
    -------

    """
    return df.iloc[start_value::value]


def downsample_dict(data_dict, value):
    key_list = list(data_dict.keys())
    downsampled_dict = dict()

    key_list_down = key_list[::value]
    for key in key_list_down:
        downsampled_dict[key] = data_dict[key]

    return downsampled_dict


def get_xy_of_dict(data_dict):
    """
    get x and y list out of dictionary

    Parameters
    ----------
    data_dict: Dicitonary

    Returns
    -------

    """
    y = list()
    x = list()
    for timestamps in data_dict.keys():
        #print(data_dict[timestamps], timestamps)
        x.append(timestamps)
        y.append(float(data_dict[timestamps]))
    return x, y


def butterworth_filter(y):
    """
        Calculate butterworth-filter-coeff and apply to inputsignal
        Can be used to reduce noise of a signal
    Parameters
    ----------
    y : array_like : input signal that gets filtered

    Returns
    -------
    Filtered version of input
    """
    b, a = signal.butter(5, 0.1)
    filtered_y = signal.filtfilt(b, a, y)
    return filtered_y


def get_averagelist_of_axis(ax, start=0, end=None):
    average_y = statistics.mean(ax[start:end])
    average_list = [average_y] * len(ax[start:end])
    return average_list

def normalize_signal(list_amplitude):
    """
    Normalizes (0 to 1) a list of amplitudes
    Parameters
    ----------
    list_amplitude

    Returns
    -------
    Normalized list of amplitudes
    """
    # Normalize
    norm_amplitude = np.linalg.norm(list_amplitude)
    print(norm_amplitude)
    list_amplitude_normalized = list_amplitude / norm_amplitude
    return list_amplitude_normalized

