#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 13 21:18:13 2022

@author: au
"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from tkinter import filedialog, Tk
import os, csv, glob 
import numpy as np


class MyPlots():

    def __init__(self) -> None:
        self.line_style = ["solid", "dashed", "dotted", "dashdot"]

    def get_path(self, initial_directory):
            root=Tk()
            root.withdraw()
            path = filedialog.askdirectory(initialdir=initial_directory, title='Please select the source directory!!!')
            print(path)
            root.destroy()
            return path

    def get_file_list(self,path, file_type):
        # All files ending with .csv
        file_list = glob.glob(path + "/*." + file_type)
        return file_list

    def plot_Spectrum(self,file_path,legend,fig_name, W, P, x_label, y_label, *args):
        # device_name = fl
        xy_label_fontsize, axis_value_fontsize,legend_fontsize, lwidth, x_min, x_max,y_min, y_max = args

        fig,ax = plt.subplots()
        
        # xy_label_fontsize = 14
        plt.xlabel(x_label,fontsize = xy_label_fontsize)
        plt.ylabel(y_label,fontsize = xy_label_fontsize)
        
        # lwidth = 1
        lstyle = 0
        plt.plot(W, P, color = "blue", linewidth = lwidth,linestyle = self.line_style[lstyle], label=f'{legend}')
        
        # x_min, x_max = 1280, 1295
        # y_min, y_max = -75, -10
        
        plt.xlim([x_min, x_max])
        plt.ylim([y_min, y_max])
        #plt.figure(dpi=300,figsize=(6, 8))
        
        # axis_value_fontsize = 10
        plt.xticks(fontsize = axis_value_fontsize)
        plt.yticks(fontsize = axis_value_fontsize)
        
        
        legend_fontsize = 12
        legend_position = 0

        plt.legend(fontsize = legend_fontsize, loc = 0, facecolor = None, edgecolor = "red")
        
        # plt.title(plot_title)
        plt.grid(True)
        plt.show()
        
        #plt.title(f'{fig_name}')
        self.save_plot(file_path,fig_name, fig)


    def plot_XY(self,file_path,fl, I, V, x_label, y_label, *args):
        # device_name = fl
        xy_label_fontsize, axis_value_fontsize, legend_fontsize, lwidth, x_min, x_max,y_min, y_max = args
        fig,ax = plt.subplots()
        
        # xy_label_fontsize = 14
        plt.xlabel(x_label,fontsize = xy_label_fontsize)
        plt.ylabel(y_label,fontsize = xy_label_fontsize)
        
        # lwidth = 1
        lstyle = 0
        plt.plot(I, V, color = "blue", linewidth = lwidth,linestyle = self.line_style[lstyle])
        
        # x_min, x_max = 1280, 1300
        # y_min, y_max = -85, -10
        
        plt.xlim([x_min, x_max])
        plt.ylim([y_min, y_max])
        # #plt.figure(dpi=300,figsize=(6, 8))
        
        # axis_value_fontsize = 10
        plt.xticks(fontsize = axis_value_fontsize)
        plt.yticks(fontsize = axis_value_fontsize)
        
        
        #plt.title(f'{fl}')
        plt.grid(True)
        plt.show()
        
        self.save_plot(file_path, fl, fig)

    def plot_LIV(self,file_path,fl, x, y1, y2, x_label, y_label, y_label2, x_min, x_max,y_min, y_max,auto_range_xy = False):
        """
            Plot in y1 |___| y2 format
                        x 
            Labels: Voltage versus Power or Current
        """
        #labels = {"Voltage":" (V)", "Current":" (mA)","Power":" (mW)"}
        legend_fontsize = 15
        label_fontsize = 20
        lwidth = 2
        
        fig,ax = plt.subplots()

        plt.title(fl)
        
        # make a plot
        lstyle = 0
        ax.plot(x, y1, color = "red", linewidth = lwidth, linestyle = self.line_style[lstyle], label="None")
        # set x-axis label
        ax.set_xlabel(x_label, fontsize=label_fontsize)
        # set y-axis label
        ax.set_ylabel(y_label, color = "red", fontsize = label_fontsize)

        # twin object for two different y-axis on the sample plot
        ax2=ax.twinx()
        # make a plot with different y-axis using second axis object
        lstyle = 1
        ax2.plot(x, y2, color = "blue", linewidth = lwidth,linestyle = self.line_style[lstyle],  label=None)
        ax2.set_ylabel(y_label2, color = "blue", fontsize = label_fontsize)
        
        xy_label_fontsize = 16
        if (auto_range_xy):
            #x_min, x_max = 0, 150
            plt.xlim([x_min, x_max])
        
            #y_min, y_max = -0, 26
            plt.ylim([y_min, y_max])
        
        # plt.legend(line_style[:2], ['Voltage','Power'],
        #            fontsize = legend_fontsize)
        # plt.legend(fontsize = legend_fontsize, loc = 0, facecolor = None,edgecolor = "red")

        # defining legend style and data
        blue_line = mlines.Line2D([], [],linestyle = self.line_style[0], color='red', label='Voltage')
        reds_line = mlines.Line2D([], [],linestyle = self.line_style[1], color='blue', label='Power')
        
        plt.legend(handles=[blue_line, reds_line],fontsize = legend_fontsize)
        
        ax.xaxis.set_tick_params(labelsize = xy_label_fontsize)
        ax.yaxis.set_tick_params(labelsize = xy_label_fontsize)
        ax2.yaxis.set_tick_params(labelsize = xy_label_fontsize)
        
        # plt.grid(axis="y")
        ax.grid(True)
        plt.show()
        
        # plt_name = "T1"
        self.save_plot(file_path, fl, fig)
        
        # fl = "220805_1.8mm_1pMIR_LIV"
        # fig.savefig(f'{fl}.jpg',
        #             format='jpeg',
        #             dpi=600,
        #         bbox_inches='tight')
    def plot_IV(self,file_path,fl, x, y, x_label, y_label, x_min, x_max,y_min, y_max,auto_range_xy = False):
        """
            Plot in y1 |___| y2 format
                        x 
            Labels: Voltage versus Power or Current
        """
        #labels = {"Voltage":" (V)", "Current":" (mA)","Power":" (mW)"}
        legend_fontsize = 15
        xy_label_fontsize = 20
        lwidth = 2
        
        fig,ax = plt.subplots()

        plt.title(fl)
        
        # xy_label_fontsize = 14
        plt.xlabel(x_label,fontsize = xy_label_fontsize)
        plt.ylabel(y_label,fontsize = xy_label_fontsize)
        
        # lwidth = 1
        lstyle = 0
        plt.plot(x, y, color = "blue", linewidth = lwidth,linestyle = self.line_style[lstyle])
        
        slope_range= (-75,75)
        
        slope, c = self.get_slope_LIV(x, y, slope_range)
        #Yslope = slope*Is + c
        #plt.plot(Is, Yslope,color= "red",linewidth = 3, linestyle ='--')
        plt.text(75,1,"Slope is %f"%(slope))
        print(f"{fl}-Slope: {slope}, Constant: {c}")
        
        
        #plt.title(f'{fl}')
        plt.grid(True)
        plt.show()
        
        # plt_name = "T1"
        self.save_plot(file_path, fl, fig)
        
        # fl = "220805_1.8mm_1pMIR_LIV"
        # fig.savefig(f'{fl}.jpg',
        #             format='jpeg',
        #             dpi=600,
        #         bbox_inches='tight')


        

    selected = [9,17,23,8,2,24,4,6]

    def save_plot(self,file_path, fig_name, fig):
        fig_name = fig_name.strip(".scv")
        #print(f'{file_path}/{fl}.jpg')
       
        fig.savefig(f'{file_path}/{fig_name}.png',
                    format='png',
                    dpi=600,
                bbox_inches='tight')
        


    
    def plot_on_same_fig(self, file_path, filenames, file_type, responsivity, x_label, y_label, fl_label, lpos, plot_type, fig_name, *args):
        xy_label_fontsize, axis_value_fontsize,legend_fontsize, lwidth, x_min, x_max, y_min, y_max = args

        fig,ax = plt.subplots()
        if (plot_type == "SPT"):
            for i,file1 in enumerate(filenames):
                file = file_path + "/" + file1                
                P,W = self.open_file_spt(file)
                try:
                    plt.plot(W, P, linewidth = lwidth, label=fl_label[i]) #,linestyle = self.line_style[lstyle]
                except IndexError:
                    plt.plot(W, P, linewidth = lwidth) 

        else:
            I = []
            for i,file1 in enumerate(filenames):
                file = file_path + "/" + file1
                
                Ic,V,P = self.open_file(file, file_type,responsivity)
                    
                x_length = len(Ic)
                if (x_length > len(I)):
                    I = Ic
            
                if (plot_type == "IV"):
                    try: plt.plot(I, V, linewidth = lwidth, label = fl_label[i])
                    except IndexError: plt.plot(I, V, linewidth = lwidth)
                elif(plot_type == "LI"):  
                    try : plt.plot(I, P, linewidth = lwidth, label = fl_label[i])
                    except IndexError: plt.plot(I, P, linewidth = lwidth)
            
        # plt.title(plot_title)
        plt.xticks(fontsize= axis_value_fontsize)
        plt.yticks(fontsize= axis_value_fontsize)
        plt.legend(fontsize= legend_fontsize,loc=lpos)

        plt.xlabel(x_label,fontsize = xy_label_fontsize)
        plt.ylabel(y_label,fontsize = xy_label_fontsize)

        plt.xlim([x_min, x_max])
        plt.ylim([y_min, y_max])

        plt.grid(True)
        plt.show()

        self.save_plot(file_path, fig_name, fig)
    

    def open_file(self,filename, file_type, responsivity):
        I,V,P = [],[],[]
        
        if (file_type == "csv"):                    
            df = pd.read_csv(filename)
        elif (file_type == "dat"): 
            df = pd.read_table(filename, sep=",")
        
        if (len(df.columns) == 3):
            if (file_type == "csv"):                    
                df.columns = ['Current', 'Voltage', 'Power']
                I = df['Current']*1e0
            elif (file_type == "dat"): 
                df.columns = ['Current', 'Power', 'Voltage']
                I = df['Current']*1e3
            
            P = df['Power']*1e3/responsivity
            
            V = df['Voltage']      

        elif (len(df.columns) == 2):
            df.columns = ['Current', 'Voltage']
            
            I = df['Current']*1e0
            V = df['Voltage']
        
        return (I,V,P)
    
    def open_file_spt(self,filename):
        df = pd.read_csv(filename)

        df.columns = ['Wavelength', 'Power']
                
        W = df["Wavelength"] # Conver mA
        P = df["Power"]

        return(P,W)
    
    def get_slope_LIV(self, x, y, slope_range = (0, None)):
        """
        return the slope of line for given interval
        ie. slope efficiency and resistance
        """
        start, end = slope_range
        if (end != None):
            x = x[start:end]
            y = y[start:end]
        m, b = np.polyfit(x, y, 1) # m = slope, b = intercept
        return (m,b)
            
        



    