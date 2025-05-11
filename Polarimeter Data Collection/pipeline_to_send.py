import math
import matplotlib.pyplot as plt
import numpy as np
import os
from scipy.optimize import curve_fit


class Pol_Measurement:
    """
    Class that can be used to retrieve attributes and stuff from multiple measurements with the
    polarimeter. Seems like a good idea to me lol. The idea is to reorganize all the data from the
    csv files into attributes, and then create methods useful for data analysis.
    """
    
   
    # Initialize measurement.
    def __init__(self, name: str, file_path: str):
        self.name = name
        self.path = file_path
        
        # Opening csv and collecting data out of it
        file = open(self.path)
        
        # String with all file content
        file_content = file.read()
        file_content_lines = file_content.splitlines()
        
        # Splitting settings content out
        settings_dict = {}
        for i in range(7):
            settings_list = file_content_lines[i].split(" : ;")
            if settings_list[0][2] == "Â¿":
                str_new_lst = []
                for l in range(len(settings_list[0]) - 3):
                    str_new_lst.append(settings_list[0][l + 3])
                settings_list[0] = "".join(str_new_lst)
            for j in range(len(settings_list)):
                if settings_list[j][-1] == ",":
                    str_new_lst = []
                    for k in range(len(settings_list[j]) - 1):
                        str_new_lst.append(settings_list[j][k])
                    settings_list[j] = "".join(str_new_lst)
            settings_dict[settings_list[0]] = settings_list[1]
        self.settings = settings_dict
        self.sample_rate = self.settings["Basic Sample Rate [Hz]"]
        self.wavelength = self.settings["Wavelength [nm]"]
        
        
        # Creating data dictionary:
        data_dict = {}
        # Creating key values for data dict (from row 9 in csv file)
        key_vals = file_content_lines[8].split("; ")
        
        
        # Creating data dictionary
        data_dict = {}
        # -1 comes from the final column being "warnings", which are empty
        
        for x in range(len(key_vals) - 1):
            data_dict[key_vals[x]] = []
            self.data_keys = list(data_dict.keys())
            # Getting the data out into a dictionary of lists of data:
            
            
        # -9 since the data doesn't start until line 10
        for n in range(len(file_content_lines) - 9):
            data_list = file_content_lines[n + 9].split(";")
            
            # Again, empty warning column is avoided with -1, as it results in a list of ","s
            for m in range(len(data_list) - 1):
                if m > 1:
                    data_dict[key_vals[m]] += [float(data_list[m])]
                else:
                    data_dict[key_vals[m]] += [data_list[m]]
        self.data = data_dict
        
        
        # Getting the angle from the name
        name_str_list = self.name.split("_")
        
        
        
        if len(name_str_list) > 2:
            print(name_str_list)
            
            self.angle = float(name_str_list[2])
            
        else:
            
            self.angle = None


    def __time_to_milliseconds(self) -> list[float]:
        
        time_list = self.data["Elapsed Time [hh:mm:ss:ms]"]
        time_ms_list = []
        
        for i in range(len(time_list)):
            
            split_time = time_list[i].split(":")
            
            time_ms_list.append(3600000 * float(split_time[0]) + 60000 * float(split_time[1]) + 1000 * float(split_time[2]) + float(split_time[3]))
        
        return time_ms_list

    def average(self, param: str):
        """
        :param param: String in self.data_keys.
        :return:
        """
        if param not in self.data_keys:
            print(f"ERROR: Please input one of the following data keys: {self.data_keys}")
        else:
            data_list = self.data[param]
            if type(data_list[0]) == float:
                sum_val = 0
                for i in range(len(data_list)):
                    sum_val += data_list[i]
                return sum_val / len(data_list)
            else:
                print("Cannot execute average on non-numerical values")

    def stdev(self, param: str):
        """
        :param param: String in self.data_keys.
        :return:
        """
        if param not in self.data_keys:
            print(f"ERROR: Please input one of the following data keys: {self.data_keys}")
        else:
            data_list = self.data[param]
            if type(data_list[0]) == float:
                #perform stdev computation
                sum_val = 0
                for i in range(len(data_list)):
                    sum_val += (data_list[i] - self.average(param)) ** 2
                return math.sqrt(sum_val / len(data_list))
            else:
                print("Cannot execute average on non-numerical values")

    def create_plot_to_time(self, param: str, data_point_len, data_jump):
        data_dict = self.data
        data = data_dict[param]
        time_list = self.__time_to_milliseconds()
        data_adj = []
        time_list_adj = []
        if data_point_len == "All":
            data_point_len = len(data)
        if len(data) < data_jump * data_point_len:
            print("Data out of index range")
        for i in range(data_point_len):
            data_adj.append(data[i+i*data_jump])
            time_list_adj.append(time_list[i])
        plt.scatter(time_list_adj, data_adj)
        plt.xlabel("Time [ms]")
        plt.ylabel(f"{param}")
        plt.title(f"{param} to time, {self.name}")

    def plot_2param(self, param_x: str, param_y: str):
        data_dict = self.data
        raise NotImplementedError

    def plot_hist(self, param, bins):
        data_dict = self.data
        data = data_dict[param]
        plt.hist(data, bins=bins, color="skyblue", edgecolor="black")
        plt.ylabel("Frequency")
        plt.xlabel(f"{param} value")
        plt.title(f"{param}, {self.name}")

        

