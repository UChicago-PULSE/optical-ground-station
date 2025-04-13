# imports needed
import zwoasi as asi
import sys
import os
from astropy.io import fits

# suppress this weird error message
import logging
logging.getLogger().setLevel(logging.CRITICAL)
# first load ZWOASI SDK (library of C commands)

sdk_filename = '/Users/ashleyashiku/Desktop/CubeSat/ASI_Camera_SDK/ASI_linux_mac_SDK_V1.37/lib/mac/libASICamera2.dylib'

asi.init(sdk_filename)

print(f"Number of connected cameras: {asi.get_num_cameras()}")

# List cameras and connect to first
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

print("Getting camera property.")
camprop = camera.get_camera_property()
print(camprop)
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
# Use the camera
# writing function to take 8-bit mono image

def eightimage(name):
    """
    This function will take in a file name and take and save a FITS file.
    """
    print('Capturing a single 8-bit mono image')

    # where to save it
    save_dir = "/Users/ashleyashiku/Desktop/CubeSat/cameratest/"
    os.makedirs(save_dir, exist_ok=True)

    camera.set_image_type(asi.ASI_IMG_RAW8)
    image = camera.capture()
    print(f'image taken')

    # specify image name
    imagename = name + ".fits"
    filename = os.path.join(save_dir,imagename)
    fits.writeto(filename, image, overwrite=True)

    print(f"image should be saved in {filename}")

eightimage("test1")