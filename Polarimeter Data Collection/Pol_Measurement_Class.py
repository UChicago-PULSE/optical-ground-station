class Pol_Measurement:
    """
    Class that can be used to retrieve attributes and stuff from multiple measurements with the
    polarimeter. Seems like a good idea to me lol.
    """
    # Initialize measurement
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
        # Getting the data out into a dictionary of lists of data:
        # -9 since the data doesn't start until line 10
        for n in range(len(file_content_lines)-9):
