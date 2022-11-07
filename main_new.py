# -*- coding: utf-8 -*-
"""
Created on Thu Apr  7 15:24:06 2022

@author: ali.uzun
"""

import sys
#sys.path.append("\\\\fs1\\Docs2\\ali.uzun\\My Documents\\My Files\\Scripts\\Python\\III-V Scripts\\src\\")
import pandas as pd
import time

from Keithley26xx_GPIB import smu26xx
from Initialize_Connection import Initialize_GPIB
from Data_Analysis import Data_Analysis
from Newport_844_PE import Newport_844_PE
from Sweep_Function import IV_Sweep
from OpenFile import OpenFile
from Thorlab_USBPM100D import Thorlab_100D

fl = OpenFile()
da = Data_Analysis()

#####-------------- Keithley Settings -----------####
gpib_index = 0
addr = 26 # change it if necessery
addr = 28 # change it if necessery

####----------

def list_device_GPIB():
    initialize_connection = Initialize_GPIB()
    print(initialize_connection.get_device_list())
    initialize_connection.terminate_connection()
    

def newport_USBPM_test():
    newport_PM = Newport_844_PE()
    newport_ranges = ('AUTO', '30.0mW', '3.00mW', '300uW', '30.0uW', '3.00uW', '300nW', '30.0nW')
    rindex = 0
    newport_PM.set_range(rindex)
    
    for i in range(10):
        data = newport_PM.get_data()
        print(data)
    #print(type(data))
    newport_PM.close_connection()

def thorlab_PM100D_test():
    thorlab_PM = Thorlab_100D()
 
    # Open connection
    thorlab_PM.Initialize_connection()

    
    # # get power reading
    for i in range(5):
        data = thorlab_PM.get_power_reading()
        print(data)
         
    #close connection
    thorlab_PM.close_connection()
    
def keithley_test():
    initialize_connection = Initialize_GPIB()
    #gpib_index = 0
    #addr = 26 # change it if necessery
    inst = initialize_connection.connect_device(gpib_index, addr) # connect to device#

    # create an object
    keithley_GPIB =  smu26xx(inst)
    #keithley_GPIB.set_display("a", "DCAMPS") #DCVOLTS, DCAMPS
    
    keithley_GPIB.set_mode("a","DCAMPS")
    
    

def keithley_function():
    initialize_connection = Initialize_GPIB()
    #gpib_index = 0
    #addr = 26 # change it if necessery
    inst = initialize_connection.connect_device(gpib_index, addr) # connect to device#

    # create an object
    keithley_GPIB =  smu26xx(inst)
    keithley_GPIB.set_limit("a", "v", 3)
    #keithley_GPIB.reset("b")
    keithley_GPIB.turn_ON_ChA() 
    # set_cur = 20
    # keithley_GPIB.set_current_ChA(set_cur*1e-3)
    keithley_GPIB.turn_OFF_ChA()
    

def probe_alingmment_test():
    initialize_connection = Initialize_GPIB()
    #gpib_index = 0
    #addr = 26 # change it if necessery
    inst = initialize_connection.connect_device(gpib_index, addr) # connect to device#

    # create an object
    keithley_GPIB =  smu26xx(inst)
    
    # data = newport_PM.get_power_reading()
    
    keithley_GPIB.set_limit("a", "v", 3)
    keithley_GPIB.turn_ON_ChA()
    set_cur = 50
    keithley_GPIB.set_current_ChA(set_cur*1e-3)
    
    
    for i in range(200):
         time.sleep(0.3)
         data = keithley_GPIB.get_current_ChB()
         #data = newport_PM.get_power_reading()
    
         print(data)
    #time.sleep(50)
    keithley_GPIB.turn_OFF_ChA()
    keithley_GPIB.turn_OFF_ChB()
    # newport_PM.close_connection()
    return()
     


