import numpy as np
import sys
np.set_printoptions(threshold=sys.maxsize)
from AnalysisModules.analysis_constant import *
from AnalysisModules.Indices import Index
from GutGuiModules.utility import *
from GutGuiModules.constants import *
import logging

class RecreatedAnalysis:
    # performs analyses necessary for recreated image
    def __init__(self, path, data_cube, wavelength, index_number, specs, params, listener, mask=None):

        # inputs
        self.path = path
        self.data_cube = data_cube
        self.mask = mask
        self.wavelength = wavelength
        self.absorbance = bool(specs[0])
        self.normal = not bool(specs[1])
        self.negative = bool(specs[2])

        # params
        self.R1 = params[0]
        self.R2 = params[1]
        self.S1 = params[2]
        self.S2 = params[3]
        self.T1 = params[4]
        self.T2 = params[5]
        self.U1 = params[6]
        self.U2 = params[7]

        # calculated generally
        self.x1 = None
        self.x2 = None
        self.x_absorbance = None
        self.x_reflectance = None
        self.x_absorbance_w = None
        self.x_reflectance_w = None
        self.x_absorbance_masked = None
        self.x_absorbance_masked_w = None
        self.x_reflectance_masked = None
        self.x_reflectance_masked_w = None

        # specific to module
        self.sto2 = None
        self.sto2_masked = None
        self.nir = None
        self.nir_masked = None
        self.thi = None
        self.thi_masked = None
        self.twi = None
        self.twi_masked = None

        self._x_absorbance_gradient = None
        self._x_absorbance_gradient_min_1 = None
        self._x_absorbance_gradient_min_2 = None
        self._x_absorbance_min_570_590 = None
        self._x_absorbance_min_740_780 = None
        self._x_absorbance_mean_825_925 = None
        self._x_absorbance_mean_655_735 = None
        self._x_absorbance_mean_530_590 = None
        self._x_absorbance_mean_785_825 = None
        self._x_absorbance_mean_880_900 = None
        self._x_absorbance_mean_955_980 = None

        self._x_reflectance_gradient = None
        self._x_reflectance_gradient_min_1 = None
        self._x_reflectance_gradient_min_2 = None
        self._x_reflectance_min_570_590 = None
        self._x_reflectance_min_740_780 = None
        self._x_reflectance_mean_825_925 = None
        self._x_reflectance_mean_655_735 = None
        self._x_reflectance_mean_530_590 = None
        self._x_reflectance_mean_785_825 = None
        self._x_reflectance_mean_880_900 = None
        self._x_reflectance_mean_955_980 = None

        self.analysis()

    def analysis(self):
        self._calc_general()
        self._calc_sto2()
        self._calc_nir()
        self._calc_thi()
        self._calc_twi()

    def update_mask(self, new_mask):
        self.mask = new_mask
        self.analysis()

    def update_wavelength(self, new_wavelength):
        self.wavelength = new_wavelength
        self.analysis()

    def update_normal(self, new_normal):
        self.normal = new_normal
        self.analysis()

    def update_absorbance(self, new_absorbance):
        self.absorbance = new_absorbance
        self.analysis()

    def update_index(self, new_index_number):
        self.index_number = new_index_number
        self.analysis()

    def get_sto2(self):
        return self.sto2

    def get_sto2_masked(self):
        return self.sto2_masked

    def get_nir(self):
        return self.nir

    def get_nir_masked(self):
        return self.nir_masked

    def get_thi(self):
        return self.thi

    def get_thi_masked(self):
        return self.thi_masked

    def get_twi(self):
        return self.twi

    def get_twi_masked(self):
        return self.twi_masked

    def _calc_general(self):
        logging.debug("CALCULATING: RECREATED IMAGE...")
        self.__calc_x1(self)
        self.__calc_x_reflectance()
        self.__calc_x2()
        self.__calc_x_absorbance()

    def _calc_sto2(self):
        logging.debug("CALCULATING: STO2...")
        if self.absorbance:
            self._x_absorbance_gradient = np.gradient(self.x_absorbance, axis=2)
            self._x_absorbance_gradient_min_1 = self._x_absorbance_gradient[:, :, 14:18].min(axis=2)  # between 570nm and 590nm
            self._x_absorbance_gradient_min_2 = self._x_absorbance_gradient[:, :, 48:56].min(axis=2)  # between 740nm and 780nm
            temp1 = self._x_absorbance_gradient_min_1 / self.R1
            temp2 = self._x_absorbance_gradient_min_2 / self.R2
        else:
            self._x_reflectance_gradient = np.gradient(self.x_reflectance, axis=2)
            self._x_reflectance_gradient_min_1 = self._x_reflectance_gradient[:, :, 14:18].min(axis=2)  # between 570nm and 590nm
            self._x_reflectance_gradient_min_2 = self._x_reflectance_gradient[:, :, 48:56].min(axis=2)  # between 740nm and 780nm
            temp1 = self._x_reflectance_gradient_min_1 / self.R1
            temp2 = self._x_reflectance_gradient_min_2 / self.R2
        self.sto2 = temp1 / (temp1 + temp2)
        logging.debug("Complete Sto2 Mean: " + str(self.sto2[:, :].mean()))
        if self.mask is not None:
            self.sto2_masked = np.ma.array(self.sto2[:, :], mask=[self.mask])
            logging.debug("Masked Sto2 Mean: " + str(self.sto2_masked.mean()))

    def _calc_nir(self):
        logging.debug("CALCULATING: NIR...")
        if self.absorbance:
            self._x_absorbance_mean_825_925 = self.x_absorbance[:, :, 65:85].mean(axis=2)  # between (825nm : 925nm)
            self._x_absorbance_mean_655_735 = self.x_absorbance[:, :, 31:47].mean(axis=2)  # between (655nm : 735nm)
            temp1 = self._x_absorbance_mean_825_925 / self._x_absorbance_mean_655_735
        else:
            self._x_reflectance_mean_825_925 = self.x_reflectance[:, :, 65:85].mean(axis=2)  # between (825nm : 925nm)
            self._x_reflectance_mean_655_735 = self.x_reflectance[:, :, 31:47].mean(axis=2)  # between (655nm : 735nm)
            temp1 = self._x_reflectance_mean_825_925 / self._x_reflectance_mean_655_735
        self.nir = (temp1 - self.S1) / (self.S2 - self.S1)
        logging.debug("Complete NIR Mean: " + str(self.nir[:, :].mean()))
        if self.mask is not None:
            self.nir_masked = np.ma.array(self.nir[:, :], mask=[self.mask])
            logging.debug("Masked NIR Mean: " + str(self.nir_masked.mean()))

    def _calc_thi(self):
        logging.debug("CALCULATING: THI...")
        if self.absorbance:
            self._x_absorbance_mean_530_590 = self.x_absorbance[:, :, 6:18].mean(axis=2)  # between (530nm : 590nm)
            self._x_absorbance_mean_785_825 = self.x_absorbance[:, :, 57:65].mean(axis=2)  # between (785nm : 825nm)
            temp1 = self._x_absorbance_mean_530_590 / self._x_absorbance_mean_785_825
        else:
            self._x_reflectance_mean_530_590 = self.x_reflectance[:, :, 6:18].mean(axis=2)  # between (530nm : 590nm)
            self._x_reflectance_mean_785_825 = self.x_reflectance[:, :, 57:65].mean(axis=2)  # between (785nm : 825nm)
            temp1 = self._x_reflectance_mean_530_590 / self._x_reflectance_mean_785_825
        self.thi = (temp1 - self.T1) / (self.T2 - self.T1)
        logging.debug("Complete THI Mean: " + str(self.thi[:, :].mean()))
        if self.mask is not None:
            self.thi_masked = np.ma.array(self.thi[:, :], mask=[self.mask])
            logging.debug("Masked THI Mean: " + str(self.thi_masked.mean()))

    def _calc_twi(self):
        logging.debug("CALCULATING: TWI...")
        if self.absorbance:
            self._x_absorbance_mean_880_900 = self.x_absorbance[:, :, 76:80].mean(axis=2)  # between (880nm : 900nm)
            self._x_absorbance_mean_955_980 = self.x_absorbance[:, :, 91:96].mean(axis=2)  # between (955nm : 980nm)
            temp1 = self._x_absorbance_mean_880_900 / self._x_absorbance_mean_955_980
        else:
            self._x_reflectance_mean_880_900 = self.x_reflectance[:, :, 76:80].mean(axis=2)  # between (880nm : 900nm)
            self._x_reflectance_mean_955_980 = self.x_reflectance[:, :, 91:96].mean(axis=2)  # between (955nm : 980nm)
            temp1 = self._x_reflectance_mean_880_900 / self._x_reflectance_mean_955_980
        self.twi = (temp1 - self.U1) / (self.U2 - self.U1)
        logging.debug("Complete TWI Mean: " + str(self.twi[:, :].mean()))
        if self.mask is not None:
            self.twi_masked = np.ma.array(self.twi[:, :], mask=[self.mask])
            logging.debug("Masked TWI Mean: " + str(self.twi_masked.mean()))

    @staticmethod
    def __calc_x1(self):
        # normalise
        if self.normal:
            self.x1 = self.data_cube/np.ma.max(self.data_cube)
        else:
            self.x1 = self.data_cube
        # mask negatives
        if self.negative:
            self.x1 = np.ma.array(self.x1, mask=self.x1<0)

    def __calc_x_reflectance(self):
        self.x_reflectance = self.x1

        if self.wavelength[0] != self.wavelength[1]:
            wav_lower = int(round(max(0, min(self.wavelength)), 0))
            wav_upper = int(round(min(max(self.wavelength), 99), 0))
            self.x_reflectance_w = np.mean(self.x_reflectance[:, :, wav_lower : wav_upper], axis=2)
        else:
            self.x_reflectance_w = self.x_reflectance[:, :, self.wavelength[0]]

        if self.mask is not None:
            mask = np.logical_not(np.array([self.mask.T] * 100).T)
            self.x_reflectance_masked = np.ma.array(self.x_reflectance[:, :, :], mask=mask)
            # self.x_reflectance_masked_w = np.ma.array(self.x_reflectance[:, :, self.wavelength[0]], mask=self.mask)
            if self.wavelength[0] != self.wavelength[1]:
                wav_lower = int(round(max(0, min(self.wavelength)), 0))
                wav_upper = int(round(min(max(self.wavelength), 99), 0))
                self.x_reflectance_masked_w = np.ma.array(np.mean(self.x_reflectance[:, :, wav_lower: wav_upper], axis=2), mask=self.mask)
            else:
                self.x_reflectance_masked_w = np.ma.array(self.x_reflectance[:, :, self.wavelength[0]], mask=self.mask)

    def __calc_x2(self):
        self.x2 = -np.ma.log(self.x1)
        self.x2 = np.ma.array(self.x2, mask=~np.isfinite(self.x2))
        if self.negative:
            self.x2 = np.ma.array(self.x2, mask=self.x2<0)

    def __calc_x_absorbance(self):
        self.x_absorbance = self.x2

        if self.wavelength[0] != self.wavelength[1]:
            wav_lower = int(round(max(0, min(self.wavelength)), 0))
            wav_upper = int(round(min(max(self.wavelength), 99), 0))
            self.x_absorbance_w = np.mean(self.x_absorbance[:, :, wav_lower : wav_upper], axis=2)
        else:
            self.x_absorbance_w = self.x_absorbance[:, :, self.wavelength[0]]

        if self.mask is not None:
            # self.x_absorbance_masked = self.__apply_2DMask_on_3DArray(self.mask, self.x_absorbance)
            mask = np.logical_not(np.array([self.mask.T] * 100).T)
            self.x_absorbance_masked = np.ma.array(self.x_absorbance[:, :, :], mask=mask)
            # self.x_absorbance_masked = np.ma.array(self.x_absorbance[:, :, :], mask=np.array([self.mask] * 100))
            if self.wavelength[0] != self.wavelength[1]:
                wav_lower = int(round(min(0, min(self.wavelength)), 0))
                wav_upper = int(round(max(max(self.wavelength), 99), 0))
                self.x_absorbance_masked_w = np.ma.array(np.mean(self.x_absorbance[:, :, wav_lower: wav_upper], axis=2),
                                                         mask=self.mask)
            else:
                self.x_absorbance_masked_w = np.ma.array(self.x_absorbance[:, :, self.wavelength[0]], mask=self.mask)

