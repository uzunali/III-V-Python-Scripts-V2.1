# -*- coding: utf-8 -*-
"""
Created on Mon Dec 19 16:41:23 2022

@author: ali.uzun
"""



from datetime import datetime
from ctypes import cdll,c_long, c_ulong, c_uint32,byref,create_string_buffer,c_bool,c_char_p,c_int,c_int16,c_double, sizeof, c_voidp
from TLPM import TLPM
import time


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



# # set current range
# current_to_Measure = c_double(1)
# tlPM.setCurrentRange(current_to_Measure)

time.sleep(5)

power_measurements = []
times = []
count = 0
while count < 10:
    power =  c_double()
    tlPM.measPower(byref(power))
    power_measurements.append(power.value)
    times.append(datetime.now())
    print(power.value)
    count+=1
    time.sleep(0.2)

# wavelength = c_double()
# TLPM_ATTR_SET_VAL = c_int16(1)
# wl = tlPM.getWavelength(TLPM_ATTR_SET_VAL, byref(wavelength))
# print(wl)

# wavelength = c_double(1500)
# wl = tlPM.setWavelength(byref(wavelength))
# print(wl)

brightness = c_double(0)
tlPM.setDispBrightness(brightness)

tlPM.close()
print('End program')
