import nexstar
import serial
import threading
import time
import numpy as np
import matplotlib.pyplot as plt
#from scipy.differentiate import derivative
import numdifftools as nd
max_slew_rate=5*60*60
def two_comp_derivative(func, t_array):
  f1=lambda t: func(t)[:,0]
  f2=lambda t: func(t)[:,1]
  df1=nd.Derivative(f1,n=1)
  df2=nd.Derivative(f2,n=1)
  return np.stack((df1(t_array), df2(t_array)),axis=1)
def deg_to_arcsec(deg):
    arcsec=(60**2)*deg
    return(arcsec)

class Schedule_gen():
    def __init__(self,t0,tf,t_step,function):
        #Make time array
        step_num=np.floor((tf-t0)/t_step)
        self.time_array=t0+t_step*np.arange(step_num)
        self.time_step=t_step
        self.evaluate_position=function
        self.tf=tf
    
    def get_deriv_old(self):
        '''
        This method of getting the derivatives just evaluates the actual function's derviative at the necesseary points, which doesn't quite
        reflect what we're doing here. what we want is just the slope from one evaluated position to the next
        '''
        return two_comp_derivative(self.evaluate_position, self.time_array)
    def get_deriv_slope(self):
        '''
        Gets derivates by just calculationg a slope between points, super simple. 
        '''
        int_pos_array=np.append(self.time_array,self.tf)
        int_positions=self.evaluate_position(int_pos_array)
        deltas=int_positions[1:]-int_positions[:-1]
        deltas[:-1]=np.copy(deltas[:-1])/self.time_step
        deltas[-1]=deltas[-1]/(self.tf-self.time_array[-1])
        return(deltas)
    
    def put_together(self):
        sched=dict()
        sched["time_step"]=self.time_step
        sched["time_array"]=self.time_array
        sched["int_pos_time_array"]=np.append(self.time_array,self.tf)
        sched["int_positions"]=self.evaluate_position(sched["int_pos_time_array"])
        sched["slew_rates"]= self.get_deriv_slope()
        sched["func"]=self.evaluate_position
        return(sched)
    