def create_file_paths_non_recursive(dir_path: str) -> list[str]:
    """
    :param dir_path: path of directory as a string
    :return: returns file paths inside of the directory
    """
    if not os.path.exists(dir_path) or not os.path.isdir(dir_path):
        raise ValueError("The provided path is not a valid directory.")
    else:
        file_paths = [os.path.join(dir_path, file_name) for file_name in os.listdir(dir_path) if
                      os.path.isfile(os.path.join(dir_path, file_name))]
        return file_paths

def create_file_paths_recursive(dir_path: str, file_paths: list) -> list[str]:
    """
    :param dir_path: path of directory as a string
    :return: returns file paths inside of the directory. Works for a directory of directories
    """
    if os.path.isfile(dir_path):
        
        file_paths.append(dir_path)
        return file_paths
    
    elif os.path.isdir(dir_path):
        for file_name in os.listdir(dir_path):
            file_paths = create_file_paths_recursive(os.path.join(dir_path, file_name), file_paths)
        return file_paths

def create_measurement_objects(file_paths: list[str]):
    """
    :param file_paths: list of file paths as strings
    :return: returns a list of polarization measurement objects
    """
    measurement_list = []
    
#     print('Im here')
    for path in file_paths:
        path_str_lst = path.split(r"/")
        print(path_str_lst)
        str_name = path_str_lst[-1]
        measurement_list.append(Pol_Measurement(str_name, path))
        
    print(measurement_list)
    return measurement_list


def show_multi_plots(measured_objects, method_name, *args):
    num_plots = len(measured_objects)
    rows = math.ceil(math.sqrt(num_plots))  # Number of rows (rounded up)
    cols = math.ceil(num_plots / rows)      # Number of columns

    fig, axes = plt.subplots(rows, cols, figsize=(12, 12))  # Adjust figure size for better visibility
    axes = axes.flatten()  # Flatten 2D array of axes for easy iteration

    for i, obj in enumerate(measured_objects):
        plt.sca(axes[i])  # Set current subplot
        plot_method = getattr(obj, method_name, None)
        plot_method(*args)

    # Hide any unused subplots
    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])

    plt.tight_layout()  # Prevent overlap
    plt.show()


def multiplot_method_together(measured_objects, method_name, *args):
    plt.figure()
    for i in range(len(measured_objects)):
        obj = measured_objects[i]
        plot_method = getattr(obj, method_name, None)
        plot_method(*args)
    plt.title("Multi-figure plot")
    plt.show()
    
    
    

def create_angle_list(measured_objects):
    angle_lst = []
    for i in range(len(measured_objects)):
        angle_lst.append(measured_objects[i].angle)
    return angle_lst

def create_avg_list(measured_objects, param):
    avg_list = []
    for obj in measured_objects:
        avg_list.append(obj.average(param))
    return avg_list

def create_stdev_list(measured_objects, param):
    stdev_list = []
    
    for obj in measured_objects:
        stdev_list.append(obj.stdev(param))
        
    return stdev_list

