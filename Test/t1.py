import glob
import pyvisa

path = r'\\FS1\Docs2\ali.uzun\My Documents\My Files\Measurements\Caladan\Caladan 22\Caladan SOI\2022-07-19 do6209 QDL SOI11'
#p = repr(path)[1:-1] #changing path to raw string to avoid back slash error
measurement_base_path = r'\\FS1\Docs2\ali.uzun\My Documents\My Files\Measurements\Caladan\Caladan 22'
# ----- FOLDER UNDER BASE DIRECTORY --------- 
save_to_folder = r"\Run-2 do6209\2022-11-03 1.5 mm 1pMIR&EF" + "\\"

path = measurement_base_path + save_to_folder
#print(path)
file_list = glob.glob(path + "/*." + "csv")

#print(file_list)