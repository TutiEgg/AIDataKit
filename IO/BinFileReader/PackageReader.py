import numpy as np
import pandas as pd
from SWAI.Util.util_classes import CustomtqdmBar
from SWAI.IO.BinFileReader.DataPackage import SinglePackage, MultiPackage


class PackageReader():
    """
    This class is for reading out packages out of binary file.
   """
    def __init__(self, l_packages: list, 
                 ):
        """
        Initilization function
        Parameters
        ----------
        """
        self.l_packages = l_packages

        # create a dict for statistiks
        self.d_amount_pkgs = {}
        for pkg in self.l_packages:
            self.d_amount_pkgs[pkg.sensorname] = 0
        
        self.d_statistic =  {
                            'num_read_bytes':   None,
                            'num_main_pkgs':    None,
                            'num_multiple_pkgs': 0,
                            }    
        
        # number of headers depend on how depth is nesting of the value in packages
        self.l_name_values = []
        
        self.l_offsets = [0]
        # iterate over all packages
        # create_list_with all values which will be extracted from the raw data
        for i, pkg in enumerate(self.l_packages):
            
            ### Single Package
            if type(pkg) == SinglePackage:
                self.l_name_values.extend(pkg.d_pckg_vals.keys())
                if i < len(self.l_packages)- 1:
                    self.l_offsets.append(pkg.num_values + self.l_offsets[-1])
            
        # get the header naming by the package and sensornames
        self.d_sensorname, self.l_offsets = self._get_sensorname_and_value_names(self.l_packages)            
        self.l_name_values = self._get_read_out_helpers(self.d_sensorname)
        
        self.num_values_pkg = len(self.l_name_values)
        
        # Privat
        self.idx_main_pkg = 0       # abs idx of the current main pkg (is updated in function)
        self.idx_main_pkg_next = 0  # abs idx of the next main pkg found by reg_ex
        self.idx_pkg = 0            # abs idx in the current main pkg for reading out the subpackges

    def _get_read_out_helpers(self, d_sensornames:dict):
        """
        This functin is for generating a list of all single values, and a list were offsets are included 
        for the different keys in the dict
        """
        l_names_values = []
        l_offsets = [0]
        for i, key in enumerate(d_sensornames.keys()):
            l_names_values.extend(d_sensornames[key])
            if i < len(d_sensornames.keys()) - 1:
                l_offsets.append(len(d_sensornames[key])+ l_offsets[-1])
        
        return l_names_values

    def _get_sensorname_and_value_names(self, l_pkgs):
        """
        This function is for getting the sensornames and the names of the values of each sensor out of the 
        packages which are in the bin file
        """
        d_sensornames = {}
        l_names_values = []
        l_offsets = [0]

        ### Single Package
        for pkg in l_pkgs:
            if type(pkg) == SinglePackage:
                if pkg.sensorname not in d_sensornames.keys():
                        d_sensornames[pkg.sensorname] = list(pkg.d_pckg_vals.keys())         
                        l_offsets.append(pkg.num_values + l_offsets[-1])
                else:
                    pass#raise ValueError("Don't use Sensornames twice")

            ### Multi Package
            elif type(pkg) == MultiPackage:
                num_values = 0
                # get all the sensornames from the package
                for i, sub_pkg in enumerate(pkg.l_packages):
                    new_sensorname = '_'.join([pkg.sensorname, sub_pkg.sensorname])
                    if new_sensorname not in d_sensornames.keys():
                        d_sensornames[new_sensorname] = list(sub_pkg.d_pckg_vals.keys())
                        num_values += len(d_sensornames[new_sensorname])         
                    else:
                        pass #raise ValueError("Don't use Sensornames twice")

                l_offsets.append(num_values + l_offsets[-1])

        return d_sensornames, l_offsets
    
 
    def reset_values(self):
        """
        Resets all the used value in the class
        """
        self.idx_main_pkg = 0      
        self.idx_main_pkg_next = 0  
        self.idx_pkg = 0
        self.d_amount_pkgs = dict.fromkeys(self.d_amount_pkgs, 0)
        self.d_statistic = dict.fromkeys(self.d_statistic, 0)    


    def read_out_raw_file(self, data):
        """ 
        This is the main function for reading out the whole data file
        Parameters
        ----------
        data : bytes
        """
        self.reset_values()
        l_return_data = []
        c_tqdm = CustomtqdmBar(total_abs=len(data), desc='Reading raw file')
        flag_search = True
        last_idx = 0

        ### lopp over data and check for packages
        
        while(flag_search):
            last_idx = self.idx_pkg
            l_data_pkg = [None] * self.num_values_pkg # empty list to put in every value which is recieved
            found_pkg = self.check_for_pkg(idx = self.idx_pkg, data=data)
            if found_pkg is not None:
                self.read_data_of_package(found_pkg,
                                        data=data,
                                        idx=self.idx_pkg,
                                        l_data=l_data_pkg)
                
                
                # create statistik for the status of the different data
                self.d_amount_pkgs[found_pkg.sensorname] += 1
                l_return_data.append(l_data_pkg)
                
                # update the current idx in the bin file
                self.idx_pkg += found_pkg.num_bytes_package
            
            ### no pkg was found --> skip one byte
            else:
                self.idx_pkg += 1

            
            ### check termination condition
            if self.idx_pkg > len(data):
                flag_search = False
            c_tqdm.update(self.idx_pkg-last_idx)

        return l_return_data


    def read_data_of_package(self, pkg, data, idx, l_data):
        """
        Reads out the data of one package
        """
        # read out the data of the subpackage by calling the function of the subpackage
        data_values = pkg.get_data_from_package(data, idx)
        offset =self.l_offsets[self.l_packages.index(pkg)] # get offset for the pkg

        # put the data in the list of the paket
        l_data[offset : (offset + pkg.num_values)] = data_values


    def search_reg_ex_main_pkg(self, idx: int, data: bytes):
        """search for the main pkg
        
        Returns
        -------
        ret_value: int
            if there is a match int with start idx is ereturned, else None
        """
        ret_val = None
        match = self.reg_ex.search(data, idx)
        if match:
            ret_val = match.span()[0] # start idx
        return ret_val
    

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
                break # not implemented when their are more then one package

        # Check the detected packages
        if len(l_detected_packages) == 1:
            found_pkg = l_detected_packages[0]
        elif len(l_detected_packages) > 1:
            found_pkg = self.handle_multiple_fitting_packages(l_detected_packages)

        return found_pkg
    
    def check_end_of_main_pkg_reached(self,):
        """
        Checks if the end of the main pkg is reached
        if reached returns True, else False
        """
        ret = False
        if self.idx_sub_pkg >= self.idx_main_pkg_next:
            ret = True
        else:
            ret = False
            
        return ret
    
    def get_size_from_data(self, len_data):
        """
        Calculate the size of the file by the found subpackages
        Returns
        -------
        num_bytes : int
            The number of bytes which could be found correctly by  reading out the file
        """
        num_bytes = 0

        # header main package
        # amount of recieved pkgs by length of the data list
        num_bytes += len_data * self.len_main_pkg_header
        
        # check the amount of every subpackage
        for pkg in self.l_packages:
            num_bytes += self.d_amount_pkgs[pkg.sensorname] * pkg.num_bytes_package

        self.d_statistic['num_read_bytes'] = num_bytes
        self.d_statistic['num_main_pkgs'] = len_data

    def calculate_samplerate_of_packages(self):
        """ calculates the sample rate of the different pkgs """


    def handle_multiple_fitting_packages(self, l_detected_pkg):
        """returns the better fitting package
        Returns
        -------
        found_pkg: object of DataPackage
            The pkg that fits the best
        """
        # todo search best fitting Package
        self.d_statistic['num_multiple_pkgs'] += 1
        return l_detected_pkg[0]
    
    def set_idx_main_pkg(self, idx):
        self.idx_main_pkg = idx

    def set_idx_main_pkg_next(self, idx):
        self.idx_main_pkg_next = idx

    def convert_data_to_pandas(self, 
                               l_data: list,
                               l_multi_header = ['Sensor', 'Sensor_values']):
        """
        Converts the data to pandas by adding a Sensor header and a Sensorvalue header
        """
        # create an header with multiindex 
        l_multi_header = ['Sensor', 'Sensor_values']
        l_tuples =[]

        # get all naming stuff for columns
        for key in self.d_sensorname.keys():
            for value_name in self.d_sensorname[key]:
                l_tuples.append((key, value_name))
        
        # create the pandas df
        header = pd.MultiIndex.from_tuples(l_tuples, names=l_multi_header)
        #np_data = np.array(l_data, dtype=object)
        df = pd.DataFrame(l_data, columns=header)
        # in converts partly none to NaN to avoid inconsistency, convert them back to none
        df = df.astype(object).replace(np.nan, None)
       

        return df