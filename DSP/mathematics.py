import math
import numpy as np
import numbers
from typing import Iterable, Union
import decimal

from scipy.stats import linregress  ## delete again if slope function wrong, if it works, add scipy to setup.py

from numpy.fft import fft, ifft, rfft


# ..todo:: functions for signalprocessing could / maybe should be able to deal with signals consisting of: tuple(time-values, values) - or equivilent functions should be added.


def timeseries_differential(signal, order=1):
    """ Diffenretial Function for discrete time series signal.

    .. deprecated:: diff_n_values replacing this function!

    Parameters
    ----------
    signal : np.array, list
        Signal for which to calc derivative.
    order : int
        How much to look into past.

    Returns
    -------
    diff : np.array, list
        Derivative of 'signal'.


    Examples
    -------
    >>> a = np.array([2,2,3,4,5,5,3,3,2,2])
    >>> timeseries_differential(a, order=1)
    array([ 0,  1,  1,  1,  0, -2,  0, -1,  0])
    >>> timeseries_differential(a, order=2)
    array([ 1,  2,  2,  1, -2, -2, -1, -1])
    """
    #raise DeprecationWarning('There is a function doing this and more - see: SWAI/DSP/mathematics/diff_n_values')
    #return 0
    diff = np.zeros_like(signal[:-order])
    for idx, elem in enumerate(signal[:-order]):
        diff[idx] = signal[idx + order] - elem

    # print('there is a function doing this and more - see: SWAI/DSP/mathematics/diff_n_values')

    return diff


