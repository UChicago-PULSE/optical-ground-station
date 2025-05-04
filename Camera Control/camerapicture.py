# imports needed
import zwoasi as asi
import sys
import os
from astropy.io import fits
from cameraconnect import camera
"""
This file is to take images.
"""

print("...")
print("test changing exposure time.")
camera.set_control_value(asi.ASI_EXPOSURE, 58)
settings2 = camera.get_control_values()
print(settings2['Exposure'])
print(exposureconvert(1))
#get_camera_info = asi.ASISetControlValue(0, ASI_EXPOSURE, 10000, ASI_FALSE)
#print(get_camera_info)



# Use the camera
# writing function to take 8-bit mono image

def eightimage(name):
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

eightimage("may3_58micron")