import numpy as np
#import librosa


def moving_window(signal, win_length, overlap):
    """ Generating overlapping windows of given length and with given overlap

    Parameters
    ----------
    signal
    win_length
    overlap : int
        Overlapt beteween two windows. Depending on the overlap, some values might be missing in the end, as
        there is no padding
        ..todo:: add padding

    Returns
    ----------
    windowed_signal

    Examples
    ----------
    >>> test_signal = np.arange(12)
    >>> windowed = moving_window(test_signal, win_length=6, overlap=3)
    >>> print(windowed.shape)
    (3, 6)
    >>> print(windowed[2])
    [ 6  7  8  9 10 11]


    ..todo:: win_number instead of overlap?
    """
    windowed_signal = np.lib.stride_tricks.sliding_window_view(signal, win_length)[::win_length - overlap]
    return windowed_signal


def linearization(values):
    """ TODO: deprecated? normaliozation does the same?
    """
    assert False, 'normaliozation does the same'
    min = np.min(values)
    max = np.max(values)
    norm_value_list = list()
    for v in values:
        norm_value_list.append((v-min) / (max-min))
    norm_values = np.array(norm_value_list)
    return norm_values


def flip(signal, mode=None, *args):
    """ Flipping a time series signal.

    If mode is 'mean', signal gets flipped along it's mean, to keep mean.
    Else signal gets flipped along 0-Axis.

    Parameters
    ----------
    signal :
    mode : int


    Returns
    -------

    >>> a = np.array([3,4,5,3,2,1])
    >>> flip(a, mode='mean')
    array([3., 2., 1., 3., 4., 5.])
    >>> flip(a, mode=None)
    array([-3, -4, -5, -3, -2, -1])
    """
    if mode == 0:
        print('Function was changes. Mode=0 is not flipping along mean anymore!')
    signal = np.array(signal)
    if mode == 'mean':
        mean = np.mean(signal)
        flipped_signal = -signal+2*mean
    else:
        flipped_signal = -signal
    return flipped_signal


def normalization(x):
    """ perform a min-max scaling as normalization
        Values after normalizing : {0 to 1}

        ! Seems to increase chance of overfitting in NNs

    x_new = (x - x_min)/ (x_max - x_min)

    Parameters
    ----------
    x : np.array

    Returns
    -------
    np.array
    """
    x_min = np.min(x)
    x_max = np.max(x)
    x_new = x
    # prevent divide by zero
    if (x_max - x_min) > 0:
        x_new = (x - x_min)/(x_max - x_min)
    return x_new


def nonzero_min(array):
    """ Set all values that are zero to the min value above zero.

    Parameters
    ----------
    array : np.array
        Input array
    Returns
    -------
    np.array
    """
    array[array == 0] = np.min(array[array > 0])
    return array


def normalize(x, n, unsigned=False):
    """

    Parameters
    ----------
    x : np.array
        input signal
    n : int
    unsigned : bool

    Returns
    -------

    """
    limit = pow(2, n)
    x_norm = np.clip(x, -limit, limit) / limit
    if unsigned:
        x_norm = x_norm + limit
    return x_norm


def quantize(x, num_val):
    """ Quantize signal
    Note that the float values in the function are not exact so a small epsilon value is added to compensate for this.
    This might result in an incorrect ouput, depending on the size of the input values (very unlikely though as epsilon
    is small).

    Parameters
    ----------
    x : np.array
        input signal
    num_val : int
        quantization steps
    Returns
    -------
    >>> x = np.arange(0, 1, 0.1)
    >>> print(x)
    [0.  0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9]
    >>> x_q = quantize(x, 4)
    >>> print(x_q)
    [0.   0.   0.25 0.25 0.5  0.5  0.5  0.75 0.75 1.  ]

    """

    # find quantisation levels
    max_ind = np.argmax(x)
    min_ind = np.argmin(x)
    diff_max_min = x[max_ind] - x[min_ind]
    # quantisation step size
    step_size = diff_max_min/num_val
    levels = list()
    max_level = x[min_ind]
    # float values are not exact, must add small epsilon to find all levels
    epsilon = step_size/1000
    while max_level <= (x[max_ind]+epsilon):
        levels.append(max_level)
        max_level += step_size

    quantised_array = list()
    for e in x:
        # find closest quantisation level and append to quantised_array
        quantised_array.append(min(levels, key=lambda some_level: abs(some_level-e)))

    return np.array(quantised_array, dtype=np.float32)

# Is this function needed ?
def simple_slicing(path, sr, duration):
    """ Split a signal into even nonoverlapping slices.

    Can be used for dataaugmentation.

    Parameters
    ----------
    path
    sr
    duration

    Returns
    -------

    """
    signal, sr = librosa.load(path, sr=sr)
    step = len(signal)/(sr*duration)
    l_slices = list()
    for n in range(int(step)):
        l_slices.append(signal[n*sr*duration:n*sr*duration+sr*duration])
    return l_slices


def mean_window(signal, win_size=10000, dtype=None):
    """ Calculate mean values for window.

    Can be used for downsampling.

    Parameters
    ----------
    signal : list(), np.array
        input signal
    win_size : int
        number of elements to calc mean on

    Returns
    -------
    windowed_mean : np.array
        Outputsignal

    Examples
    -------
    >>> signal = [2,3,4,5,9,1,4,6,8,3,5,7]
    >>> mean_window(signal, win_size=3)
    array([3., 5., 6., 5.])
    >>> mean_window(signal, win_size=4)
    array([3.5 , 5.  , 5.75])
    >>> mean_window(signal, win_size=4, dtype=int)
    array([3, 5, 5])
    >>> mean_window(np.array(signal), win_size=4)
    array([3.5 , 5.  , 5.75])

    """
    new_signal_length = int(np.floor(len(signal)/win_size))
    windowed_mean = np.zeros(new_signal_length)

    for n in range(new_signal_length):
        windowed_mean[n] = np.mean(signal[n*win_size:(n*win_size+win_size)])
    if dtype:
        windowed_mean = windowed_mean.astype(dtype)
    return windowed_mean


if __name__ == '__main__':
    values = [1,6,0,3,5,8,3,3,4,8,3,4,6,9]

    print(repr(normalize(values, 2, False)))
    print(repr(normalize(values, 8, False)))
    print(repr(normalize(values, 2, True)))
    print(repr(normalize(values, 8, True)))

    values = [1.2, 6.9, 0, 7.9, 5, 8.6, 3, 3, 4, 8, 3.5, 4, 6.3, 9.9, 3.4, 5.9]
    print(repr(normalize(values, 2, False)))
    print(repr(normalize(values, 8, False)))
    print(repr(normalize(values, 2, True)))
    print(repr(normalize(values, 8, True)))




