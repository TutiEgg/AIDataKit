import re
# from SWAI.IO.BinFileReader.PackageReader import PackageReader

# todo implementation
# - no footer needed
# - felxible size of the data package

class BaseDataPackage():
    """
    This class is for handling packages of the type:
    header | data | footer
    header | data
    Therefore regularexpression are created, ...
    """
    def __init__(self,
                 sensorname: str,
                 sensor_type: str,
                 package_header: list,
                 num_bytes_header: int,
                 num_bytes_data: int,
                 num_bytes_package: int,
                 package_footer:list = None,
                 num_bytes_footer: int= None,
                 ):
        """ 
        Intilization function for the DataPackage

        Parameters
        ----------
        d_package_vals : dict
            In this dict all the values of the data package have to be defined in the following way:
            e.g.
            d_package_values = {'temp': {
                                        'type':     'float'
                                        'signed':   True
                                        'bytes':    4,
                                        'endian':   'big',
                                        },
                                'X':    {
                                        'type':     'int',
                                        'signed':   True
                                        'bytes':    3,
                                        'endian':   'big',
                                }
            type could be int, float have to be implemented

        sensorname: str
            name of the sensor    
        sensor_type: str
            type of the sensor eg. vibration
        package_header: list
            list with the possible header for the package
            Use double backslash '\\' , for example 0x24 is a $
            and a $ will do something different for the regular expression
            --> therefore use double backslash
            eg. [b'\\xAD\\xAF',...]
        package_footer: list,
            list with the possible footer for the package
            eg. [b'\\x0D\\x0A',...]
        num_bytes_data: int
            number of bytes of the header
        num_bytes_data: int
            number of bytes of the transmitted data
        num_bytes_data: int
            number of bytes of the footer
        num_bytes_package: int
            size of the whole package: header + data + footer = package_size_bytes
        Returns
        -------
        bool
        """
        self.num_values = 0 
        self.sensorname = sensorname
        self.sensor_type = sensor_type
        self.package_header = package_header
        self.package_footer = package_footer
        self.num_bytes_header = num_bytes_header
        self.num_bytes_footer = num_bytes_footer 
        self.num_bytes_data = num_bytes_data
        self.num_bytes_package = num_bytes_package

        self.l_reg_ex = self._get_reg_ex() # list with all regular expression objects for searching the packages in the data

    def _check_input_parameters(self):
        """ Check all the given input parameters if they are ok
            Parameters
            ----------

            Returns
            -------
        """
        # todo: check the parameter if everything fits together
    
    def _get_reg_ex(self):
        """
        This functions is for internal use to create all the regular expressions
        in format header|data|footer or header|data 
        Returns
        -------
        l_reg_ex: list
            including all regular expressions objects
        """
        l_reg_ex = []
        for header in self.package_header:
            if self.package_footer is not None:
                for footer in self.package_footer:
                    l_reg_ex.append(self.create_single_reg_ex(header=header,
                                            data_size=self.num_bytes_data,
                                            footer=footer,
                                            flags=re.DOTALL))
            else:
                l_reg_ex.append(self.create_single_reg_ex(header=header,
                                        data_size=self.num_bytes_data,
                                        flags=re.DOTALL))

        return l_reg_ex
    
    def check_reg_ex(self, data, start_pos: int):
        """
        This function is for checking all the regular expressions 
        on the data at the current start position

        Parameters
        ----------
        data : string, bytes
            the data which should be checked
        pos: int
            current index in the data, from here the searching will start

        Returns
        -------
        bool
            if reg_ex fits True else False
            
        """
        endpos = start_pos + self.num_bytes_package # so only one check is possible
        for reg_ex in self.l_reg_ex:
            match = reg_ex.search(data, start_pos, endpos)
           
            if match:
                return True
        
        return False
    
    def get_data_from_package(self):
        """
            Have to be overwritten
        """
        pass



    def create_single_reg_ex(self, header: bytes, data_size: int, footer: bytes=None, flags=None):
        """ 
        This function is for creating a single reg_expression for the Data Package 
        out of header, data_size and footer
        Parameters
        ---------
        header : bytes
            header in bytes format eg. b'\xAB'
        data_size : int
            number of bytes between header an footer with data
        footer : bytes
            footer in bytes format eg. b'\xAB\x0D'
        flags :
            flags for the regular expression compiling
        
        Return
        -------
        reg_ex: regular expression object
            compiled regular_expression object
        """
        # placholder for data part
        # . stands in regexpression for all chracters without \n
        # {n} n times 
        str_data_size = bytes('.{{{}}}'.format(data_size), 'utf-8')
        
        if footer is not None:
            pattern = header + str_data_size + footer
        else:
            pattern = header + str_data_size

        reg_ex = re.compile(pattern,flags)

        return reg_ex

