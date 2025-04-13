# imports 

### for array operations
import numpy as np

### for plotting
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt


### for operations on FITS images
from astropy.io import fits

### statistics functions needed in this tutorial
from scipy import stats
from scipy.stats import norm

image = fits.open('/Users/ashleyashiku/Desktop/CubeSat/cameratest/test1.fits')

print("here is the image info")
image.info()
print("")
header = image[0].header
imagedata = image[0].data
print("here is the pixel dimensions")
print(imagedata.shape)

countvalues = imagedata.flatten()

print(np.max(countvalues))
print(np.min(countvalues))

print("")
print("histogram")
plt.hist(countvalues,bins=100);
plt.yscale('log')
from IPython.display import Image
# Load image from local storage
#Image(filename = '/Users/ashleyashiku/Desktop/CubeSat/cameratest/test1.fits', width = 400)