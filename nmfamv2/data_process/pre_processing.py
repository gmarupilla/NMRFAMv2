from nmfamv2.spectrum import Spectrum
from nmfamv2.metabolite.metabolite import Metabolite

import sys


def check_parameters(mixture, metabolite_list):
    if not isinstance(mixture, Spectrum):
        print("Error")
        sys.exit()
    if not isinstance(metabolite_list, list):
        print("Error")
        sys.exit()
    if len(metabolite_list) == 0:
        print("Error")
        sys.exit()
    if not isinstance(metabolite_list[0], Metabolite):
        print("Error")
        sys.exit()


def resize_metabolites(mixture, metabolite_list):
    for i in range(len(metabolite_list)):
        metabolite_list[i].resize(mixture.ppms[0], mixture.ppms[len(mixture.ppms) - 1], len(mixture.ppms))


def normalize(metabolite_list):
    for i in range(len(metabolite_list)):
        metabolite_list[i].normalize()


def auto_shift_metabolites(mixture, metabolite_list):
    for i in range(len(metabolite_list)):
        shift_amount = metabolite_list[i].auto_shift(mixture.values)  # Shift metabolite relative to mixture
    # TODO: Must record shift amount


def save_metbolites(metabolite_list):
    for i in range(len(metabolite_list)):
        metabolite_list[i].save("resizedMetabolites/")


def pre_process(mixture, metabolite_list):
    # Perform data checks
    check_parameters(mixture, metabolite_list)

    print("starting peak conversions")
    # For each metabolite in metabolite_list, we need to convert peak_ppms to peak_inds
    for i in range(len(metabolite_list)):
        metabolite_list[i].convertPeakPPMsToPeakInds()

    print("starting resize")
    # Resize metabolites to the size of the mixture
    resize_metabolites(mixture, metabolite_list)

    print("starting normalize")
    # Normalize metaboilite data
    normalize(metabolite_list)

    # saveMetbolites(metabolite_list)

    # Shift metabolites
    auto_shift_metabolites(mixture, metabolite_list)
