# BinFileReader

The BinFileReader is for reading out data of .bin file. The data can be in the following structure:

pkg 1 | pkg 2 | pkg 1 pkg 3 |.....

The Packages can have the structure

- header | data | footer

- header | data

- or The Package includes Subpackages e.g.:
  header | subheader 1| data1| subheader2 | data 2 |footer2 |.....

# Usage

1. Create a config.py file where all the packages are defined inside or new datatypes which are transmitted.
   
   Use SinglePackages when the package consists of header, data (and footer)
   
   Use Multipackage if in the Package are multiple Packages with differetn Subheaders like described in the beginning 
   
   ```python
   from SWAI.IO.BinFileReader.DataPackage import *
   from SWAI.IO.BinFileReader.StdDatatypes import StdDatatypes as std
   from SWAI.IO.BinFileReader.OwnDatatypes import OwnDatatypes
   
   d_adxl_package = {'temp':     std.d_s16_be,
                     'X':        std.d_s24_le,
                     'Y':        std.d_s24_le,
                     'Z':        std.d_s24_le,
                     'CRC':      std.d_u8
             }
   
   pkg_adxl_front = SinglePackage(d_package_vals=d_adxl_package,
                          sensorname = 'ADXL_front',
                         sensor_type= 'Vibration',
                         package_header= [b'\\xC8'],
                         package_footer= [b'\x0D\x0A'],
                         num_bytes_header= 1,
                         num_bytes_data= 12,
                         num_bytes_footer= 2,
                         num_bytes_package= 15,
                         ))
   
   l_vib_packages =[
                       pkg_adxl,
                       pkg_adis,
                       pkg_iis3,
                   ]
   
   # just as dummy
   d_vib_package = {'data': std.d_u8}
   
   pkg_vib_31 = MultiPackage(l_packages=l_vib_packages,
                           d_package_vals=d_vib_package,   
                           sensorname = 'Vib_31',
                           sensor_type= 'Vibration',
                           package_header= [b'\\x31\\x42\\x49\\x56'],
                           num_bytes_header= 4,
                           num_bytes_data= 256,
                           num_bytes_package= 260,
                           flag_overlap_pkgs=True
                           )
   ```

2. Initialize the MainPackageReader and read out the data of the file
   
   Exampel Code:

```python
# create list of all packages which are expected
l_packages = [
             pkg_timestamp,  
             pkg_adxl_front,
             pkg_vib_31
             ]

# read in the file
path_bin_file = r"data.bin"
with open(path_bin_file, "rb") as file:
 raw_file = file.read()

# create a Package Reader object for reading out the raw file
package_reader_main = PackageReader(l_packages=l_packages)

data = package_reader_main.read_out_raw_file(raw_file)
```

# Classes, Class-Diagramm

## Class PackageReader

This is the main class for reading out binary file

**Arguments**

- l_subpackges : list with the objects of the Singel /Multipackages



**Functionality**

This class iterates over the whole file and searches for the different packages.

If a package is found, in the next step the data of the package will be read out.

For the single interpretation of the bytes in a Package the method of the package is called to read out the data.

In the end the functions returns a list of lists with the data. This can be converted to pandas dataframe for ecample.

## Class SingelPackage

This class is for handling packages of the type:

    header | data | footer

    header | data

For reading them out regular expressions are created

**Todo**

- packages with no footer also possible

- flex size of data

**Functionality**

- It creates a regex by the initilization data

- Interprets the single bytes by the defined values



## MultiPackage

This class is inheritance from the DataPackage class and overwrite the read data stuff

    It is for package like

    Header | data | footer

    Header | data

    here the data part can again consits of

    h|d|f|h|d|f|...

**Note:**

This Type can handle data which is overlapping to the next package. By setting flag True, there will be created a internal buffer which concatenates the different packages for reading them out

```
flag_overlapping_pkgs : bool
    if True the data can be randomly splitted, so some of the data can be in the next
```



## Class StdDatatypes

