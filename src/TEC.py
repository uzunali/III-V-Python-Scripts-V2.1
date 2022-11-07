# -*- coding: utf-8 -*-
"""
Created on Wed Oct  5 14:12:36 2022

@author: ali.uzun
"""


import pyvisa 
import time
import pyvisa 
import numpy as np
import pandas as pd


rm = pyvisa.ResourceManager() 
rm.list_resources()
print (' Connected devices are ', rm.list_resources())
########################################################################
#
# Defining          Temp Loop
#                   Channel A Voltage Loop
#                   Channel B Current Loop
#
#                   Dataframe Format
#
#                   Filename
########################################################################

temp_range =(25, 30)

volt_CHa_START      =  0.20
volt_CHa_STOP      =   0.20 
volt_CHa_STEP      =   0.05

cur_CHb_START       = -0.15
cur_CHb_STOP        = 0.15
cur_CHb_STEP        = 0.005


Filename = 'INL_Row12Col1'
Result=pd.DataFrame()
########################################################################
#
# GPIB Access
#
########################################################################
keithley2510 = rm.open_resource('GPIB::15')

########################################################################
#
# Setting 2510 limits and reset
#
########################################################################
keithley2510.write('*RST')
keithley2510.write('UNIT:TEMP CEL')
keithley2510.write('SOUR:TEMP:PROT 100') 
keithley2510.write('SOUR:TEMP:PROT:LOW 10')
keithley2510.write('SENS:CURR:PROT 2')

########################################################################

        
########################################################################
#
# Setting PID for VCSEL setup
#
########################################################################

keithley2510.write('SOUR:TEMP:LCON 150')
keithley2510.write('SOUR:TEMP:LCON:INT 10') 
keithley2510.write('SOUR:TEMP:LCON:DER 00') 

########################################################################
#
# Setting TEMP and Settling within 0.1C boundary
#
########################################################################

for target_temp in temp_range:
    keithley2510.write('SOUR:TEMP '+ str(target_temp))
    keithley2510.write('OUTP ON')
    ####################################################################
    #
    # Setting TEMP and Settling within 0.1C boundary
    #
    ####################################################################
    temp=float(keithley2510.query('OUTPUT 15;:MEAS:TEMP?'))
    while (abs(target_temp-temp)>0.1):
        time.sleep(15)
        temp=float(keithley2510.query('OUTPUT 15;:MEAS:TEMP?'))
        print (target_temp,temp ,target_temp-temp)
        
########################################################################
#
# Turn off sources
#
########################################################################
  

keithley2510.write('OUTP OFF')   
      
  
keithley2510.write('OUTP OFF')