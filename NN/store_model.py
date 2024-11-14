import glob
import os
from tensorflow import keras

def get_best_ckpt(log_dir):
    """
        Return best ckpt from log_dir of a trained model

    Parameters
    ----------
    log_dir : str or Path
        path to directory where log files are stored

    Returns
    -------
    best_ckpt : Path
        Path to hdf5 file with best metric
    """
    ckpt_path = os.path.join(log_dir, 'ckpt/*.hdf5')
    ckpt_files = glob.glob(ckpt_path)
    best_ckpt = 'weights.000-99.99.hdf5'
    best_epoch = 0
    for hdf5 in ckpt_files:
        epoch_info = int(os.path.basename(hdf5).split('.')[1].split('-')[0])
        if best_epoch <= epoch_info:
            best_ckpt = hdf5
            best_epoch = epoch_info
    return(best_ckpt)


def store_best_model(path, replace=True):
    """
        ..todo:: check if modelfile exists and if it is .h5, .hdf5 or .keras

    Parameters
    ----------
    path : path, str
        Path to directory that includes model.h5
    replace : bool
        replace current model.h5 or generate new

    Returns
    -------

    """
    model = keras.models.load_model(path + 'model.keras')
    model.load_weights(get_best_ckpt(path))
    if replace:
        model.save(os.path.join(path, 'model.keras'))
    else:
        model.save(os.path.join(path, 'model_best.keras'))
    print('model stored!')

if __name__ == '__main__':
    store_best_model(r'R:AITADPython\KWS_AITAD\KWS_AITAD\NN\model_logs\2022_03_23_114733_CNN_nnom_R_nnomMFCC\\')