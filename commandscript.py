import nexstar
import serial
import threading
import time


ser = serial.Serial(
    port='/dev/tty.PL2303G-USBtoUART10',
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
    s = ser.read(100)
    # time.sleep(3)
    # ser.close()

    return(s)

nexstarComm(nexstar.slewALT_Negative)
time.sleep(1)
nexstarComm(nexstar.slewALT_Positive)
time.sleep(1)
nexstarComm(nexstar.slewALT_STOP)
nexstarComm(nexstar.slewAZM_Negative)
time.sleep(1)
nexstarComm(nexstar.slewAZM_Positive)
time.sleep(1)
nexstarComm(nexstar.slewAZM_STOP)



