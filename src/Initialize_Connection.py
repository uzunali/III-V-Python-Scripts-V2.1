#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  3 20:47:39 2021

@author: aliuzun
"""
import pyvisa


class Initialize_GPIB():
    
    def __init__(self):
        self.rm = pyvisa.ResourceManager()
    
    def get_device_list(self):
        resources = self.rm.list_resources()
        return resources

    def connect_device(self, gpib_index, addr):
        self.inst = self.rm.open_resource("GPIB%d::%d::INSTR" %(gpib_index, addr))
        return self.inst

    def terminate_connection(self):
        #self.rm.write("smua.source.levelv=0")
        #self.rm.write("smub.source.levelv=0")
        self.rm.close()
        