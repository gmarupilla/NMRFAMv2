import nmrglue as ng
import numpy as np
import pandas as pd
from scipy import interpolate


def getMixtureDataFrom1rFiles(path_to_1r):
    dic, mixture_values = ng.bruker.read_pdata(path_to_1r)
    # print(dic)
    # print(mixture_values)
    # print("acqus")
    # print(dic.get("acqus"))
    mixture_values = list(mixture_values)
    # mixture_values.reverse()
    np.asarray(mixture_values)
    # print(dic)
    # SW = dic.get("acqus").get("SW")
    # SF = dic.get("procs").get("SF")
    # SW_p = dic.get("procs").get("SW_p")
    # SW_h = dic.get("acqus").get("SW_h")
    # OFFSET = dic.get("procs").get("OFFSET")
    # SWP = SW
    # width = SWP / SF
    # PPM = SWP / (len(mixture_values) - 1)
    # print("OFFSET: ",OFFSET)
    # print("SWP: ",SWP)

    # offset = (float(dic['acques']['SW']) / 2) - (float(dic['acqus']['01']

    offset = (float(dic['acqus']['SW']) / 2) - (float(dic['acqus']['O1']) / float(dic['acqus']['BF1']))
    print(offset)
    start = float(dic['acqus']['SW']) - offset
    print("start")
    print(start)
    end = -offset
    print("end")
    print(end)
    step = float(dic['acqus']['SW']) / len(mixture_values)
    print(step)
    mixture_ppm_axis = np.arange(start, end, -step)[:len(mixture_values)]
    return mixture_ppm_axis, mixture_values


def readMixtureFromCSV(path_to_mixture_csv="sample_data/mixture.csv"
                       ):
    mixture_df = pd.read_csv(path_to_mixture_csv)

    return list(mixture_df["ppms"]), list(mixture_df["values"])


def resizer(ppm, val, num, newppmtuple):
    # print(len(ppm))
    # print(len(val))
    f = interpolate.interp1d(ppm, val)
    new_ppm = np.linspace(newppmtuple[0], newppmtuple[1], num)
    new_vals = f(new_ppm)

    return new_vals


def readMixtureFrom1r(path):
    dic, old_signal_height = ng.bruker.read_pdata(path)
    final_mixture.reverse()
    # Generate ppms
    size = 32768
    lower_bound = -3.24102
    upper_bound = 12.78428
    ppm_axis = []
    total_range = upper_bound - lower_bound
    step = total_range / size
    curr_index_value = lower_bound
    for i in range(size):
        ppm_axis.append(curr_index_value)
        curr_index_value = curr_index_value + step

    final_mixture = resizer(ppm_axis, old_signal_height, 32768, (-1, 12)).tolist()

    size = 32768
    lower_bound = -1
    upper_bound = 12
    ppm_axis = []
    total_range = upper_bound - lower_bound
    step = total_range / size
    curr_index_value = lower_bound
    for i in range(size):
        ppm_axis.append(curr_index_value)
        curr_index_value = curr_index_value + step
    return ppm_axis, final_mixture


def tests():
    mixture_ppm_axis, mixture_values = getMixtureDataFrom1rFiles("1r_files/3")
    print(mixture_ppm_axis)
    print(mixture_values)

# tests()
