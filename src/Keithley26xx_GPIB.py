# -*- coding: utf-8 -*-
"""
Created on Wed Nov  3 15:04:36 2021

@author: ali.uzun
"""
from src.Initialize_Connection import Initialize_GPIB


class smu26xx():
     # define strings that are used in the LUA commands
    CHANNEL_A = "a"
    CHANNEL_B = "b"
    # defines an arbitrary word; when used the program tries to access all available channels
    CHANNEL_ALL = "all"

    CURRENT_MODE = "DCAMPS"
    VOLTAGE_MODE = "DCVOLTS"

    DISPLAY_VOLTAGE = 'DCVOLTS'
    DISPLAY_CURRENT = 'DCAMPS'
    DISPLAY_RESISTANCE = 'OHMS'
    DISPLAY_POWER = 'WATTS'

    SENSE_MODE_2_WIRE = 'SENSE_LOCAL'
    SENSE_MODE_4_WIRE = 'SENSE_REMOTE'

    UNIT_VOLTAGE = "v"
    UNIT_CURRENT = "i"
    UNIT_CURRENT_VOLTAGE = "iv"
    UNIT_POWER = "p"
    UNIT_RESISTANCE = "r"

    STATE_ON = "ON"
    STATE_OFF = "OFF"

    SPEED_FAST = 0.01
    SPEED_MED = 0.1
    SPEED_NORMAL = 1
    SPEED_HI_ACCURACY = 10


    def __init__(self,inst):
        self.inst = inst

    def smu_write(self,cmd):
        self.inst.write(cmd)
    
    def get(self, function, cmd):
        self.inst.query("print(voltage)")


    def set_current(self,channel, current):
        """
        Parameters
        ----------
        channel : String
            a or b.
        current : integer
            current in mA.

        Returns
        -------
        None.

        """
        query = f"smu{channel}.source.leveli={current}"
        self.inst.write(query)
        # return query
    
    def set_voltage(self,channel, voltage):
        """
        Parameters
        ----------
        channel : String
            a or b.
        current : integer
            current in V.

        Returns
        -------
        None.
        """
        query = f"smu{channel}.source.levelv={voltage}"
        self.inst.write(query)
        # return query
    
    # def get_current(self, channel):
    #     self.inst.write(f"current = smu{channel}.measure.i()")
        
    #     cmd = self.inst.query("print(current")
    #     current = float(cmd)
        
    #     return current
    
    def get_voltage(self, channel):
        self.inst.write(f"voltage = smu{channel}.measure.v()")
        
        # inst.write("smua.source.output=smua.OUTPUT_OFF") 
        voltage = float(self.inst.query("print(voltage)"))
        return(voltage)    
    
    def get_current(self, channel):
        self.inst.write(f"current = smu{channel}.measure.i()") 
        # inst.write("smua.source.output=smua.OUTPUT_OFF") 
        current = float(self.inst.query("print(current)"))
        
        return current
    
    # def set_current_ChB(self,current):
    #     query = "smub.source.leveli=%f" % current
    #     self.inst.write(query)
    
    # def set_voltage_ChB(self,voltage):
    #     query = "smub.source.levelv=%f" % voltage
    #     self.inst.write(query)
    

    
    # def get_voltage_ChB(self):
    #     self.inst.write("voltage = smub.measure.v()")
    #     # inst.write("smua.source.output=smua.OUTPUT_OFF") 
    #     voltage = float(self.inst.query("print(voltage)"))
    #     return voltage
    def turn_ON(self, channel):
        #cmd = 'smu' + str(channel) + '.source.output = smu' + str(channel) + '.OUTPUT_ON'
        cmd = f'smu{channel}.source.output = smu{channel}.OUTPUT_ON'
        self.inst.write(cmd)
        #self.inst.write("smu{channel}.source.output = smu{channel}.OUTPUT_ON")
        
    def turn_OFF(self, channel):
        #cmd = 'smu' + str(channel) + '.source.output = smu' + str(channel) + '.OUTPUT_ON'
        cmd = f'smu{channel}.source.output = smu{channel}.OUTPUT_OFF'
        self.inst.write(cmd)
    
    def turn_ON_ChA(self):
        self.inst.write("smua.source.output = smua.OUTPUT_ON")
    
    def turn_OFF_ChA(self):
        self.inst.write("smua.source.output = smua.OUTPUT_OFF")
    
    
    def turn_ON_ChB(self):
        self.inst.write("smub.source.output = smub.OUTPUT_ON")
    
    def turn_OFF_ChB(self):
        self.inst.write("smub.source.output = smub.OUTPUT_OFF")

    def set_limit(self, channel, unit, value):
        """
        command used to set the limits for voltage, current or power
        channel: a, b
        unit: volate-v, current-i
        """
        # send the command to the SourceMeter
        cmd = 'smu' + str(channel) + '.source.limit' + str(unit) + ' = ' + str(value)
        self.inst.write(cmd)

    def reset(self, channel):
        """
        restore the default settings
        channel: a, b, all
        """
        cmd = 'smu' + str(channel) + '.reset()'
        self.inst.write(cmd)
    
    def set_display(self, channel, function):
        """
        defines what measurement will be shown on the display
        channel: a, b
        function:     
            DISPLAY_VOLTAGE = 'DCVOLTS'
            DISPLAY_CURRENT = 'DCAMPS'
            DISPLAY_RESISTANCE = 'OHMS'
            DISPLAY_POWER = 'WATTS'
        """
        cmd = 'display.smu' + str(channel) + '.measure.func = display.MEASURE_' + str(function)
        self.smu_write(cmd)
    
    def set_mode(self, channel, mode):
        """
        Sets the channel into current or voltage source mode.

        In this mode you set the current/voltage and can measure voltage/current, resistance and power.
        channel: a, b
        function:     
            VOLTAGE_MODE = 'DCVOLTS'
            CURRENT_MODE = 'DCAMPS'
        """
        cmd = 'smu' + str(channel) + '.source.func = ' + 'smu' + str(channel) + '.OUTPUT_' + str(mode)

    def set_range(self, channel, unit, range):
        # set the source range
        cmd = 'smu' + str(channel) + '.source.range' + str(unit) + ' = ' + str(range)
        self.smu_write(cmd)

        # set the measurement range
        cmd = 'smu' + str(channel) + '.measure.range' + str(unit) + ' = ' + str(range)
        self.smu_write(cmd)
        
    def set_range_ChB(self, rg):
        # set the measurement range
        cmd = 'smub.measure.range' + 'i' + ' = ' + str(rg)
        self.smu_write(cmd)
        
        


