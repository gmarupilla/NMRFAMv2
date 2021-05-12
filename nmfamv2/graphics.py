# Errors thrown: metabolite_list is not the same size as the each_metabolite_scale

import os
import sys
import matplotlib.pyplot as plt
from nmfamv2.metabolite.metabolite import Metabolite
from .spectrum import Spectrum


# In the graphic object, we'd like to have:
# 1) Each metabolite object reference
# 2) Each metabolite's desired scale (1D list)
# 3) The mixture object reference
class MixtureGraphic:
    def __init__(self, mixture):
        self.mixture = mixture

    def write_mixture(self, full_path, name="mixture"):
        plt.plot(self.mixture.ppms, self.mixture.values)
        plt.title(name)
        plt.savefig(os.path.join(full_path, name), dpi=800)


class MetaboliteGraphic:
    def __init__(self, metabolite_list):
        self.metabolite_list = metabolite_list

    def write_metabolites(self, full_path, name_modifier=""):
        for metab in self.metabolite_list:
            if not os.path.isdir(os.path.join(full_path, metab.name)):
                os.mkdir(os.path.join(full_path, metab.name))
            plt.plot(metab.ppms, metab.values)
            plt.title(metab.name + name_modifier)
            plt.savefig(os.path.join(full_path, metab.name, metab.name + name_modifier), dpi=800)
            plt.cla()


class ScaledGraphic:
    def __init__(self, metabolite_list, mixture, each_metabolite_scale):
        if metabolite_list is None or mixture is None or each_metabolite_scale is None:
            print("Error None param when creating Graphic object")
            sys.exit()
        if len(metabolite_list) != len(each_metabolite_scale):
            print("Error creating Graphic object")
            sys.exit()
        self.metabolite_list = metabolite_list
        self.mixture = mixture
        self.each_metabolite_scale = each_metabolite_scale

    def write_all_scaled_mat_plot_graphics(self, full_path):
        for i in range(len(self.metabolite_list)):
            metab = self.metabolite_list[i]
            scaled_metab_vals = []
            for val in metab.values:
                scaled_metab_vals.append(val * self.each_metabolite_scale[i])

            plt.plot(self.mixture.ppms, self.mixture.values)
            plt.plot(metab.ppms, scaled_metab_vals)
            plt.savefig(os.path.join(full_path, metab.name), dpi=2400)
            plt.cla()

    def write_fitted_mat_plot_graphic(self, full_path):
        fitted_values = [0] * len(self.mixture.ppms)
        for i in range(len(self.metabolite_list)):
            metab = self.metabolite_list[i]
            for j in range(len(metab.values)):
                fitted_values[j] = fitted_values[j] + (metab.values[j] * self.each_metabolite_scale[i])
        plt.plot(self.mixture.ppms, self.mixture.values)
        plt.plot(self.mixture.ppms, fitted_values)
        plt.savefig(os.path.join(full_path, "FittedMixture"), dpi=2400)
        plt.cla()


# TODO: Move to tests


def test_mixture():
    mixture = Spectrum([0, 1, 2, 3, 4, 5, 6, 7], [1, 1, 1, 1, 1, 1, 1, 1])
    graphic = MixtureGraphic(mixture)


def test_scaled_all():
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

    graphic = ScaledGraphic(metabolite_list, mixture, scales)
    graphic.write_all_scaled_mat_plot_graphics("test_dir/")


def test_scaled_fitted():
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

    graphic = ScaledGraphic(metabolite_list, mixture, scales)
    graphic.write_fitted_mat_plot_graphic("test_dir/")

# test_all()
# test_fitted()
