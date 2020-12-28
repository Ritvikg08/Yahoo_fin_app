from yf_data import *
from database import *
from tkinter import *
from _tkinter import *


root=Tk() #Constructor --> Blank Window

#UPDATE DATABASE
root.title("StockDB App")
myLabel= Label(root,text="UPDATE DB")
myLabel.grid(row=0,column=1)
button1=Button(root, text='Update All', fg='red',command=updateAllStocksDB)
button1.grid(row=1,column=1)

#SHOW THE LIST OF ALL STOCKS




#ADD NEW STOCK TO DATABASE
myLabel= Label(root,text="ADD NEW STOCK")
myLabel.grid(row=2,column=1)
label_1=Label(root, text="Stock Symbol")
label_1.grid(row=3,column=0)
entry_1=Entry(root)
entry_1.grid(row=3,column=1)
button2=Button(root, text='submit', fg='blue',command=lambda: addFullStockData(entry_1.get().split(',')))
button2.grid(row=4,column=1)

#GET DATA FOR A STOCK 
myLabel1= Label(root,text="GET STOCK DATA")
myLabel1.grid(row=6,column=1)
label_name=Label(root, text="Stock Symbol")
label_name.grid(row=7,column=0)
entry_name=Entry(root)
entry_name.grid(row=7,column=1)

label_2=Label(root, text="From Date(In dd-mm-yyyy)")
label_2.grid(row=8,column=0)
label_3=Label(root, text="To Date(In dd-mm-yyyy)")
label_3.grid(row=8,column=4)
entry_2=Entry(root)
entry_2.grid(row=8,column=1)
entry_3=Entry(root)
entry_3.grid(row=8,column=5)
button3=Button(root, text='submit', fg='blue',command=lambda: get_StockData(entry_name.get(),datetime.strptime(entry_2.get().replace('-',''), "%d%m%Y").date(),datetime.strptime(entry_3.get().replace('-',''), "%d%m%Y").date()))
button3.grid(row=9,column=2)


#button2=Button(bottomFrame text='Show Stock Data', fg='blue',command=showStockData)
root.mainloop() #Keep the window on screen until we close
exit(0)

