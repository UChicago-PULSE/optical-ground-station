from tkinter import *
from tkinter import ttk
import nexstar_alt
import serial
import time

#Make serial connection

ser = serial.Serial(
    port='/dev/tty.PL2303G-USBtoUART110',
    baudrate=9600,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    timeout=1
)
#Define some slewing-related stuff
def nexstarComm(command):
    ser.write(command)
def Stop():

    nexstarComm(nexstar_alt.slewALT_STOP)
    time.sleep(0.1)
    nexstarComm(nexstar_alt.slewAZM_STOP)

    

    
def variable_rate_AZM_slew(arcsec_rate):
     nexstarComm(nexstar_alt.slewAZM_var(arcsec_rate))
def variable_rate_ALT_slew(arcsec_rate):
     nexstarComm(nexstar_alt.slewALT_var(arcsec_rate))

#Define functions for the callback on each button
def slew_pos_AZM(*args):
    rate = float(rate_entry.get())
    variable_rate_AZM_slew(rate)
def slew_neg_AZM(*args):
    rate = float(rate_entry.get())
    variable_rate_AZM_slew(-rate)
def slew_pos_ALT(*args):
    rate = float(rate_entry.get())
    variable_rate_ALT_slew(rate)
def slew_neg_ALT(*args):
    rate = float(rate_entry.get())
    variable_rate_ALT_slew(-rate)


#Basic setup
root = Tk()
root.title("Silly controller")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)


#Enter slew rate
rate = StringVar()
rate_entry = ttk.Entry(mainframe, width=7, textvariable=rate)
rate_entry.grid(column=2, row=1, sticky=(W, E))
ttk.Label(mainframe, text='Enter arcsecond rate here:').grid(column=1, row=1, sticky=W)


#Make the buttons for moving
ttk.Button(mainframe, text="->", command=slew_pos_AZM).grid(column=3, row=3,sticky=W)
ttk.Button(mainframe, text="<-", command=slew_neg_AZM).grid(column=1, row=3, sticky=E)
ttk.Button(mainframe, text="up", command=slew_pos_ALT).grid(column=2, row=2, sticky=S)
ttk.Button(mainframe, text="STOP", command= Stop).grid(column=2, row=3, sticky=W)
ttk.Button(mainframe, text="down", command=slew_neg_ALT).grid(column=2, row=4, sticky=N)



for child in mainframe.winfo_children(): 
    child.grid_configure(padx=5, pady=5)
#Set the focus on the rate_entry widget
rate_entry.focus()


root.mainloop()