###########################################################################################################
class SinglePackage(BaseDataPackage):
    """
    This class is for handling packages of the type:
    header | data | footer
    header | data
    where data is really data --> x,y,z,...
    Therefore regularexpression are created, ...
    """
    def __init__(self,
                 d_package_vals: dict,
                 sensorname,
                 sensor_type,
                 package_header,
                 num_bytes_header,
                 num_bytes_data,
                 num_bytes_package,
                 package_footer = None,
                 num_bytes_footer= None,
                 ):
        """ 
        Intilization function for the DataPackage
        Parameters
        ----------
        d_package_vals : dict
            In this dict all the values of the data package have to be defined in the following way:
            e.g.
            d_package_values = {'temp': {
                                        'type':     'float'
                                        'signed':   True
                                        'bytes':    4,
                                        'endian':   'big',
                                        },
                                'X':    {
                                        'type':     'int',
                                        'signed':   True
                                        'bytes':    3,
                                        'endian':   'big',
                                }
            type could be int, float have to be implemented
        """
        super().__init__(   sensorname = sensorname,
                    sensor_type = sensor_type,
                    package_header=package_header,
                    num_bytes_header=num_bytes_header,
                    num_bytes_data=num_bytes_data,
                    num_bytes_package=num_bytes_package,
                    package_footer=package_footer,
                    num_bytes_footer=num_bytes_footer)
        
        # package vals have to be separated by the sensors
        self.d_pckg_vals = d_package_vals
        self.num_values = len(self.d_pckg_vals.keys())

    def get_data_from_package(self,data: bytes, start_pos: int):
        """
        Reads out the bytes of the package and converty the bytes to the correct datatype

        Parameters
        ----------
        data : bytes
            the input data
        start_pos : int
            index of start_pos of the package,
            Note: the offset of the header will be added in this function

        Returns
        -------
        l_values : list
            list includeing all the values from the package in the order of the keys in the dict
        """
        l_values =[]
        temp_value = 0
        start_pos += self.num_bytes_header
        # iterate over all values in the package
        for key in self.d_pckg_vals.keys():
            # get the data bytes for the current package values
            # could also be more than one value
            l_data_key= []
            for i in range(0,self.d_pckg_vals[key]['num_values']):
                num_of_bytes = self.d_pckg_vals[key]['bytes']    
                temp_bytes = data[start_pos +(i*num_of_bytes) : start_pos + (i+1)*num_of_bytes ]
            
                # interpret the bytes
                if self.d_pckg_vals[key]['type'] == 'int':
                    temp_value = int.from_bytes(temp_bytes, 
                                                byteorder=self.d_pckg_vals[key]['endian'],
                                                signed=self.d_pckg_vals[key]['signed'])
                
                elif self.d_pckg_vals[key]['type'] == 'float':
                    raise NotImplementedError("The data type float is not implemented yet")
                
                else:
                    raise KeyError("The data type {} is not supported".format(self.d_pckg_vals[key]['type']))

                #start_pos += self.d_pckg_vals[key]['bytes']
                l_data_key.append(temp_value)

            start_pos += num_of_bytes

            if len(l_data_key) == 1:
                l_values.append(l_data_key[0])
            elif len(l_data_key) > 1:
                l_values.append(l_data_key)

        return l_values


