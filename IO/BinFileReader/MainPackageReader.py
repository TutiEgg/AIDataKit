import re
from tqdm import tqdm
import numpy as np
import copy
import pandas as pd
from SWAI.Util.util_classes import CustomtqdmBar


class MainPackageReader():
    """
    This class is for reading out packages out of binary file.

    The structure of the binary files should be the following way. More detailed it is documented 
    in the read me
    [main_pkg_header1, subpkg1, subpkg2,...][main_pkg_header1, subpkg1, subpkg2,...]

    naming:
    main_pkg = the main pakcge so the big one where the subpakcges are inside
    """

    def __init__(self, l_subpackages: list, 
                 b_str_reg_ex=b'.{2}\xfe\xca',
                 len_main_pkg_header = 4,
                 ):
        """
        Initilization function
        Parameters
        ----------
        l_subpackages: list
            list with the objects of the subpackages
        b_str_reg_ex: str
            the string should include the regex exspression for searching the header in the binary file
        len_main_pkg_header: int
            number of bytes for the main pkg header defined in the b_str_reg_ex
        """
        self.reg_ex = re.compile(b_str_reg_ex, flags= re.DOTALL)
        self.len_main_pkg_header = len_main_pkg_header # len in beytes
        self.l_subpackages = l_subpackages

        # create a dict for statistiks
        self.d_amount_pkgs = {}
        for pkg in self.l_subpackages:
            self.d_amount_pkgs[pkg.sensorname] = 0
        
        self.d_statistic =  {
                            'num_read_bytes':   None,
                            'num_main_pkgs':    None,
                            'num_multiple_pkgs': 0,
                            }    
        
        self.l_name_values = []
        self.l_offsets = [0]
        for i, pkg in enumerate(self.l_subpackages):
        
        # create_list_with all values
            self.l_name_values.extend(pkg.d_pckg_vals.keys())
            if i < len(self.l_subpackages)- 1:
                self.l_offsets.append(pkg.num_values + self.l_offsets[-1])
        self.num_values_pkg = len(self.l_name_values)
        
        # Privat
        self.idx_main_pkg = 0       # abs idx of the current main pkg (is updated in function)
        self.idx_main_pkg_next = 0  # abs idx of the next main pkg found by reg_ex
        self.idx_sub_pkg = 0         # abs idx in the current main pkg for reading out the subpackges

 
    def reset_values(self):
        """
        Resets all the used value in the class
        """
        self.idx_main_pkg = 0      
        self.idx_main_pkg_next = 0  
        self.idx_sub_pkg = 0
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

        # create prograsse bar with amount of characters in raw file
        pbar = CustomtqdmBar(total_abs=len(data))

        ## loop over the main packages as long as the header could be found
        # add something if there is nothing, so the idx will be increased
        while(idx := self.search_reg_ex_main_pkg(idx = self.idx_sub_pkg,data=data)) is not None:
            self.set_idx_main_pkg(idx)
            if (idx := self.search_reg_ex_main_pkg(idx = self.idx_main_pkg + 1,data=data)) is not None:
                self.set_idx_main_pkg_next(idx)

            self.idx_sub_pkg = self.idx_main_pkg + self.len_main_pkg_header
            
            ## loop over data in a main pkg
            l_data_pkg = [None] * self.num_values_pkg # create empty list for later writing recieved data inside
            flag_search_in_sub_pkg = True

            while(flag_search_in_sub_pkg):
                found_pkg = self.check_for_sub_pkg(idx = self.idx_sub_pkg, data=data)
                if found_pkg is not None:
                    self.read_data_of_package(found_pkg,
                                            data=data,
                                            idx=self.idx_sub_pkg,
                                            l_data=l_data_pkg)
                    
                    
                    # create statistik for the status of the different data
                    self.idx_sub_pkg += found_pkg.num_bytes_package

                    self.d_amount_pkgs[found_pkg.sensorname] += 1

                else:
                    if not self.check_end_of_main_pkg_reached():
                        self.idx_sub_pkg +=1
                    else:
                        flag_search_in_sub_pkg= False

            l_return_data.append(l_data_pkg)
            pbar.update(self.idx_main_pkg_next - self.idx_main_pkg)
            
        pbar.close()

        self.read_bytes = self.get_size_from_data(len_data=len(l_return_data))

        return l_return_data


    def read_data_of_package(self, pkg, data, idx, l_data):
        """
        Reads out the data of one package
        """
        
        idx_offset = self.l_subpackages.index(pkg)
        # read out the data of the subpackage
        data_values = pkg.get_data_from_package(data, idx)

        # put the data in the list of the paket
        offset =self.l_offsets[idx_offset]
        num_values = pkg.num_values
        l_data[offset : (offset + num_values)] = data_values


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
    

    def check_for_sub_pkg(self, idx: int, data: bytes):
        """ This funktion is for checking which package fits for the specific position in the data
        
        Returns
        -------
        found_pkg: object of DataPackage
            None if no package was find
        """
        l_detected_packages = []
        found_pkg = None

        # search for all possible packages
        for pkg in self.l_subpackages:
            if pkg.check_reg_ex(data, start_pos=idx):
                l_detected_packages.append(pkg)
                break # at the moment their is nothing implemented if there are two packages

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
        if self.idx_sub_pkg >= self.idx_main_pkg_next -1:
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
        for pkg in self.l_subpackages:
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
        for pkg in self.l_subpackages:
            for value in pkg.d_pckg_vals.keys():
                l_tuples.append((pkg.sensorname,value))
        l_tuples[0:10]

        # create the oandas df
        header = pd.MultiIndex.from_tuples(l_tuples, names=l_multi_header)
        np_data = np.array(l_data, dtype=object)
        df = pd.DataFrame(np_data, columns=header)

        return df
    
    





        





