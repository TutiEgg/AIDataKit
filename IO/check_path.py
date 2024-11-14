"""
    ..todo: Function like unique_file_name but with appending date
"""
import os.path


def unique_file_name(path_to_file):
    """ Append an unique number to a path if there is a file with this name already

    Parameters
    ----------
    path_to_file : str, path

    Returns
    -------
    new_path : str, path
         new path to file

    """
    n = 0
    path_to_file = '{}_{}.{}'.format(path_to_file.split('.')[0], '0', *path_to_file.split('.')[1:])
    while os.path.exists(path_to_file):
        suffix_split = path_to_file.split('.')
        idx = suffix_split[0].rfind(str(n))
        if idx > 0:
            n_len = len(str(n))
            n = n + 1
            path_to_file = path_to_file[:idx] + str(n) + path_to_file[idx+n_len:]
        else:
            path_to_file = '{}_{}.{}'.format(suffix_split[0], str(n), *suffix_split[1:])
    return ''.join(path_to_file)


def main():
    print(unique_file_name(r'D:\AITADPython\KWS_AITAD\KWS_AITAD\Test_1.wav'))

    
if __name__ == '__main__':
    main()
