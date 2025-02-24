from Pol_Measurement_Class import Pol_Measurement
import os
import math
import matplotlib.pyplot as plt

#file_path = r"C:\Users\juani\Personal\CubeSat\Polarimeter Data\Sample_polarimeter.csv"
#measurement_1 = Pol_Measurement("Measure 1", file_path)

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

measured_objects = create_measurement_objects(create_file_paths_recursive(r"C:\Users\juani\Personal\CubeSat\Polarimeter Data", []))

def show_multi_plots(method_name, *args):
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


def multiplot_method_together(method_name, *args):
    plt.figure()
    for i in range(len(measured_objects)):
        obj = measured_objects[i]
        plot_method = getattr(obj, method_name, None)
        plot_method(*args)
    plt.title("Multi-figure plot")
    plt.show()

#show_multi_plots("create_plot_to_time", "S 0 [mW]", 30)
#show_multi_plots("plot_hist", "S 0 [mW]", 50)
#multiplot_method_together("create_plot_to_time", "S 0 [mW]", 30)