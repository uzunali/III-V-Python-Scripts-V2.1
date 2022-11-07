#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 20 23:55:05 2022

@author: au
"""

# -*- encoding: utf-8 -*-
'''
@Author  :   Ali Uzun 
@Time    :   2022/07/03 20:52:35
@Version :   1.0
'''

# here put the import lib
import time
from Keithley26xx_GPIB import smu26xx
from Initialize_Connection import Initialize_GPIB
from Data_Analysis import Data_Analysis
from Newport_844_PE import Newport_844_PE
from Sweep_Function import IV_Sweep
from OpenFile import OpenFile
from Thorlab_USBPM100D import Thorlab_100D

from tkinter import *
from tkinter import ttk
from tkinter.font import BOLD
from PIL import ImageTk, Image



gpib_index = 0
addr = 26 # change it if necessery


    
    
    
class Photonics_Escape_Room():
    def __init__(self,root) -> None:
        self.root = root
        self.frame = Frame(self.root)

        self.box_width = 5
        self.font_size = 14
        self.bd = 3
        self.entry_list = [] 
        self.passcode = "281820"
        self.user_code = []
        self.passcode_checklist = {"D1":None,"D2":None,"D3":None,"D4":None,"D5":None,"D6":None}
        self.passcode_status = None
        self.message = []
        self.initial_message = " START MEASUREMENT! "

        self.data_read = False
        
        # True --> read power from power meter, False --> Channel B of keithley
        self.Select_Power_Reading_Device = {1:"Keithley_ChB", 2:"Newport_PM", 3:"Thorlab_PM"}
        self.power_read_index = 1

        self.test = 0

        self.Widgest()
        self.frame.pack(fill=BOTH, expand=True)
        
        self.Open_Connections()
    
    def Open_Connections(self):
        self.initialize_connection = Initialize_GPIB()
    
        inst = self.initialize_connection.connect_device(gpib_index, addr) # connect to device#
        # create an object
        self.keithley_GPIB =  smu26xx(inst)
            
        
        self.newport_PM = Newport_844_PE()
        self.is_Newport_Con_Open = False
        
        self.save_data = OpenFile()
        
        
    
    def Widgest(self):


        # # # IPIC logo
        # image = ImageTk.PhotoImage(Image.open("tyndall.png"))       
        # label = ttk.Label(self.frame, image=image, width=20 )
        # label.photo = image   # assign to class variable to resolve problem with bug in `PhotoImage`

        # label.grid(row=0, column=1, columnspan=6,rowspan=1,padx=(40, 0), sticky=EW)

        self.Result_Box()

        turn_on = Button(self.frame,text= "ON",font=("Times",13),fg="blue", bd = 5, height= 2, width=15, command=self.Turn_On)
        turn_on.grid(row=1,column=5,columnspan=2, padx=10, sticky=EW)

        turn_on.bind("<Return>", self.Turn_On)

        turn_off = Button(self.frame,text= "OFF",font=("Times",13),fg="blue", bd = 5, height= 2, width=15, command=self.Turn_Off)
        turn_off.grid(row=2,column=5,columnspan=2, padx=10, sticky=EW)

        turn_off.bind("<Return>", self.Turn_Off)



        start = Button(self.frame,text= "START",font=("Times",13, BOLD),fg="blue",bd = 4, height= 2, width=10, command=self.Start)
        start.grid(row=4, column=5, columnspan=2, padx = 5, pady = 4, sticky=EW)
        start.bind("<Return>", self.Start)

        stop = Button(self.frame,text= "STOP",font=("Times",13, BOLD),fg="blue",bd = 4, height= 2, width=10, command=self.Stop)
        stop.grid(row=5, column=5, columnspan=2, padx = 5, pady = 4, sticky=EW)

        reset = Button(self.frame,text= "RESET",font=("Times",13),fg="blue", height= 2, width=5, command=self.Reset)
        reset.grid(row=7,column=2,columnspan=2, padx = 5, pady = 10, sticky=EW)
        # reset.bind("<Return>", self.Enter)

        quit = Button(self.frame,text= "QUIT",font=("Times",13),fg="blue", height= 2, width=5, command=self.Quit)
        quit.grid(row=7,column=4,columnspan=2, padx = 5, pady = 10,sticky=EW)
        quit.bind("<Return>", self.Quit)
        
        
        rows = 8
        self.get_power_from = IntVar()
        R1 = Radiobutton(self.frame, text="Keithley ChB", variable = self.get_power_from, value=1,
                          command=self.get_RadioSel)
        R1.grid(row=rows ,column = 1, columnspan=2, padx = 5, pady = 10,sticky=W)

        R2 = Radiobutton(self.frame, text="Newport PM", variable = self.get_power_from, value=2,
                          command=self.get_RadioSel)
        R2.grid(row=rows ,column = 3, columnspan=2, padx = 5, pady = 10,sticky=W)

        R3 = Radiobutton(self.frame, text="Thorlab PM", variable = self.get_power_from, value=3,
                          command=self.get_RadioSel)
        R3.grid(row=rows ,column = 5, columnspan=2, padx = 5, pady = 10,sticky=W)
        
        
        
        rows = 9
        self.filepath = StringVar() # Value saved here

        def search():
          print(variable1.get())
          return ''

        l1 = Label(self.frame, text="File Path")
        l1.grid(row=rows, column=1,sticky=W, padx = 15)

        path = Entry(self.frame, width=60, textvariable = self.filepath)
        path.grid(row=rows, column=2, columnspan=6, sticky=W)
        
        
        rows = 10
        cols = 1
        
        Label(self.frame, text="Start (mA):").grid(row = rows, column = cols,sticky=W, padx = 15)
        
        self.sweep_start = IntVar()
        Estart = Entry(self.frame, width=4, textvariable = self.sweep_start)
        Estart.grid(row=rows, column=cols + 1, sticky=W)
        Estart.delete(0, 'end')
        Estart.insert(INSERT, 0)
        
        cols = cols + 2
        Label(self.frame, text="Step (mA):").grid(row = rows, column = cols,sticky=W, padx = 15)
        
        self.sweep_step = IntVar()
        Estep = Entry(self.frame, width=4, textvariable = self.sweep_step)
        Estep.grid(row=rows, column=cols + 1, sticky=W)
        Estep.delete(0, 'end')
        Estep.insert(INSERT, 2)
        
        cols = cols + 2
        Label(self.frame, text="End (mA):").grid(row = rows, column = cols,sticky=W, padx = 15)
        
        self.sweep_end = IntVar()
        Eend = Entry(self.frame, width=4, textvariable = self.sweep_end)
        Eend.grid(row=rows, column=cols + 1, sticky=W)
        Eend.delete(0, 'end')
        Eend.insert(INSERT, 140)
        
        cols = 1
        rows = 11
        Label(self.frame, text="Voltage Limit (V):").grid(row = rows, column = cols,sticky=W, padx = 15)
        self.vol_limit = IntVar()
        Evlim = Entry(self.frame, width=4, textvariable = self.vol_limit)
        Evlim.grid(row=rows, column=cols + 1, sticky=W)
        
        Evlim.delete(0, 'end')
        Evlim.insert(INSERT, 3)
        
        rows = 12
        ssweep = Button(self.frame,text= "Start Sweep",font=("Times",13),fg="blue", height= 2, width=5, command=self.Sweep)
        ssweep.grid(row=rows,column=2,columnspan=2, padx = 5, pady = 10, sticky=EW)
        ssweep.bind("<Return>", self.Sweep)


    def Result_Box(self):

        row_index=1
        col_index=1
        message = Label(self.frame,text = "Set Current (mA) ",fg="black",bd = 5,font=("Times",16))
        message.grid(row=row_index, column = col_index, columnspan=2, padx = 10,sticky=W)
        # message.config({"background": "White"})

        initial_text = "%s"%"Current"
        self.I_set = Entry(self.frame,font = "Helvetica %d bold"%self.font_size, justify="center", bd = self.bd, width=self.box_width)
        self.I_set.insert(-1, initial_text)
        self.I_set.grid(row = row_index,
            column = col_index + 2,
            columnspan=2,
            padx=(10, 0),
            pady=5,
            ipady=10,
            sticky=EW)
        self.I_set.bind("<Button-1>", self.on_click1)
        #E1.config({"background": "Red"})

        row_index=2
        col_index=1
        
        message = Label(self.frame,text = "Set Voltage Limit (V) ",fg="black",bd = 5,font=("Times",16))
        message.grid(row = row_index, column = col_index, columnspan=2,padx = 10,sticky=W)

        initial_text = "%s"%"Voltage"
        self.V_limit = Entry(self.frame,font = "Helvetica %d bold"%self.font_size, justify="center", bd = self.bd, width=self.box_width)
        self.V_limit.insert(-1, initial_text)
        self.V_limit.grid(row = row_index,
            column = col_index + 2,
            columnspan=2,
            padx=(10, 0),
            pady=5,
            ipady=10,
            sticky=EW)
        self.V_limit.bind("<Button-1>", self.on_click2)

        row_index=3
        col_index=1
        message = Label(self.frame,text = " %s READINGS %s" % ("-"*10,"-"*10),fg="black",bd = 5,font=("Times",16))
        message.grid(row = row_index, column = col_index, columnspan=6, padx = 10,sticky=EW)

        row_index=4
        col_index=1
        self.message = Label(self.frame,text = "Current Read (mA) ",fg="black",bd = 5,font=("Times",16))
        self.message.grid(row = row_index, column = col_index, columnspan=2,padx = 10,sticky=W)

        initial_text = "%s"%" "
        self.I = Entry(self.frame,font = "Helvetica %d bold"%self.font_size, justify="center", bd = self.bd, width=self.box_width*2)
        self.I.insert(-1, initial_text)
        self.I.grid(row = row_index,
            column = col_index + 2,
            columnspan=2,
            padx=(10, 0),
            pady=5,
            ipady=10,
            sticky=EW)
        
        row_index = 5
        col_index = 1
        message = Label(self.frame,text = "Voltage Read (V) ",fg="black",bd = 5,font=("Times",16))
        message.grid(row = row_index, column = col_index, columnspan=2,padx = 10,sticky=W)

        initial_text = "%s"%" "
        self.V = Entry(self.frame,font = "Helvetica %d bold"%self.font_size, justify="center", bd = self.bd, width=self.box_width*2)
        self.V.insert(-1, initial_text)
        self.V.grid(row = row_index,
            column = col_index + 2,
            columnspan=2,
            padx=(10, 0),
            pady=5,
            ipady=10,
            sticky=EW)
        
        row_index = 6
        col_index = 1
        message = Label(self.frame,text = "Power Read (W) ",fg="black",bd = 5,font=("Times",16))
        message.grid(row = row_index, column = col_index, columnspan=2,padx = 10,sticky=W)

        initial_text = "%s"%" "
        self.P = Entry(self.frame,font = "Helvetica %d bold"%self.font_size, justify="center", bd = self.bd, width=self.box_width*2)
        self.P.insert(-1, initial_text)
        self.P.grid(row = row_index,
            column = col_index + 2,
            columnspan=2,
            padx=(10, 0),
            pady=5,
            ipady=10,
            sticky=EW)

        self.entry_list= [self.I_set, self.V_limit, self.I, self.V, self.P]
        

    def on_click1(self,event):
        e_index = 0
        self.entry_list[e_index].delete(0, 'end')

    def on_click2(self,event):
        e_index = 1
        self.entry_list[e_index].delete(0, 'end')
    

    def Turn_On(self):
        # pass
        # set voltage limit in channel A
        voltage_limit = float(self.V_limit.get())
        self.keithley_GPIB.set_limit("a", "v", voltage_limit)

        # set the current in channel A
        set_cur = float(self.I_set.get())
        self.keithley_GPIB.set_current_ChA(set_cur*1e-3)
        
        # Turn onn chanlle A
        self.keithley_GPIB.turn_ON_ChA()
      

    def Turn_Off(self):
        # pass
        self.keithley_GPIB.turn_OFF_ChA()
        self.keithley_GPIB.turn_OFF_ChB()
    
    def Start(self):
        self.data_read = True
        
        self.get_data()
    
    def Stop(self):
        self.data_read = False
        
        # if (self.is_Newport_Con_Open):
        #     # self.newport_PM = Newport_844_PE()
        #     self.newport_PM.close_connection()
            
        self.keithley_GPIB.turn_OFF_ChA()
        self.keithley_GPIB.turn_OFF_ChB()
        

            
    def get_data(self):
        
        currentA, voltageA, power = None, None, None
        self.power_read_index = self.get_power_from.get()

        while(self.data_read): #
        
            self.P.delete(0, 'end')
            self.V.delete(0,'end')
            self.keithley_GPIB.turn_ON_ChA()
            
            
            if (self.Select_Power_Reading_Device[self.power_read_index] == "Newport_PM"):
                power = self.newport_PM.get_data()
                self.is_Newport_Con_Open = True
            elif (self.Select_Power_Reading_Device[self.power_read_index] == "Keithley_ChB"):
                self.keithley_GPIB.turn_ON_ChB()
                power = self.keithley_GPIB.get_current_ChB()
                # pass
            
            voltageA = self.keithley_GPIB.get_voltage_ChA()
            # currentA = self.keithley_GPIB.get_current_ChA()
            
            s = self.P.insert(-1, "%s" % power)
            s = self.V.insert(-1, "%s" % voltageA)
            # #
            
            print("I= %s mA, V= %s V, P= %s \n" %(currentA, voltageA, power))
            
            self.root.update()
            
        if (self.is_Newport_Con_Open): 
            power = self.newport_PM.get_data()
            print("Last P= %s \n" %(power))
            self.newport_PM.close_connection()
        # self.keithley_GPIB.turn_OFF_ChA()
        # self.keithley_GPIB.turn_OFF_ChB()
        
    
    
    def Reset(self):
        self.P.delete(0, 'end')
        self.V.delete(0, 'end')
        self.Turn_Off()
        if (not self.is_Newport_Con_Open):
            self.newport_PM = Newport_844_PE()
            
        self.keithley_GPIB.turn_OFF_ChA()
        self.keithley_GPIB.turn_OFF_ChB()
    
    def Quit(self):
        self.keithley_GPIB.turn_OFF_ChA()
        self.keithley_GPIB.turn_OFF_ChB()
        
        self.root.destroy()
        
    
    def get_RadioSel(self):
       selection = "You selected power reading source " + str(self.Select_Power_Reading_Device[self.power_read_index] )
       # label.config(text = selection)
       print(selection)
      



    def select_file(self):
        filetypes = (
            ('text files', '*.txt'),
            ('All files', '*.*')
        )
    
        filename = fd.askopenfilename(
            title='Open a file',
            initialdir='/',
            filetypes=filetypes)
    
        showinfo(
            title='Selected File',
            message=filename
        )

    

        
    
    def Sweep(self):
    

        # sweep_function = IV_Sweep(initialize_connection, keithley_GPIB, save_data, newport_PM)
        sweep_function = IV_Sweep(self.initialize_connection, self.keithley_GPIB, self.save_data, self.newport_PM)
    

        power_reading_from = ["Newport_PM", "Keithley_ChB","Other"] # 0 or 1
        
        power_index = 0 # 0 or 1
    
        #filename = "220712_QDLdo6209R2_BCBSi_1.8mm_RWxum_1pMIR_XxXum_Dev2_20C.csv"
        
        #_Ref_Attenuator884UVR
        filename = "220719_do6209QDL_SOI11_60nmPECDV-SiO2_1.8mm_1pMIR_%s_R-TT1-D1_r2.csv" % power_reading_from[power_index]
        filename = self.filepath.get()
        
        measurement_base_path = "\\\\FS1\\Docs2\\ali.uzun\\My Documents\\My Files\\Measurements\\Caladan\\Caladan 22\\"

        save_to_folder = "Caladan SOI\\2022-07-21 AU2-1\\"
        #save_to_folder = "Test\\"
        #save_to_folder = "20220628 3um Si ridge WG\\220708 AU-2276-3umSOI-C2 AU3bQ3\\"
        
        full_path = measurement_base_path + save_to_folder + filename
        print(full_path)
    
        # header for csv file: first column, second column, third column
        header = ["Current (mA)", "Voltage (V)", "Power (mW)"]
    
        
        voltage_limit = self.vol_limit.get() #4 # V
        start_value = self.sweep_start.get() #0
        stop_value =  self.sweep_end.get() #40 #mA
        step_size = self.sweep_step.get()#2 #mA
        
        LIV_sweep = True # True is LIV sweep. False IV
        if (LIV_sweep):
            if (self.Select_Power_Reading_Device[self.power_read_index] == "Newport_PM"):
                sweep_function.LIV_sweep_NewportPM(full_path, header, start_value=start_value, stop_value=stop_value, step_size=step_size, voltage_limit = voltage_limit)
            
                self.is_Newport_Con_Open = True
            elif (self.Select_Power_Reading_Device[self.power_read_index] == "Keithley_ChB"):
                #current_ranges = [1E-7, 1E-6, 1E-5, 1E-4, 1E-3, 1E-2, 1E-1, 1, 1.5]
                rg = 1E-1 # keithley channel range
                self.keithley_GPIB.set_range_ChB(rg)
                
                # Responsivity of Detector (A/W), 818IR Ge Detector
                R = 0.65  
                
                sweep_function.LIV_sweep_KeithleyChB(full_path, header, R, start_value=start_value, stop_value=stop_value, step_size=step_size, voltage_limit = voltage_limit)
            else:
                print("No reading!!!!!")

            
            # if (power_reading_from[power_index] == "Newport_PM"):
                
            #     newport_ranges = ('AUTO', '30.0mW', '3.00mW', '300uW', '30.0uW', '3.00uW', '300nW', '30.0nW')
            #     rindex = 2
            #     # newport_PM.set_range(rindex)
            #     sweep_function.LIV_sweep_NewportPM(full_path, header, start_value=start_value, stop_value=stop_value, step_size=step_size, voltage_limit = voltage_limit)
            
            # elif (power_reading_from[power_index] == "Keithley_ChB"):
            #     #current_ranges = [1E-7, 1E-6, 1E-5, 1E-4, 1E-3, 1E-2, 1E-1, 1, 1.5]
            #     rg = 1E-1 # keithley channel range
            #     self.keithley_GPIB.set_range_ChB(rg)
    
            #     # Responsivity of Detector (A/W), 818IR Ge Detector
            #     R = 0.65  
    
            #     sweep_function.LIV_sweep_KeithleyChB(full_path, header, R, start_value=start_value, stop_value=stop_value, step_size=step_size, voltage_limit = voltage_limit)
            # else:
            #     print("No reading!!!!!")
        else:
            is_IV = True  
    
            if (is_IV):
    
                sweep_function.IV_sweep(full_path, header, start_value=start_value, stop_value=stop_value, step_size = step_size, voltage_limit = voltage_limit)
            
            else:
                current_limit = self.voltage_limit.get() #5 # mA
                start_value = 0
                stop_value = 3 # V
                step_size = 0.1 # V
    
                sweep_function.VI_sweep(full_path, header, start_value=start_value, stop_value=stop_value, step_size = step_size, current_limit = current_limit)
    
        
        # if (LIV_sweep):
        #     plot_sweep(filename, full_path)
        # else:
        #     plot_sweep_IV(filename, full_path)
        
        # if (self.is_Newport_Con_Open):
        #     # self.newport_PM = Newport_844_PE()
        #     self.newport_PM.close_connection()
        if (self.is_Newport_Con_Open): 
            power = self.newport_PM.get_data()
            print("Last P= %s \n" %(power))
            self.newport_PM.close_connection()
            
        self.keithley_GPIB.turn_OFF_ChA()
        self.keithley_GPIB.turn_OFF_ChB()
    
    def Sweep2(self):

        initialize_connection = Initialize_GPIB()
        inst = initialize_connection.connect_device(gpib_index, addr) # connect to device#

        # create an object
        keithley_GPIB =  smu26xx(inst)
        save_data = OpenFile()
        
        newport_PM = Newport_844_PE()

        sweep_function = IV_Sweep(initialize_connection, keithley_GPIB, save_data, newport_PM)

        #filename = "L-TT2-D1-R2do5960_1.5mm_1pMIR_RW_3um_MIR_6.5x52um_Keithley_ChB.csv"
        power_reading_from = ["Newport_PM", "Keithley_ChB","Other"] # 0 or 1
        power_index = 1 # 0 or 1

        #filename = "220712_QDLdo6209R2_BCBSi_1.8mm_RWxum_1pMIR_XxXum_Dev2_20C.csv"
        
        #_Ref_Attenuator884UVR
        filename = "220810_do6209QDL_SU8-SiN_1.8mm_RW2.5um_1pMIR_6x50_%s_BottomSet-B9-r4-R075-Lens+GeDetector.csv" % power_reading_from[power_index]
        
        measurement_base_path = "\\\\FS1\\Docs2\\ali.uzun\\My Documents\\My Files\\Measurements\\Caladan\\Caladan 22\\"
        save_to_folder = "20220628 3um Si ridge WG\\220701 After Glue Drop\\"
        save_to_folder = "2022-07-07 AU3bQ3 QDL\\AU-2276-Si\\"
        save_to_folder = "AU3bQ4\AU-220711-BCBSi\\"
        save_to_folder = "Run-2 do6209\SiBCB-2\\2022-07-12 do6209 QDL\\"
        save_to_folder = "Test\\"
        # save_to_folder = "2022-08-03 SU8-SiN WG\\"
        #save_to_folder = "20220628 3um Si ridge WG\\220708 AU-2276-3umSOI-C2 AU3bQ3\\"
        
        full_path = measurement_base_path + save_to_folder + filename
        
        #filename = "A3473PO-LR3-FP2.csv"
        #full_path = "\\\\FS1\\Docs2\\ali.uzun\\My Documents\\My Files\\Measurements\\Fatih\\2022-07-22 LIV\\%s" % filename
        
        print(full_path)

        # header for csv file: first column, second column, third column
        header = ["Current (mA)", "Voltage (V)", "Power (mW)"]

        

        voltage_limit = 4 # V
        start_value = 0
        stop_value = 120 #mA
        step_size = 2 #mA
        
        # voltage_limit = self.vol_limit.get() #4 # V
        # start_value = self.sweep_start.get() #0
        # stop_value =  self.sweep_end.get() #40 #mA
        # step_size = self.sweep_step.get()#2 #mA
        
        LIV_sweep = True # True is LIV sweep. False IV
        if (LIV_sweep):
            
            
            if (power_reading_from[power_index] == "Newport_PM"):
                
                newport_ranges = ('AUTO', '30.0mW', '3.00mW', '300uW', '30.0uW', '3.00uW', '300nW', '30.0nW')
                rindex = 2
                # newport_PM.set_range(rindex)
                sweep_function.LIV_sweep_NewportPM(full_path, header, start_value=start_value, stop_value=stop_value, step_size=step_size, voltage_limit = voltage_limit)
            
            elif (power_reading_from[power_index] == "Keithley_ChB"):
                #current_ranges = [1E-7, 1E-6, 1E-5, 1E-4, 1E-3, 1E-2, 1E-1, 1, 1.5]
                rg = 1E-1 # keithley channel range
                keithley_GPIB.set_range_ChB(rg)

                # Responsivity of Detector (A/W), 818IR Ge Detector
                R = 0.75  

                sweep_function.LIV_sweep_KeithleyChB(full_path, header, R, start_value=start_value, stop_value=stop_value, step_size=step_size, voltage_limit = voltage_limit)
            else:
                print("No reading!!!!!")
        else:
            is_IV = True  

            if (is_IV):

                sweep_function.IV_sweep(full_path, header, start_value=start_value, stop_value=stop_value, step_size = step_size, voltage_limit = voltage_limit)
            
            else:
                current_limit = 50 # mA
                start_value = 0
                stop_value = 3 # V
                step_size = 0.1 # V

                sweep_function.VI_sweep(full_path, header, start_value=start_value, stop_value=stop_value, step_size = step_size, current_limit = current_limit)

        
        if (LIV_sweep):
            plot_sweep(filename, full_path)
        else:
            plot_sweep_IV(filename, full_path)
        
        inst.close()

        
    def Warning_Window(self):
        #Create a Button to Open the Toplevel Window
        top= Toplevel(self.root)
        top.geometry("700x300")
        top.title("Child Window")
        #Create a label in Toplevel window
        Label(top, text= "Please Enter a number in each cell!")

    
    

        
        


def main():
    root = Tk()
    root.title(string='III-V Material & Devices')
    root.geometry("700x600")
    root.resizable(width=True, height=True)
    app = Photonics_Escape_Room(root)
    root.mainloop()

if __name__ == '__main__':
    main()