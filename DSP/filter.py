import math

import numpy as np


def hp_filter(signal, cuto_freq, sr):
    """ Highpass filter

    Parameters
    ----------
    signal : np.array
    cuto_freq : int
        frequenzy for cutoff
    sr : int
        samplerate

    Returns
    -------

    """
    x_fft = np.fft.rfft(signal)

    n = ((cuto_freq * x_fft.shape[0]) // sr)
    x_fft[:n] = x_fft[:n] * 0
    x_i_filt = np.fft.irfft(x_fft)

    return x_i_filt


def lp_filter(signal, cuto_freq, sr):
    """ Lowpass filter

    Parameters
    ----------
    signal : np.array
    cuto_freq : int
        frequenzy for cutoff
    sr : int
        samplerate

    Returns
    -------

    """
    x_fft = np.fft.rfft(signal)

    n = ((cuto_freq * x_fft.shape[0]) // sr)
    x_fft[n:] = x_fft[n:] * 0
    x_i_filt = np.fft.irfft(x_fft)

    return x_i_filt


def moving_average_filter(signal, windowsize, stepsize= 1, pad=False, pad_width= 1, pad_value= 0,):
    """ 1-D moving average filter

    Parameters
    ----------
    signal : list, np.array
    windowsize : int
    stepsize : int
    pad : bool
    pad_width : int
    pad_value : float

    Returns
    -------
    array/list: signal where average moving filter with windowsize and stepsize has been applied.
                The input signal can be padded with a given value and padding width before calculation.

    Examples
    -------
    >>> signal = np.array((0,2,2,4,4,4,4,5,5,6,7,7,8))
    >>> m_avg = moving_average_filter(signal, 5)
    >>> print(m_av
    [1.3333334 2.        2.4       3.2       3.6       4.2       4.4
     4.8       5.4       6.        6.6       7.        7.3333335]
    >>> signal = np.array((0,2,2,4,4,4,4,5,5,6,7,7,8))
    >>> m_avg = moving_average_filter(signal, windowsize=5, stepsize=2)
    >>> print(m_avg)
    [2.4 3.6 4.4 5.4 6.6 7.5 8. ]
    >>> signal = np.array((0,2,2,4,4,4,4,5,5,6,7,7,8))
    >>> m_avg = moving_average_filter(signal, windowsize=5, pad= True, pad_width= 2, pad_value= 0)
    >>> print(m_avg)
    [0.        0.5       0.8       1.6       2.4       3.2       3.6
     4.2       4.4       4.8       5.4       6.        6.6       5.6
     4.4       3.75      2.6666667]


    """
    if isinstance(signal, list):
        signal = np.array(signal)
    if pad:
        pad = np.array([pad_value] * pad_width)
        signal = np.append(pad, np.append(signal, pad))
    # ..todo: check if there is a more "pythonic" and simpler way - maybe with np.convolute()?
    if stepsize == 1:
        lower = int(np.floor(windowsize / 2))
        upper = int(np.ceil(windowsize / 2))
        moving_mean = np.zeros_like(signal, dtype=np.float32)
        for i in range(len(signal)):
            if lower > i:
                low = i
            else:
                low = lower
            if i > len(signal) - upper:
                up = len(signal) - i
            else:
                up = upper
            moving_mean[i] = np.mean(signal[i - low:i + up], dtype=np.float32)
        return moving_mean
    else:
        lower = 0
        upper = windowsize
        size = int(np.ceil(len(signal) / stepsize))
        x = signal[-1]
        while len(signal) % size != 0:
            signal = np.insert(signal, len(signal), x)
        moving_mean = np.zeros(size, dtype=np.float32)
        for i in range(size):
            moving_mean[i] = np.mean(signal[lower:upper], dtype=np.float32)
            lower += stepsize
            upper += stepsize
        return moving_mean


def downsampling(data, number_samples):
    """
    Down sampling of the data to a max given amount of samples
    Parameters
    ----------
    data : numpy
        array which provides the samples in second dimension
    number_samples : int
        max number of samples should be returned

    Returns
    Array with the max amount or less samples
    -------

    """
    step_size = math.ceil(data.shape[1] / number_samples)
    if step_size == 0:
        step_size = 1
    downsampled_data = data[:,0::step_size]

    return downsampled_data

