import time
import pandas as pd
import numpy as np


def save_estimates(estimates):
    df = pd.DataFrame(np.array([[*estimates]]), columns=["estimates"])
    timestamp = str(int(time.time()))
    df.to_csv("saved_estimates/" + timestamp + "estimates.csv")
