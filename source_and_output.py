from utility import *
import numpy as np
from copy import deepcopy
from tkinter import filedialog

# Manages the source and output directory
class SourceAndOutput:
    def __init__(self, source_and_output_frame):
        # Root
        self.root = source_and_output_frame

        # GUI
        self.select_data_cube_button = None
        self.select_output_dir_button = None

        # Data
        self.data_cube = None
        self.path = ""

        # Widget Initialization
        self._init_widgets()

    # Makes a deep copy of the original data cube
    def get_data_cube(self):
        return deepcopy(self.data_cube)

    def get_path(self):
        return self.path

    def _init_widgets(self):
        self._build_select_dc_button()
        self._build_select_od_button()

    def _build_select_dc_button(self):
        self.select_data_cube_button = make_button(self.root, text="Select Data Cube",
                                                   command=self._set_data_cube, padx=10, pady=10, row=1, column=0)

    def _build_select_od_button(self):
        self.select_output_dir_button = make_button(self.root, text="Select Output Folder",
                                                   command=self._set_output_dir, padx=10, pady=10, row=2, column=0)

    def _set_data_cube(self):
        self.data_cube = self.__process_data_cube()

    def _set_output_dir(self):
        self.path = self.__get_path("Select a folder for the output to be stored.")

    def __process_data_cube(self):
        path = self.__get_path("Select a data cube (ending in .dat)")
        if path[-4:] != ".dat":
            # TODO: MAKE POP UP ERROR MESSAGE
            print("Not a dat file!")
            return None
        else:
            data = np.fromfile(path, dtype='>f')  # returns 1D array and reads file in big-endian binary format
            data_cube = data[3:].reshape(640, 480, 100)  # reshape to data cube and ignore first 3 values which are wrong
            return data_cube

    def __get_path(self, title):
        path = filedialog.askopenfilename(parent=self.root, title=title)
        return path