class OGS_control:
    def __init__(self,name):
        self.path_name=name
        self.global_start_time=time.time()
        self.data_interval=0.1
        self.horizon_aligned=False
        #Initialize slew rates object
        self.slew_rates=list((0,0))
        #Initialize the serial connection
        self.ser = serial.Serial(
        port='/dev/tty.PL2303G-USBtoUART110',
        baudrate=9600,
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        timeout=1)
        
        self.get_azm_alt_runtime=self.measure_runtime_of_get_coords()
        #test connection
        print('connected:', self.ser.name)


    def hex_to_dec(self,s):
        i = int(s, 16)
        return(i)
    def dev_to_hex(self,s):
        i = hex(s)
        return(i)
    
    def nexstarComm_read_until(self,command,stop_char):
        self.ser.write(command)
        s = self.ser.read_until(stop_char)
        return(s)
    
        
    
    def Stop(self):
        self.nexstarComm_read_until(nexstar.slewAZM_STOP,b'#')
        self.nexstarComm_read_until(nexstar.slewALT_STOP,b'#')

    def get_azmalt_degrees(self):
        #Max rotation, maximum decimal number stotred in 4 hex numbers, represents one full rotation
        rot=65535
        #Gets the bytestring
        out_bstring=self.nexstarComm_read_until(nexstar.getAZM_ALT ,b"#")
        #print(out_bstring)
        #Turn it into a regular string
        out_string=out_bstring.decode()
        try:
            az_s,alt_s=out_string.split(",")
        except:
            print("Error here",out_string)
        alt_s,az_s=alt_s.replace("#","") , az_s.replace("#","")
        alt,azm=360*self.hex_to_dec(alt_s)/rot , 360*self.hex_to_dec(az_s)/rot
        #Put return angle between 0 and 360 degrees
        #alt=np.where(alt>180,alt,alt-360)
        #azm=np.where(azm>360,azm,azm-360)
        alt= alt % 360
        azm= azm % 360
        if not self.horizon_aligned:
            return(azm,alt)
        else:
            return(azm-self.zero_azm,alt-self.zero_alt)
  
    def horizon_north_align(self,alt_offset=0):
        '''
        The way this command is meant to be used is that the telescope should be pointing roughly at plevel and northbound. At
        which point this command should be run, which will align the telescope.
        '''
      
        self.zero_azm,self.zero_alt=self.get_azmalt_degrees()
        self.zero_alt-=alt_offset
        print(self.zero_azm,self.zero_alt)
        self.horizon_aligned=True
        print("Alignment attempted")
    def measure_runtime_of_get_coords(self):
        N=10
        time_list=list()
        for a in np.arange(N):
            iter_start_time=time.time()
            (azm_s,alt_z)=self.get_azmalt_degrees()
            dt=time.time()-iter_start_time
            time_list.append(dt)
        #plt.plot(np.arange(len(time_list)),time_list)
        #plt.show()
        print(np.average(time_list))
        return(np.average(time_list))
    def measure_runtime_of_sending_slew_rates(self):
        N=100
        time_list=list()
        alt_slr=np.linspace(0,7200,N)
        azm_slr=np.linspace(0,-7200,N)
        slr_list=np.stack((alt_slr,azm_slr),axis=1)
        
        for a in np.arange(N):
            iter_start_time=time.time()
            alt_slr,az_slr=slr_list[a]
            self.var_AZM_slew(az_slr)
            self.var_ALT_slew(alt_slr)
            dt=time.time()-iter_start_time
            time_list.append(dt)
        self.Stop()
        plt.plot(np.arange(len(time_list)),time_list,'bs')
        plt.show()
        return(np.average(time_list))

    def measure(self,azm_alt_list):

        (azm_s,alt_z)=self.get_azmalt_degrees()
        dt=time.time()-self.global_start_time
        azm_alt_list.append([dt,azm_s,alt_z,self.slew_rates[0],self.slew_rates[1]])
        return(azm_alt_list)
        """
        These two functions are defined as below so that when we send new slew rates, we also update self.slew_rates,
        which lets me append to the data list the commanded slew rates
        """
    def var_AZM_slew(self,rate):
        self.nexstarComm_read_until(nexstar.slewAZM_var(rate),b'#')
        self.slew_rates[1]=rate
    def var_ALT_slew(self,rate):
        self.nexstarComm_read_until(nexstar.slewALT_var(rate),b'#')
        self.slew_rates[0]=rate
    #This might be flipped, watch out!
    def Go_to_AZM_ALT_sat(self,azm,alt):
        full_rot=65536 
        alt_frac=alt/360
        azm_frac=azm/360
        alt_out=hex(round(full_rot*alt_frac))
        azm_out=hex(round(full_rot*azm_frac))
        print((alt_out,azm_out))
        self.nexstarComm_read_until(nexstar.gotoAZM_ALT(azm_out,alt_out),b'#')

    def Go_To_azm_alt(self,target_azmalt,prec=10):
        """
        Go to function that uses only structure from this file. 
        """
        maxrate=3600/3600
        #Assume a=4deg/s^2
        a=4.  #deg/s^2
        #determne max angle of accelerating domain
        theta_accel=0.5*((maxrate/3600)**2)/a
        accel_domain_time=(maxrate/3600)/a
        #Get angular difference
        (cur_azm,cur_alt)=self.get_azmalt_degrees()
        curazmalt=np.array([cur_azm,cur_alt])
        difs=targetazmalt-curazmalt
        argmax=np.argmax(difs)
        #Figure out if we are inside or outside accelerating domain in both dimensions
        accel_domain= abs(difs)<theta_accel
        #Get times to stop in each dimension
        slew_time=np.zeros(2)
        slew_time[accel_domain]=np.sqrt(np.abs((2*difs[accel_domain])/a))
        #We use 2*theta_accel to account for movement while decelerating
        slew_time[~accel_domain]=accel_domain_time + (np.abs(difs[~accel_domain])-2*theta_accel)/maxrate

        #Actually slew!
        #Setup altaz list
        m_azm_alt_list=list()
         
        #Get initial time
        goto_start_time=time.time()
        self.var_AZM_slew(maxrate*3600*np.sign(difs[0]))
        self.var_ALT_slew(maxrate*3600*np.sign(difs[1]))
        self.slew_rates=np.array([maxrate,maxrate])
        first=True
 
        while time.time()-goto_start_time<slew_time.max():
            if first:
                bool_arr=time.time()-goto_start_time<slew_time
                first=False
            nbool_arr=time.time()-goto_start_time<slew_time
            #Detect if we reached any stop times
            if np.array_equiv(nbool_arr,bool_arr):
                self.measure(m_azm_alt_list)
                continue
            #If we have, send new slew rates
            int_arr=nbool_arr.astype(int)
            self.var_AZM_slew(int_arr[0]*maxrate*3600*np.sign(difs[0]))
            self.var_ALT_slew(int_arr[1]*maxrate*3600*np.sign(difs[1]))
            self.slew_rates=3600*np.sign(difs)*int_arr*np.array([maxrate,maxrate])
            bool_arr=nbool_arr
        self.Stop()
        self.slew_rates=np.array([0,0])
        #Wait for things to settle down
        wait_time_start=time.time()
        wait_time=2
        while time.time()<wait_time_start+wait_time:
            self.measure(m_azm_alt_list)
        #Now, calibrate
        #We should be completely inside the acceleration domain here
        #Get difs
        (cur_azm,cur_alt)=self.get_azmalt_degrees()
        curazmalt=np.array([cur_azm,cur_alt])
        difs=targetazmalt-curazmalt
        while difs.max()>prec:
            #Get difs
            (cur_azm,cur_alt)=self.get_azmalt_degrees()
            curazmalt=np.array([cur_azm,cur_alt])
            difs=targetazmalt-curazmalt #in degrees
            self.var_AZM_slew(difs[0]*3600)
            self.var_ALT_slew(difs[1]*3600)
            self.slew_rates=difs*3600
            self.measure(m_azm_alt_list)
        
        return(m_azm_alt_list)
            
            

            
    def do_the_thing(self):
        """
        This command is a intial version of what schedules will look like, set slew rates, wait with measured wait for some 
        time, and write all of that data out.
        """
        self.global_start_time=time.time()
        #Setup altaz list
        m_azm_alt_list=list()
        self.var_AZM_slew(3600)
        self.var_ALT_slew(0)
    
        m_azm_alt_list+=self.measured_wait(2-0.085)
        self.var_AZM_slew(-3600)
        self.var_ALT_slew(0)
        m_azm_alt_list+=self.measured_wait(2-0.085)
        self.Stop()
        return(m_azm_alt_list)

    def follow_schedule(self,schedule):
        self.global_start_time=time.time()
        """
        Takes in a schedule dict as built up by the Schedule_gen class and follows said schedule, doing measured waits at the time intervals
        and returning the recorded positions.

        self.correction_factor: Multiplied with the error angle to give a corrective adjustment. Set to 0 for no correction.
        """
        #self.correction_factor=2
    
        #Setup altaz list
        m_azm_alt_list=list()
        for time_ind in np.arange(len(schedule["time_array"])):
            if time_ind!=0:
                dv=schedule["slew_rates"][time_ind]-schedule["slew_rates"][time_ind-1]
                #print('dv:',dv)
            while (time.time()-self.global_start_time)+self.get_azm_alt_runtime+0.2 <schedule["time_array"][time_ind]:
                self.measure(m_azm_alt_list)
                pass
            #Set the slew rates
            dt=time.time()-self.global_start_time
            alt_slr,az_slr=deg_to_arcsec(schedule["slew_rates"][time_ind])
            #add slew rate correction 
            #if False:
            if len(m_azm_alt_list)>0:
                cur_time,cur_azm,cur_alt=m_azm_alt_list[-1][0],m_azm_alt_list[-1][1],m_azm_alt_list[-1][2]
                #print(cur_time,cur_azm,cur_alt)
                corr_slope_azm=self.correction_factor*deg_to_arcsec((self.func([cur_time])[1]-cur_azm)/self.time_step)
                corr_slope_alt=self.correction_factor*deg_to_arcsec((self.func([cur_time])[0]-cur_alt)/self.time_step)
                print("Measured",cur_azm,cur_alt)
                print("Correction ",corr_slope_azm,corr_slope_alt)

            else:
                corr_slope_azm=0
                corr_slope_alt=0
            if abs(az_slr+corr_slope_azm)<max_slew_rate:
                self.var_AZM_slew(az_slr+corr_slope_azm)
            else:
                sig=int(np.sign(az_slr+corr_slope_azm))
                self.var_AZM_slew(max_slew_rate*sig)
            if abs(alt_slr+corr_slope_alt)<max_slew_rate:
                self.var_ALT_slew(alt_slr+corr_slope_alt)
            else:
                sig=int(np.sign(az_slr+corr_slope_azm))
                self.var_ALT_slew(max_slew_rate*sig)
            #Wait and save to list
        self.measure(m_azm_alt_list)
         
        return(m_azm_alt_list,schedule)
    def do_schedule_and_plot(self,schedule,c_factor):
        self.correction_factor=c_factor
        #self.correction_factor=1
        self.func=schedule["func"]
        self.time_step=schedule["time_step"]
        data_list,schedule=self.follow_schedule(schedule)
        self.Stop()
        data_arr=np.array(data_list)
        print(data_list)

        #Plot path actually taken vs path intended
        fig, ax = plt.subplots(2,2,figsize=(12, 8))
        fig.suptitle(f"Correction factor is {c_factor}")
        #Altitude
        ax[0,0].plot(data_arr[:,0],data_arr[:,2],'bs',label="Altitude measured")
        ax[0,0].plot(schedule["int_pos_time_array"],schedule["int_positions"][:,0],'r',label="Altitude intended")
        ax[0,0].legend(loc='lower left')
        ax[0,0].set_xlabel("Seconds")
        ax[0,0].set_ylabel("Degrees")
        ax[0,0].set_title("Altitude")
        #Altitude error 
        ax[1,0].plot(data_arr[:,0],data_arr[:,2]-self.func(data_arr[:,0])[:,0],'r')
        RMS_alt=np.sqrt((1/len(data_arr[:,2]))*np.sum((data_arr[:,2]-self.func(data_arr[:,0])[:,0])**2))
        ax[1,0].set_xlabel("Seconds")
        ax[1,0].set_ylabel("Degrees")
        ax[1,0].set_title(f"Altitude error, RMS={RMS_alt} deg")
        #Azimuth
        ax[0,1].plot(data_arr[:,0],data_arr[:,1],'bs',label="Azimuth measured")
        ax[0,1].plot(schedule["int_pos_time_array"],schedule["int_positions"][:,1],'r',label="Azimuth intended")
        ax[0,1].legend(loc='lower left')
        ax[0,1].set_xlabel("Seconds")
        ax[0,1].set_ylabel("Degrees")
        ax[0,1].set_title("Azimuth")
        #Azimuth error
        ax[1,1].plot(data_arr[:,0],data_arr[:,1]-self.func(data_arr[:,0])[:,1],'r')
        RMS_azm=np.sqrt((1/len(data_arr[:,1]))*np.sum((data_arr[:,1]-self.func(data_arr[:,0])[:,1])**2))
        ax[1,1].set_xlabel("Seconds")
        ax[1,1].set_ylabel("Degrees")
        ax[1,1].set_title(f"Azimuth error, RMS={RMS_azm} deg")
        plt.tight_layout()
        plt.show()
    def do_and_plot(self):
        data_list=self.do_the_thing()
        data_arr=np.array(data_list)
        print(data_list)
        fig, ax = plt.subplots(1,3,figsize=(12, 8))
        ax[0].plot(data_arr[:,0],data_arr[:,1],'s',label="Altitude")
        ax[0].axvline(x=2)
        ax[1].plot(data_arr[:,0],data_arr[:,2],'s',label="Azimuth")
        ax[2].plot(data_arr[:,0][:-1],-data_arr[:-1,0]+data_arr[1:,0],'s')
        ax[2].set_title("Time between data points")
        ax[2].legend()
        ax[0].set_xlabel("Seconds")
        ax[1].set_xlabel("Seconds")
        ax[2].set_xlabel("Seconds")
        ax[0].set_title("Altitude")
        ax[1].set_title("Azimuth")
        plt.show()




