"""
This file is for reading in serial data and dump the data in an binary file
"""
import threading
import time
import serial
import os


def dump_serial_data(port, target_dir, file_name,baudrate=115200):
    """
    This function is for starting a serial connection and dump all the data into a bin file.
    The function will run until keyboard interrupt

    Parameters
    ----------
    port : str
        port for the serial conenction e.g. COM5
    baudrate : int
        baudrate for the connection
    target_dir : path
        path to the target dir
    file_name: str
        name of the file which will be dumped
    Returns
    -------

    """
    print("start serial connection...")
    serial_connection = serial.Serial(port, baudrate)

    file_name += '.bin'
    file_path = os.path.join(target_dir,file_name)
    print("saving file to: ", file_path)

    binary_file = open(file_path, "wb")
    startTime = time.time_ns()

    print(" start reading serial prot ...")
    buffer_size = 0
    try:
        while 1:
            binary_file.write(serial_connection.read())

            buffer_size += 1
            # flush clear the intern created buffer of the file
            if buffer_size > 5000:
                buffer_size = 0
                binary_file.flush()

    except KeyboardInterrupt:
        elapsedTime = time.time_ns() - startTime
        print(f"elapsed time since start {elapsedTime} ns > {elapsedTime/10e8}")
        binary_file.close()
