#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   Ali Uzun 
@Created On    :   2022/11/11 14:12:54
@Version :   1.0
'''

# here put the import lib

import time
from tkinter import filedialog, Tk
import pandas as pd
from src.Parameters import *


class WL_Sweep():
    """
        Implements the functionality for currnet or volateg sweep on channel A/B of the SMU.

        Args:
            initialize_connection: Initialize_GPIB() object 
            keithley_GPIB: Keithley GPIB command library (smu26xx)
            save_data: Write to csv file (Save_Data)
    """
    def __init__(self, initialize_connection, tuneable_laser_GPIB, save_data, newport_PM):
        self.initialize_connection = initialize_connection
        self.tl_GPIB = tuneable_laser_GPIB
        self.save_data = save_data
        self.newport_PM = newport_PM
    
    
    def wavelength_sweep_1300nmLS(self, filename, header, wl_start_value, wl_stop_value, wl_step_size): 
        """
        Sweep wavelength in tunable laser ang gets power from the selected source ( Newport power meter, thorlab or keithley as photocurrent) 
    
        """
        
        self.save_data.save_to_csv_file(filename, header, header_flag=True) # add the header for file
        value_i = wl_start_value
        while value_i <= wl_stop_value:
            
            # print("Set value is %f %s \n" % (value, unit))
            self.tl_GPIB.set_wavelength(value_i*1e-9)
            #keithley_GPIB.set_voltage_ChA(value_i)
            
            self.tl_GPIB.turn_ON()       
            time.sleep(keithley_sleep_time)      
    
            self.keithley_GPIB.turn_ON_ChB() 
            # correct sing in reading
            #currentb = -1*self.keithley_GPIB.get_current_ChB()
            #if (currentb <0):

            power = self.newport_PM.get_data()
                   
            print("Wl=%s mA, P=%s V \n" %(value_i, power))    
        
            data = [value_i, power ]
            self.save_data.save_to_csv_file(filename, data, header_flag = False)
            value_i = value_i + wl_step_size      
        
        # turn OFF channels 
        self.tl_GPIB.turn_OFF()       
        
        #self.initialize_connection.terminate_connection()
        # close the file
        self.save_data.close_file()