import pyvisa
#t_list_cmds = ['CTRWL', 'SPAN', 'REFL', 'LSCL', 'RESLN', 'AVG', 'SEGP', 'SENS', 'MONO', 'TR' + trace]

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


def set_sweep_parameter(OSA,centre_wavelength, span, num_of_sample, scan, resoultion, sensitivity):
    OSA.write(f"CTRWL {centre_wavelength}") #specify center wl
    OSA.write(f"SPAN {span}") #span of measurement
    OSA.write(f"SMPL {num_of_sample}") #samplying number
    OSA.write(f"RESLN {resoultion}") #resolution in nm
    OSA.write(f"{scan}") #repeat or single scans
    OSA.write(f"SENS {sensitivity}") #resolution in nm
    

align_true = 0
if (align_true):
    set_sweep_parameter(OSA, 1295, 10, 5001, "RPT", 1, 1)

else:
    set_sweep_parameter(OSA, 1280, 140, 10001, "SGL", 0.01, 1)