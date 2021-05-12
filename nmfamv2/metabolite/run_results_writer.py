import os

import numpy as np
import pandas as pd


def write_metabolites():
    print("TODO")


class RunResultsWriter:
    def __init__(self, results_dir):
        self.results_dir = results_dir
        self.top_dirname = os.path.join(results_dir, "results")

        self.mixture_dir = os.path.join(self.top_dirname, "mixtures")
        self.metab_dir = os.path.join(self.top_dirname, "metabolites")
        self.estimate_dir = os.path.join(self.top_dirname, "estimates")

        os.mkdir(self.top_dirname)
        os.mkdir(self.mixture_dir)
        os.mkdir(self.metab_dir)
        os.mkdir(self.estimate_dir)

    """
        ppms	   values
        __________________
        ppm[0]	   val[0]
        ppm[1]     val[1]
        ppm[2]     val[2]
        ppm[...]   val[...]
    """

    def write_mixture(self, mixture, name_mod=""):
        df = pd.DataFrame(np.array([mixture.ppms, mixture.values]).T, columns=["ppms", "values"])
        df.to_csv(os.path.join(self.mixture_dir, name_mod + "mixture.csv"), index=False)

    """
        name1	       name2		  name3	...
        ______________________________________________
        scale1[0]	   scale2[0]	  scale3[0]
        scale1[1]	   scale2[1]      scale3[1]
        scale1[2]	   scale2[2]	  scale3[2]
        scale1[...]    scale2[...]	  scale3[...]
    """
    def write_estimates(self, estimates_scales, estimate_names, metabolite_names):

        """
            Estimate_scales should be passed as list of lists with form...

            estimate_names[0]	estimate_names[1]	estimate_names[2]	estimate_names[...]
            metab[0]
            metab[1]
            metab[2]
            metab[3]
            metab[...]
        """
        estimate_names.insert(0, "names")
        scales_np_arr = np.array(estimates_scales)
        names_np_arr = np.array([metabolite_names]).transpose()
        np_arr = np.append(names_np_arr, scales_np_arr, axis=1)
        # np_arr = np.concatenate(names_np_arr, scales_np_arr)
        df = pd.DataFrame(np_arr, columns=estimate_names)
        df.to_csv(os.path.join(self.estimate_dir, "estimates.csv"), index=False)


############### TESTS ##############

from nmfamv2.spectrum import Spectrum

# TODO: Move tests


def test_writeMixture():
    mixture = Spectrum([0, 1, 2, 3, 4, 5, 6, 7], [1, 1, 1, 1, 1, 1, 1, 1])
    runResWriter = RunResultsWriter("RunResultsTest")
    runResWriter.write_mixture(mixture, "shifted")


def test_writeEstimates():
    metabolite_names = ["A", "B", "C"]
    estimate_names = ["Pre", "10%", "20%", "30%", "40%", "Final"]
    estimates_scales = [
        [.5, .51, .52, .53, .54, .543],
        [.2, .19, .192, .1921, .1921, .192],
        [0, 0, .1, .08, .071, .071]
    ]
    runResWriter = RunResultsWriter("RunResultsTest")
    runResWriter.write_estimates(estimates_scales, estimate_names, metabolite_names)


def test_fullWriteTest():
    metabolite_names = ["A", "B", "C"]
    estimate_names = ["Pre", "10%", "20%", "30%", "40%", "Final"]
    estimates_scales = [
        [.5, .51, .52, .53, .54, .543],
        [.2, .19, .192, .1921, .1921, .192],
        [0, 0, .1, .08, .071, .071]
    ]
    runResWriter = RunResultsWriter("RunResultsTest")
    runResWriter.write_estimates(estimates_scales, estimate_names, metabolite_names)

    mixture = Spectrum([0, 1, 2, 3, 4, 5, 6, 7], [1, 1, 1, 1, 1, 1, 1, 1])
    runResWriter.write_mixture(mixture, "shifted")

# test_writeMixture()
# test_writeEstimates()
# test_fullWriteTest()