def diff_n_values(signal: Iterable, windowsize: int = 3, symetrical: Union[bool, str] = "left",
                  padding=True, debugging=False) -> Iterable:
    """numerical first order differential: defaults to a windowsize of 3, and is calulated leftsided
    =>calculates for every value, starting at the value at index[windowsize], the difference between value[i]-value[i-windowsize]

    Parameters
    ----------
    padding: Union[bool, str, int]
        if and how to pad Data
    signal : Iterable
        list or np.array (the signal to be processed)
    windowsize : int
        the distance in amount of values to be seperated
    symetrical : bool, optional
        whether the calculation should be performed symetrical or in only one direction (True | right | left)

    Raises
    ------
    ValueError
        if n is not an integer
    NotImplementedError
        when trying to use padding - since this is still missing!

    >>> diff_n_values([0,1,2,3,4,5,6,7,8,9], windowsize=3, symetrical="left", padding = True, debugging = True)
    [0, 0, 2, 2, 2, 2, 2, 2, 2, 2]
    >>> diff_n_values([0,1,2,3,4,5,6,7,8,9], windowsize=2, symetrical="left", padding = True, debugging = True)
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    >>> diff_n_values([0,1,2,3,4,5,6,7,8,9], windowsize=-1, symetrical="left", padding = True, debugging = True)
    Traceback (most recent call last):
        ...
    ValueError: windowsize must be an positive integer greater than 0!

    >>> diff_n_values([0,1,2,3,4,5,6,7,8,9], windowsize=3, symetrical="left", padding = False, debugging = True)
    [2, 2, 2, 2, 2, 2, 2, 2]
    
    # >>> diff_n_values([0,1,2,3,4,5,6,7,8,9], windowsize=10, symetrical="left", padding = False, debugging = True)
    # 'WARNING: half-windowsize is bigger than signal length!'

    >>> diff_n_values([0,1,2,3,4,5,6,7,8,9], windowsize=5, symetrical="left", padding = False, debugging = True)
    [4, 4, 4, 4, 4, 4]
    
    """
    # type checks:
    if not isinstance(windowsize, int) or windowsize < 2:
        raise ValueError('windowsize must be an positive integer greater than 0!')
    if not isinstance(signal, Iterable):
        raise ValueError('signal must be an iterable!')
    if symetrical is True and (windowsize % 2 == 0):
        raise ValueError('if symmetrical, windowsize must be a uneven integer!')
    if isinstance(padding, str):
        raise NotImplementedError('Not jet implemented to call padding like "same" - feel free to add! ;)')
    if not (isinstance(padding, int) or isinstance(padding, bool) or isinstance(padding, float)):
        raise ValueError('Padding must be an int, float or bool!')
    
    # plausibility checks for windowsize:
    if len(signal)//2 < windowsize:
        raise Warning('WARNING: windowsize is bigger than half the signal length!')


    ## isn't the if check unnecessary as it always returns True for any of the values "left", "right", True? Could just directly decrease windowsize by 1. Or should it only be decreased if symmetrical is True (would make more sense)?
    if symetrical:
        #if debugging:
        #    print("windowsize adjusted...")
        windowsize -= 1 #correct windowsize for calculation of non-symetrical derifitives.So that if windowsize is set to 2, the differential will be calculated with only one additional value! 

    
    diff_signal = [0]*len(signal)
    if symetrical == True:
        for idx in range(windowsize//2 , len(signal)- (windowsize//2) ):
            diff_signal[idx] = signal[idx + (windowsize//2)] - signal[idx - (windowsize // 2)]
    elif symetrical in ["left", "l", "LEFT"]:
        for idx in range(windowsize, len(signal)):
            diff_signal[idx] = signal[idx] - signal[idx - windowsize]
    elif symetrical in ["right", "r", "RIGHT"]:
        for idx in range(len(signal) - windowsize):
            diff_signal[idx] = signal[idx + windowsize] - signal[idx]
    else:
        raise ValueError('symmetrical must either be [True,False,"left","right"]')
        
    if padding is False:
        if symetrical == True:
            diff_signal = diff_signal[windowsize//2 : -windowsize//2] 
        elif symetrical in ["left", "l", "LEFT"]:
            diff_signal = diff_signal[windowsize:]
        else:
            diff_signal = diff_signal[:windowsize]

    return diff_signal
    # print(f'len diff init: {len(diff_signal)}')

    # if symetrical is True:
    #     for idx, _ in enumerate(diff_signal): 
    #         diff_signal[idx] = (signal[idx + (windowsize // 2)] - signal[idx - (windowsize // 2)])
    #     return diff_signal
    # elif symetrical in ["left", "l", "LEFT"]:
    #     for idx, value in enumerate(diff_signal):
    #         diff_signal[idx + windowsize] = value - signal[idx]
    #     return diff_signal
    # elif symetrical in ["right", "r", "RIGHT"]:
    #     for idx, value in enumerate(signal:=(signal[:-windowsize])):
    #         diff_signal[idx] = signal[idx + windowsize] - value
    #     return diff_signal
    # else:
    #     raise ValueError('symmetrical must either be [True,False,"left","right"]')


def max_grad(signal: list, windowsize: int = 3, symetrical: Union[bool, str] = True) -> float:
    """Maximum Gradient, calculated symetrical or left / right with a given windowsize

    Parameters
    ----------
    signal: list
        list or list like with __get_item__() method
    windowsize: int
        window or distance of gradient operation
    symetrical: Union[bool, str]
        if and how to calculate differential (symetrical, left or right)

    Returns
    -------
    maximum_gradient: float

    """
    return np.max(diff_n_values(np.array(signal), windowsize=windowsize, symetrical=symetrical))


def min_grad(signal: list, windowsize: int = 3, symetrical: Union[bool, str] = True) -> float:
    """Minimal Gradient, calculated symetrical or left / right with a given windowsize

    Parameters
    ----------
    signal: list
        list or list like with __get_item__() method
    windowsize: int
        window or distance of gradient operation
    symetrical: Union[bool, str]
        if and how to calculate differential (symetrical, left or right)

    Returns
    -------
    minimum_gradient: float

    """
    return np.min(diff_n_values(signal, windowsize=windowsize, symetrical=symetrical))


def integral(signal: list, two_dim=False) -> float:
    """..todo:: should be compatable with 2D-signals: (time_values, values)
    integral of a given signal

    Parameters
    ----------
    signal: list or list like
        the signal the integral should be calulated of, 2D list if two_dim is True

    two-dim: boolean
        True if 2D-signal (time_values, values), False if 1D-signal (values), default: False

    Returns
    -------
    integral: float
        the calculated numerical integral (sum(values))/length(signal)

    >>> s = [0, 1, 2, 3, 4]
    >>> assert integral(s) == 10/5 # 2
    >>> s = [[2, 4, 6, 8, 10], [0.5, 1.0, 1.5, 2.0, 2.5]]
    >>> assert integral(s, two_dim=True) == 30/2 #15

    """
    if two_dim:
        time_values = signal[1]
        dt = time_values[len(list(time_values)) - 1] - time_values[0]
        return (np.sum(signal[0])) / dt
    else:
        dt = len(list(signal))
        return (np.sum(signal)) / dt

    #dt = len(list(signal))
    #return (np.sum(signal)) / dt


def local_min(signal, windo_size = None):
    """ Get local minima for discrete signal.

    All indizies are found, which have bigger direct neighbours!

    Parameters
    ----------
    signal : np.array
        input signal

    Returns
    -------

    """
    if windo_size is None:
        windo_size = 0
        
    index = list()
    for k in range(1 + windo_size//2, len(signal) - 1 - windo_size//2):
        ## shouldn't it be a strict inequality since function is looking indices with greater direct neighbours?
        if signal[k] <= signal[k + 1] and signal[k] <= signal[k - 1]:
            if index and index[-1] == (k - 1):
                index.pop()
            index.append(k)
    return index


def local_max(signal, windo_size = None):
    """ Get local maxima for discrete signal.

    All indices are found, which have smaller direct neighbours!

    Parameters
    ----------
    signal : np.array
      input signal

    Returns
    -------

    """
    index = list()
    for k in range(1, len(signal) - 1):
        ## shouldn't it be a strict inequality since function is looking indices with smaller direct neighbours?
        if signal[k] >= signal[k + 1] and signal[k] >= signal[k - 1]:
            index.append(k)
    return index


def absolute_max_difference(signal):
    return max(signal)-min(signal)


def relative_total_slope(signal: list) -> float:
    """dY/dX -> equivilant to total slope from first to last value (normalized by the signal length)

    Parameters
    ----------
    signal: list or list like
        signal to calculate the slope / relative difference of

    Returns
    -------
    relative difference (last-first)/signal_length

    >>> s=[0,1,2,3,4,5]
    >>> assert relative_total_slope(s) == 5/6

    """
    dY = signal[-1] - signal[0]
    dX = len(list(signal))
    return dY / dX


def slope(signal) -> float:
    """relative slope over complete Signal -> (signal[-1]-signal[0])/totalLengthofSignal

    Parameters
    ----------
    signal : list or list like with indices
        the signal to be processed

    Returns
    -------
    float
        the standard slope of the total signal

    .. todo::this function is actually the relative total slope defined above -> a general slope function should return something like the slope of the regression line!
    """
    #try:
     #   dY = (signal[-1] - signal[0])
      #  dX = len(list(signal))
       # return dY / dX
    #finally:
     #   raise DeprecationWarning('this function has been replaced by: relative_total_slope - to be more accurate! another function calculating the slope of the regression line should be implented!... ')


    ## is ind_list_correct or shoudl signal be 2D list? Or should in_list maybe start with 1 instead of 0?
    #ind_list = [i for i in range(len(signal))]
    #return linregress(ind_list, signal).slope
    assert False, "Test to see if function is still being used"


# Mathematical functions ==============================================================================================

def round_half_down(n, decimals=0):
    """
    Rounds a number up on *.6 and on *.5 down

    :param n:           number
    :param decimals:    Which decimal place is rounded to
    """
    multiplier_plus_1 = 10 ** (decimals+1)
    multiplier = 10 ** decimals
    deciding_decimal = int((str(math.floor(n*multiplier_plus_1)).split(".")[0])[-1])
    if deciding_decimal > 5:
        # round up
        return math.ceil(n*multiplier) / multiplier
    else:
        # round down
        return math.floor(n*multiplier) / multiplier


def round_down(n, decimals=0):
    """

    Parameters
    ----------
    n
    decimals

    Returns
    -------

    """
    multiplier = 10 ** decimals
    return math.floor(n * multiplier) / multiplier


def round_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.ceil(n * multiplier) / multiplier


def multiply_values(values, multiplier=1, round_format=None, round_digits=3, multi_dim=False):
    """

    .. todo:: change function so that it works for multidimensional list, right now only works for 2D list

    Rounds all numeric values in a multidimensional-list.
    if no round_format is given he will give the value back (with multiplier)
    round_format = Normal rounds the value round_digits
    Parameters
    ----------
    values
    multiplier
    round_format
    round_digits
    multi_dim: bool

    Returns
    -------

    """

    def multiply_value(value):
        if round_format == "down":
            return round_down(value, round_digits)
        elif round_format == "Up":
            return round_up(value, round_digits)
        elif round_format == "Normal":
            return round(value * multiplier, round_digits)
        else:
            return value * multiplier

    # Set New value/values
    if isinstance(values, np.ndarray) or isinstance(values, list):
        if multi_dim:
            new_value = list()
            for a_list in values:
                value_list = list()
                for v in a_list:
                    value_list.append(multiply_value(float(v)))
                new_value.append(value_list)
        else:
            new_value = list()
            for v in values:
                new_value.append(multiply_value(float(v)))
    elif isinstance(values, numbers.Number):
        new_value = multiply_value(values)
    else:
        print("[Error] wrong value-format: ", type(values))
        return

    return new_value





if __name__ == '__main__':
    # signal = [2, 3, 5, 1, 4, 6, 3, 6, 7, 3, 6, 3, 8, 5, 3, 4, 9, 3, 5, 8, 9, 6, 7]
    # print(timeseries_differential(signal))
    rundoctests = True
    if rundoctests:
        import doctest
        doctest.testmod()
    
    # print(diff_n_values([0,1,2,3,4,5,6,7,8,9]))


