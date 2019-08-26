from AnalysisModules.analysis_abs import AbsSpecAnalysis
from AnalysisModules.analysis_hist import HistogramAnalysis
from AnalysisModules.analysis_new import NewAnalysis
from AnalysisModules.analysis_recreated import RecreatedAnalysis
from GutGuiModules.utility import *
import numpy as np
import logging


class ModuleListener:
    def __init__(self):
        # {module_name: module}
        self.modules = {}

        # SOURCE AND OUTPUT VALUES
        # {data_cube_path: analysis object}
        self.results = {}
        self.current_rendered_result_path = None
        self.selected_paths = []
        self.output_folder = None  # init with None intentionally

        # NOTE: THE FOLLOWING ONLY CONTROLS WHAT TO RENDER, NOT WHAT IS SAVED

        self.data_cube = None
        self.dc_path = None

        # ANALYSIS AND FORM
        self.normal = None
        self.absorbance = None
        self.wavelength = None
        self.index = None
        self.index_number = None
        self.histogram_specs = None
        self.ab_spec_specs = None
        self.recreated_specs = None
        self.new_specs = None
        self.params = [0.2, -0.03, -0.46, 0.45, 0.4, 1.55, 0.1, -0.5]

        # ORIGINAL IMAGE
        self.mask = []

        # DIAGRAM
        self.is_masked = False

    # ------------------------------------------ INITIALIZATION OF DATA CUBE -----------------------------------------

    def submit_data_cube(self, data_cube, dc_path):
        logging.debug("ANALYZING DATA CUBE AT " + dc_path)

        self.data_cube = data_cube
        self.dc_path = dc_path
        self.results[dc_path] = ['hist', 'abs', 'rec', 'new']

        if self.modules[ANALYSIS_AND_FORM]:
            self.wavelength = self.modules[ANALYSIS_AND_FORM].get_wavelength()
            self.index = self.modules[ANALYSIS_AND_FORM].index_selected
            self.mask = self.modules[ORIGINAL_COLOUR].mask_raw
            self.is_masked = self.modules[DIAGRAM].is_masked

            # specs = (absorbance/reflectance, original/norm, negatives yes/no)
            self.histogram_specs = self.modules[HISTOGRAM].specs
            self.ab_spec_specs = self.modules[ABSORPTION_SPEC].specs
            self.recreated_specs = self.modules[RECREATED_COLOUR].specs
            self.new_specs = self.modules[NEW_COLOUR].specs

            # update each based on inputs
            self._make_new_hist_analysis(dc_path, data_cube, self.wavelength, self.mask,
                                         self.histogram_specs)
            self._make_new_abs_analysis(dc_path, data_cube, self.wavelength, self.mask, self.ab_spec_specs)
            self._make_new_rec_analysis(dc_path, data_cube, self.wavelength, self.mask,
                                        self.recreated_specs, self.params)
            self._make_new_new_analysis(dc_path, data_cube, self.wavelength, self.index, self.mask, self.new_specs)

    def set_data_cube(self, dc_path):
        logging.debug("SELECTED DATA CUBE AT: " + dc_path)
        self.current_rendered_result_path = dc_path
        self.broadcast_new_data()

    def update_selected_paths(self, selected_paths):
        self.selected_paths = selected_paths

    def delete_analysis_result(self, path):
        logging.debug("DELETING DATA CUBE: " + path)
        self.results[path] = None
    # ---------------------------------------------------- MISC ------------------------------------------------------

    def attach_module(self, module_name, mod):
        self.modules[module_name] = mod

    def instant_save_points(self):
        point_bools = self.modules[ORIGINAL_COLOUR].get_bools()
        data = self.get_coords(point_bools)
        self.modules[SAVE].instant_save_points(data, title="MASK_COORDINATES")

    def update_saved(self, saves_key, value):
        logging.debug("UPDATING " + saves_key + " TO " + str(value))
        self.modules[SAVE].update_saves(saves_key, value)

    # --------------------------------------------------- GETTERS ----------------------------------------------------

    def get_result(self, path):
        if self.results[path] is not None:
            return self.results[path]

    def get_mask(self):
        if len(self.mask) != 0:
            return self.mask
        else:
            return np.asarray([[False for _ in range(640)] for _ in range(480)])

    def get_wl(self):
        if self.is_masked:
            return self.get_result(self.current_rendered_result_path)[3].get_wl_data_masked()
        else:
            return self.get_result(self.current_rendered_result_path)[3].get_wl_data()

    def get_idx(self):
        if self.is_masked:
            return self.get_result(self.current_rendered_result_path)[3].index_masked
        else:
            return self.get_result(self.current_rendered_result_path)[3].index

    def get_coords(self, point_bools):
        point_coords = self.modules[ORIGINAL_COLOUR].coords_list
        data = [[float(point_coords[i][0] + 1), float(point_coords[i][1] + 1)] for i in range(10) if
                point_bools[i] and point_coords[i] != (None, None)]
        return data

    # ------------------------------------------------- DATA GETTERS -------------------------------------------------

    def get_current_original_data(self):
        data = self.modules[ORIGINAL_COLOUR].original_image_data
        if not self.is_masked:
            return data
        else:
            mask = np.array([self.mask.T] * 3).T
            return np.ma.array(data, mask=mask)

    def get_current_rec_data(self):
        data = self.modules[RECREATED_COLOUR].recreated_colour_image_data
        if not self.is_masked:
            return data
        else:
            return np.ma.array(data, mask=self.mask)

    def get_current_norm_rec_data(self):
        image = self.modules[RECREATED_COLOUR].recreated_colour_image_data
        data = image / np.ma.max(image)
        if not self.is_masked:
            return data
        else:
            return np.ma.array(data, mask=self.mask)

    def get_current_new_data(self):
        data = self.modules[NEW_COLOUR].new_colour_image_data
        if not self.is_masked:
            return data
        else:
            return np.ma.array(data, mask=self.mask)

    def get_current_norm_new_data(self):
        image = self.modules[NEW_COLOUR].new_colour_image_data
        data = image / np.ma.max(image)
        if not self.is_masked:
            return data
        else:
            return np.ma.array(data, mask=self.mask)

    # --------------------------------------------------- NAMING -----------------------------------------------------

    def get_csv_rec_info(self):
        # retrieve data: display, csv number
        display = self.modules[RECREATED_COLOUR].displayed_image_mode
        num = self.modules[RECREATED_COLOUR].spec_number
        info = '_' + str(display) + '_fromCSV' + str(num)
        return info

    def get_csv_new_info(self):
        # retrieve data: display, csv number
        display = self.modules[NEW_COLOUR].displayed_image_mode
        num = self.modules[NEW_COLOUR].spec_number
        mod = ''
        if display == WL:
            mod = '_WL_' + str(self.wavelength[0] * 5 + 500) + '-' + str(self.wavelength[1] * 5 + 500)
        elif display == IDX:
            mod = '_IDX' + str(self.index)
        info = str(mod) + '_fromCSV' + str(num)
        return info

    def get_save_og_info(self, display, image):
        # e.g. og_image_RGB-cs_masked.png
        # e.g. og_image_THI_whole_data.csv
        grey = self.modules[ORIGINAL_COLOUR].gs
        colour = '-cs'
        if grey:
            colour = '-gs'
        if image:
            return 'og_image_' + display + colour
        else:
            return 'og_image_' + display + '_data'

    def get_save_rec_info(self, display, image):
        # e.g. rec_image_fromCSV2_with-scale_STO2-gs-0.112341-30.122421_whole.png
        # e.g. rec_image_fromCSV2_with-scale_STO2-0.112341-30.122421_masked_data.csv
        num = self.modules[RECREATED_COLOUR].spec_number
        lower = round(float(self.modules[RECREATED_COLOUR].lower_scale_value), 4)
        upper = round(float(self.modules[RECREATED_COLOUR].upper_scale_value), 4)
        grey = self.modules[RECREATED_COLOUR].gs
        colour = '-cs-'
        if grey:
            colour = '-gs-'
        if image:
            return 'rec_image_fromCSV' + str(num), display + colour + str(lower) + '-' + str(upper)
        else:
            return 'rec_image_fromCSV' + str(num) + '_' + display + '-' + str(lower) + '-' + str(upper) + '_data'

    def get_save_new_info(self, display, image):
        # e.g. new_image_fromCSV2_with-scale_IDX1-gs-0.112341-30.122421_masked.png
        # e.g. new_image_fromCSV2_with-scale_WL-500-560-0.112341-30.122421_whole_data.csv
        mod = ''
        num = self.modules[NEW_COLOUR].spec_number
        lower = round(float(self.modules[NEW_COLOUR].lower_scale_value), 4)
        upper = round(float(self.modules[NEW_COLOUR].upper_scale_value), 4)
        if display == 'WL':
            mod = '_WL-' + str(self.wavelength[0] * 5 + 500) + '-' + str(self.wavelength[1] * 5 + 500)
        elif display == 'IDX':
            mod = '_IDX' + str(self.index)
        grey = self.modules[NEW_COLOUR].gs
        colour = '-cs-'
        if grey:
            colour = '-gs-'
        if image:
            return 'new_image_fromCSV' + str(num), mod + colour + str(lower) + '-' + str(upper)
        else:
            return 'new_image_fromCSV' + str(num) + mod + '-' + str(lower) + '-' + str(upper) + '_data'

    def get_save_hist_info(self, scale, image, masked, path):
        # e.g. histogram_fromCSV1_(0-3)-(0-200000)-0.01_with-scale_np.png
        # e.g. histogram_fromCSV9_(0-3)-(0-200000)-0.01_with-scale_np_STO2-csv7-cs-2.62299-0.22225.png
        # e.g. histogram_fromCSV12_(0-3)_(0-200000)-0.01_with-scale_np_IDX3-csv1-gs-2.62299-0.22225.png
        num = self.modules[HISTOGRAM].spec_number
        (xmin, xmax, ymin, ymax, step) = self.generate_hist_values_for_saving(masked, path)
        parametric = self.modules[HISTOGRAM].parametric
        non_parametric = self.modules[HISTOGRAM].non_parametric
        limits = '_(' + str(xmin) + '-' + str(xmax) + ')-(' + str(ymin) + '-' + str(ymax) + ')-' + str(step) + '_'
        scale_mod = 'wo-scale_'
        if scale:
            scale_mod = 'with-scale_'
        p_mod = ''
        if parametric:
            p_mod = 'p_'
        if non_parametric:
            p_mod = 'np_'
        if num == 9 or num == 10:
            data_mod = self.get_abbreviated_rec_info()
        elif num == 11 or num == 12:
            data_mod = self.get_abbreviated_new_info()
        else:
            data_mod = ['', '']
        masked_mod = 'whole'
        if masked:
            masked_mod = 'masked'
        if image:
            return 'histogram_fromCSV' + str(num) + limits + scale_mod + p_mod + data_mod[0] + masked_mod
        else:
            return 'histogram_fromCSV' + str(num) + limits + p_mod + data_mod[1] + masked_mod + '_data'

    def generate_hist_values_for_saving(self, masked, path):
        if not masked:
            arr = self.modules[HISTOGRAM].whole_stats
            return [round(float(arr[i]), 4) for i in range(5)]
        else:
            arr = self.modules[HISTOGRAM].masked_stats
            if arr != [None, None, None, None, None]:
                return [round(float(arr[i]), 4) for i in range(5)]
            else:
                masked_data = self.results[path][0].histogram_data_masked
                lower = np.ma.min(masked_data)
                upper = np.ma.max(masked_data)
                step = 0.01
                bins = np.arange(start=lower, stop=upper + step, step=step)
                histogram_data = np.histogram(masked_data, bins=bins)
                y_min = np.round(np.ma.min(histogram_data[0]), 4)
                y_max = np.round(np.ma.max(histogram_data[0]), 4)
                x_min = np.round(histogram_data[1][0], 4)
                x_max = np.round(histogram_data[1][-1], 4)
                return [x_min, x_max, y_min, y_max, step]

    def get_save_abs_info(self, scale, image):
        # e.g. abspec_fromCSV1_(0-3)_(0-200000)_with-scale.png
        # e.g. abspec_fromCSV1_(0-3)_(0-200000)_with-scale_data.csv
        num = self.modules[ABSORPTION_SPEC].spec_number
        xmin = round(float(self.modules[ABSORPTION_SPEC].x_lower_scale_value), 4)
        xmax = round(float(self.modules[ABSORPTION_SPEC].x_upper_scale_value), 4)
        ymin = round(float(self.modules[ABSORPTION_SPEC].y_lower_scale_value), 4)
        ymax = round(float(self.modules[ABSORPTION_SPEC].y_upper_scale_value), 4)
        limits = '_(' + str(xmin) + '-' + str(xmax) + ')-(' + str(ymin) + '-' + str(ymax) + ')_'
        scale_mod = 'wo-scale'
        if scale:
            scale_mod = 'with-scale'
        if image:
            return 'abspec_fromCSV' + str(num) + limits + scale_mod
        else:
            return 'abspec_fromCSV' + str(num) + limits + 'data'

    def get_abbreviated_rec_info(self):
        # e.g. [0] = STO2-csv7-cs-2.62299-0.22225
        # e.g. [1] = STO2-csv7-2.62299-0.22225
        display = self.modules[RECREATED_COLOUR].displayed_image_mode
        num = self.modules[RECREATED_COLOUR].spec_number
        lower = round(float(self.modules[RECREATED_COLOUR].lower_scale_value), 4)
        upper = round(float(self.modules[RECREATED_COLOUR].upper_scale_value), 4)
        scale_mod = '-' + str(lower) + '-' + str(upper)
        grey = self.modules[RECREATED_COLOUR].gs
        colour = '-cs'
        if grey:
            colour = '-gs'
        image = display + '-csv' + str(num) + colour + scale_mod + '_'
        csv = display + '-csv' + str(num) + scale_mod + '_'
        return [image, csv]

    def get_abbreviated_new_info(self):
        # e.g. [0] = WL-500-500-csv7-cs-2.62299-0.22225
        # e.g. [1] = IDX4-csv7-2.62299-0.22225
        display = self.modules[NEW_COLOUR].displayed_image_mode
        num = self.modules[NEW_COLOUR].spec_number
        lower = round(float(self.modules[NEW_COLOUR].lower_scale_value), 4)
        upper = round(float(self.modules[NEW_COLOUR].upper_scale_value), 4)
        scale_mod = '-' + str(lower) + '-' + str(upper)
        grey = self.modules[NEW_COLOUR].gs
        colour = '-cs'
        if grey:
            colour = '-gs'
        if display == WL:
            mod = 'WL_' + str(self.wavelength[0] * 5 + 500) + '-' + str(self.wavelength[1] * 5 + 500)
        elif display == IDX:
            mod = 'IDX' + str(self.index)
        image = mod + '-csv' + str(num) + colour + scale_mod + '_'
        csv = mod + '-csv' + str(num) + scale_mod + '_'
        return [image, csv]

    # ------------------------------------------------ CSV FUNCTIONS --------------------------------------------------

    def ref_data_cube(self, path):
        # 1. Original reflectance
        # Data cube is originally same for all, use hist because its the first in the list
        cube = self.get_result(path)[0].data_cube.tolist()
        logging.debug("REMOVING NEGATIVE VALUES...")
        for i in range(len(cube)):
            for j in range(len(cube[i])):
                for k in range(len(cube[i][j])):
                    cube[i][j][k] = str(float(cube[i][j][k]))
                progress(j + i * len(cube[i]), 307200)
        return cube

    def ref_non_neg_cube(self, path):
        # 2. Original reflectance without negative values --> 1 with spaces for
        # negative values
        cube = self.get_result(path)[0].data_cube.tolist()
        logging.debug("REMOVING NEGATIVE VALUES...")
        for i in range(len(cube)):
            for j in range(len(cube[i])):
                for k in range(len(cube[i][j])):
                    if cube[i][j][k] < 0:
                        cube[i][j][k] = float('NaN')
                    else:
                        cube[i][j][k] = str(float(cube[i][j][k]))
                progress(j + i * len(cube[i]), 307200)
        return cube

    def ref_norm_cube(self, path):
        # 3. Normalised reflectance --> 1 divded by max(1)
        cube = self.get_result(path)[0].data_cube
        max_val = np.ma.max(cube)
        for i in range(len(cube)):
            for j in range(len(cube[i])):
                for k in range(len(cube[i][j])):
                    cube[i][j][k] = str(float(cube[i][j][k] / max_val))
                progress(j + i * len(cube[i]), 307200)
        return cube

    def ref_norm_non_neg_cube(self, path):
        # 4. Normalised reflectance without negative values --> 3 with spaces
        # for negative values
        cube = self.get_result(path)[0].data_cube
        logging.debug("REMOVING NEGATIVE VALUES...")
        cube = cube / np.ma.max(cube)
        cube = cube.tolist()
        for i in range(len(cube)):
            for j in range(len(cube[i])):
                for k in range(len(cube[i][j])):
                    if cube[i][j][k] < 0:
                        cube[i][j][k] = float('NaN')
                    else:
                        cube[i][j][k] = str(float(cube[i][j][k]))
                progress(j + i * len(cube[i]), 307200)
        return cube

    def ab_data_cube(self, path):
        # 5. Original absorbance --> -log() of 2
        cube = self.get_result(path)[0].data_cube.tolist()
        logging.debug("REMOVING NEGATIVE VALUES...")
        for i in range(len(cube)):
            for j in range(len(cube[i])):
                for k in range(len(cube[i][j])):
                    if cube[i][j][k] <= 0:
                        cube[i][j][k] = float('NaN')
                    else:
                        cube[i][j][k] = str(float(-np.log(cube[i][j][k])))
                progress(j + i * len(cube[i]), 307200)
        return cube

    def ab_non_neg_cube(self, path):
        # 6. Original absorbanve without negative values --> 5 with spaces for
        # negative values
        cube = self.get_result(path)[0].data_cube.tolist()
        logging.debug("REMOVING NEGATIVE VALUES...")
        for i in range(len(cube)):
            for j in range(len(cube[i])):
                for k in range(len(cube[i][j])):
                    if cube[i][j][k] <= 0 or cube[i][j][k] > 1:
                        cube[i][j][k] = float('NaN')
                    else:
                        cube[i][j][k] = str(float(-np.log(cube[i][j][k])))
                progress(j + i * len(cube[i]), 307200)
        return cube

    def ab_norm_cube(self, path):
        # 7. Normalised absorbance --> 5 divided by max(5)
        cube = self.get_result(path)[0].data_cube.tolist()
        logging.debug("FINDING MAX...")
        max5 = -np.ma.log(np.ma.min(np.ma.abs(cube)))
        logging.debug("REMOVING NEGATIVE VALUES...")
        for i in range(len(cube)):
            for j in range(len(cube[i])):
                for k in range(len(cube[i][j])):
                    if cube[i][j][k] <= 0:
                        cube[i][j][k] = float('NaN')
                    else:
                        cube[i][j][k] = str(float(-np.log(cube[i][j][k])) / max5)
                progress(j + i * len(cube[i]), 307200)
        return cube

    def ab_norm_non_neg_cube(self, path):
        # 8. Normalised absorbance without negative values --> 7 with spaces for
        # negative values
        cube = self.get_result(path)[0].data_cube.tolist()
        logging.debug("FINDING MAX...")
        max5 = -np.ma.log(np.ma.min(np.ma.abs(cube)))
        logging.debug("REMOVING NEGATIVE VALUES...")
        for i in range(len(cube)):
            for j in range(len(cube[i])):
                for k in range(len(cube[i][j])):
                    if cube[i][j][k] <= 0 or cube[i][j][k] > 1:
                        cube[i][j][k] = float('NaN')
                    else:
                        cube[i][j][k] = str(float(-np.log(cube[i][j][k])) / max5)
                progress(j + i * len(cube[i]), 307200)
        return cube

    # ------------------------------------------------- SUBMITTERS ---------------------------------------------------

    def submit_mask(self, new_mask):
        logging.debug("NEW MASK: [...]")
        self.mask = new_mask
        self.update_analysis(mask=self.mask)
        if self.is_masked:
            self.broadcast_new_data()

    def submit_wavelength(self, new_wavelength):
        logging.debug("NEW WAVELENGTH: " + str(new_wavelength))
        self.wavelength = new_wavelength
        self.update_analysis(wavelength=self.wavelength)
        self.broadcast_new_data()

    def submit_index(self, new_index_number):
        logging.debug("SETTING NEW INDEX: [...]")
        self.index_number = new_index_number
        self.update_analysis(index_number=self.index_number)
        self.broadcast_new_data()

    def submit_is_masked(self, new_is_masked):
        logging.debug("USING WHOLE IMAGE? " + str(new_is_masked))
        self.is_masked = new_is_masked
        self.broadcast_new_data()

    def submit_params(self):
        self.params = self.modules[PARAMETER].get_params()
        self._make_new_rec_analysis(self.dc_path, self.data_cube, self.wavelength, self.mask,
                                    self.recreated_specs, self.params)
        self.broadcast_to_recreated_image()

    # ------------------------------------------------ BROADCASTERS --------------------------------------------------

    def broadcast_new_data(self):
        self.broadcast_to_histogram()
        self.broadcast_to_absorption_spec()
        self.broadcast_to_recreated_image()
        self.broadcast_to_new_image()
        self.broadcast_to_original_image()

    def broadcast_to_histogram(self):
        if self.is_masked:
            new_histogram_data = self.get_result(self.current_rendered_result_path)[0].histogram_data_masked
        else:
            new_histogram_data = self.get_result(self.current_rendered_result_path)[0].histogram_data
        self.modules[HISTOGRAM].update_histogram(new_histogram_data)

    def broadcast_to_absorption_spec(self):
        if self.is_masked:
            new_absorption_spec = self.get_result(self.current_rendered_result_path)[1].absorption_roi_masked[:, 1]
        else:
            new_absorption_spec = self.get_result(self.current_rendered_result_path)[1].absorption_roi[:, 1]
        self.modules[ABSORPTION_SPEC].update_absorption_spec(new_absorption_spec)

    def broadcast_to_recreated_image(self):
        display_mode = self.modules[RECREATED_COLOUR].displayed_image_mode
        new_data = None
        if display_mode == STO2:
            new_data = self.get_result(self.current_rendered_result_path)[2].sto2
        elif display_mode == NIR:
            new_data = self.get_result(self.current_rendered_result_path)[2].nir
        elif display_mode == THI:
            new_data = self.get_result(self.current_rendered_result_path)[2].thi
        elif display_mode == TWI:
            new_data = self.get_result(self.current_rendered_result_path)[2].twi
        self.modules[RECREATED_COLOUR].update_recreated_image(new_data)

    def broadcast_to_new_image(self):
        display_mode = self.modules[NEW_COLOUR].displayed_image_mode
        new_data = None
        if display_mode == WL:
            new_data = self.get_result(self.current_rendered_result_path)[3].get_wl_data()
        elif display_mode == IDX:
            new_data = self.get_result(self.current_rendered_result_path)[3].index
        self.modules[NEW_COLOUR].update_new_colour_image(new_data)

    def broadcast_to_original_image(self):
        # Use hist to get new images from the file as its the first in analysis list
        display_mode = self.modules[ORIGINAL_COLOUR].displayed_image_mode
        new_data = None
        if display_mode == RGB:
            logging.debug("GETTING RGB IMAGE")
            new_data = self.get_result(self.current_rendered_result_path)[0].get_rgb_og()
        elif display_mode == STO2:
            logging.debug("GETTING STO2 IMAGE")
            new_data = self.get_result(self.current_rendered_result_path)[0].get_sto2_og()
        elif display_mode == NIR:
            logging.debug("GETTING NIR IMAGE")
            new_data = self.get_result(self.current_rendered_result_path)[0].get_nir_og()
        elif display_mode == THI:
            logging.debug("GETTING THI IMAGE")
            new_data = self.get_result(self.current_rendered_result_path)[0].get_thi_og()
        elif display_mode == TWI:
            logging.debug("GETTING TWI IMAGE")
            new_data = self.get_result(self.current_rendered_result_path)[0].get_twi_og()
        self.modules[ORIGINAL_COLOUR].update_original_image(new_data)

    # ----------------------------------------------- MODULE UPDATERS ------------------------------------------------

    def update_analysis(self, mask=None, wavelength=None, index_number=None):
        for path, result_list in self.results.items():  # for each of the cubes
            if mask is not None:
                logging.debug("UPDATING MASK")
                for i in range(4):
                    result_list[i].update_mask(mask)
            if wavelength is not None:
                logging.debug("UPDATING WAVELENGTH TO: " + str(wavelength))
                for i in range(4):
                    result_list[i].update_wavelength(wavelength)
            if index_number is not None:
                logging.debug("UPDATING INDEX TO: " + str(index_number))
                result_list[3].update_index(index_number)

    def update_histogram_specs(self, spec_tup):
        self.histogram_specs = spec_tup
        self._make_new_hist_analysis(self.dc_path, self.data_cube, self.wavelength, self.mask, self.histogram_specs)
        self.broadcast_to_histogram()

    def update_abs_specs(self, spec_tup):
        self.ab_spec_specs = spec_tup
        self._make_new_abs_analysis(self.dc_path, self.data_cube, self.wavelength, self.mask, self.ab_spec_specs)
        self.broadcast_to_absorption_spec()

    def update_recreated_specs(self, spec_tup):
        self.recreated_specs = spec_tup
        self._make_new_rec_analysis(self.dc_path, self.data_cube, self.wavelength, self.mask, self.recreated_specs,
                                    self.params)
        self.broadcast_to_recreated_image()

    def update_new_specs(self, spec_tup):
        self.new_specs = spec_tup
        self._make_new_new_analysis(self.dc_path, self.data_cube, self.wavelength, self.index, self.mask,
                                    self.new_specs)
        self.broadcast_to_new_image()

    # -------------------------------------------- CREATE MODULE OBJECTS ---------------------------------------------

    # Use the path of the data cube as an identifier

    def _make_new_hist_analysis(self, path, data_cube, wavelength, mask, spec_tup):
        self.results[path][0] = HistogramAnalysis(path, data_cube, wavelength, spec_tup, ModuleListener(), mask)

    def _make_new_abs_analysis(self, path, data_cube, wavelength, mask, spec_tup):
        self.results[path][1] = AbsSpecAnalysis(path, data_cube, wavelength, spec_tup, ModuleListener(), mask)

    def _make_new_rec_analysis(self, path, data_cube, wavelength, mask, spec_tup, params):
        self.results[path][2] = RecreatedAnalysis(path, data_cube, wavelength, spec_tup, params, ModuleListener(), mask)

    def _make_new_new_analysis(self, path, data_cube, wavelength, index, mask, spec_tup):
        self.results[path][3] = NewAnalysis(path, data_cube, wavelength, index, spec_tup, ModuleListener(), mask)
