from Pol_Measurement_Class import Pol_Measurement
import os
import math
import matplotlib.pyplot as plt


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
    for path in file_paths:
        path_str_lst = path.split("\\")
        str_name = path_str_lst[-1]
        measurement_list.append(Pol_Measurement(str_name, path))
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

def plot_avg_with_stdev(measured_objects, param):
    # Ignore the figure() argument if you want to show multiple graphs in a single window
    #plt.figure()
    average_param_lst = create_avg_list(measured_objects, param)
    angle_lst = create_angle_list(measured_objects)
    stdev_lst = create_stdev_list(measured_objects, param)
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


def overlay_graph(mo_1: list, mo_2: list, key):
    fig = plt.figure()
    # Producing data for first measurement
    average_param_lst_1 = create_avg_list(mo_1, key)
    angle_lst_1 = create_angle_list(mo_1)
    stdev_lst_1 = create_stdev_list(mo_1, key)

    # Producing data for second measurement
    average_param_lst_2 = create_avg_list(mo_2, key)
    angle_lst_2 = create_angle_list(mo_2)
    stdev_lst_2 = create_stdev_list(mo_2, key)

    # Plotting axes for both
    ax1 = fig.add_subplot(111)
    ax1.scatter(angle_lst_1, average_param_lst_1, s = 10, c = 'b', marker = "s", label = 'first')
    ax1.scatter(angle_lst_2, average_param_lst_2, s = 10, c = 'r', marker = "o", label = 'second')
    # fmt = none adds errorbars without overriding scatter

    plt.errorbar(angle_lst_1, average_param_lst_1, yerr=stdev_lst_1, fmt='None', color='red')
    plt.errorbar(angle_lst_2, average_param_lst_2, yerr=stdev_lst_2, fmt='None', color='red')

    plt.xlabel("Angle [deg]")
    plt.ylabel(key)
    plt.title(f"Angle vs {key}")
    plt.show()


def overlay_multi_graphs(mo_1: list, mo_2: list, keys: list, rows, columns):
    fig = plt.figure()
    # Plotting average with stdev
    for i in range(len(keys)):
        plt.subplot(rows, columns, i + 1)
        # Producing data for first measurement
        average_param_lst_1 = create_avg_list(mo_1, keys[i])
        angle_lst_1 = create_angle_list(mo_1)
        stdev_lst_1 = create_stdev_list(mo_1, keys[i])

        #Producing data for second measurement
        average_param_lst_2 = create_avg_list(mo_2, keys[i])
        angle_lst_2 = create_angle_list(mo_2)
        stdev_lst_2 = create_stdev_list(mo_2, keys[i])

        # Plotting axes for both
        ax1 = fig.add_subplot(111)
        ax1.scatter(angle_lst_1, average_param_lst_1, s = 10, c = 'b', marker = "s", label = 'first')
        ax1.scatter(angle_lst_2, average_param_lst_2, s = 10, c = 'r', marker = "o", label = 'second')
        # fmt = none adds errorbars without overriding scatter

        plt.errorbar(angle_lst_1, average_param_lst_1, yerr=stdev_lst_1, fmt='None', color='red')
        plt.errorbar(angle_lst_2, average_param_lst_2, yerr=stdev_lst_2, fmt='None', color='red')

        plt.xlabel("Angle [deg]")
        plt.ylabel(keys[i])
        plt.title(f"Angle vs {keys[i]}")
    plt.show()

# measured_objects_1 = create_measurement_objects(create_file_paths_non_recursive(r"C:\Users\juani\Personal\CubeSat\Polarimeter Data\Fiber Experiment\panda_normal_sofia_April 1, 2025"))
# measured_objects_2 = create_measurement_objects(create_file_paths_non_recursive(r"C:\Users\juani\Personal\CubeSat\Polarimeter Data\Fiber Experiment\panda_normal_oliver_April 3, 2025"))
# measured_objects_3 = create_measurement_objects(create_file_paths_non_recursive(r"C:\Users\juani\Personal\CubeSat\Polarimeter Data\Fiber Experiment\panda_normal_oliver_April 24, 2025"))

# print(measured_objects_1[0].data_keys)

# params = ['DOP[%] ', 'Ellipticity[Â°] ', 'Phase Difference[Â°] ', 'Power[mW] ']
# for param in params:
#    plot_avg_with_stdev(measured_objects_2, param)
#    plt.show()