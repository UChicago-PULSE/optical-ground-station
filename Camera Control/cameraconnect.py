# imports needed
import zwoasi as asi
import sys
import os
from astropy.io import fits

# suppress this weird error message
import logging
logging.getLogger().setLevel(logging.CRITICAL)

# first load ZWOASI SDK (library of C commands)
sdk_filename = '/Users/ashleyashiku/Desktop/PULSE-A/ASI_Camera_SDK/ASI_linux_mac_SDK_V1.37/lib/mac/libASICamera2.dylib'
asi.init(sdk_filename)

# Now we're connecting to camera.
print(f"Number of connected cameras: {asi.get_num_cameras()}")

# list cameras and connect to first
num_cameras = asi.get_num_cameras()
if num_cameras == 0:
    print('No cameras found')
    sys.exit(0)

cameras_found = asi.list_cameras()  # Models names of the connected cameras

if num_cameras == 1:
    camera_id = 0
    print('Found one camera: %s' % cameras_found[0])
else:
    print('Found %d cameras' % num_cameras)
    for n in range(num_cameras):
        print('    %d: %s' % (n, cameras_found[n]))
    # TO DO: allow user to select a camera
    camera_id = 0
    print('Using #%d: %s' % (camera_id, cameras_found[camera_id]))

camera = asi.Camera(camera_id)

print("...")
print("Getting camera property.")
cam_prop = camera.get_camera_property()
print(f"Gain: {cam_prop['ElecPerADU']:2f}")
print(f"Pixel size: {cam_prop['PixelSize']}")
#print(asi._get_camera_property)

# getting all camera controls (from demo code)
"""
print('')
print('Camera controls:')
controls = camera.get_controls()
for cn in sorted(controls.keys()):
    print('    %s:' % cn)
    for k in sorted(controls[cn].keys()):
        print('        %s: %s' % (k, repr(controls[cn][k])))
"""

settings = camera.get_control_values()
print("...")
print("here are the current camera controls.")
print(settings)

def exposureconvert(mine, status = False):
    """
    Silly little function to know exposure times. Camera works with exposure times in microseconds (10^-6). Default is
    you enter your time in seconds and function spits out the value in microseconds for you to enter. If status = True, 
    it will do the backwards conversion. Enter in the camera's exposure time and it will convert to seconds for you.
    """
    if status:
        return mine/1000000
    else:
        return mine*1000000
    

"""
Note for future: can clean up this function with a def if main, run main function thing.
"""