def create_plot_avg_to_angle(measured_objects, param):
    average_param_lst = create_avg_list(measured_objects, param)
    angle_lst = create_angle_list(measured_objects)
    plt.scatter(angle_lst, average_param_lst)
    plt.xlabel("Angle [deg]")
    plt.ylabel(param)

def create_plot_stdev_to_angle(measured_objects, param):
    stdev_param_lst = create_stdev_list(measured_objects, param)
    angle_lst = create_angle_list(measured_objects)
    plt.scatter(angle_lst, stdev_param_lst)
    plt.xlabel("Angle [deg]")
    plt.ylabel(param)

def plot_avg_with_stdev(measured_objects, param, check_points=False, fit=False, p0=[1, 1,0,0], maxfev=5000):
    # Ignore the figure() argument if you want to show multiple graphs in a single window
    #plt.figure()
    
    average_param_lst = create_avg_list(measured_objects, param)
#     print(f' this is the average parms lst: {average_param_lst}')
    
#     print('-'*20)
    
    angle_lst = create_angle_list(measured_objects)
#     print(f' this is the angle list: {angle_lst}')
    
#     print('-'*20)
    
    stdev_lst = create_stdev_list(measured_objects, param)
#     print(f' this is the standard deviation list: {stdev_lst}')
    
    if check_points: #only use when need to check points 
        average_param_lst2 = check_points_func(average_param_lst, angle_lst)
        
        
    if fit:
        line_of_fit1, x1 = poly_fit(angle_lst, average_param_lst)
        
        #fit of a fit
        
        line_of_fit2, x2 = cosine_fit(line_of_fit1, x1, angle_lst, p0=p0)
        
#         if only_poly_fit:
      
#         plt.plot(x1, line_of_fit1, color='magenta')
        plt.plot(x2, line_of_fit2, color='black')
        
         
    plt.scatter(angle_lst, average_param_lst)
    
    # fmt = none adds errorbars without overriding scatter
    plt.errorbar(angle_lst, average_param_lst, yerr=stdev_lst, fmt='None', color='red')
    plt.xlabel("Angle [deg]")
    plt.ylabel(param)
    plt.title(f"Angle vs {param}")


def multiple_avgwstdev_plots(measured_objects, param_keys: list[str], rows, columns):
    plt.figure()
    for i in range(len(param_keys)):
        plt.subplot(rows, columns, i + 1)
        plot_avg_with_stdev(measured_objects, param_keys[i])
        plt.title(f"Angle vs {param_keys[i]}")
    plt.show()

    
    
def check_points_func(param_points, angle_list):
    
    for i in range(len(angle_list)):
        
        if angle_list[i] == 0.0:
            
            param_points[i] = param_points[i] - 360.
                 
    return param_points


def poly_fit(angle, params, porder=5):
    
    """
    This is a polynomial fit. 
    """
    
    
    polyfit = np.polyfit(angle, params, porder)
    
    x = np.linspace(min(angle), max(angle), 500)
    
    pfit = np.poly1d(polyfit) 
    
    ftest = pfit(x)

    return ftest, x

def cosine_model(x, A, B, C, D):
    return A * np.cos(B * np.radians(x) + C) + D


def cosine_fit(ftest, x, p0=[1,1,0,0], maxfev=5000):
    
    """
    This is a cosine fit. Can be used to fit for the fit, which is what we are using it for.
    
    maxfev - is the number of max iterations for the fit.
    
    p0- is the initial guess for the fit. 
    
    x- array values for input function
    
    ftest- function to be fitted. 
    
    """
    
    popt_cosine, _ = curve_fit(cosine_model, x, ftest, p0=p0, maxfev=maxfev)
    x_fit = np.linspace(min(x), max(x), 500)
    
    print(f'This is my Initial Guess: {popt_cosine}')
    
    print(' ')
    
    print(f'This is the Function of best fit: {popt_cosine[0]:.2f}*cos({popt_cosine[1]:.2f}x + {popt_cosine[2]:.2f}) + {popt_cosine[-1]:.2f}')

    # Compute fitted curves
    params_fit_cosine = cosine_model(x_fit, *popt_cosine)
    
    return params_fit_cosine, x_fit







