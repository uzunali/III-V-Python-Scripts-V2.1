import pyvisa

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


def set_sweep_parameter(OSA,centre_wavelength, span, num_of_sample, resoultion,scan):
    OSA.write(f"CTRWL {centre_wavelength}") #specify center wl
    OSA.write(f"SPAN {span}") #span of measurement
    OSA.write(f"SMPL {num_of_sample}") #samplying number
    OSA.write(f"RESLN {resoultion}") #resolution in nm
    OSA.write(f"{scan}") #repeat or single scans

set_sweep_parameter(OSA, 1290, 20, 5001, 1, "RPT")

#set_sweep_parameter(OSA, 1280, 20, 10001, 0.001, "SGL")