This class hold the definition of standard datatypes of data

 which is transmitted and saved in a bin file definition of standard datatypes

for example:

```python
d_u8 = { 'type':       'int'  # ['int','float']
         'signed':     True   # [True,False]
         'bytes':      4      # number of bytes
         'endian':     'big'  # ['big','little']
         'num_values': 1      # number of values repeating
       },
```

 **Note:** If there are some different Datatypes needed define own dict or add it to the class OwnDatatypes

## Class OwnDatatypes

here can be added some own Datatypes

## BinFileReader (old --> for hummel kalttest)

The BinFileReader is for reading out data of .bin file. The data have to be in the following structure:

| Main Pkg header | Sub-pkg header1 | Data 1 | Sub-pkg footer 1 | Sub-pkg header2 | Data 2 | Sub-pkg footer 2 | ... |
|:---------------:|:--------------- | ------ | ---------------- | --------------- | ------ | ---------------- | --- |

# Usage

1. Create a config.py file where all the packages are defined inside or new datatypes which are transmitted
   
   ```python
   from SWAI.IO.BinFileReader.DataPackage import *
   from SWAI.IO.BinFileReader.StdDatatypes import StdDatatypes as std
   
   d_adxl_package = {  'temp':     std.d_s16_be,
       'X':        std.d_s24_le,
                   'Y':        std.d_s24_le,
                   'Z':        std.d_s24_le,
                   'CRC':      std.d_u8
               }
   
    pkg_adxl_front = DataPackage(d_package_vals=d_adxl_package,
                            sensorname = 'ADXL_front',
                           sensor_type= 'Vibration',
                           package_header= [b'\\xC8'],
                           package_footer= [b'\x0D\x0A'],
                           num_bytes_header= 1,
                           num_bytes_data= 12,
                           num_bytes_footer= 2,
                           num_bytes_package= 15,
                           ))
   ```

2. Initialize the  MainPackageReader and read out the data of the file 
   
   Exampel Code:

```python
# create list of all packages which are expected
l_packages = [
             pkg_timestamp,  
             pkg_adxl_front,
             ]
# read in the file
path_bin_file = r"data.bin"
with open(path_bin_file, "rb") as file:
 raw_file = file.read()

# create a Package Reader object for reading out the raw file
raw_file_reader = MainPackageReader( l_subpackages=l_packages,
                                     b_str_reg_ex=b'.{2}\xfe\xca',
                                     len_main_pkg_header = 4,) 

data = raw_file_reader.read_out_raw_file(raw_file)
```

# Classes, Class-Diagramm

## Class MainPackageReader

This is the main class for reading out binary file

**Arguments**

- l_subpackges : list with the objects of the subpackages

- b_str_reg_ex: str
  
  the string should include the regex exspression for searching the header in the 

- len_main_pkg_header: int
  
  number of bytes for the main pkg header defined in the b_str_reg_ex

**Functionality**

This class iterates over the whole file and searches for the main header

if the main header is found, in the next step it will be checked for subpackages

if no subpackage is found anymore or the next main header follows then the next main package will be read out

For the single interpretation of the bytes in a subpackage the class of the subpackages is called

## Class DataPackage

This class is for defineing a subpackages.

 It handels packages of the type:

    header | data | footer

For reading them out regular expressions are created

**Todo**

- packages with no footer also possible

- flex size of data

**Functionality**

- It creates a regex by the initilization data

- Interprets the single bytes by the defined values

## Class StdDatatypes

This class hold the definition of standard datatypes of data

 which is transmitted and saved in a bin file definition of standard datatypes

for example:

```python
d_u8 = { 'type':       'int'  # ['int','float']
         'signed':     True   # [True,False]
         'bytes':      4      # number of bytes
         'endian':     'big'  # ['big','little']
         'num_values': 1      # number of values repeating
       },
```

 **Note:**  If there are some different Datatypes needed define own dict or add it to the class OwnDatatypes

## Class OwnDatatypes

here can be added some own Datatypes
