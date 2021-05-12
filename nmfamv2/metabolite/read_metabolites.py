import pandas as pd

from nmfamv2.data_process.data_conversion import list_from_list_string

import xml.etree.ElementTree as ET
import os
import sys


# ReadMetabolites function must return the following:
#    names, metabolite_ppms, metabolite_values, metabolite_peak_ppms


def read_metabolites_from_csv(path_to_ppms="sample_data/metabolite_ppms.csv",
                           path_to_values="sample_data/metabolite_values.csv",
                           path_to_peaks="sample_data/metabolite_peaks.csv"):
    metabolite_ppms_df = pd.read_csv(path_to_ppms)
    metabolite_values_df = pd.read_csv(path_to_values)
    metabolite_peak_ppms_df = pd.read_csv(path_to_peaks)

    metabolite_ppms_names = list(metabolite_ppms_df.columns)
    metabolite_values_names = list(metabolite_values_df.columns)
    metabolite_peaks_ppms_names = list(metabolite_peak_ppms_df["names"])

    ###### CHECK NAMES ######
    if not isinstance(metabolite_ppms_names, list):
        print("Error: metabolite_ppms_names not of type list")
        sys.exit()
    if not isinstance(metabolite_values_names, list):
        print("Error: metabolite_values_names not of type list")
        sys.exit()
    if not isinstance(metabolite_peaks_ppms_names, list):
        print("Error: metabolite_peaks_ppms_names not of type list")
        sys.exit()

    if len(metabolite_ppms_names) != len(metabolite_values_names):
        print("Error: metabolite_ppms_names length does not equeal metabolite_values_names length")
        sys.exit()

    if len(metabolite_ppms_names) != len(metabolite_peaks_ppms_names):
        print("Error: metabolite_ppms_names length does not equeal metabolite_peaks_ppms_names length")
        sys.exit()
    # Check that all of the names are the same and in the same order
    for i in range(len(metabolite_ppms_names)):
        if (metabolite_ppms_names[i] != metabolite_values_names[i] or metabolite_values_names[i] !=
                metabolite_peaks_ppms_names[i]):
            print("Error: name arrays do not match at index " + str(i) + " the name in metabolite_ppms_names is '" +
                  metabolite_ppms_names[i] + "' and the name in metabolite_values_names is '" + metabolite_values_names[
                      i] + "' and the name in metabolite_peaks_ppms_names is '" + metabolite_peaks_ppms_names[i] + "'")
            sys.exit()

    # Check that length is non-zero
    if len(metabolite_ppms_names) == 0:
        print("Error: name arrays are empty")
        sys.exit()
    #########################

    ###### Create arrays of ppms and values #####

    names = metabolite_ppms_names  # Can now just refer to both 'metabolite_ppms_names' and 'metabolite_values_names' as 'names' because they have been checked that they are the same
    ppms_list = []
    values_list = []
    for i in range(len(names)):
        ppms_list.append(list(metabolite_ppms_df[names[i]]))
        values_list.append(list(metabolite_values_df[names[i]]))

    ###### CHECK PPMS and VALUES are all lists ######
    if len(ppms_list) != len(values_list):
        print("Error: length of ppms list not equal to length of values list")
        sys.exit()

    if len(ppms_list) == 0:
        print("Error: length of ppms list or values list == 0")
        sys.exit()

    baseline_length = len(ppms_list[0])

    for i in range(len(ppms_list)):
        if not isinstance(ppms_list[i], list):
            print("Error: ppm element not of type 'list'")
            sys.exit()
        if not isinstance(values_list[i], list):
            print("Error: values element not of type 'list'")
            sys.exit()
        if len(ppms_list[i]) != baseline_length:
            print("Error: ppms_list has an element that does not conform to baseline length")
            sys.exit()
        if len(values_list[i]) != baseline_length:
            print("Error: values_list has an element that does not conform to baseline length")
            sys.exit()
    #########################

    ##### Read PeakVals #####
    peak_ppms_list = []

    peak_values = list(metabolite_peak_ppms_df["values"])
    for i in range(len(peak_values)):
        peak_ppms_list.append(list_from_list_string(peak_values[i], float))

    return names, ppms_list, values_list, peak_ppms_list


