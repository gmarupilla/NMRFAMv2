# metabolite.py is a subclass of spectrum.py

import os
import sys

import pandas as pd
from .resize_function import extend_ppm
from .resize_function import resizer
from .shift_functions import check_metabolite_shift
from .shift_functions import get_shift_score

from .spectrum import Spectrum


class Metabolite(Spectrum):
    # TODO: are peaks passed as ppms or inds
    def __init__(self, name, ppms, values, peak_ppms=None, peak_inds=None, new_ppms=None, norm=None):
        super().__init__(ppms, values, peak_ppms, peak_inds)
        self.ppms = new_ppms.tolist()
        self.values = norm
        self.name = name
        self.shift = 0
        self.original_shift_score = None
        self.shift_score = None
        self.min_scale = None
        self.max_scale = None
        self.riemannSum = None

    def resize(self, left_ppm_bound, right_ppm_bound, new_size):
        if self.riemannSum is not None:
            print("ERROR: [metabolite.py][resize] Cannot resize after calculating riemannSum")
            sys.exit()

        new_ppms, new_values = extend_ppm(self.ppms, self.values, (left_ppm_bound, right_ppm_bound))
        # Resize metabolites
        new_ppms, new_values = resizer(new_ppms, new_values, new_size, (left_ppm_bound, right_ppm_bound))

        # ppms, values = resizePPMsAndValues(self.ppms, self.values, left_ppm_bound, right_ppm_bound, new_size)
        self.values = new_values.tolist()
        # self.convertPeakPPMsToPeakInds()  # method needs to be added

        if len(self.ppms) != new_size or len(self.values) != new_size:
            print("Error: resize in Metabolite did not return proper data")
            sys.exit()

    def normalize(self):
        # print(self.name)
        sum_ = sum(self.values)
        norm = [float(i) / sum_ for i in self.values]

    def auto_shift(self, mixture_values):

        if len(mixture_values) != len(self.values):
            print(
                "ERROR in auto_shift: the length of the mixture_values does not equal the length of the metabolite values")
            sys.exit()
        if self.peak_ppms is None:
            print("ERROR in auto_shift in Metabolite ")
            sys.exit()
        self.original_shift_score = get_shift_score(self.values, self.peak_inds, mixture_values)
        self.shift, self.shift_score = check_metabolite_shift(self.values, self.peak_inds, mixture_values)

        self.shift_ppm_peaks(self.shift)
        if self.shift < 0:
            self.shift_left(self.shift * -1)
        else:
            self.shift_right(self.shift)

    def shift_ppm_peaks(self, shift_val):
        for i in range(len(self.peak_ppms)):
            self.peak_ppms[i] = self.peak_ppms[i] + shift_val

    def calc_riemann_sum(self):
        self.riemannSum = sum(self.values)

    def get_log_data(self):
        log_data = {
            "start_ppm": self.ppms[0],
            "end_ppm": self.ppms[len(self.ppms) - 1],
            "ppms_length": len(self.ppms),
            "values_length": len(self.values),
            "peak_count": len(self.peak_ppms),
            "peak_ppms": self.peak_ppms,
            "peak_inds": self.peak_inds,
            "shifted_from_original_position": self.shifted,
            "name": self.name,
            "shift": self.shift,
            "original_shift_score": self.original_shift_score,
            "shift_score": self.shift_score
        }
        return log_data

    def save(self, parent_directory):
        metab_directory = parent_directory + self.name
        try:
            os.mkdir(metab_directory)
        except OSError:
            print("Directory creation failed: " + metab_directory)
        else:
            print(metab_directory + " created")

        df = pd.DataFrame({'ppms': self.ppms, 'values': self.values})
        df.to_csv(metab_directory + "/data", index=False)
