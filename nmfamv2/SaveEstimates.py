import pandas as pd
import numpy as np

from time import time


def saveEstimates(estimates):
    df = pd.DataFrame(np.array([[*estimates]]), columns=["estimates"])
    timestamp = str(int(time.time()))
    df.to_csv("saved_estimates/" + timestamp + "estimates.csv")