def grab_gizzmo_metabolites(path_to_directory, metabolite_names):
    # TODO:

    fariba_list = ["DL-2-Aminobutyric acid", "4-methyl-2-oxovaleric acid", "3-hydroxy-3-methylglutaric acid",
                   "3-Hydroxybutyrate",
                   "dl-3-aminoisobutyric acid", "5-aminovaleric acid", "methyl 4-aminobutyrate", "acetic acid",
                   "L-Alanine",
                   "l-anserine", "L-Arginine", "L-Asparagine", "D-Aspartate", "Benzoate", "Betaine", "butyric acid",
                   "Choline",
                   "Citrate", "Creatine", "creatine phosphate", "Creatinine", "DSS", "Ethanol", "Formate",
                   "fumaric acid", "l-glutamic acid", "L-Glutamine", "Glycerol", "Glycine", "L-Histidine",
                   "isobutyric acid",
                   "L-Isoleucine", "l-(+) lactic acid", "l_leucine", "L-Lysine", "malic acid", "Methanol",
                   "L-Methionine", "Myo-Inositol",
                   "acetyl-l-carnitine", "acetylcholine", "l-ornithine", "L-Phenylalanine", "L-Proline",
                   "1,2-propanediol", "R-(+)-2-Pyrrolidinone-5-carboxylate", "pyruvic acid", "Sarcosine",
                   "dioctyl sulfosuccinate", "Taurine",
                   "L-Threonine", "L-Tryptophan", "l-tyrosine", "Uridine", "L-Valine"]

    for i in range(len(fariba_list)):
        fariba_list[i] = fariba_list[i].lower()

    metab_names = []
    metab_ppms = []
    metab_vals = []

    metab_peak_ppms = []
    finished = False
    counter = 0

    read_names = []
    # TODO: directory?
    for bmse_dir in os.listdir(directory):
        if "bmse" in bmse_dir:
            for sim_dir in os.listdir(directory + "/" + bmse_dir):
                if sim_dir == "simulation_1":
                    tree = ET.parse(directory + "/" + bmse_dir + "/simulation_1/spin_simulation.xml")
                    tree_root = tree.getroot()
                    metab_name = tree_root.find("name").text
                    if not metab_name.lower().strip() in fariba_list and not metab_name.lower() in read_names:
                        continue

                    if not os.path.exists(directory + "/" + bmse_dir + "/simulation_1/B0s/sim_600MHz"):
                        continue

                    metab_df = pd.read_csv(directory + "/" + bmse_dir + "/simulation_1/B0s/sim_600MHz")

                    metab_ppm = list(metab_df['ppm'])
                    metab_val = list(metab_df['val'])
                    if not os.path.exists(
                            directory + "/" + bmse_dir + "/simulation_1/peaks/sim_600MHz_peaks_standard.csv"):
                        continue
                    metab_peak_ppm = list(
                        pd.read_csv(directory + "/" + bmse_dir + "/simulation_1/peaks/sim_600MHz_peaks_standard.csv")[
                            "PPM"])
                    read_names.append(metab_name)
                    print("---------")
                    print(bmse_dir)
                    print(metab_name)
                    print("---------")
                    original_length = len(metab_ppm)
                    metab_names.append(metab_name)
                    metab_ppms.append(metab_ppm)
                    metab_vals.append(metab_val)
                    metab_peak_ppms.append(metab_peak_ppm)
                    counter = counter + 1

    print("READ ", counter, " METABOLITES")

    return metab_names, metab_ppms, metab_vals, metab_peak_ppms  # ,metab_peak_inds


read_metabolites_from_csv()
