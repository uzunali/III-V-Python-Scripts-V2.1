import pandas as pd
import matplotlib as plt

data=pd.DataFrame(columns=("C1","C2","C3"))


for i in range (10):
    datarow={"C1":i,"C2":i*2, "C3":i*3}
    
    data = data.append(datarow, ignore_index = True)


Filename = "mt_file"
data.to_csv(Filename + '.csv',index=False)



data.plot.line(x="C1", y="C2",xlim=(0,10), ylim=(0,20), legend = 0, fontsize = 14, linewidth =3)






