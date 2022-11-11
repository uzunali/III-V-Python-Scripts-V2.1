import win32gui
import win32com.client
import time
import traceback


class Newport_844_PE:
    def __init__(self) -> None:
        self.DeviceHandle = None
        self.device_status = None
        self.OphirCOM = None
        self.first_data = True
        self.initialize_dev()

    def initialize_dev(self):
        try:
            self.OphirCOM = win32com.client.Dispatch("OphirLMMeasurement.CoLMMeasurement")
            # Stop & Close all devices
            self.OphirCOM.StopAllStreams() 
            self.OphirCOM.CloseAll()
            # Scan for connected Devices
            self.DeviceList = self.OphirCOM.ScanUSB()
            print(self.DeviceList)
            device_index = 0
            if len(self.DeviceList)>1:
                device_index = int(input("Please select the device you want to connect! (0 for first device)"))
            self.create_connection(device_index)
               
        except OSError as err:
            print("OS error: {0}".format(err))
        except:
            traceback.print_exc()
    
    def create_connection(self,device_index):
        device = self.DeviceList[device_index]   	# if any device is connected
        self.DeviceHandle = self.OphirCOM.OpenUSBDevice(device)	# open first device
        is_exists = self.OphirCOM.IsSensorExists(self.DeviceHandle, 0)
        self.device_status = is_exists
    
    def close_connection(self):
        #win32gui.MessageBox(0, 'Connection is termineted!', '', 0)
        # Stop & Close all devices
        self.OphirCOM.StopAllStreams()
        self.OphirCOM.CloseAll()
        # Release the object
        self.OphirCOM = None
            
    
    def set_range(self, range_index):
        options = ('AUTO', '30.0mW', '3.00mW', '300uW', '30.0uW', '3.00uW', '300nW', '30.0nW')
        # An Example for Range control. first get the ranges
        ranges = self.OphirCOM.GetRanges(self.DeviceHandle, 0)
        print (ranges)
        self.OphirCOM.SetRange(self.DeviceHandle, 0, ranges[0]-1)
        self.close_connection()

    def get_data(self):

        if self.device_status:
            if(self.first_data):
                self.OphirCOM.StartStream(self.DeviceHandle, 0)		# start measuring
                self.first_data = False
            		
            time.sleep(.2)				# wait a little for data
            data = self.OphirCOM.GetData(self.DeviceHandle, 0)
            if len(data[0]) > 0:		# if any data available, print the first one from the batch
                #print('Reading = {0}, TimeStamp = {1}, Status = {2} '.format(data[0][0] ,data[1][0] ,data[2][0]))
                return(data[0][0])

            else:
                print('\nNo Sensor attached to {0} !!!'.format(self.device))
                return
        #self.close_connection()
         
             



# d = Newport_844_PE()

# d.set_range(range_index=2)
# d.get_data(20)

# d.close_connection()