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
from src.PM_Newport_844PE import Newport_844_PE
from src.PM_Thorlab_USBPM100D import Thorlab_100D

from src.Data_Analysis import Data_Analysis
from src.OpenFile import OpenFile
from src.Sweep_Function import IV_Sweep
from src.Wavelength_Sweep_1300nmLS import WL_Sweep

from src.MyPlots import MyPlots
import Test_Functions as TF

from src.TLPM import TLPM
from ctypes import   c_uint32,byref,create_string_buffer,c_bool,c_char_p,c_int,c_int16,c_double, sizeof, c_voidp

fl = OpenFile()
da = Data_Analysis()

myplt = MyPlots()

#####-------------- Keithley Settings -----------####
gpib_index = 0
addr = 26 # change it if necessery
#addr = 28 # change it if necessery
    

##### ------ INPUTs -------- #####

# ----- YOUR BASE DIRECTORY ---------
measurement_base_path = r'\\FS1\Docs2\ali.uzun\My Documents\My Files\Measurements\Caladan\Caladan 23' 
# ----- FOLDER UNDER BASE DIRECTORY --------- 
save_to_folder = r"2023-05-02 QDL Run N-Metal" 
# save_to_folder = r"Test" 
# save_to_folder = r"2023-01-31 MTP4"
# save_to_folder = r"Test"
#save_to_folder = r"DFB Laser\DFB-1\2022-11-24 Chip4 1.8-1.9mm" 

power_reading_from = {0:"Keithley",1:"Newport_PM", 2:"Thorlab_PM", 3:"None"} # power meeter for optical power reading
# 0 for Keithley_ChB, 1 for Newport_PM, 2 for Thorlab_PM 
power_index = 3  # 0 - 1 - 2

select_sweep_type = {0:"LIV",1:"IV", 2:"VI"}
# 0 for LIV, 1 for IV, 2 for VI 
sweep_index = 1 # 0 - 1 - 2

####------- Responsivity of Newport 818IR detector
R = 0.67 # Calibrated on 03-11-2022
#R = 1
#R = 0.72 

#filename = "Run2-do6209_CF-Laser_CL-2mm_RW-2.5um_%s_Photocurrent_r1.csv" % power_reading_from[power_index]

filename = "AU2eQ1-Top N-Metal TLM_R-175um_IV-Sweep_Ring-1"
#filename = "AU2eQ1-Probe-TEST-on-same-metal-IV-2"
filename = "TEST"

file_record_index = 1

if(power_index == 0):
    filename = filename + "_%s_R-%s_r%s.csv" % (power_reading_from[power_index],str(R),str(file_record_index))
else:
    filename = filename + "_r%s.csv" % str(file_record_index)


#filename = "test_file.csv"

file_directory = measurement_base_path + "\\"+ save_to_folder + "\\" # Folder the filde will be saved
full_path = file_directory + filename # full path for file

print(full_path)


#### ----- CURRENT SWEEP SETTINGS ---------
voltage_limit = 4.50 # V
current_start_value = -100
current_stop_value = 100 #mA
current_step_size = 2 #mA


#### ----- VOLTAGE SWEEP SETTINGS ---------
current_limit = 100 # mA
voltage_start_value = -1
voltage_stop_value = 1 # V
voltage_step_size = 0.05 # V

#### -- wavelength for Thorlab PM
wavelength = 1200 # nm


#### --------- INPUTs ------ #####

def wavelength_sweep():
    gpib_index = 0
    addr = 22 # change it if necessery
    initialize_connection = Initialize_GPIB()
    tuneable_laser_GPIB = initialize_connection.connect_device(gpib_index, addr) # connect to device#

    # create an object
    tuneable_laser_GPIB =  smu26xx(tuneable_laser_GPIB)
    save_data = OpenFile()
    
    newport_PM = Newport_844_PE()
    thorlab_PM = Thorlab_100D(wavelength)

    sweep_function = WL_Sweep(initialize_connection, tuneable_laser_GPIB, save_data, newport_PM)

    header = ["Wavelength (nm)", "Optical Power (dBm)"]
    #### -----
    wl_start_value = 1260 # in nm
    wl_stop_value = 1330
    wl_step_size = 1
    #### -----
    sweep_function.wavelength_sweep_1300nmLS(filename, header, wl_start_value, wl_stop_value, wl_step_size)

