import pandas as pd

# TODO: Remove hardcoded PATH below
path_to_mixture_csv = "sample_data/mixture.csv"


def readMixtureFromCSV():
    mixture_df = pd.read_csv(path_to_mixture_csv)

    return list(mixture_df["ppms"]), list(mixture_df["values"])
