

# -*- coding: utf-8 -*-
"""
Created on Thu Dec 30 17:53:25 2021

@author: yeasir.arafat
"""

######################################################################################
"User Input variables"
Keithley_GPIB_Addr = 26
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
from TLPM import TLPM

# Open Visa connections to instruments

rm = pyvisa.ResourceManager()
keithley = rm.open_resource(  'GPIB1::' + str(Keithley_GPIB_Addr)  )

keithley.write("*RST") #Resetting the instrument
#print("reset the instrument")

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

tlPM.close()

tlPM = TLPM()
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
time.sleep(1)
#set the wavelength to be measured
wavelength = c_double(1950)
wl = tlPM.setWavelength(wavelength)
print(wl)


# wavelength = c_double()
# TLPM_ATTR_SET_VAL = c_int16(1)
# wl = tlPM.getWavelength(TLPM_ATTR_SET_VAL, byref(wavelength))
# print(wl)




time.sleep(1)




#set to current source, voltage meas

keithley.write(":SOUR:FUNC CURR")
keithley.write(":SOUR:CURR:VLIM " + str(Max_voltage)) 
keithley.write(":SENS:FUNC 'VOLT'")
keithley.write(":SENS:VOLT:RANG:AUTO ON")
keithley.write(":OUTPut:STAT ON")   

######################################################################################
"Loop to sweep"
power_measurements = []
times = []
Voltage=[]
Current = []
Power = []
for I in N.linspace(start, stop, num=numpoints, endpoint=True):
    print("Current set to: " + str(I) + " A" )
    Current.append(I)   #Storing the set current vaue to Voltage
    keithley.write(":SOUR:CURR " + str(I))
    time.sleep(1)    # add second between
    
    data = keithley.query(":READ?")   #returns string with many values (V, I, ...)
    answer = data.split(',')    # remove delimiters, return values into list elements
    V = eval( answer.pop(0) )
    Voltage.append(V)
    print("Voltage = " + str(Voltage[-1]) + ' V')   # print last read value
    
    power =  c_double()
    tlPM.measPower(byref(power))
    power_measurements.append(power.value)
    times.append(datetime.now())
    print(power.value)
    
#end for(I)
keithley.write(":OUTP OFF")     # turn off the output

#keithley.write("SYSTEM:KEY 23") # go to local control

#Closing all instruments
keithley.close()
#power_meter.Close()
tlPM.close()
######################################################################################

''' SAVE CSV FILE'''


#Getting date/time for info file
Date = "Date of test = "
Time = "Time of test = "

#Saving File

index = 0
with open(file_name + ".csv", 'w', newline='') as csvfile:
    
    fieldnames =['Current (A)', 'Voltage (V)', 'Power (W)'] #setting the row titles
    
    thewriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    thewriter.writeheader()
    
    for currents in Current:
        
        powers = power_measurements[index]
        voltages= Voltage[index]
        thewriter.writerow({'Current (A)':currents, 'Voltage (V)': voltages, 'Power (W)':powers}) #adding lists to rows
        index = index + 1

#plot VI and LI curves
plt.figure(1)
plt.plot(Current, Voltage, 'o-')
plt.xlabel('Current(A)')
plt.ylabel('Voltage(V)')
plt.grid(True, alpha=0.5)
plt.savefig(file_name + "_IV.png",dpi=600) #plt.savefig('figure name.type',dpi=resulution)
plt.show()

plt.figure(2)
plt.plot(Current, power_measurements, 'o-')
plt.xlabel('Current(A)')
plt.ylabel('Power(W)')
plt.grid(True, alpha=0.5)
plt.savefig(file_name + "_LI.png",dpi=600) #plt.savefig('figure name.type',dpi=resulution)
plt.show()