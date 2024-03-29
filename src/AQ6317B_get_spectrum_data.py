# -*- coding: utf-8 -*-
"""
Created on Thu Nov 24 14:28:06 2022

@author: ali.uzun
"""


'''Adding Packages'''
import pyvisa
import matplotlib.pyplot as plt
import os 
import csv
import time
from datetime import date
from datetime import datetime
import pandas as pd
from datetime import datetime


now = datetime.now()
# convert to string
date_time = now.strftime("%Y-%m-%d %H-%M-%S") 

#Set path for file to be saved to 
#path ="\\10.204.28.1\docs2\owen.moynihan\My Documents\Project work\Test programs\Python Files\OSA\Take spectrum"
# ----- YOUR BASE DIRECTORY ---------
#measurement_base_path = "\\\\FS1\\Docs2\\ali.uzun\\My Documents\\My Files\\Measurements\\Caladan\\Caladan 22\\"
measurement_base_path = r'\\FS1\Docs2\ali.uzun\My Documents\My Files\Measurements\Caladan\Caladan 23' 
# ----- FOLDER UNDER BASE DIRECTORY --------- 
#save_to_folder = "Run-2 do6209\\2022-11-03 1.5 mm 1pMIR&EF\\"
save_to_folder = r"DFB Laser\DFB-1\2022-11-24 Chip4 1.8-1.9mm" + "\\"
save_to_folder = r"AU2eQ4\2023-06-26 AU2eQ4 QDL on Si + BCB" 

save_to_folder = r"\AU4bQ3\OnGaAs" 
save_to_folder = r"AU4bQ3\2023-08-08 CF-AR"
save_to_folder = "2023-08-23 SOIs"

save_to_folder = r"AU2eQ2-DFB-Batch 2\2023-08-14 DFB R3"
# measurement_base_path = "\\\\FS1\\Docs2\\ali.uzun\\My Documents\\My Files\\Measurements\\Caladan\\Caladan 22\\"
# save_to_folder = "Run-2 do6209\\2022-12-19\\"
# save_to_folder =  "Run-1 do5960\\2022-12-20\\"

T = 20
CL = "1.0mm"
RW = "3.5um"
DevID = 1
#DevLabel ="CleavedFacet-MIR6.0x56um" + "P-N Top Contact"
DevLabel ="EF-DFB-5DEG"
DevLabel ="EF HR"


DevIdentifier = f"AU2eQ2 Batch 2-QDL on GaAs-{DevLabel}" #+"-Top Contact n-from3umlaser"

file_record_index = 1



Idrive = 100 #mA
span = 20 # nm
#filename = "Run1-do5960_EF-Laser_CL-2.0mm_RW-3.0um_dev2_SPT_%smA.csv"%Idrive
#filename = f"AU2eQ4_EF Al HR_CL1mm_RW3.5um_Laser on GaAs_SPT_{Idrive}_40nmSpan.csv"


file_record_index = 1

filename = f"{date_time}_{DevIdentifier}-CL{CL}-RW{RW}_DevID{DevID}_SPT_T{T}C_Bias{Idrive}mA-Span{span}nm.csv"
#filename = f"{date_time}_{DevIdentifier}_SPT_T{T}C_Bias{Idrive}mA-Span{span}nm.csv"



#filename = "TEST"
#full_path = measurement_base_path + save_to_folder + filename

file_directory = measurement_base_path + save_to_folder # Folder the filde will be saved
file_directory = measurement_base_path + "\\"+ save_to_folder + "\\" # Folder the filde will be saved
full_path = file_directory + filename # full path for file
print(full_path)

#path = file_directory + filename # full path for file
#r_path = fp + filename # Folder the filde will be saved

''' program starts here'''

#r_path=  repr(path)[1:-1] #changing path to raw string to avoid back slash error

index = 0

rm = pyvisa.ResourceManager()
print(rm.list_resources())

OSA = rm.open_resource('GPIB0::1::INSTR')

OSA.timeout = None #High resolution files can take longer than timeout time 

print(OSA.query("*IDN?")) # Check to make sure it is OSA
#GETTING POWER OF SPECTRUM
OSA.write("LDATA") #Trace A level data
#data_B = OSA.write("LDATB") #Trace B level data
#data_C = OSA.write("LDATC") #Trace C level data

print(OSA.read_bytes)

spectrum = OSA.read()  # reading output from OSA

spectrum_float = [float(s) for s in spectrum.split(',')] # splitting list elements into floats 
spectrum_float.pop(0) # taking out first term - not a data point

#GETTING WAVELENGTHS SPAN
OSA.write("WDATA") # writting command to get wavelength data
wl = OSA.read() # reading output from OSA
#print(spectrum_float)

wl_float = [float(s) for s in wl.split(',')] # splitting list elements into floats 
wl_float.pop(0) # taking out first term - not a data point
#print(wl_float)

fig,ax = plt.subplots()
x_min, x_max = 1270, 1310
#plt.xlim([x_min, x_max])
      
            #y_min, y_max = -0, 26
y_min, y_max = -85,-30
#plt.ylim([y_min, y_max])
#PLOTTING SPECTRUM
plt.plot(wl_float, spectrum_float, linewidth = 0.4)
plt.xlabel("Wavelength (nm)")
plt.ylabel("Power (dBm)")
plt.ylim(-85)
plt.show()


#MAKING CSV FILE OF DATA
#os.chdir(fp)
header = ["Wavelength (nm)", "Power Spectrum (dBm)"]
data = pd.DataFrame(columns=tuple(header))
C1,C2 = "Wavelength (nm)", "Power Spectrum (dBm)"

lp = len(wl_float)
print(f"Wavelength point: {lp}")  
for i in range(len(wl_float)):
     
    power = spectrum_float[i]
    wavelength = wl_float[i]         
          
    datarow={C1:wavelength, C2:power}
    
    data = data.append(datarow, ignore_index = True)
    
        
## SAVE as csv FILE
data.to_csv(full_path,index=False)