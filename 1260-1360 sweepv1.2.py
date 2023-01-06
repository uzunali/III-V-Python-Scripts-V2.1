"""
Created on Fri Dec 17 16:02:57 2021 @author: owen.moynihan
"""
import win32gui
import win32com.client
import traceback
import pyvisa 
import time
from datetime import date
from datetime import datetime
import csv
import getpass
import matplotlib.pyplot as plt
from datetime import date
from datetime import datetime


from src.Keithley26xx_GPIB import smu26xx
from src.Initialize_Connection import Initialize_GPIB

from src.OpenFile import OpenFile

gpib_index = 0
addr = 26 # change it if necessery
initialize_connection = Initialize_GPIB()
keithley_inst = initialize_connection.connect_device(gpib_index, addr) # connect to device#

# create an object
keithley_GPIB =  smu26xx(keithley_inst)

save_data = OpenFile()
    

'''SET START/END/INTERVAL WAVELENGTHS HERE'''
start_wl = 1250E-9
end_wl = 1360E-9
interval = 1E-9

'''SET POWER AND UNITS HERE''' #not working at the moment for some reason
Pow = 3

Pow_unit = 'DBM' # Can set W, MW, UW, NW, PW, DBM, DBMW ...

''' SET NAME OF CSV FILE'''
path = r"\\FS1\Docs2\ali.uzun\My Documents\My Files\Measurements\Caladan\Caladan 22\Caladan SOI\SOI-2"


'''AUTOMATION STARTS HERE: PLEASE DO NOT CHANGE WITHOUT APPROVAL'''

#creating empty list to take values
wavelengths = []
powers = []

#index used in for loop
index = 0

#changing wavelengths from floats to integers so they can be used in for loop
start_wl_x = start_wl*1E9
end_wl_x = end_wl*1E9
interval_x = interval*1E9

interval_x = int(interval_x) 
end_wl_x = int(end_wl_x)
start_wl_x = int(start_wl_x)

#Checking all connected devices
OphirCOM = win32com.client.Dispatch("OphirLMMeasurement.CoLMMeasurement")
DeviceList = OphirCOM.ScanUSB()
print(DeviceList)

rm = pyvisa.ResourceManager()
print(rm.list_resources())


#Opening tuneable laser source from GPIB
tune_laser = rm.open_resource('GPIB0::22::INSTR')

#Opening power supply
#power_supply = rm.open_resource('GPIB1::26::INSTR')

# #Opening Power Meter using Serial number and using channel (0-3)
# power_meter = OphirCOM.OpenUSBDevice('991112')
# channel = 0

# #Setting range to auto and measurement mode to Power (Check Ophir optoelectronics manual for indexing)
# OphirCOM.SetRange(power_meter, channel, 0)
# OphirCOM.SetMeasurementMode(power_meter, channel, 0)

#Opening tuneable laser source from GPIB
keithley_gpib = rm.open_resource('GPIB0::26::INSTR')

#Creating instrument info for info file 
tune_laser_info = 'TUNEABLE LASER = ' + tune_laser.query("*IDN?")
#power_supply_info = 'POWER SUPPLY = ' + power_supply.query("*IDN?")
#power_meter_info ='Power Meter = ' + str(OphirCOM.GetDeviceInfo(power_meter))

today = date.today()
now = datetime.now()
Time = now.strftime("%H:%M:%S")
print("Time =", Time)
info = ["Name of tester: " + getpass.getuser(), "Date: " + str(today) , "Time: " + str(Time) , tune_laser_info ]
#print(info)

#Sets unit for power
tune_laser.write(":POW:UNIT " + Pow_unit)
#Sets power for laser
#tune_laser.write(":POW " + str(Pow))
#Turns laser on
tune_laser.write(":OUTP ON")

#OphirCOM.StartStream(power_meter, channel)

bias_voltage = -0.0
# Turn ON Channel A and B
keithley_GPIB.turn_ON('a')
keithley_GPIB.turn_ON('b')
keithley_GPIB.set_voltage(channel = "a", voltage = bias_voltage)

fl = "AfterInfill_SOI11_1.5mmQDL-EF-RW5um_R-ST2-D2_WavelengthSweep_RoomLigthOFF_BiasVoltage %f V_Power % d dBm_r1.csv"% (bias_voltage,Pow)
file_name = path + "\\" +fl  #AUTOMATICALLY SETS AS CSV FILE
header = ["Wavelength (nm)", "Photocurrent (A)"]
f = open('%s' % file_name, 'w', newline='')
writer = csv.writer(f)
# write the data
writer.writerow(header)
#Starting sweep for wavelength and recording power everytime
for wl in range(start_wl_x, end_wl_x + 1, interval_x):
    tune_laser.write(":WAVE " + str(wl) + "nm") #changing wavelength on laser 
    wavelengths.append(wl) #adding wavelength to file
    
    #try if statement that if nothing try again
    time.sleep(0.3)
    power_reading = -1*keithley_GPIB.get_current("b")
    #if tuple is empty, wait until its not empty

    print(power_reading)
       
    powers.append(power_reading)
    
    data = [wl,  power_reading ]
    writer.writerow(data)
    #value_i = value_i + step_size 
    
   
f.close()

plt.plot(wavelengths, powers)
plt.title("Plot of " + str(file_name))
plt.xlabel('Wavelength (nm)')
plt.ylabel('Photocurrent (A)')


print(wavelengths)
print(powers)    
print(len(wavelengths))
print(len(powers))

#Turning the laser off    
tune_laser.write(":OUTP OFF")
    


#Saving info to info file
info_file = open(file_name + "_info" + ".txt","w")
info_file.writelines(info) 
info_file.close()       


#Closing out all instruments
tune_laser.close()
#power_supply.close()
#power_meter.close()
# OphirCOM.StopAllStreams() 
# OphirCOM.CloseAll()

keithley_GPIB.turn_OFF('a')
keithley_GPIB.turn_OFF('b')


#save_data.close_file()