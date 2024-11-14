import serial
import time
from io import BytesIO


def streamer(path, seconds = 30, port = 'COM4', baudrate = '115200'):
    """
    The function collects the serial data coming from the sensor for the amount of time specified in seconds and
    writes it on the file for which the path is given.

    Parameters
    ----------
    path: string
        Path of the file data is written in for data collection.
    seconds: int
        Time in seconds to run the program for data collection.
    port: string
        Communication port of the system for serial data communication, each system has its own port
        for it and needs to be changed according to the system, check in Device Manager under Ports(COM & LPT) after
        connecting the usb cable connected to the board with the system.
    baudrate: string
        The rate at which the data is being communicated, for this the maximum is selected.

    Returns
    -------
    None

    """
    ser = serial.Serial(
        port=port,
        baudrate=baudrate,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=0)
    ser.close()
    ser.open()
    ser.flushInput()  # aktuellen Inputbuffer leeren


    data = b''
    t0 = time.time()
    rec_seconds = 0
    while (rec_seconds<seconds):
        bytesToRead = ser.readline()
        print(bytesToRead)
        data += (bytesToRead)
        t1 = time.time()
        rec_seconds = t1 - t0
    ser.close()

    write_byte = BytesIO(data)
    with open(path, "wb") as f:
        f.write(write_byte.getbuffer())


def main():
    streamer(r"C:\Users\yc7mcor5\Desktop\Hummel_projekt_pre\back_idleGas_no_test.bin")


if __name__ == "__main__":
    main()