"""
Makes a test pass
a constrols time scale of sine wave
b controls amplitude
c controls the offset of the sine wave from 0, should be equal to whatever offset is given in altitude
"""
alt_offset_val=0
time_step=0.5
a=3
b=5
c=alt_offset_val
def f(x):
    if len(x)==1:
        x=x[0]
        return(np.stack(((c+b*np.cos(x/a)-b),(-b*np.cos(x/a)+b)),axis=0))
    else:
        return(np.stack(((c+b*np.cos(x/a)-b),(-b*np.cos(x/a)+b)),axis=1))
def g(x):
    if x<2:
        return(np.stack((b*x,-b*x),axis=1))
    else:
        return(np.stack((-b*x+2*b,b*x-2*b),axis=1))
Schedule_builder=Schedule_gen(0,4*np.pi*a,time_step,f)
#Schedule_builder=Schedule_gen(0,4,time_step,g)
schedule=Schedule_builder.put_together()
control_object=OGS_control("first pass")
control_object.horizon_north_align(alt_offset=alt_offset_val)
print(control_object.Go_To_azm_alt(10,7))
time.sleep(0.1)
#control_object.Go_To_azm_alt(-1,+1)
print(control_object.get_azmalt_degrees())
#print(schedule)
#for corr_factor in np.linspace(1.5,3.5,10):
 #   control_object=OGS_control("first pass")
 #   control_object.horizon_north_align(alt_offset=alt_offset_val)
 #   print(control_object.do_schedule_and_plot(schedule,corr_factor))

