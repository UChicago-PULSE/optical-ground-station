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

