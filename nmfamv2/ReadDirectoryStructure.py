import os
import nameTranslator as nt
import pandas as pd

# TODO: nt?, directory?, directory or directory_path?
def readDirectoryStructure(number_translated_name_list, directory_path):
    for bmse_dir in os.listdir(directory_path):
        # if the directory name contains "bmse"...
        if "bmse" in bmse_dir:
            # List all directories in the bmseXXXX directory
            for sim_dir in os.listdir(directory + "/" + bmse_dir):
                # Parse the bmseXXXX's xml file
                tree = ET.parse(directory + "/" + bmse_dir + "/simulation_1/spin_simulation.xml")
                tree_root = tree.getroot()

            # Get metabolite name from the bmseXXXX directory
        metab_name = tree_root.find("name").text

        # Translate the name to its correct code mapping
        name_trans_number = nt.translateName(metab_name)

        if name_trans_number in number_translated_name_list:
            metab_df = pd.read_csv(directory + "/" + bmse_dir + "/simulation_1/B0s/sim_600MHz")
            metab_ppm = list(metab_df['ppm'])
            metab_val = list(metab_df['val'])
            if not os.path.exists(directory + "/" + bmse_dir + "/simulation_1/peaks/sim_600MHz_peaks_standard.csv"):
                continue
            metab_peak_ppm = list(
                pd.read_csv(directory + "/" + bmse_dir + "/simulation_1/peaks/sim_600MHz_peaks_standard.csv")["PPM"])
            read_names.append(metab_name)
            original_length = len(metab_ppm)
            metab_names.append(metab_name)
            metab_ppms.append(metab_ppm)
            metab_vals.append(metab_val)
            metab_peak_ppms.append(metab_peak_ppm)

# if not os.path.exists(directory + "/" + bmse_dir + "/simulation_1/B0s/sim_600MHz"):
#    continue
