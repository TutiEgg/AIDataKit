
class StdDatatypes:
        """ 
        This class hold the definition of standard datatypes of data 
        which is transmitted and saved in a bin file
        Here are all possible datatypes specified to simplify later the specification of a package

        definition of standard datatypes
        d_u8 = {
                'type':    'int','float',
                'signed':   True,False
                'bytes':    number of bytes
                'endian':   'big','little'
                'num_values' :number of values repeating
                },
        --> if there are more values needed then 1 define the datatype in the other class OwnDatatypes
        """
   
        d_u8 = {
                        'type':    'int',
                        'signed':   False,
                        'bytes':    1,
                        'endian':   'big',
                        'num_values':1
                        }

        d_s8 = {
                        'type':    'int',
                        'signed':   False,
                        'bytes':    1,
                        'endian':   'big',
                        'num_values':1
                        }

        d_s16_le ={
                        'type':    'int',
                        'signed':  True,
                        'bytes':    2,
                        'endian':   'little',
                        'num_values':1
                        }

        d_u16_le ={
                        'type':    'int',
                        'signed':  False,
                        'bytes':    2,
                        'endian':   'little',
                        'num_values':1
                        }

        d_s16_be ={
                        'type':    'int',
                        'signed':  True,
                        'bytes':    2,
                        'endian':   'big',
                        'num_values':1
                        }

        d_u16_be ={
                        'type':    'int',
                        'signed':  False,
                        'bytes':    2,
                        'endian':   'big',
                        'num_values':1
                        }

        d_s24_le ={
                        'type':    'int',
                        'signed':  True,
                        'bytes':    3,
                        'endian':   'little',
                        'num_values':1
                        }

        d_s24_be ={
                        'type':    'int',
                        'signed':  True,
                        'bytes':    3,
                        'endian':   'big',
                        'num_values':1
                        }

        d_s32_le ={
                        'type':    'int',
                        'signed':  True,
                        'bytes':    4,
                        'endian':   'little',
                        'num_values':1
                        }

        d_u32_le ={
                        'type':    'int',
                        'signed':  False,
                        'bytes':    4,
                        'endian':   'little',
                        'num_values':1
                        }

        d_s32_be ={
                        'type':    'int',
                        'signed':  True,
                        'bytes':    4,
                        'endian':   'big',
                        'num_values':1
                        }

        d_u32_be ={
                        'type':    'int',
                        'signed':  False,
                        'bytes':    4,
                        'endian':   'big',
                        'num_values':1
                        }