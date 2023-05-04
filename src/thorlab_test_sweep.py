
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 30 17:53:25 2021

@author: yeasir.arafat
"""

######################################################################################
"User Input variables"
Keithley_GPIB_Addr = 28
file_name = 'Sweep_GaSb_laser'
start = 0e-3     # starting value of Current sweep
stop = 100e-3     # ending value 
numpoints = 21  # number of points in sweep
Max_voltage= 3.0 # Max reading voltage

#######################################################################################

"Open Instrument and set in Voltage source Mode"

import pyvisa        # PyVISA module, for GPIB comms
import numpy as N    # enable NumPy numerical analysis
import time          # to allow pause between measurements
import os            # Filesystem manipulation - mkdir, paths etc.
import matplotlib.pyplot as plt # for python-style plottting, like 'ax1.plot(x,y)'
import win32com.client
import csv
from datetime import datetime
from ctypes import   c_uint32,byref,create_string_buffer,c_bool,c_char_p,c_int,c_int16,c_double, sizeof, c_voidp
from src.TLPM import TLPM

from src.Keithley26xx_GPIB import smu26xx
from src.Initialize_Connection import Initialize_GPIB
from src.Newport_844_PE import Newport_844_PE
#from Thorlab_USBPM100D import Thorlab_100D

from src.OpenFile import OpenFile

import pandas as pd
import matplotlib.pyplot as plt

fl = OpenFile()

#Connecting Power Meter

tlPM = TLPM()
deviceCount = c_uint32()
tlPM.findRsrc(byref(deviceCount))

print("devices found: " + str(deviceCount.value))

resourceName = create_string_buffer(1024)

for i in range(0, deviceCount.value):
    tlPM.getRsrcName(c_int(i), resourceName)
    print(c_char_p(resourceName.raw).value)
    break

# tlPM.close()

# tlPM = TLPM()
#resourceName = create_string_buffer(b"COM1::115200")
#print(c_char_p(resourceName.raw).value)
tlPM.open(resourceName, c_bool(True), c_bool(True))

message = create_string_buffer(1024)
tlPM.getCalibrationMsg(message)
print(c_char_p(message.raw).value)

#resetting wavlength by a random value
wavelength = c_double(1800)
wl = tlPM.setWavelength(wavelength)
print(wl)
time.sleep(0.2)
#set the wavelength to be measured
wavelength = 1500
wavelength = c_double(wavelength)
wl = tlPM.setWavelength(wavelength)
print(wl)



#####-------------- Keithley Settings -----------####
gpib_index = 0
addr = 28 # change it if necessery

initialize_connection = Initialize_GPIB()
#gpib_index = 0
#addr = 26 # change it if necessery
inst = initialize_connection.connect_device(gpib_index, addr) # connect to device#

# create an object
keithley_GPIB =  smu26xx(inst)
save_data = OpenFile()
#def LIV_sweep_KeithleyChB(self, filename, header, R, start_value, stop_value, step_size, voltage_limit = 3): 
"""
Sweep current in channel A and measure volatage, get current reading from channel B 
It could be photocurrent reading in which photodetector directly connected to Channel B of Keithley
Or Analog Out of Power meter connedted to channel B of Keithley.

R: responsivity of photodetector (0.65 for 818 IR Ge Detector)
header: [Current, Voltage, Power]
start_value = (Integer) Current sweep start ie. 0 
stop_value = (Iteger) Current sweep stop value ie. 100 for 100mA 

