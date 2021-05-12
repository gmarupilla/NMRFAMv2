import json
import os

from nmfamv2.graphics import MetaboliteGraphic, MixtureGraphic, ScaledGraphic


class RunLog:
    def __init__(self, user_dir):
        self.user_dir = user_dir
        self.top_dirname = os.path.join(user_dir, "logs")

        self.mixture_dir = os.path.join(self.top_dirname, "mixtures")
        self.metab_dir = os.path.join(self.top_dirname, "metabolites")
        self.fitted_dir = os.path.join(self.top_dirname, "fitted")

        os.mkdir(self.top_dirname)
        os.mkdir(self.mixture_dir)
        os.mkdir(self.metab_dir)
        os.mkdir(self.fitted_dir)

    def log_mixture(self, mixture, label):
        # Write Log Data
        mixLogData = mixture.getLogData()
        with open(os.path.join(self.mixture_dir, "mixture" + label + ".txt"), 'w') as file:
            file.write(json.dumps(mixLogData))

        # Write Graphs
        mixtureGraphic = MixtureGraphic(mixture)
        mixtureGraphic.write_mixture(self.mixture_dir, label)

    def log_metab_list(self, metabolite_list, label):
        # Write Log Data
        for metab in metabolite_list:
            metabLogData = metab.getLogData()
            with open(os.path.join(self.metab_dir, metab.name + label + ".txt"), 'w') as file:
                file.write(json.dumps(metabLogData))

        # Write Graphs
        metaboliteGraphic = MetaboliteGraphic(metabolite_list)
        metaboliteGraphic.write_metabolites(self.metab_dir, label)

    def log_fitted_all_metabs(self, metabolite_list, mixture, each_metabolite_scale, path=""):
        new_path = self.fitted_dir + path
        if not os.path.isdir(new_path):
            os.mkdir(new_path)
        scaledGraphic = ScaledGraphic(metabolite_list, mixture, each_metabolite_scale)
        scaledGraphic.write_all_scaled_mat_plot_graphics(self.fitted_dir + path)

    def log_fitted_metabs(self, metabolite_list, mixture, each_metabolite_scale, path=""):
        new_path = self.fitted_dir + path
        if not os.path.isdir(new_path):
            os.mkdir(new_path)
        scaledGraphic = ScaledGraphic(metabolite_list, mixture, each_metabolite_scale)
        scaledGraphic.write_fitted_mat_plot_graphic(self.fitted_dir + path)


from nmfamv2.spectrum import Spectrum
from nmfamv2.metabolite.metabolite import Metabolite


# TODO: Move tests


def test_logMixture():
    runLog = RunLog("RunLogTests")

    mixture = Spectrum([0, 1, 2, 3, 4, 5, 6, 7], [1, 1, 1, 1, 1, 1, 1, 1])
    runLog.log_mixture(mixture, "original")


def test_logMetab():
    runLog = RunLog("RunLogTests")

    metabolite_list = [
        Metabolite("A", [0, 1, 2, 3, 4, 5, 6, 7], [0, 0, 0, 0, 0, 0, 1, 0], peak_ppms=[6], peak_inds=[6]),
        Metabolite("B", [0, 1, 2, 3, 4, 5, 6, 7], [0, 0, 1, 0, 0, 0, 0, 0], peak_ppms=[2], peak_inds=[2]),
        Metabolite("C", [0, 1, 2, 3, 4, 5, 6, 7], [0, 0, 0, 0, 0, 0, 1, 0], peak_ppms=[6], peak_inds=[6])
    ]
    runLog.log_metab_list(metabolite_list, "shifted")


def test_logAllFitted():
    runLog = RunLog("RunLogTests")

    # Define metabolite_list
    metabolite_list = [
        Metabolite("A", [0, 1, 2, 3, 4, 5, 6, 7], [0, 0, 0, 0, 0, 0, 1, 0], peak_ppms=[6], peak_inds=[6]),
        Metabolite("B", [0, 1, 2, 3, 4, 5, 6, 7], [0, 0, 1, 0, 0, 0, 0, 0], peak_ppms=[2], peak_inds=[2]),
        Metabolite("C", [0, 1, 2, 3, 4, 5, 6, 7], [0, 0, 0, 0, 0, 0, 1, 0], peak_ppms=[6], peak_inds=[6])
    ]

    # Define a mixture
    mixture = Spectrum([0, 1, 2, 3, 4, 5, 6, 7], [1, 1, 1, 1, 1, 1, 1, 1])

    # Create scales
    scales = [3, 4, 2]

    runLog.log_fitted_all_metabs(metabolite_list, mixture, scales)


def test_logFitted():
    runLog = RunLog("RunLogTests")

    # Define metabolite_list
    metabolite_list = [
        Metabolite("A", [0, 1, 2, 3, 4, 5, 6, 7], [0, 0, 0, 0, 0, 0, 1, 0], peak_ppms=[6], peak_inds=[6]),
        Metabolite("B", [0, 1, 2, 3, 4, 5, 6, 7], [0, 0, 1, 0, 0, 0, 0, 0], peak_ppms=[2], peak_inds=[2]),
        Metabolite("C", [0, 1, 2, 3, 4, 5, 6, 7], [0, 0, 0, 0, 0, 0, 1, 0], peak_ppms=[6], peak_inds=[6])
    ]

    # Define a mixture
    mixture = Spectrum([0, 1, 2, 3, 4, 5, 6, 7], [1, 1, 1, 1, 1, 1, 1, 1])

    # Create scales
    scales = [3, 4, 2]

    runLog.log_fitted_metabs(metabolite_list, mixture, scales)

# test_logMixture()
# test_logMetab()
# test_logAllFitted()
# test_logFitted()
