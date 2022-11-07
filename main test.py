# -*- coding: utf-8 -*-
"""
Created on Thu Apr  7 15:24:06 2022

@author: ali.uzun
"""

import sys

import time

from src.Data_Analysis import Data_Analysis
from src.OpenFile import OpenFile
from MSs.MyPlots import MyPlots

fl = OpenFile()
da = Data_Analysis()
mplt = MyPlots()

#####-------------- Keithley Settings -----------####
gpib_index = 0

addr = 28 # change it if necessery

####----------


def plot_sweep(filename, full_path):
    x_label = "Current (mA)"
    y_label1 = "Voltage (V)"
    y_label2 = "Optical Power (W)"

    plot_title = filename
    plot_title = "1mm EF"
    try:
        I,V,P = fl.read_csv_file(full_path)
        P = P*1e0
        da.plot_LIV(I, V, P, x_label, y_label1, y_label2, plot_title)

    except:
        #df = pd.read_csv (filename)
        #df.columns = ['Current', 'Voltage','Power']
        I,V = fl.read_csv_file(full_path)
        da.plot_XY(I, V, x_label, y_label1, plot_title)
    
    #plt_name = full_path.split(".")[0]
    #da.save_plot(plt_name)


if __name__ == "__main__":
    #LIV()
    #newport_USBPM_test()

    
    filename = "plot_test" + ".csv"
    
    file_path = "\\\\FS1\\Docs2\\ali.uzun\\My Documents\\My Files\\Scripts\\Python\\III-V Python Scripts D27102022\\" 
    xy_label_fontsize, axis_value_fontsize, legend_fontsize, lwidth, x_min, x_max,y_min, y_max = 14, 12, 12, 2, 0, 100, 0, 2.5
    x_label, y_label = "XX", "YY"

    file = file_path + filename
    I,V,P = mplt.open_file(file)
    fl = "FIG-NAME"
    mplt.plot_XY(file_path,fl, I*1e3, V, x_label, y_label, xy_label_fontsize, axis_value_fontsize, legend_fontsize, lwidth, x_min, x_max,y_min, y_max)

        
    #plot_sweep(filename, full_path)