def main(): #voltage_limit,start_value,stop_value,step_size

    initialize_connection = Initialize_GPIB()
    keithley_inst = initialize_connection.connect_device(gpib_index, addr) # connect to device#

    # create an object
    keithley_GPIB =  smu26xx(keithley_inst)
    save_data = OpenFile()
    #newport_PM = Newport_844_PE()
    newport_PM = None
    thorlab_PM = None
    if (power_reading_from[power_index] != "Keithley_ChB"):
        
        try: newport_PM = Newport_844_PE()
        except:
            NameError
            print("Newport PM is NOT connected !!!!!")
        
        try: 
            thorlab_PM = Thorlab_100D()
            #resetting wavlength by a random value
            # tlPM = TLPM()
            # wavelength = c_double(1310)
            # wl = tlPM.setWavelength(wavelength)
            # print(wl)
            # time.sleep(0.2)
            # #set the wavelength to be measured !!!!
            # wavelength = 1550
            # wavelength = c_double(wavelength)
            # wl = tlPM.setWavelength(wavelength)
            # print(wl)
            # tlPM.close()
        except:
            NameError
            print("Thorlab PM is NOT connected !!!!!")
               
        
    sweep_function = IV_Sweep(initialize_connection, keithley_GPIB, save_data, newport_PM, thorlab_PM)

    
    if(R == 1):
        header = ["Current (mA)", "Voltage (V)", "Photocurrent (A)"]
    else:  
        header = ["Current (mA)", "Voltage (V)", "Power (W)"]

    
        
    if (select_sweep_type[sweep_index] == "LIV"): # sweep current on ChA, reads voltage. Power readings are from selected power meter
        
        keithley_GPIB.keithley_current_mode("a", display = "DCVOLTS")
        
        if (power_reading_from[power_index] == "Newport_PM"):
            
            #newport_ranges = ('AUTO', '30.0mW', '3.00mW', '300uW', '30.0uW', '3.00uW', '300nW', '30.0nW')
            #rindex = 2
            # newport_PM.set_range(rindex)
            sweep_function.LIV_sweep_PM(full_path, header, power_reading_from[power_index],
                                               start_value = current_start_value, stop_value = current_stop_value, step_size = current_step_size, voltage_limit = voltage_limit)
        if (power_reading_from[power_index] == "Thorlab_PM"):
            

            sweep_function.LIV_sweep_PM(full_path, header, power_reading_from[power_index],
                                               start_value = current_start_value, stop_value = current_stop_value, step_size = current_step_size, voltage_limit = voltage_limit)
        
        elif (power_reading_from[power_index] == "Keithley"):
            #current_ranges = [1E-7, 1E-6, 1E-5, 1E-4, 1E-3, 1E-2, 1E-1, 1, 1.5]
            #rg = 1E-1 # keithley channel range
            #keithley_GPIB.set_range_ChB(rg)

            # Responsivity of Detector (A/W), 818IR Ge Detector
            

            sweep_function.LIV_sweep_KeithleyChB(full_path, header, R, 
                                                 start_value = current_start_value, stop_value = current_stop_value, step_size = current_step_size, voltage_limit = voltage_limit)
        else:
            print("No power source selected !!!!!")
        
        ###----------------- plot the sweep -------------
        x_min, x_max =0, 1
        y_min, y_max = 0, 4
        auto_range_xy = False
        #plot_sweep(filename, full_path)
        x_label = "Current (mA)"
        y_label_Left = "Voltage (V)"
        y_label_right = "Optical Power (W)"

        I,V,P = fl.read_csv_file(full_path)
        #P = P*1e0
        file_path = file_directory
        myplt.plot_LIV(file_path, filename, I, V, P, x_label, y_label_Left, y_label_right,x_min, x_max,y_min, y_max,auto_range_xy)



    elif (select_sweep_type[sweep_index] == "IV"): # sweep current on ChA and reads voltage
        keithley_GPIB.keithley_current_mode("a", display = "DCVOLTS")
        header = ["Current (mA)", "Voltage (V)"]
        sweep_function.IV_sweep(full_path, header, 
                                start_value = current_start_value, stop_value = current_stop_value, step_size = current_step_size, voltage_limit = voltage_limit)
        
        ###----------------- plot the sweep -------------
        x_label = "Current (mA)"
        y_label_Left = "Voltage (V)"
        
        x_min, x_max =0, 1
        y_min, y_max = 0, 5
  
        I,V,P = fl.read_csv_file(full_path)
        #P = P*1e0
        file_path = file_directory
        figname = filename
        myplt.plot_IV(file_path,figname, I, V, x_label, y_label_Left, x_min, x_max,y_min, y_max,auto_range_xy = False)
    
    elif (select_sweep_type[sweep_index] == "VI"): # sweep voltage on ChA, reads current
        header = ["Voltage (V)","Current (mA)"]
        # set the keithley voltahe mode and read current
        #Voltage range 40V, Curruent range to 100mA
        keithley_GPIB.keithley_voltage_mode("a", display = "DCAMPS")


        sweep_function.VI_sweep(full_path, header, 
                                start_value = voltage_start_value, 
                                stop_value = voltage_stop_value, 
                                step_size = voltage_step_size, 
                                current_limit = current_limit)
        ###----------------- plot the sweep -------------
        
        x_label = "Voltage (V)"
        y_label = "Current (mA)"
        
        x_min, x_max =0, 1
        y_min, y_max = 0, 5
  
        I,V,P = fl.read_csv_file(full_path)
        #P = P*1e0
        file_path = file_directory
        figname = filename
        myplt.plot_IV(file_path,figname, I, V, x_label, y_label, x_min, x_max,y_min, y_max,auto_range_xy = False)
    

    else: 
        print(" No sweep selected !!!")

    
            
    
    keithley_inst.close()


if __name__ == "__main__":
    main()
    
    #TF.list_device_GPIB()
    #TF.keithley_setVoltageChA(gpib_index,addr)
    #TF.probe_alingmment_test(gpib_index,addr)
    #TF.keithley_setVoltageChA(gpib_index,addr) 
    #get_current_In_ChB  ()  
    #plot_test()
    #keithley_test()
    #newport_USBPM_test()
    #TF.thorlab_PM100D_test()
    #get_current_In_ChB()
    #keithley_function()
    
    #TF.keithley_change_mode(gpib_index, addr)

