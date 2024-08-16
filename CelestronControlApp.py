'''

Created on Mar 28, 2021

@author: doktorbrown


Modified Code of How to create Stopwatch
https://www.geeksforgeeks.org/python-create-a-stopwatch-using-clock-object-in-kivy-using-kv-file/
'''
import serial
import nexstar
import kivy
from kivy.app import App
from datetime import datetime

kivy.require('1.11.1')

from kivy.lang import Builder
from kivy.properties import NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock


# Create the .kv file and load it by using Builder
Builder.load_string('''



<RoundButton@Button>:
    background_color: 0,0,0,0
    canvas.before:
        Color:
            rgba: (.7,.7,.7,0.7) if self.state=='normal' else (0.82,0.96,0.92,1)
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [10,]

<RoundToggleButton@ToggleButton>:
    background_color: 0,0,0,0
    canvas.before:
        Color:
            rgba: (.7,.7,.7,0.7) if self.state=='normal' else (0.82,0.96,0.92,1)
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [10,]



<MainWindow>:

    # Assigning the alignment to buttons
    BoxLayout:
        orientation: 'horizontal'

        # Create Button


                          #
        # RoundButton:
            # text: 'AZ -9'
            # on_press: root.azm_negative()
            # on_release: root.azm_stop()
            #
        # RoundButton:
            # text: 'AZ -5'
            # on_press: root.azm_negative_five()
            # on_release: root.azm_stop()
            #
        # RoundButton:
            # text: 'AZ -1'
            # on_press: root.azm_negative_one()
            # on_release: root.azm_stop()


        Button:
            text: 'AZ -9'
            on_press: root.azm_negative()
            on_release: root.azm_stop()

        Button:
            text: 'AZ -5'
            on_press: root.azm_negative_five()
            on_release: root.azm_stop()

        Button:
            text: 'AZ -1'
            on_press: root.azm_negative_one()
            on_release: root.azm_stop()


        Button:
            text: 'AZ +1'
            on_press: root.azm_positive_one()
            on_release: root.azm_stop()



        Button:
            text: 'AZ +5'
            on_press: root.azm_positive_five()
            on_release: root.azm_stop()

        Button:
            text: 'AZ +9'
            on_press: root.azm_positive()
            on_release: root.azm_stop()











    BoxLayout:
        orientation: 'vertical'

        Button:
            text: 'ALT +9'
            on_press: root.alt_positive()
            on_release: root.alt_stop()

        Button:
            text: 'ALT +5'
            on_press: root.alt_positive_five()
            on_release: root.alt_stop()



        Button:
            text: 'ALT +1'
            on_press: root.alt_positive_one()
            on_release: root.alt_stop()


        Button:
            text: 'ALT -1'
            on_press: root.alt_negative_one()
            on_release: root.alt_stop()


        Button:
            text: 'ALT -5'
            on_press: root.alt_negative_five()
            on_release: root.alt_stop()


        Button:
            text: 'ALT -9'
            on_press: root.alt_negative()
            on_release: root.alt_stop()



    # Create the Label
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: str(round(root.number))
            text_size: self.size
            halign: 'center'
            valign: 'middle'

        Label:
            id: timeLabel
            text: str(root.timeNow)
            text_size: self.size
            halign: 'center'
            valign: 'middle'

        # Label:
            # id: internalTime
            # text: str(root.get_time)
            # text_size: self.size
            # halign: 'center'
            # valign: 'middle'

        Label:
            id: readAzimuth
            text: str(root.displayAzimuth)
            text_size: self.size
            halign: 'center'
            valign: 'middle'

        Label:
            id: readAltitude
            text: str(root.displayAltitude)
            text_size: self.size
            halign: 'center'
            valign: 'middle'

        Button:
            text: 'SYNC TIME'
            on_press: root.set_time()

        Button:
            text: 'GET TIME'
            on_press: root.get_time()
''')

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


def nexstarComm(command):

    ser.write(command)
    s = ser.read(100)
    # time.sleep(3)
    # ser.close()

    return(s)




# Create the Layout class
class MainWindow(BoxLayout):

    number = NumericProperty()
    timeNow=str(datetime.now())
    displayAzimuth=(nexstarComm(nexstar.getAZM_ALT_PRECISE))
    displayAltitude=(nexstarComm(nexstar.getRA_DEC_PRECISE))


    def __init__(self, **kwargs):

        # The super() builtin
        # returns a proxy object that
        # allows you to refer parent class by 'super'.
        super(MainWindow, self).__init__(**kwargs)

        # Create the clock and increment the time by .1 ie 1 second.
        Clock.schedule_interval(self.increment_time, .1)
        self.increment_time(0)
        # Clock.schedule_interval(self.increment_time, .1)
        # self.increment_time(0)

    # To increase the time / count
    def increment_time(self, interval):
        timeNow=str(datetime.now())
        displayAzimuth=(nexstarComm(nexstar.getAZM_ALT_PRECISE))
        displayAltitude=(nexstarComm(nexstar.getRA_DEC_PRECISE))
        # print(displayAzimuth)
        # print(timeNow)
        self.number += .1
        self.ids.timeLabel.text = timeNow
        self.ids.readAzimuth.text = str(displayAzimuth)
        self.ids.readAltitude.text = str(displayAltitude)


    def azm_negative(self,*args):
        nexstarComm(nexstar.slewAZM_Negative)

    def azm_positive(self,*args):
        nexstarComm(nexstar.slewAZM_Positive)

    def azm_negative_five(self,*args):
        nexstarComm(nexstar.slewAZM_NegativeFive)

    def azm_positive_five(self,*args):
        nexstarComm(nexstar.slewAZM_PositiveFive)

    def azm_negative_one(self,*args):
        nexstarComm(nexstar.slewAZM_NegativeOne)

    def azm_positive_one(self,*args):
        nexstarComm(nexstar.slewAZM_PositiveOne)

    def azm_stop(self,*args):
        nexstarComm(nexstar.slewAZM_STOP)

    def alt_negative(self,*args):
        nexstarComm(nexstar.slewALT_Negative)

    def alt_positive(self,*args):
        nexstarComm(nexstar.slewALT_Positive)

    def alt_negative_one(self,*args):
        nexstarComm(nexstar.slewALT_NegativeOne)

    def alt_positive_one(self,*args):
        nexstarComm(nexstar.slewALT_PositiveOne)

    def alt_negative_five(self,*args):
        nexstarComm(nexstar.slewALT_NegativeFive)

    def alt_positive_five(self,*args):
        nexstarComm(nexstar.slewALT_PositiveFive)

    def alt_stop(self,*args):
        nexstarComm(nexstar.slewALT_STOP)

    def set_location(self,*args):
        nexstarComm(nexstar.setLocation)

    def get_location(self,*args):
        nexstarComm(nexstar.getLocation)

    def set_time(self,*args):
        nexstarComm(nexstar.setTime)

    def get_time(self,*args):
        nexstarComm(nexstar.getTime)



# Create the App class
class Celestron_ControlApp(App):
    def build(self):
        return MainWindow()

# Run the App
Celestron_ControlApp().run()
