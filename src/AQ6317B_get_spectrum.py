'''
SAVES SPECTRUM FROM ANDO OSA IN C.107 

MAKE SURE IT IS CONNECTED AND THE GPIB ADRESS IS CORRECT

SAVES AS CSV FILE AT PATH SPECIFIED 

ANY PROBLEMS ASK ME - OWEN MOYNIHAN
'''

'''Adding Packages'''
import pyvisa
import matplotlib.pyplot as plt
import os 
import csv
import time
from datetime import date
from datetime import datetime
import pandas as pd

#from ANDO_AQ6317B_functions import *

def set_sweep_parameter(OSA,centre_wavelength, span, num_of_sample, resoultion,scan):
    OSA.write(f"CTRWL {centre_wavelength}") #specify center wl
    OSA.write(f"SPAN {span}") #span of measurement
    OSA.write(f"SMPL {num_of_sample}") #samplying number
    OSA.write(f"RESLN {resoultion}") #resolution in nm
    #OSA.write(f"{sensitivity}") #Sensitivity scan
    OSA.write(f"{scan}") #repeat or single scans


def get_data(OSA, filename):
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
    print(spectrum_float)
    
    wl_float = [float(s) for s in wl.split(',')] # splitting list elements into floats 
    wl_float.pop(0) # taking out first term - not a data point
    print(wl_float)
    
    #PLOTTING SPECTRUM
    plt.plot(wl_float, spectrum_float, linewidth = 0.4)
    plt.xlabel("Wavelength (nm)")
    plt.ylabel("Power (dBm)")
    plt.ylim(-100)
    plt.show()
    
    
    #MAKING CSV FILE OF DATA
    #os.chdir(fp)
    header = ["Wavelength (nm)", "Power Spectrum (dBm)"]
    data = pd.DataFrame(columns=tuple(header))
    C1,C2 = "Wavelength (nm)", "Power Spectrum (dBm)"
    
    for wl in wl_float:
         
        power = spectrum_float[index]
        wavelength = wl_float[index]         
          
        print("W = %s mA, P = %s \n" %(wavelength, power))    
        
        datarow={C1:wavelength, C2:power}
        
        data = data.append(datarow, ignore_index = True)
        
            
    ## SAVE as csv FILE
    data.to_csv(filename + '.csv',index=False)


# '''Input parameters here'''
# #Name  your file 
# file_name = 'Spectrum_test'

# #Set path for file to be saved to 
# path ="\\10.204.28.1\docs2\owen.moynihan\My Documents\Project work\Test programs\Python Files\OSA\Take spectrum"
# # ----- YOUR BASE DIRECTORY ---------
# #measurement_base_path = "\\\\FS1\\Docs2\\ali.uzun\\My Documents\\My Files\\Measurements\\Caladan\\Caladan 22\\"
# measurement_base_path = r'\\FS1\Docs2\ali.uzun\My Documents\My Files\Measurements\Caladan\Caladan 22' + "\\"
# # ----- FOLDER UNDER BASE DIRECTORY --------- 
# #save_to_folder = "Run-2 do6209\\2022-11-03 1.5 mm 1pMIR&EF\\"
# save_to_folder = r"DFB Laser\DFB-1\2022-11-24 Chip4 1.8-1.9mm" + "\\"

# fp = "\\\\FS1\Docs2\\ali.uzun\\My Documents\\My Files\\Measurements\\Caladan\\Caladan 22\\DFB Laser\\DFB-1\\2022-11-24 Chip4 1.8-1.9mm" + "\\"
# filename = "DFB-1_Chip4_CL1.8mm_5deg_A5_ARCoated_dev2_SPT_100mA"
# filename = "TEST"

# file_directory = measurement_base_path + save_to_folder # Folder the filde will be saved

# path = file_directory + filename # full path for file
# r_path = fp + filename # Folder the filde will be saved

''' program starts here'''

#r_path=  repr(path)[1:-1] #changing path to raw string to avoid back slash error

index = 0

rm = pyvisa.ResourceManager()
print(rm.list_resources())

OSA = rm.open_resource('GPIB0::1::INSTR')

OSA.timeout = None #High resolution files can take longer than timeout time 

print(OSA.query("*IDN?")) # Check to make sure it is OSA

### Sweep Settings
#OSA.write("CTRWL 1550") #specify center wl
#OSA.write("SPAN 50") #span of measurement
#OSA.write("SMPL 1000") #samplying number
#OSA.write("RESLN 1") #resolution in nm
#OSA.write("RPT") #repeat scans
#OSA.write("SGL") #single scan

set_sweep_parameter(OSA, 1285, 20, 5001, 0.01, "SGL")

#set_sweep_parameter(OSA, 1285, 60, 5001, 0.1, "RPT")