def plot_sweep(filename, full_path):
    x_label = "Current (mA)"
    y_label1 = "Voltage (V)"
    y_label2 = "Optical Power (W)"

    plot_title = filename
  
    I,V,P = fl.read_csv_file(full_path)
    P = P*1e0
    da.plot_LIV(I, V, P, x_label, y_label1, y_label2, plot_title)
    


   
    
    #plt_name = full_path.split(".")[0]
    #da.save_plot(plt_name)
    
def plot_sweep_IV(filename, full_path):
    x_label = "Current (mA)"
    y_label1 = "Voltage (V)"
    y_label2 = "Optical Power (W)"

    plot_title = filename
    df = pd.read_csv(full_path)
    df.columns = ['Current', 'Voltage']
    
    I = df['Current']*1e0
    V = df['Voltage']


    #I,V = fl.read_csv_file(full_path)
    da.plot_XY(I, V, x_label, y_label1, plot_title)


def main():

    initialize_connection = Initialize_GPIB()
    inst = initialize_connection.connect_device(gpib_index, addr) # connect to device#

    # create an object
    keithley_GPIB =  smu26xx(inst)
    save_data = OpenFile()
    
    newport_PM = Newport_844_PE()

    sweep_function = IV_Sweep(initialize_connection, keithley_GPIB, save_data, newport_PM)

    #filename = "L-TT2-D1-R2do5960_1.5mm_1pMIR_RW_3um_MIR_6.5x52um_Keithley_ChB.csv"
    power_reading_from = ["Newport_PM", "Keithley_ChB","Other"] # 0 or 1
    power_index = 1 # 0 or 1

    #filename = "220712_QDLdo6209R2_BCBSi_1.8mm_RWxum_1pMIR_XxXum_Dev2_20C.csv"
    
    #_Ref_Attenuator884UVR
    filename = "DFB-1_Cleaved_Facet_Chip4_CL1.8mm_5deg_A5_dev3_r2_%s_.csv" % power_reading_from[power_index]
    filename = "221013_Au3bQ3_CF_RW3.5um_CL2mm_%s_T90C_r1.csv" % power_reading_from[power_index]
    
    measurement_base_path = "\\\\FS1\\Docs2\\ali.uzun\\My Documents\\My Files\\Measurements\\Caladan\\Caladan 22\\"
    save_to_folder = "20220628 3um Si ridge WG\\220701 After Glue Drop\\"
    save_to_folder = "2022-07-07 AU3bQ3 QDL\\AU-2276-Si\\"
    save_to_folder = "AU3bQ4\AU-220711-BCBSi\\"
    save_to_folder = "Run-2 do6209\SiBCB-2\\2022-07-12 do6209 QDL\\"
    save_to_folder = "Caladan SOI\\2022-07-19 AU2-1 SOI11\\"
    save_to_folder = "2022-July AU3bQ3\\2022-10-07\\"
    save_to_folder = "DFB Laser\\DFB-1\\2022-10-18\\"
    #save_to_folder = "2022-July AU3bQ4\\2022-10-13\\"
    save_to_folder = "2022-July AU3bQ3\\2022-10-19 CF 2mm\\"
    
    full_path = measurement_base_path + save_to_folder + filename
    
    #filename = "A3473PO-LR3-FP2.csv"
    #full_path = "\\\\FS1\\Docs2\\ali.uzun\\My Documents\\My Files\\Measurements\\Fatih\\2022-07-22 LIV\\%s" % filename
    
    print(full_path)

    # header for csv file: first column, second column, third column
    header = ["Current (mA)", "Voltage (V)", "Power (mW)"]

    

    voltage_limit = 3 # V
    start_value = 0
    stop_value = 400 #mA
    step_size = 2 #mA
    
    LIV_sweep = True # True is LIV sweep. False IV
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
        plot_sweep(filename, full_path)
    else:
        plot_sweep_IV(filename, full_path)
    
    inst.close()


if __name__ == "__main__":
    main()
    
    #list_device_GPIB()
    #keithley_function()
    #probe_alingmment_test()
    #keithley_test() 
    #get_current_In_ChB  ()  
    #plot_test()
    #keithley_test()
    #newport_USBPM_test()
    #thorlab_PM100D_test()
    #get_current_In_ChB()
    #keithley_function()

