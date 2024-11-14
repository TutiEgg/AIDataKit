""" Scripts used by the GUI to read different Modeloutputs   """

import random
import serial
import time
import sys, inspect


class BaseReaderScript():
    """ Baseclass for Readerscripts.
        function reader has to be overwirtten!
        Global dict READERSCRIPT_DICT has to be fitted.

    """
    def __init__(self, origin):
        """ e.G. Load File or Serial

        Parameters
        ----------
        origin
        """
        pass

    def reader(self):
        """ Read Element from File or Serial.
            Add time.sleep if needed.

        Returns
        -------

        """
        raise NotImplementedError


class ScriptTest(BaseReaderScript):
    def __init__(self):
        pass

    def reader(self):
        string_list = ["1", "2", "3"]
        return '{}'.format(random.choice(string_list))


class FileReaderScript(BaseReaderScript):
    def __init__(self, origin):
        self.path = origin
        with open(self.path, 'r') as f:
            self.lines = f.read().splitlines()

    def reader(self):
        if self.lines:
            next = self.lines.pop(0)
            time.sleep(1)
            return next
        else:
            return None


class PressureSerial(BaseReaderScript):

    def __init__(self, origin):
        self.ser = serial.Serial()
        self.ser.baudrate = 115200

        self.ser.port = origin
        try:
            self.ser.close()
            print('Serial closed')
        except:
            print("Serial Port could not be closed, because it wasn't opened yet")
        self.ser.open()
        print('Serial opened')

    def reader(self):
        """ Reading pressure serial port from serial_port

            Reads the serial port and returns the state of the filter thanks to the data sent by the pressure sensor.

            Parameters
            ----------
            serial_port : String
                serial port to connect to

            Returns : int
                State of the filter
                0 = healthy
                1 = warning
                2 = used
                3 = error
            -------

            """
        # if not isinstance(serial_port, str):
        #    return 3

        while self.ser.in_waiting == 0:
            pass

        data = self.ser.read(1)

        if data == b'\xc0':
            return '0'
        elif data == b'\xc1':
            return '1'
        elif data == b'\xc2':
            return '2'
        else:
            return '3'


class KochenReader(BaseReaderScript):
    def __init__(self, origin):
        self.path = origin
        self.file = open(self.path, 'r')
        self.all_labels = {
            'preparation' : '1',
            'heat_water' : '2',
            'boiling' : '3',
            'add_noodles' : '4',
            'boiling_noodles' : '5',
            'downshift_4' : '6',
            'heating_pan' : '7',
            'heating_pattys' : '8',
            'noise' : '9'
        }

    def reader(self):
        line = self.file.readline()[:-1]
        if line == '':
            return None
        else:
            if line == 'label':
                line = self.file.readline()[:-1]
                return line
            else:
                line = self.file.readline()[:-1]
                return 'probability : ' + line


""" ADD NEW SCRIPTS BEFORE THIS PART !!! """

def _get_classes():
    classes = list()
    for name, obj in inspect.getmembers(sys.modules[__name__]):
        if inspect.isclass(obj):
            if obj.__name__ != 'BaseReaderScript':
                classes.append(obj)
    return classes


READERSCRIPT_LIST = _get_classes()

