 #------------------------------
    def Device_Analysis(self, file_type):
        """
            Open files at selected path and for each device you could calculate/get
            1) Threshold current
            2) Slope efficiency
            3) Differential Resistance

            file_type: "csv" or "dat"
        """
        x_label = "Current (mA)"

        filepath = fl.get_files_path()
        file_list = fl.get_file_list(filepath, file_type)
        device_name = [] # devicel label on plot
             
        X = []
        Vs = []
        Ps =[]
        try:
            for filename in file_list:
                fn = filename.split("/")[-1].split(".")[0]
                #fn ="_".join(fn.split("_")[2:])
                device_name.append(fn)
                if(file_type == "csv"):
                    I,V,P = fl.read_csv_file(filename)
                else:
                    I,V,P = fl.read_dat_file(filename)
                if (len(I)> len(X)):
                    X = I.tolist()
                Vs.append(V.tolist())
                try: Ps.append(P.tolist())
                except(AttributeError):
                    pass
        except ValueError:
            print(fn)

        y_label = "Power mW)"
        self.plot_XYs(device_name,x_label,y_label,X,Ps, plot_title = None)

        y_label = "Voltage (V)"
        self.plot_XYs(device_name,x_label,y_label,X,Vs,plot_title = None)



    def Device_Analysis_v2(self, is_LI = True):
        """
            Open selected file and for each device you could calculate/get
            1) Threshold current
            2) Slope efficiency
            3) Differential Resistance

            Labels: Voltage versus Power or Current
        """
        filename = fl.get_signle_file()
        labels = {"Voltage":" (V)", "Current":" (mA)","Power":" (mW)"}
        plot_text = {"Voltage":"R:%f Ohm", "Power":"Slope Efficiency: %f W/A"}

        df = pd.read_csv(filename)
        col_name = df.columns
        x = df[col_name[0]]
        device_name = col_name[1:] # label for device on plot
        x_label = x.name + labels[x.name]
        plot_title = "IV Plot"
        y_label = "Voltage (V)"
        #plot_title%("IV")
        if (is_LI):
            y_label = "Optical Power (mW)"
            plot_title = "LI Plot"
            #plot_title%("LI")
    
        ys = []
        for i in range(len(col_name)-1):
            y = df[col_name[i+1]]
            dev_label = col_name[i+1]
            
            self.plot_XY(x_label, y_label, x, y, dev_label,range = (20, None), show_slope = False)
            slope_range = input("Enter the range start and end: (i.e 25, 100) ")
            range_start = int(slope_range.split(",")[0])
            range_end = int(slope_range.split(",")[1])
            self.plot_XY(x_label, y_label, x, y, dev_label,range = (range_start, range_end), show_slope = True)
            repeat = input("Repeat the plot!!! (y or n)")

            if (repeat=="y"):
                range_start = int(slope_range.split(",")[0])
                range_end = int(slope_range.split(",")[1])
                self.plot_XY(x_label, y_label, x, y, dev_label,range = (range_start, range_end), show_slope = True)


            ys.append(y)
    
    #------------------------------

    def plot_XY_withSlope(self, device_name, x_label, y_label, x, y, plot_title, range = (20, None), show_slope = False):
        """
            Return XY plor for given x,y pair. 
            Labels: Voltage versus Power or Current
        """
        #labels = {"Voltage":" (V)", "Current":" (mA)","Power":" (mW)"}
        #plot_text = {"Voltage":"R:%f Ohm", "Power":"Slope Efficiency: %f W/A"}
       
        t=0
        if (t):
            plt.xlabel(x_label)
            plt.ylabel(y_label)
            plt.plot(x, y, linewidth=4)
            if (show_slope):
                slope, c = self.get_slope(x,y,range)
                plt.plot(x, slope*x+ c,'--',Label=device_name)
                #if(y.name == "Voltage"):
                #    slope = slope*1e3
                plt.text(x[20], y[100], "Slope is %f"%(slope))
            plt.title(plot_title)
            plt.grid(True)
            plt.show()
        else:
            plot_title = ""
            device_name = [device_name]
            self.plot_XYs(device_name, x_label, y_label, x, y, plot_title = plot_title, legend_font=10, legend_position=0, label_fontsize=18,axis_value_fontsize=14, lwidth = 2)
  # if (QDL_Coupon):
    #     save_to = "Run-2 do6209\\do6209 QDL Coupon\\do6209_QDL_on_60nm_PECVD SiO2\\2022-01-18\\"
    #     save_to = "Run-2 do6209\\do6209 QDL Coupon\\AU-2-1\\2022-02-28\\" 
    #     #save_to = "Run-2 do6209\\do6209 QDL Coupon\\QDL on Al2O3\\SOI3\\2022-02-09\\"
        
    # else:
    #     #save_to = "Run-2 do6209\\do6209 QDL Coupon\\AU-2-1\\2022-01-07\\"
    #     device_list = {0:"Cleaved Facet Device", 1:"Etched Facet Device",2:"1pMIR Device",3:"2pMIR Device"}
    #     device_lemgth = {0:"CL1mm",1:"CL1.5mm",2:"CL2mm", 3:"CL1.9mm"}
    #     device_index = 2
    #     length_index = 2
    #     save_to = "Run-2 do6209\\do6209 FPL on GaAs\\Devices\\%s\\%s\\Detector Test\\" % (device_list[device_index],device_lemgth[length_index])
    #     save_to = "Run-1 do5960\\do5960 FPL on GaAs\\Devices\\%s\\%s\\" % (device_list[device_index],device_lemgth[length_index])
        
    