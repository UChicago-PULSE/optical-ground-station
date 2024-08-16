'''
Created on Mar 28, 2021

@author: doktorbrown

basic usb control Class for celestron nexstar 5se mount.  additional controls for svbony305 camera
'''

import serial
from datetime import datetime
# from datetime import time
import time
# import kivy
# from kivy.app import App
# from kivy.uix.gridlayout import GridLayout
# from kivy.uix.label import Label
# from kivy.uix.button import Button
# from kivy.clock import Clock
# from functools import partial
from kivy.event import EventDispatcher
# from kivy.uix.textinput import TextInput
# from kivy.uix.behaviors import ButtonBehavior
# from kivy.uix.widget import Widget
#




# control the mount
#need to search /dev
#likely not the same ID on pi
ser = serial.Serial(
#     port='/dev/cu.usbmodem14241',
#     port='/dev/cu.usbmodem14211',
#     port='/dev/serial/by-id/usb-UNIDEN_AMERICA_CORP._BCD436HP_Serial_Port-if00', #on raspberry pi
#     port='/dev/cu.usbmodem14231',
    # port='/dev/cu.usbmodem1411',
    port='/dev/tty.PL2303G-USBtoUART10',
    baudrate=9600,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    timeout=1

)


#test connection
print('connected:', ser.name)

class Nexstar(EventDispatcher):
    def __init__(self, **kwargs):
        self.register_event_type('on_test')
        super(Nexstar, self).__init__(**kwargs)

    # def nexstarComm(command):
    #
        # ser.write(command)
        # s = ser.read(100)
        # # time.sleep(3)
        # # ser.close()
        #
        # return(s)

    def timeGetter():#will be used to update via setTime push if system vs. scanner time drifts beyond a set delta
    #     today=str(datetime.today())
        # d=str(date.time())
        t=str(datetime.now())
        # print("NOW:  ",t)
        x= t.split()
        dateNow= x[0]
        d=str(dateNow.split())
        # print(len(d))
        yearNow=d[4:6]
        # print("yearNow", yearNow)
        monthNow=d[7:9]
        # print("monthNow",monthNow)
        dayNow=d[10:12]
        # print("dayNow", dayNow)
        y= x[1]
        z=y.split(".")
        timeNow= z[0]
        v=str(timeNow.split())
        # print(len(v))
        hourNow=v[2:4]
        # print("hourNow", hourNow)
        minNow=v[5:7]
        # print("minNow",minNow)
        secNow=v[8:10]
        # print("secNow", secNow)

        return (hourNow,minNow,secNow,monthNow,dayNow,yearNow)

    print(timeGetter())





    #GOTO Commands
    #need to figure out coordinate encoding to hex to pass into this
    #65536/360
    #65536/90

    def gotoRA_DEC(RA,DEC):
        raDec=bytes('R'+ (RA) + ',' + (DEC),'utf-8')
        print("raDec inside gotoRA_DEC  :",  raDec)
        # time.sleep(4)
        return raDec

    def gotoAZM_ALT(ALT,AZM):
        azmAlt=bytes('B'+ (ALT) + ',' + (AZM),'utf-8')
        print("azmAlt inside gotoAZM_ALT  :",  azmAlt)
        # time.sleep(4)
        return azmAlt

    def azm_alt_precise_decimal():
        a=nexstarComm(getAZM_ALT_PRECISE)
        azimuth_decimal=float(a[0])
        altitude_decimal=float(a[1])
        return azimuth_decimal,altitude_decimal

    #Get Position Commands
getRA_DEC = bytes('E','utf-8')
getRA_DEC_PRECISE = bytes('e','utf-8')
getAZM_ALT = bytes('Z','utf-8')
getAZM_ALT_PRECISE = bytes('z','utf-8')

#Tracking Commands
getTrackingMode = bytes('t','utf-8')

#Time/Location Commands
# Location:
# N 40.64600° W 78.09062°
# N40º 30’ 46”  W78º 05’ 24”
# Format= ABCDEFGH
# A=40
# B=30
# C=46
# D=0
# E=78
# F=5
# G=24
# H=1

getLocation = bytes('w','utf-8')
print("getLocation",getLocation)
# b"('\x00\x00K\x1a\x00\x01#"
# b'(\x1e.\x00N\x05\x18\x01#'
setLocation = bytes('W'+ chr(40)+chr(30)+chr(46)+chr(0)+chr(78)+chr(5)+chr(24)+chr(1), 'utf-8')
print("setLocation",setLocation)


