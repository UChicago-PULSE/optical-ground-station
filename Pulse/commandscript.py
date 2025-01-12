import nexstar
import serial
import threading
import time


ser = serial.Serial(
    port='/dev/tty.PL2303G-USBtoUART110',
    baudrate=9600,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    timeout=1
)

#test connection
print('connected:', ser.name)



# Small script to go Up, Down, Left, Right, and Stop

def nexstarComm(command):
    ser.write(command)

def nexstarComm_read(command,bytes):

    ser.write(command)
    #time.sleep(0.05)
    #print(ser.in_waiting)
    s = ser.read(bytes)
    return(s)
#test alignment
#print(nexstarComm(nexstar.isAlignmentComplete))

def two_direction_slew():
    # This starts slewing in the positive alitude direction, 
    nexstarComm(nexstar.slewALT_Negative)
    time.sleep(1)
    #nexstarComm(nexstar.slewAZM_Positive)
    #time.sleep(2)
    #nexstarComm(nexstar.slewAZM_STOP)
    nexstarComm(nexstar.slewALT_STOP)
#two_direction_slew()    
def variable_rate_AZM_slew(arcsec_rate):
     nexstarComm(nexstar.slewAZM_var(arcsec_rate))
     #nexstarComm(nexstar.slewAZM_STOP)
#variable_rate_AZM_slew(10000)

def get_altaz_while_slewing():
    nexstarComm(nexstar.slewAZM_Negative)
    time.sleep(1)
    print(nexstarComm(nexstar.getAZM_ALT ))
    time.sleep(1)
    print(nexstarComm(nexstar.getAZM_ALT ))
    time.sleep(1)
    print(nexstarComm(nexstar.getAZM_ALT ))
    nexstarComm(nexstar.slewAZM_STOP)
#get_altaz_while_slewing()
def Stop():
    nexstarComm(nexstar.slewAZM_STOP)
    nexstarComm(nexstar.slewALT_STOP)
import numpy as np
def accelerate_slew(start_slew_rate,end_slew_rate,duration):
    steps=100
    times=np.linspace(0,duration,steps)
    slew_rates=np.linspace(start_slew_rate,end_slew_rate,steps)
    for time_loc,rate in list(enumerate(slew_rates)):
        variable_rate_AZM_slew(rate)
        #print(times[time_loc])
        time.sleep(duration/steps)
    #Stop()
accelerate_slew(500,10000,3)
accelerate_slew(10000,0,3)
Stop()
import time
import matplotlib.pyplot as plt
def measure_command_time(start_slew_rate,end_slew_rate,duration):
    steps=30
    #times=np.linspace(0,duration,steps)
    slew_rates=np.linspace(start_slew_rate,end_slew_rate,steps)
    total_start_time=time.time()
    times=[]
    for time_loc,rate in list(enumerate(slew_rates)):
        individual_time_start=time.time()
        variable_rate_AZM_slew(rate)
        print(nexstarComm(nexstar.getAZM_ALT ))
        print(time_loc)
        individual_time_end=time.time()
        times.append(individual_time_end-individual_time_start)
        #print(times[time_loc])
        time.sleep(duration/steps)
    total_end_time=time.time()
    Stop()
    print("Average time to send a command is "+str((total_end_time-total_start_time)/len(slew_rates))+" seconds")
    plt.hist(times,bins=10)
    plt.show()

#measure_command_time(1000,2000)

#print(type(nexstarComm(nexstar.getAZM_ALT )))
Stop()