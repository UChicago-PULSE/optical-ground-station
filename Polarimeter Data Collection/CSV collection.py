from Pol_Measurement_Class import Pol_Measurement
import os

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