getTime = bytes('h','utf-8')

H=Nexstar.timeGetter()
print("H",H[0],H[1],H[2],H[3],H[4],H[5])
# Q=hour
# R=min
# S=sec
# T=month
# U=day
# V=year
# W=251 (offset from GMT. 256 - zone   -5UTC = 251)
# X=1 for Daylight Savings, 0 for Standard Time

setTime = bytes('H'+
                chr(int(H[0]))+
                chr(int(H[1]))+
                chr(int(H[2]))+
                chr(int(H[3]))+
                chr(int(H[4]))+
                chr(int(H[5]))+
                chr(251)+
                chr(1),
                'utf-8')
# print("setTime",setTime)
# print(nexstarComm(getTime))
# print("setTime set",nexstarComm(setTime))
# time.sleep(4)



#Miscellaneous Commands
getVersion = bytes('V', 'utf-8')
getDeviceVersion_AZ_RA_Motor = bytes('P'+ chr(1)+chr(16)+chr(254)+chr(0)+chr(0)+chr(0)+chr(2), 'utf-8')
getDeviceVersion_ALT_DEC_Motor = bytes('P'+ chr(1)+chr(17)+chr(254)+chr(0)+chr(0)+chr(0)+chr(2), 'utf-8')
getDeviceVersion_GPS = bytes('P'+ chr(1)+chr(176)+chr(254)+chr(0)+chr(0)+chr(0)+chr(2), 'utf-8')
getDeviceVersion_RTC = bytes('P'+ chr(1)+chr(178)+chr(254)+chr(0)+chr(0)+chr(0)+chr(2), 'utf-8')
getModel = bytes('m', 'utf-8')
# echoCheck = bytes('K'+chr(x), 'utf-8')
isAlignmentComplete = bytes('J', 'utf-8')
isGotoInProgress = bytes('L', 'utf-8')
cancelGoto = bytes('M', 'utf-8')


#Slewing Commands
#speed set in [4] (0-9)
slewAZM_Positive = bytes('P'+ chr(2)+chr(16)+chr(36)+chr(9)+chr(0)+chr(0)+chr(0), 'utf-8')
slewAZM_STOP = bytes('P'+ chr(2)+chr(16)+chr(36)+chr(0)+chr(0)+chr(0)+chr(0), 'utf-8')
slewAZM_Negative = bytes('P'+ chr(2)+chr(16)+chr(37)+chr(9)+chr(0)+chr(0)+chr(0), 'utf-8')

slewALT_Positive = bytes('P'+ chr(2)+chr(17)+chr(36)+chr(9)+chr(0)+chr(0)+chr(0), 'utf-8')
slewALT_STOP = bytes('P'+ chr(2)+chr(17)+chr(37)+chr(0)+chr(0)+chr(0)+chr(0), 'utf-8')
slewALT_Negative = bytes('P'+ chr(2)+chr(17)+chr(37)+chr(9)+chr(0)+chr(0)+chr(0), 'utf-8')

slewAZM_PositiveOne = bytes('P'+ chr(2)+chr(16)+chr(36)+chr(1)+chr(0)+chr(0)+chr(0), 'utf-8')
slewAZM_NegativeOne = bytes('P'+ chr(2)+chr(16)+chr(37)+chr(1)+chr(0)+chr(0)+chr(0), 'utf-8')

slewALT_PositiveOne = bytes('P'+ chr(2)+chr(17)+chr(36)+chr(1)+chr(0)+chr(0)+chr(0), 'utf-8')
slewALT_NegativeOne = bytes('P'+ chr(2)+chr(17)+chr(37)+chr(1)+chr(0)+chr(0)+chr(0), 'utf-8')


slewAZM_PositiveFive = bytes('P'+ chr(2)+chr(16)+chr(36)+chr(6)+chr(0)+chr(0)+chr(0), 'utf-8')
slewAZM_NegativeFive = bytes('P'+ chr(2)+chr(16)+chr(37)+chr(6)+chr(0)+chr(0)+chr(0), 'utf-8')

slewALT_PositiveFive = bytes('P'+ chr(2)+chr(17)+chr(36)+chr(6)+chr(0)+chr(0)+chr(0), 'utf-8')
slewALT_NegativeFive = bytes('P'+ chr(2)+chr(17)+chr(37)+chr(6)+chr(0)+chr(0)+chr(0), 'utf-8')