###########################################################################################################
class MultiPackage(BaseDataPackage):
    """
    This class is inheritance from the DataPackage class and overwrite the read data stuff
    It is Package like
    Header | data | footer
    Header | data 

    here the data part can again consits of
    h|d|f|h|d|f|

    """
    def __init__(self,
                 d_package_vals: dict, # have to be removed
                 l_packages,
                 sensorname,
                 sensor_type,
                 package_header,
                 num_bytes_header,
                 num_bytes_data,
                 num_bytes_package,
                 package_footer = None,
                 num_bytes_footer= None,
                 flag_overlap_pkgs = False,
                 ):
        """ 
        Intilization function for the DataPackage
        Parameters
        ----------
        l_packages:list
            list wiht all pks which are included in the data part
        flag_overlapping_pkgs : bool
            if True the data can be randomly splitted, so some of the data can be in the next package
        """
        super().__init__(   sensorname = sensorname,
                    sensor_type = sensor_type,
                    package_header=package_header,
                    num_bytes_header=num_bytes_header,
                    num_bytes_data=num_bytes_data,
                    num_bytes_package=num_bytes_package,
                    package_footer=package_footer,
                    num_bytes_footer=num_bytes_footer)
        

        self.l_packages = l_packages
        self.l_data = b''
        self.flag_overlap_pkgs = flag_overlap_pkgs 

        self.l_sensornames = []
        self.l_offsets = [0]

        # private
        self.data_buffer = b''
        self.idx_buffer = 0
        
        # iterate over all packages
        for i, pkg in enumerate(self.l_packages):
            # create_list_with all values
            self.l_sensornames.extend(pkg.d_pckg_vals.keys())
            if i < len(self.l_packages)- 1:
                self.l_offsets.append(pkg.num_values + self.l_offsets[-1])
        self.num_values_pkg = len(self.l_sensornames)


        self.d_pckg_vals = d_package_vals
        self.num_values = len(self.l_sensornames)

        # create a package reader object for reading out the data
        # self.package_reader = PackageReader(l_packages=self.l_packages)

    def get_data_from_package(self,data: bytes, start_pos: int):
        """
        Reads out the subpackges from the databracket

        Parameters
        ----------
        data : bytes
            the input data
        start_pos : int
            index of start_pos of the package,
            Note: the offset of the header will be added in this function

        Returns
        -------
        l_values : list
            list includeing all the values from the package in the order of the keys in the dict
        """
        start_pos += self.num_bytes_header
        data_snippet = data[start_pos : start_pos + self.num_bytes_data]

        if not self.flag_overlap_pkgs:
            ### have to be removed later
            # append the bytes for reading out in the end
            start_pos += self.num_bytes_header
            self.l_data += data_snippet
            return [1]

        ### overlapping pkgs
        elif self.flag_overlap_pkgs:
            # read out the new data snippet
            l_data = self.read_out_overlap_data(data_snippet)
        return l_data

    def read_out_overlap_data(self, data_snippet):
        """
        reads out of data
        """
        flag_search_pkg = True
        self.data_buffer += data_snippet # append the new data
        idx_last_pkg = 0
        l_data_pkg = [None] * self.num_values_pkg # empty list to put in every value which is recieved

        while flag_search_pkg:
           
            found_pkg = self.check_for_pkg(idx = self.idx_buffer, data=self.data_buffer)
            if found_pkg:
                self.read_data_of_package(found_pkg,
                                        data=self.data_buffer,
                                        idx=self.idx_buffer,
                                        l_data=l_data_pkg)
                
                self.idx_buffer += found_pkg.num_bytes_package
                idx_last_pkg = self.idx_buffer #saves the idx where the last pkg ended + 1

            else:
                self.idx_buffer += 1
            
             ### check termination condition
            if self.idx_buffer > len(self.data_buffer):
                flag_search_pkg = 0
        
        ### cut the buffer to not read data, reset idxes ...
        self.data_buffer = self.data_buffer[idx_last_pkg:]
        self.idx_buffer = 0

        return l_data_pkg


    def read_data_of_package(self, pkg, data, idx, l_data):
        """
        Reads out the data of one package and puts everything in list 
        """
        # read out the data of the subpackage by calling the function of the subpackage
        data_values = pkg.get_data_from_package(data, idx)
        offset =self.l_offsets[self.l_packages.index(pkg)] # get offset for the pkg

        # the data have to be saved as list in list because there could be more then one packet
        # in one big packet
        for i, value in enumerate(data_values):
            if l_data[offset+i] is None:
                l_data[offset+i] = [value]
            elif isinstance(l_data[offset+i], list):
                l_data[offset+i].append(value)
        return l_data

    

    def check_for_pkg(self, idx: int, data: bytes):
        """ This funktion is for checking which package fits for the specific position in the data
        
        Returns
        -------
        found_pkg: object of DataPackage
            None if no package was find
        """
        l_detected_packages = []
        found_pkg = None

        # search for all possible packages
        for pkg in self.l_packages:
            if pkg.check_reg_ex(data, start_pos=idx):
                l_detected_packages.append(pkg)

        # Check the detected packages
        if len(l_detected_packages) == 1:
            found_pkg = l_detected_packages[0]
        elif len(l_detected_packages) > 1:
            found_pkg = self.handle_multiple_fitting_packages(l_detected_packages)

        return found_pkg
