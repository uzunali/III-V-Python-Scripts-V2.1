# -*- coding: utf-8 -*-
"""
Created on Fri Dec 17 11:56:28 2021

@author: ali.uzun
"""

import win32gui
import win32com.client
import time
import traceback

try:
    OphirCOM = win32com.client.Dispatch("OphirLMMeasurement.CoLMMeasurement")
    # Stop & Close all devices
    OphirCOM.StopAllStreams() 
    OphirCOM.CloseAll()
    # Scan for connected Devices
    DeviceList = OphirCOM.ScanUSB()
    print(DeviceList)
    device_index = 0
    if len(DeviceList)>1:
        device_index = int(input("Please select the device you want to connect! (0 for first device)"))
    device = DeviceList[device_index]   	# if any device is connected
    DeviceHandle = OphirCOM.OpenUSBDevice(device)	# open first device
    is_exists = OphirCOM.IsSensorExists(DeviceHandle, 0)
    device_status = is_exists
       
except OSError as err:
    print("OS error: {0}".format(err))
except:
    traceback.print_exc()


OphirCOM.StartStream(DeviceHandle, 0)		# start measuring
 
for i in range(10):           		
    time.sleep(.2)				# wait a little for data
    data = OphirCOM.GetData(DeviceHandle, 0)
    if len(data[0]) > 0:		# if any data available, print the first one from the batch
        print('Reading = {0}, TimeStamp = {1}, Status = {2} '.format(data[0][0] ,data[1][0] ,data[2][0]))

    
    else:
        print('\nNo Sensor attached to {0} !!!'.format(device))
        
        
OphirCOM.StopAllStreams() 
OphirCOM.CloseAll()