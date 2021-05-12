from nmfamv2.metadata.metadata_parser import parse_metadata

from nmfamv2.mixtures.read_mixture import read_mixture_from_csv
# from ReadMixture import readMixtureFrom1r

from nmfamv2.metabolite.read_metabolites import read_metabolites_from_csv
from nmfamv2.spectrum import Spectrum
import sys

from nmfamv2.metabolite.metabolite import Metabolite


def read_metadata():
    parse_metadata("../SampleMetadata.txt")


# Metabolite list will be an array of Metabolite Objects
def read_metabolite_list():
    names, metabolite_ppms, metabolite_values, metabolite_peak_ppms = read_metabolites_from_csv()

    if len(names) != len(metabolite_ppms):
        print("DATA READ ERROR: names were not same length as metabolite_ppms")
        sys.exit()
    elif len(names) != len(metabolite_values):
        print("DATA READ ERROR: names were not same length as metabolite_values")
        sys.exit()
    elif len(names) != len(metabolite_peak_ppms):
        print("DATA READ ERROR: names were not same length as metabolite_peak_ppms")
        sys.exit()

    metabolite_objs = []

    # We now know that all are the same length
    #   We iterate through and make metabolit objects
    for i in range(len(names)):
        metab_obj = Metabolite(names[i], metabolite_ppms[i], metabolite_values[i], metabolite_peak_ppms[i])
        metabolite_objs.append(metab_obj)

    return metabolite_objs


# Mixture will be a Spectrum object
def read_mixture():
    # Get the data
    # This function must return the ppms and values of the mixture in list form
    # The function below should come from the ReadMixture file and must return ppms and values that pass the checks listed below
    ppms, values = read_mixture_from_csv()

    # ppms, values = readMixtureFrom1r(path)

    #################################
    # Check that ppms and values are the same length and that they are both lists
    if not isinstance(ppms, list):
        print("Error: ppms is not instance of list")
        sys.exit()
    elif not isinstance(values, list):
        print("Error: values is not instance of list")
        sys.exit()
    elif len(ppms) != len(values):
        print("Error: length of ppms does not equal length of values")
        sys.exit()
    elif len(ppms) == 0:
        print("Error: ppms or values have zero length")

    #################################

    # Package into a Spectrum Object -> this line should not change
    mixture_spectrum = Spectrum(ppms, values)

    return mixture_spectrum
