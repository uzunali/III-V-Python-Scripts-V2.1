

def set_sweep_parameter(OSA,centre_wavelength, span, num_of_sample, resoultion,scan):
    OSA.write(f"CTRWL {centre_wavelength}") #specify center wl
    OSA.write(f"SPAN {span}") #span of measurement
    OSA.write(f"SMPL {num_of_sample}") #samplying number
    OSA.write(f"RESLN {resoultion}") #resolution in nm
    OSA.write(f"{scan}") #repeat or single scans
