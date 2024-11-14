
class OwnDatatypes:
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
        """
        d_u32_le_n64= {
                        'type':     'int',
                        'signed':   True,
                        'bytes':    4,
                        'endian':   'little',
                        'num_values': 64 
                        }

        d_u32_le_n256= {
                        'type':     'int',
                        'signed':   True,
                        'bytes':    4,
                        'endian':   'little',
                        'num_values': 256 
                        }
        
    
