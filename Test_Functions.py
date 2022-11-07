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
    
def keithley_test(gpib_index,addr):
    initialize_connection = Initialize_GPIB()
    #gpib_index = 0
    #addr = 26 # change it if necessery
    inst = initialize_connection.connect_device(gpib_index, addr) # connect to device#

    # create an object
    keithley_GPIB =  smu26xx(inst)
    #keithley_GPIB.set_display("a", "DCAMPS") #DCVOLTS, DCAMPS
    
    keithley_GPIB.set_mode("a","DCAMPS")
    
    

def keithley_function(gpib_index,addr):
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
    

def probe_alingmment_test(gpib_index,addr):
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
     


  
