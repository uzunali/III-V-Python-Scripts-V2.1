# -*- encoding: utf-8 -*-
'''
@Author  :   Ali Uzun 
@Time    :   2022/07/03 20:52:35
@Version :   1.0
'''
dev_mode = False

# here put the import lib
import time
if (not dev_mode):
    from src.Keithley26xx_GPIB import smu26xx
    from src.Initialize_Connection import Initialize_GPIB
    from src.Data_Analysis import Data_Analysis
    from src.Newport_844_PE import Newport_844_PE
    from src.Sweep_Function import IV_Sweep
    from src.OpenFile import OpenFile
    from src.Thorlab_USBPM100D import Thorlab_100D

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
        self.Select_Power_Reading_Device = {0:"Newport", 1:"Keithley"}
        self.power_read_index = 1

        self.test = 0

        self.Widgest()
        self.frame.pack(fill=BOTH, expand=True)
        
        if (not dev_mode):
            self.Open_Connections()
    
    def Open_Connections(self):
        initialize_connection = Initialize_GPIB()
    
        inst = initialize_connection.connect_device(gpib_index, addr) # connect to device#
        # create an object
        self.keithley_GPIB =  smu26xx(inst)
            
        if (not self.power_read_index):
            self.newport_PM = Newport_844_PE()
            self.is_Newport_Con_Open = False
    
    def Widgest(self):


        # IPIC logo
        image = ImageTk.PhotoImage(Image.open("tyndall.png"))       
        label = ttk.Label(self.frame, image=image, width=20 )
        label.photo = image   # assign to class variable to resolve problem with bug in `PhotoImage`

        label.grid(row=0, column=1, columnspan=6,rowspan=1,padx=(40, 0), sticky=EW)

        self.Result_Box()

        turn_on = Button(self.frame,text= "ON",font=("Times",13),fg="blue", bd = 5, height= 2, width=15, command=self.Turn_On)
        turn_on.grid(row=1,column=5,columnspan=2, padx=10, sticky=EW)

        #turn_on.bind("<Return>", self.Turn_On)

        turn_off = Button(self.frame,text= "OFF",font=("Times",13),fg="blue", bd = 5, height= 2, width=15, command=self.Turn_Off)
        turn_off.grid(row=2,column=5,columnspan=2, padx=10, sticky=EW)

        #turn_off.bind("<Return>", self.Turn_Off)



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
        if (not self.is_Newport_Con_Open):
            self.newport_PM = Newport_844_PE()
            
        self.keithley_GPIB.turn_OFF_ChA()
        self.keithley_GPIB.turn_OFF_ChB()
        

            
    def get_data(self):
        
        currentA, voltageA, power = None, None, None

        while(self.data_read): #
            self.P.delete(0, 'end')
            self.V.delete(0,'end')
            self.keithley_GPIB.turn_ON_ChA()
            self.keithley_GPIB.turn_ON_ChB()
            
            
            if (self.Select_Power_Reading_Device[self.power_read_index] == "Newport"):
                power = self.newport_PM.get_data()
                self.is_Newport_Con_Open = True
            elif (self.Select_Power_Reading_Device[self.power_read_index] == "Keithley"):
                power = self.keithley_GPIB.get_current_ChB()
                # pass
            
            voltageA = self.keithley_GPIB.get_voltage_ChA()
            # currentA = self.keithley_GPIB.get_current_ChA()
            
            s = self.P.insert(-1, "%s" % power)
            s = self.V.insert(-1, "%s" % voltageA)
            # #
            
            print("I= %s mA, V= %s V, P= %s \n" %(currentA, voltageA, power))
            
            self.root.update()
            
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
        
    
    def Passcode_Check(self):
        for i in range(len(self.passcode)):
            key = "D%d"%(i+1)
            if(self.passcode[i] == self.user_code[i]):
                self.passcode_checklist[key] = 1
            else:
                self.passcode_checklist[key] = 0
            
            
    
    def check_cells(self):
        for i,e in enumerate(self.entry_list):
            s = e.get()
            if(not s.isnumeric()):
                self.passcode_status = 3
        if(self.passcode_status != 3):
            try:
                if(sum(self.passcode_checklist.values()) == 6):
                    self.passcode_status = 1
                else:
                    self.passcode_status = 2
            except:
                pass
                

    
    def Update_Box(self):
        #self.passcode_status = False
        for i,e in enumerate(self.entry_list):
            key = "D%d"%(i+1)
            if(self.passcode_status in [1, 2]):
                if(self.passcode_checklist[key] == 0):
                    e.config({"background": "Red"})
                else:
                    e.config({"background": "Green"})

            #self.Warning_Window()
        self.check_cells()
        

        
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
    root.geometry("700x550")
    root.resizable(width=True, height=True)
    app = Photonics_Escape_Room(root)
    root.mainloop()

if __name__ == '__main__':
    main()