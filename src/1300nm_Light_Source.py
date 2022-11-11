#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   Ali Uzun 
@Created On    :   2022/11/11 13:10:31
@Version :   1.0
'''

# here put the import lib
import pyvisa 
import time

class LS1300nm():

    def __init__(self,inst):
        self.inst = inst
    
    def get_instrument_info(self):
        #Creating instrument info for info file 
        tune_laser_info = 'TUNEABLE LASER = ' + self.inst.query("*IDN?")
    
    def set_laser_power(self, power_unit):
        #Sets unit for power
        # Can set W, MW, UW, NW, PW, DBM, DBMW ...
        self.inst.write(":POW:UNIT " + power_unit)

    def set_wavelength(self, wavelength):
        self.inst.write(":WAVE " + str(wavelength) + "nm") #changing wavelength on laser

    def turn_ON(self):
        self.inst.write(":OUTP ON")

    def turn_OFF(self):
        self.inst.write(":OUTP OFF")
     

    


