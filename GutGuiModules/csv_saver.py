from GutGuiModules.utility import *
import numpy as np
import os
import logging

class CSVSaver:
    def __init__(self, csv_frame, listener):
        self.root = csv_frame

        # Listener
        self.listener = listener

        self.ogr_butt = None
        self.ogrp_butt = None
        self.normr_butt = None
        self.normrp_butt = None
        self.ogap_butt = None
        self.norma_butt = None
        self.reflectance_text = None
        self.absorbance_text = None

        self._init_widget()

    # Helper
    def _init_widget(self):
        self._build_og_reflectance()
        self._build_og_reflectance_positive()
        self._build_norm_reflectance()
        self._build_og_absorbance_positive()
        self._build_norm_absorbance()
        self._build_text()

    def _build_og_reflectance(self):
        self.ogr_butt = make_button(self.root, text="Original to CSV (Original Data Cube)", command=self.__ogr_to_csv, row=2, column=0, outer_pady=(0, 5), outer_padx=15, width=40)

    def _build_og_reflectance_positive(self):
        self.ogrp_butt = make_button(self.root, text="Original without Negative Values to CSV", command=self.__ogrp_to_csv, row=3, column=0, outer_pady=(0, 5), outer_padx=15, width=40)

    def _build_norm_reflectance(self):
        self.normr_butt = make_button(self.root, text="Normalised to CSV", command=self.__normr_to_csv, row=4, column=0, outer_pady=(0, 5), outer_padx=15, width=40)

    def _build_norm_reflectance(self):
        self.normrp_butt = make_button(self.root, text="Normalised without Negative Values to CSV", command=self.__normrp_to_csv, row=5, column=0, outer_pady=(0, 5), outer_padx=15, width=40)

    def _build_og_absorbance_positive(self):
        self.ogap_butt = make_button(self.root, text="Original to CSV", command=self.__ogap_to_csv, row=7, column=0, outer_pady=(0, 5), outer_padx=15, width=40)

    def _build_norm_absorbance(self):
        self.norma_butt = make_button(self.root, text="Normalised to CSV", command=self.__norma_to_csv, row=8, column=0, outer_pady=(0, 15), outer_padx=15, width=40)

    def _build_text(self):
        self.reflectance_text = make_text(self.root, content="Reflectance:", bg=tkcolour_from_rgb(PASTEL_ORANGE_RGB), column=0, row=1, width=12, pady=(0, 5))
        self.absorbance_text = make_text(self.root, content="Absorbance:", bg=tkcolour_from_rgb(PASTEL_ORANGE_RGB), column=0, row=6, width=11, pady=(10, 5))

    def _make_direc(self, direc):
        if not os.path.isdir(direc):
            os.mkdir(direc)

    def _progress(self, val, total):
        update = ['-', '\\', '|', '/']
        if val != total-1:
            print(update[val%4] + ' ' + str(val+1) + '%', end="\r", flush=True)
        else:
            print(update[val%4] + ' ' + str(val+1) + '%')


    # callbacks

    def __ogr_to_csv(self):
        for path, _ in self.listener.get_results().items():
            selected_paths = self.listener.get_selected_paths()
            if path in selected_paths:
                data = self.listener.ref_data_cube(path)
                direc = os.path.dirname(path) + '/og_ref_data_slices'
                self._make_direc(direc)
                for i in range(100):
                    num = i*5 + 500
                    self._progress(i, 100)
                    big_path = direc + '/' + 'og_ref_data_slice_' + str(num) + '.csv'
                    np.savetxt(big_path, data[:,:,i], delimiter=",", fmt='%f')

    def __ogrp_to_csv(self):
        update = ['-', '\\', '|', '/']
        for path, _ in self.listener.get_results().items():
            selected_paths = self.listener.get_selected_paths()
            if path in selected_paths:
                data = self.listener.ref_non_neg_cube(path)
                direc = os.path.dirname(path) + '/og_ref_positive_data_slices'
                self._make_direc(direc)
                for i in range(100):
                    num = i*5 + 500
                    self._progress(i, 100)
                    big_path = direc + '/' + 'og_ref_positive_data_slice_' + str(num) + '.csv'
                    np.savetxt(big_path, data[:,:,i], delimiter=",", fmt='%s')
        
    def __normr_to_csv(self):
        update = ['-', '\\', '|', '/']
        for path, _ in self.listener.get_results().items():
            selected_paths = self.listener.get_selected_paths()
            if path in selected_paths:
                data = self.listener.ref_norm_cube(path)
                direc = os.path.dirname(path) + '/norm_ref_data_slices'
                self._make_direc(direc)
                for i in range(100):
                    num = i*5 + 500
                    self._progress(i, 100)
                    big_path = direc + '/' + 'norm_ref_data_slice_' + str(num) + '.csv'
                    np.savetxt(big_path, data[:,:,i], delimiter=",", fmt='%f')

    def __normrp_to_csv(self):
        update = ['-', '\\', '|', '/']
        for path, _ in self.listener.get_results().items():
            selected_paths = self.listener.get_selected_paths()
            if path in selected_paths:
                data = self.listener.ref_norm_non_neg_cube(path)
                direc = os.path.dirname(path) + '/norm_ref_data_slices'
                self._make_direc(direc)
                for i in range(100):
                    num = i*5 + 500
                    self._progress(i, 100)
                    big_path = direc + '/' + 'norm_ref_data_slice_' + str(num) + '.csv'
                    np.savetxt(big_path, data[:,:,i], delimiter=",", fmt='%s')
        
    def __ogap_to_csv(self):
        update = ['-', '\\', '|', '/']
        for path, _ in self.listener.get_results().items():
            selected_paths = self.listener.get_selected_paths()
            if path in selected_paths:
                data = self.listener.ab_non_neg_cube(path)
                direc = os.path.dirname(path) + '/og_abs_positive_data_slices'
                self._make_direc(direc)
                for i in range(100):
                    num = i*5 + 500
                    self._progress(i, 100)
                    big_path = direc + '/' + 'og_abs_data_slice_' + str(num) + '.csv'
                    np.savetxt(big_path, data[:,:,i], delimiter=",", fmt='%s')
        
    def __norma_to_csv(self):
        update = ['-', '\\', '|', '/']
        for path, _ in self.listener.get_results().items():
            selected_paths = self.listener.get_selected_paths()
            if path in selected_paths:
                data = self.listener.ab_norm_cube(path)
                direc = os.path.dirname(path) + '/norm_abs_data_slices'
                self._make_direc(direc)
                for i in range(100):
                    num = i*5 + 500
                    self._progress(i, 100)
                    big_path = direc + '/' + 'norm_abs_data_slice_' + str(num) + '.csv'
                    np.savetxt(big_path, data[:,:,i], delimiter=",", fmt='%f')
