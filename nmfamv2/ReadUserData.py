import time

from MetadataParser import parse_metadata

from ReadMixture import readMixtureFromCSV
# from ReadMixture import readMixtureFrom1r

from ReadMetabolites import readMetabolitesFromCSV
from Spectrum import Spectrum
import sys

from Metabolite import Metabolite


def readMetadata():
    parse_metadata("./SampleMetadata.txt")


# Metabolite list will be an array of Metabolite Objects
def readMetaboliteList():
    names, metabolite_ppms, metabolite_values, metabolite_peak_ppms = readMetabolitesFromCSV()

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
def readMixture(path):
    # Get the data
    # This function must return the ppms and values of the mixture in list form
    # The function below should come from the ReadMixture file and must return ppms and values that pass the checks listed below
    ppms, values = readMixtureFromCSV()

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
