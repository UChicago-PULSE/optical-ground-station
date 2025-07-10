# imports needed
import zwoasi as asi
import sys
import os
from astropy.io import fits
from cameraconnect import*
"""
This file is to take images.
"""


def takepic(exposure, gain, name, camera):
    """"
    This function will take an image. 
    Inputs:
        exposure: exposure time (micro - seconds)
        gain: camera gain
        name: name of the camera file saved
    """
    imagesetting(exposure, gain, camera)
    eightimage(name, camera)



def imagesetting(exposure, gain, camera):
    """
    This function will set the exposure time and gain of the camera.
    Inputs:
        exposure: int, exposure time, in MICROSECONDS (1e-6)
        gain: int, number of counts per electron

    """
    print("Changing exposure time.")
    camera.set_control_value(asi.ASI_EXPOSURE, exposure)
    camera.set_control_value(asi.ASI_GAIN, gain)
    settings = camera.get_control_values()
    print(f"Exposure time is now {settings['Exposure']} microseconds, {settings['Exposure']/1000000} seconds.")
    print(f"Gain is now {settings['Gain']}.")

# Use the camera
# writing function to take 8-bit mono image

def eightimage(name, camera):
    """
    This function will take in a file name and take and save a FITS file.
    """
    print('Capturing a single 8-bit mono image')

    # where to save it
    save_dir = "/Users/ashleyashiku/Desktop/PULSE-A/cameratest/"
    os.makedirs(save_dir, exist_ok=True)

    camera.set_image_type(asi.ASI_IMG_RAW8)
    image = camera.capture()
    print(f'image taken. trust me on it. ')

    # specify image name
    imagename = name + ".fits"
    filename = os.path.join(save_dir,imagename)
    fits.writeto(filename, image, overwrite=True)

    print(f"image should now be saved in {filename}. go look!")


cam_1 = camconnect()
takepic(1000,  4.736763, "firstattach", camera=cam_1)


#print("Changing exposure time.")
#camera.set_control_value(asi.ASI_EXPOSURE, 10000000)
#camera.set_control_value(asi.ASI_GAIN, 4)
#settings = camera.get_control_values()
#print(f"Exposure time is now {settings['Exposure']} microseconds, {settings['Exposure']/1000000} seconds.")
#print(f"Gain is now {settings['Gain']}.")
#get_camera_info = asi.ASISetControlValue(0, ASI_EXPOSURE, 10000, ASI_FALSE)
#print(get_camera_info)