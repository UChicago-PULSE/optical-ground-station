from Pol_Measurement_Class import Pol_Measurement
import os
import math
import matplotlib.pyplot as plt
from Data_analysis_fiber_experiment import *

telescope_object_lst = create_measurement_objects([r"C:\\Users\\juani\\Personal\\CubeSat\\Polarimeter Data\\Telescope Experiment\\Telescope_Experiment_0_Juan.csv"])
telescope_object = telescope_object_lst[0]

telescope_object.create_plot_to_time(param='DOP[%] ', data_point_len=100, data_jump=1)
plt.show()
telescope_object.create_plot_to_time(param='DOCP[%] ', data_point_len=100, data_jump=1)
plt.show()
telescope_object.create_plot_to_time(param='Ellipticity[Â°] ', data_point_len=100, data_jump=1)
plt.show()
telescope_object.create_plot_to_time(param='Power[mW] ', data_point_len=100, data_jump=1)
plt.show()

telescope_object.create_correlation('DOCP[%] ', 'DOP[%] ')
plt.show()