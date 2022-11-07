import pandas as pd
import matplotlib.pyplot as plt
from tkinter import filedialog, Tk
import os, csv, glob 

class OpenFile():
           
    def check_is_file_exist(self, filename):
        if (os.path.exists(filename)):
            return True
    
    def save_to_csv_file(self, filename, data, header_flag = True):

        if (header_flag):
            self.f = open('%s' % filename, 'w', newline='')
            if (os.path.exists(filename)):
                print("!!!! File is overwritten !!!!")
        else:
            self.f = open('%s' % filename, 'a', newline='')
    
        writer = csv.writer(self.f)
        # write the data
        writer.writerow(data)
    
    def close_file(self):
        self.f.close()
    
    def read_dat_file(self, filename):
        df = pd.read_table(filename, sep=",")
        col_names = ['Current', 'Power', 'Voltage']
        if(len(df.columns)==2):
            df.columns = ['Current', 'Voltage']
        else:
            df.columns = ['Current', 'Power', 'Voltage']
            #df.columns = col_names[:len(df.columns)]
        I = df['Current']*1e3
        V = df['Voltage']
        try:
            P = df['Power']*1e3
        except(KeyError):
            P = []
        return(I,V,P)

    def read_csv_file(self, filename):
        df = pd.read_csv (filename)
        df.columns = ['Current', 'Voltage','Power']
        
        I = df['Current']*1e0
        V = df['Voltage']
        try:
            P = df['Power']*1e0
        except (KeyError):
            P = []
        return(I,V,P)

    def get_files_path(self):
        root=Tk()
        root.withdraw()
        path = filedialog.askdirectory(initialdir=os.getcwd(), title='Please select the source directory!!!')
        print(path)
        root.destroy()
        return path

    def get_signle_file(self):
        root=Tk()
        root.withdraw()
        path = filedialog.askopenfilename(initialdir=os.getcwd(), title='Please select the file!!!')
        root.destroy()
        print(path)
        return path

    def get_file_list(self, path, file_type):
        # All files ending with .csv
        file_list = glob.glob(path + "/*." + file_type)
        return file_list

    def combine_into_signle_file(self):

        p = self.get_files_path()
        print(p)




