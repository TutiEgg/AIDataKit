from SWAI.IO.BinFileReader.DataPackage import SinglePackage
from SWAI.IO.BinFileReader.StdDatatypes import StdDatatypes as std
from SWAI.IO.BinFileReader.OwnDatatypes import OwnDatatypes

##########################
#  timestamp
##########################
d_timestamp_package = {'timestamp': std.d_u32_le}
pkg_timestamp = SinglePackage(d_package_vals=d_timestamp_package,
                            sensorname = 'timestamp',
                            sensor_type= 'timestamp',
                            package_header= [b'\\x24'],
                            package_footer= [b'\x0D\x0A\x0D\x0A'],
                            num_bytes_header= 1,
                            num_bytes_data= 4,
                            num_bytes_footer= 4,
                            num_bytes_package= 9,
                            )


##########################
#  ADXL
##########################
d_adxl_package = {  'temp':     std.d_s16_be,
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
                            )

pkg_adxl_back = SinglePackage(d_package_vals=d_adxl_package,
                            sensorname = 'ADXL_back',
                            sensor_type= 'Vibration',
                            package_header= [b'\\xC9'],
                            package_footer= [b'\x0D\x0A'],
                            num_bytes_header= 1,
                            num_bytes_data= 12,
                            num_bytes_footer= 2,
                            num_bytes_package= 15,
                            )

##########################
#  ADIS
##########################
d_adis_package = {  'DIAG_STAT':    std.d_u16_le, 
                    'X_GYRO':       std.d_s16_le,  
                    'Y_GYRO':       std.d_s16_le,
                    'Z_GYRO':       std.d_s16_le,    
                    'X':            std.d_s16_le, 
                    'Y':            std.d_s16_le, 
                    'Z':            std.d_s16_le, 
                    'TEMP':         std.d_s16_le, 
                    'DATA_CNTR':    std.d_u16_le,
                    'Checksum':     std.d_u16_le   
}

pkg_adis_front = SinglePackage(d_package_vals=d_adis_package,
                            sensorname = 'ADIS_front',
                            sensor_type= 'Vibration',
                            package_header= [b'\\xE7'],
                            package_footer= [b'\x0D\x0A'],
                            num_bytes_header= 1,
                            num_bytes_data= 20,
                            num_bytes_footer= 2,
                            num_bytes_package= 23,
                            )

pkg_adis_back = SinglePackage(d_package_vals=d_adis_package,
                            sensorname = 'ADIS_back',
                            sensor_type= 'Vibration',
                            package_header= [b'\\xE8'],
                            package_footer= [b'\x0D\x0A'],
                            num_bytes_header= 1,
                            num_bytes_data= 20,
                            num_bytes_footer= 2,
                            num_bytes_package= 23,
                            )

##########################
#  ADIS
##########################
d_iis3_package = {  'X':    std.d_s16_le,
                    'Y':    std.d_s16_le,
                    'Z':    std.d_s16_le,
                    'CRC':  std.d_u8,
                    }

pkg_iis3_front = SinglePackage(d_package_vals=d_iis3_package,
                            sensorname = 'IIS3_front',
                            sensor_type= 'Vibration',
                            package_header= [b'\\xA9'],
                            package_footer= [b'\x0D\x0A'],
                            num_bytes_header= 1,
                            num_bytes_data= 7,
                            num_bytes_footer=2,
                            num_bytes_package= 10,
                            )

pkg_iis3_back = SinglePackage(d_package_vals=d_iis3_package,
                            sensorname = 'IIS3_back',
                            sensor_type= 'Vibration',
                            package_header= [b'\\xAA'],
                            package_footer= [b'\x0D\x0A'],
                            num_bytes_header= 1,
                            num_bytes_data= 7,
                            num_bytes_footer=2,
                            num_bytes_package= 10,
                            )

##########################
#  Ultrasonic
##########################
d_ultra_package = {'US': OwnDatatypes.d_u32_le_n64}

pkg_us_front = SinglePackage(d_package_vals=d_ultra_package,
                            sensorname = 'US_front',
                            sensor_type= 'Ultrasonic',
                            package_header= [b'\\x32\\x49\\x41\\x53'],
                            package_footer= [b'\x0D\x0A\x0D\x0A'],
                            num_bytes_header= 4,
                            num_bytes_data= 256,
                            num_bytes_footer=4,
                            num_bytes_package= 264,
                            )

