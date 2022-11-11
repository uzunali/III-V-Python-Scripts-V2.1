# -*- coding: utf-8 -*-
"""
Created on Fri Dec 17 12:15:06 2021

@author: ali.uzun
"""

from datetime import datetime
from ctypes import cdll,c_long, c_ulong, c_uint32,byref,create_string_buffer,c_bool,c_char_p,c_int,c_int16,c_double, sizeof, c_voidp
from src.TLPM import TLPM
import time

class Thorlab_100D():
    def __init__(self):
        
        #self.resourceName = create_string_buffer(1024)
        self.tlPM = None
        pass
              
            
    def Initialize_connection(self):
        self.tlPM = TLPM()
        deviceCount = c_uint32()
        self.tlPM.findRsrc(byref(deviceCount))
        
        print("devices found: " + str(deviceCount.value))
        
        self.resourceName = create_string_buffer(1024)

        for i in range(0, deviceCount.value):
            self.tlPM.getRsrcName(c_int(i), self.resourceName)
            print(c_char_p(self.resourceName.raw).value)
            print("Thorlab Initialize")
            break
        # tlPM.close()

        # tlPM = TLPM()
        #resourceName = create_string_buffer(b"COM1::115200")
        #print(c_char_p(resourceName.raw).value)
        self.tlPM.open(self.resourceName, c_bool(True), c_bool(True))
        
        message = create_string_buffer(1024)
        self.tlPM.getCalibrationMsg(message)
        print("Calibration Message !!!")
        print(c_char_p(message.raw).value)
        
        # #resetting wavlength by a random value
        # wavelength = c_double(1800)
        # wl = self.tlPM.setWavelength(wavelength)
        # print(wl)
        # time.sleep(1)
        # #set the wavelength to be measured
        # wavelength = 1300
        # wavelength = c_double(wavelength)
        # wl = self.tlPM.setWavelength(wavelength)
        # print(wl)
    
    def get_power_reading(self):
        #tlPM = TLPM()
        #self.tlPM.open(self.resourceName, c_bool(True), c_bool(True))
    
        time.sleep(0.5)
        power =  c_double()
        self.tlPM.measPower(byref(power))
        #power_measurements.append(power.value)
        #times.append(datetime.now())
        return(power.value)
    
    def close_connection(self):
    
        self.tlPM.close()
    
    def set_wavelength(self, wavelength):
        tlPM = TLPM()
        tlPM.open(self.resourceName, c_bool(True), c_bool(True))
        
        # wavelength = c_double(wavelength)
        # tlPM.setWavelength(byref(wavelength))
        
        
        #resetting wavlength by a random value
        wlt = c_double(1500)
        wl = tlPM.setWavelength(wlt)
        print(wl)
        time.sleep(0.2)
        #set the wavelength to be measured
        wavelength = c_double(wavelength)
        wl = tlPM.setWavelength(wavelength)
        print(wl)
    
        tlPM.close()
        
    def get_wavelength(self):
        tlPM = TLPM()
        tlPM.open(self.resourceName, c_bool(True), c_bool(True))
        
        wavelength = c_double()
        TLPM_ATTR_SET_VAL = c_int16(0)
        wl = tlPM.getWavelength(byref(TLPM_ATTR_SET_VAL,wavelength))
        print(wl)
    
        tlPM.close()
    
    def v1(self):
        
        tlPM = TLPM()
        #resourceName = create_string_buffer(b"COM1::115200")
        #print(c_char_p(resourceName.raw).value)
        resourceName = create_string_buffer(1024)
        tlPM.open(resourceName, c_bool(True), c_bool(True))
        
        message = create_string_buffer(1024)
        tlPM.getCalibrationMsg(message)
        print(c_char_p(message.raw).value)
        
        wavelength = c_double(1500)
        tlPM.setWavelength(byref(wavelength))
        
        # # set current range
        # current_to_Measure = c_double(1)
        # tlPM.setCurrentRange(current_to_Measure)
        
        time.sleep(5)
        
        power_measurements = []
        times = []
        count = 0
        while count < 20:
            power =  c_double()
            tlPM.measPower(byref(power))
            power_measurements.append(power.value)
            times.append(datetime.now())
            print(power.value)
            count+=1
            time.sleep(1)
        
        wavelength = c_double()
        TLPM_ATTR_SET_VAL = c_int16(0)
        tlPM.getWavelength(byref(TLPM_ATTR_SET_VAL,wavelength))
        
        tlPM.close()
        print('End program')
