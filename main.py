# -*- coding: utf-8 -*-
"""
Created on Thu Apr  7 15:24:06 2022

@author: ali.uzun
"""

import sys
#sys.path.append("\\\\fs1\\Docs2\\ali.uzun\\My Documents\\My Files\\Scripts\\Python\\III-V Scripts\\src\\")
import pandas as pd
import time

from src.Keithley26xx_GPIB import smu26xx
from src.Initialize_Connection import Initialize_GPIB
from src.Newport_844_PE import Newport_844_PE
from src.Thorlab_USBPM100D import Thorlab_100D

from src.Data_Analysis import Data_Analysis
from src.OpenFile import OpenFile
from src.Sweep_Function import IV_Sweep

from MSs.MyPlots import MyPlots
import Test_Functions as TF

fl = OpenFile()
da = Data_Analysis()

myplt = MyPlots()

#####-------------- Keithley Settings -----------####
gpib_index = 0
addr = 26 # change it if necessery
addr = 28 # change it if necessery

####----------

def Thorlab100D_Test():
    thorlab_PM = Thorlab_100D()
    # Open connection
    thorlab_PM.Initialize_connection()
    # # get power reading
    for i in range(15):
        data = thorlab_PM.get_power_reading()
        print(data)
         
    #close connection
    thorlab_PM.close_connection()
    
    
##### ------ INPUTs -------- #####

# ----- YOUR BASE DIRECTORY ---------
measurement_base_path = "\\\\FS1\\Docs2\\ali.uzun\\My Documents\\My Files\\Measurements\\Caladan\\Caladan 22\\"
measurement_base_path = r'\\FS1\Docs2\ali.uzun\My Documents\My Files\Measurements\Caladan\Caladan 22' + "\\"
# ----- FOLDER UNDER BASE DIRECTORY --------- 
save_to_folder = "Run-2 do6209\\2022-11-03 1.5 mm 1pMIR&EF\\"
save_to_folder = r"Run-2 do6209\2022-11-03 1.5 mm 1pMIR&EF" + "\\"

power_reading_from = ["Newport_PM", "Keithley_ChB","Thorlab_PM", "Other"] # 0 or 1
power_index = 1 # 0 or 1

filename = "221103_Au2Q1_do6209_1pT-MIR_CL-1.5mm_RW-2.5umT3umOver80um_MIR-6.5X50um-TD4_%s_r1.csv" % power_reading_from[power_index]

file_directory = measurement_base_path + save_to_folder # Folder the filde will be saved
full_path = file_directory + filename # full path for file

print(full_path)

#### ----- CURRENT SWEEP SETTINGS ---------
voltage_limit = 3 # V
start_value = 0
stop_value = 200 #mA
step_size = 2 #mA

def main():

    initialize_connection = Initialize_GPIB()
    inst = initialize_connection.connect_device(gpib_index, addr) # connect to device#

    # create an object
    keithley_GPIB =  smu26xx(inst)
    save_data = OpenFile()
    
    newport_PM = Newport_844_PE()

    sweep_function = IV_Sweep(initialize_connection, keithley_GPIB, save_data, newport_PM)
     

    header = ["Current (mA)", "Voltage (V)", "Power (mW)"]
    
    LIV_sweep = False # True is LIV sweep. False IV

    if (LIV_sweep):
        
        if (power_reading_from[power_index] == "Newport_PM"):
            
            newport_ranges = ('AUTO', '30.0mW', '3.00mW', '300uW', '30.0uW', '3.00uW', '300nW', '30.0nW')
            rindex = 2
            # newport_PM.set_range(rindex)
            sweep_function.LIV_sweep_NewportPM(full_path, header, start_value=start_value, stop_value=stop_value, step_size=step_size, voltage_limit = voltage_limit)
        
        elif (power_reading_from[power_index] == "Keithley_ChB"):
            #current_ranges = [1E-7, 1E-6, 1E-5, 1E-4, 1E-3, 1E-2, 1E-1, 1, 1.5]
            rg = 1E-1 # keithley channel range
            keithley_GPIB.set_range_ChB(rg)

            # Responsivity of Detector (A/W), 818IR Ge Detector
            R = 0.75  
            R = 0.67 # Calibrated on 03-11-2022

            sweep_function.LIV_sweep_KeithleyChB(full_path, header, R, start_value=start_value, stop_value=stop_value, step_size=step_size, voltage_limit = voltage_limit)
        else:
            print("No reading!!!!!")
    else:
        is_IV = True  

        if (is_IV):

            sweep_function.IV_sweep(full_path, header, start_value=start_value, stop_value=stop_value, step_size = step_size, voltage_limit = voltage_limit)
        
        else:
            current_limit = 50 # mA
            start_value = 0
            stop_value = 3 # V
            step_size = 0.1 # V

            sweep_function.VI_sweep(full_path, header, start_value=start_value, stop_value=stop_value, step_size = step_size, current_limit = current_limit)
    
    
    if (LIV_sweep):
        #plot_sweep(filename, full_path)
        x_label = "Current (mA)"
        y_label_Left = "Voltage (V)"
        y_label_right = "Optical Power (mW)"

        plot_title = filename
  
        I,V,P = fl.read_csv_file(full_path)
        P = P*1e3
        file_path = file_directory
        myplt.plot_LIV(file_path, filename, I, V, P, x_label, y_label_Left, y_label_right)
            
    # else:
    #     plot_sweep_IV(filename, full_path)
    
    inst.close()


if __name__ == "__main__":
    #main()
    Thorlab100D_Test()
    #TF.ist_device_GPIB()
    #keithley_function()
    #probe_alingmment_test()
    #keithley_test() 
    #get_current_In_ChB  ()  
    #plot_test()
    #keithley_test()
    #newport_USBPM_test()
    #TF.thorlab_PM100D_test()
    #get_current_In_ChB()
    #keithley_function()