pkg_us_back = SinglePackage(d_package_vals=d_ultra_package,
                            sensorname = 'US_back',
                            sensor_type= 'Ultrasonic',
                            package_header= [b'\\x33\\x49\\x41\\x53'],
                            package_footer= [b'\x0D\x0A\x0D\x0A'],
                            num_bytes_header= 4,
                            num_bytes_data= 256,
                            num_bytes_footer=4,
                            num_bytes_package= 264,
                            )

pkg_us_32 = SinglePackage(d_package_vals=d_ultra_package,
                            sensorname = 'US_32',
                            sensor_type= 'Ultrasonic',
                            package_header= [b'\\x32\\x49\\x41\\x53'],
                            package_footer= [b'\x0D\x0A\x0D\x0A'],
                            num_bytes_header= 4,
                            num_bytes_data= 256,
                            num_bytes_footer=4,
                            num_bytes_package= 264,
                            )

pkg_us_33 = SinglePackage(d_package_vals=d_ultra_package,
                            sensorname = 'US_33',
                            sensor_type= 'Ultrasonic',
                            package_header= [b'\\x33\\x49\\x41\\x53'],
                            package_footer= [b'\x0D\x0A\x0D\x0A'],
                            num_bytes_header= 4,
                            num_bytes_data= 256,
                            num_bytes_footer=4,
                            num_bytes_package= 264,
                            )

##########################
#  CAN Data
##########################
d_rpm_package =             {'rpm':             std.d_u16_le}

pkg_rpm = SinglePackage(d_package_vals=d_rpm_package,
                            sensorname = 'rpm',
                            sensor_type= 'CAN',
                            package_header= [b'\\x52'],
                            package_footer= [b'\x0D'],
                            num_bytes_header= 1,
                            num_bytes_data= 2,
                            num_bytes_footer=1,
                            num_bytes_package= 4,
                            )
###
d_speed_backwheel_package = {'speed_backwheel': std.d_u16_le}

pkg_speed_backwheel = SinglePackage(d_package_vals=d_speed_backwheel_package,
                            sensorname = 'speed_backwheel',
                            sensor_type= 'CAN',
                            package_header= [b'\\x53'],
                            package_footer= [b'\x0D'],
                            num_bytes_header= 1,
                            num_bytes_data= 2,
                            num_bytes_footer=1,
                            num_bytes_package= 4,
                            )

###
d_oiltemp_package =         {'oiltemp':         std.d_u8}

pkg_oiltemp = SinglePackage(d_package_vals=d_oiltemp_package,
                            sensorname = 'oiltemp',
                            sensor_type= 'CAN',
                            package_header= [b'\\x54'],
                            package_footer= [b'\x0D'],
                            num_bytes_header= 1,
                            num_bytes_data= 1,
                            num_bytes_footer=1,
                            num_bytes_package= 3,
                            )

###
d_motor_temp_package =      {'motor_temp':      std.d_u8}

pkg_motor_temp = SinglePackage(d_package_vals=d_motor_temp_package,
                            sensorname = 'motor_temp',
                            sensor_type= 'CAN',
                            package_header= [b'\\x55'],
                            package_footer= [b'\x0D'],
                            num_bytes_header= 1,
                            num_bytes_data= 1,
                            num_bytes_footer=1,
                            num_bytes_package= 3,
                            )

###
d_gear_package =            {'gear':            std.d_u8}

pkg_gear = SinglePackage(d_package_vals=d_gear_package,
                            sensorname = 'gear',
                            sensor_type= 'CAN',
                            package_header= [b'\\x56'],
                            package_footer= [b'\x0D'],
                            num_bytes_header= 1,
                            num_bytes_data= 1,
                            num_bytes_footer=1,
                            num_bytes_package= 3,
                            )

##########################
#  IO-Signal
##########################
d_gear_package =            {'24V_IO':            std.d_u8}

pkg_24V_IO = SinglePackage(d_package_vals=d_gear_package,
                            sensorname = '24V_IO',
                            sensor_type= 'IO',
                            package_header= [b'\\x30'],
                            package_footer= [b'\x0D'],
                            num_bytes_header= 1,
                            num_bytes_data= 1,
                            num_bytes_footer=1,
                            num_bytes_package= 3,
                            )