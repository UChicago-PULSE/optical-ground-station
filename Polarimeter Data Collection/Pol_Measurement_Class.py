import math
import matplotlib.pyplot as plt

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
            if settings_list[0][2] == "¿":
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

    def create_plot_to_time(self, param: str, data_point_len):
        data_dict = self.data
        data = data_dict[param]
        time_list = self.__time_to_milliseconds()
        data_adj = []
        time_list_adj = []
        for i in range(data_point_len):
            data_adj.append(data[i])
            time_list_adj.append(time_list[i])
        plt.plot(time_list_adj, data_adj)
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
