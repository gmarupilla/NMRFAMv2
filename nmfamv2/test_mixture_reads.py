from .read_mixture import get_mixture_data_from_1r_files
from .read_mixture import read_mixture_from_csv

import matplotlib.pyplot as plt

mixture_ppm_axis, mixture_values = get_mixture_data_from_1r_files("1r_files/3/pdata/3")
csv_ppms, csv_mix = read_mixture_from_csv()
# print(mixture_values)
# print(csv_mix)

plt.plot(mixture_ppm_axis, mixture_values)
plt.savefig("1r_graph")
# plt.plot(csv_ppms[:7000], csv_mix[:7000])
# plt.savefig("csv_graph")