"""

power_reading_from = ["Newport_PM", "Keithley_ChB","Thorlab_PM"] # 0 or 1
power_index = 2 # 0 or 1

# filename = "220713_QDLdo6209R2_BCBSi_1.5mm_RW2.5um_1pMIR_6.5x52um_Dev4_%s_0C.csv"%power_reading_from[power_index]

#_Ref_Attenuator884UVR

filename = "221103_Au2Q1_do6209_1pMIR_CL1.5mm_RW2.5um_MIR-6.5X54um-TD2_%s_r1.csv" % power_reading_from[power_index]
filename = "Test.csv"
filename = "Run2-do6209_CF-Laser_CL-1mm_RW-2.5um_%s_r1.csv" % power_reading_from[power_index]


measurement_base_path = "\\\\FS1\\Docs2\\ali.uzun\\My Documents\\My Files\\Measurements\\Caladan\\Caladan 22\\"

#save_to_folder = "20220628 3um Si ridge WG\\220708 AU-2276-3umSOI-C2 AU3bQ3\\"
save_to_folder = "Run-2 do6209\\2022-12-19\\"

full_path = measurement_base_path + save_to_folder + filename
print(full_path)

# header for csv file: first column, second column, third column
header = ["Current (mA)", "Voltage (V)", "Power (mW)"]

f = open('%s' % full_path, 'w', newline='')
writer = csv.writer(f)
# write the data
writer.writerow(header)

voltage_limit = 3 # V
start_value = 0
stop_value = 0 #mA
step_size = 2 #mA

        
#sweep_function.LIV_sweep_NewportPM(full_path, header, start_value=start_value, stop_value=stop_value, step_size=step_size, voltage_limit = voltage_limit)
        
keithley_sleep_time = 0.2
R = 1

keithley_GPIB.set_limit(channel = "a", unit = "v", value = voltage_limit)

save_data.save_to_csv_file(filename,header, header_flag=True) # add the header for file
value_i = start_value
while value_i <= stop_value:
    
    # print("Set value is %f %s \n" % (value, unit))
    keithley_GPIB.set_current_ChA(value_i*1e-3)
    #keithley_GPIB.set_voltage_ChA(value_i)
    
    keithley_GPIB.turn_ON_ChA()       
    time.sleep(keithley_sleep_time)
        
    #currenta = self.keithley_GPIB.get_current_ChA()
    voltagea = keithley_GPIB.get_voltage_ChA()

    time.sleep(0.2)

    power =  c_double()
    tlPM.measPower(byref(power))
    power_reading = power.value
    
           
    print("I=%s mA, V=%s V, P=%s \n" %(value_i, voltagea, power_reading))    

    data = [value_i, voltagea,  power_reading ]
    
    f = open('%s' % full_path, 'a', newline='')
    writer = csv.writer(f)
    # write the data
    writer.writerow(data)

    value_i = value_i + step_size      

#print threshold
# {k: v for k, v in sorted(threshold.items(),reverse=True, key=lambda item: item[1])}

keithley_GPIB.set_voltage_ChA(0)   
keithley_GPIB.set_current_ChA(0) 

# keithley_GPIB.set_voltage_ChB(0) 
# keithley_GPIB.set_current_ChB(0)  

# turn OFF channels 
keithley_GPIB.turn_OFF_ChA()       
# keithley_GPIB.turn_OFF_ChB()

#self.initialize_connection.terminate_connection()
# close the file
f.close()
    
    

#power_meter.Close()
tlPM.close()
######################################################################################

x_label = "Current (mA)"
y_label1 = "Voltage (V)"
y_label2 = "Optical Power (mW)"

plot_title = filename
df = pd.read_csv(full_path)
df.columns = ['Current', 'Voltage', 'Power']

I = df['Current']*1e0
V = df['Voltage']
P = df['Power']*1e3 # mW

line_color_1 = "red"
line_color_2 = "blue"
label_fontsize = 12

fig,ax = plt.subplots()
    
plt.title(plot_title)
# make a plot
ax.plot(I, V, color = line_color_1)
# set x-axis label
ax.set_xlabel(x_label, fontsize=14)
# set y-axis label
ax.set_ylabel(y_label1, color = line_color_1, fontsize = label_fontsize)

# twin object for two different y-axis on the sample plot
ax2=ax.twinx()
# make a plot with different y-axis using second axis object
ax2.plot(I, P, color = line_color_2)
ax2.set_ylabel(y_label2, color = line_color_2, fontsize = label_fontsize)

plt.grid(True)
plt.show() 
