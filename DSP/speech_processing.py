""" Functions for processing audio and speech signals.

"""
import numpy as np

from filter import moving_average_filter as mavg


def vad_mavg(signal, threshold=0.50, offset_len=16000):
    """ Voice Activity Detection (VAD) by Moving average filter (mavg)

    This VAD is specialised for detecting a single spoken word in a recording without to much noise around.
    This function might not always work perfectly.
    Without `offset_len` the VAD might cut of the first and last samples from the actual voice.


    Parameters
    ----------
    signal : list, np.array
        1-D input speech signal
    threshold : float
        Value between 0-1 to define threshold for VAD.
    offset_len : int
        Length of signal after applying offset

    Returns
    -------
    vad : np.array
         cutted signal containing the detected speech

    .. todo:: what happens if actual voice length > offset length
    .. todo:: Dynamic threshold, inc. while vad_len > offset_len
    .. todo:: for pytests ask for a speech recording and add it to the pytest folders. Load it and apply the vad_mavg.

    """
    vad = np.zeros_like(signal)
    mvag = mavg(np.abs(signal), windowsize=5000) #5000
    threshold_value = np.max(mvag) * threshold
    vad[mvag > threshold_value] = 1
    vad_min = np.min(np.where(vad == 1))
    vad_max = np.max(np.where(vad == 1))
    vad_len = vad_max - vad_min
    offset_min = np.clip(int(np.ceil((offset_len - vad_len) / 2)), a_min=0, a_max=len(signal))
    offset_max = np.clip(int(np.floor((offset_len - vad_len) / 2)), a_min=0, a_max=len(signal))

    vad_off_min = np.clip(vad_min - offset_min, a_min=0, a_max=len(signal))
    vad_off_max = np.clip(vad_max + offset_max, a_min=0, a_max=len(signal))

    vad[vad_off_min:vad_off_max] = 1

    return vad

if __name__ == '__main__':
    signal = [2,3,5,9,6,7]
    print(vad_mavg(signal, threshold=0.1))