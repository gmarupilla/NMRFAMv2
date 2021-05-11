from ReadMixture import getMixtureDataFrom1rFiles
from ReadMixture import readMixtureFromCSV

import matplotlib.pyplot as plt

mixture_ppm_axis, mixture_values = getMixtureDataFrom1rFiles("1r_files/3/pdata/3")
csv_ppms, csv_mix = readMixtureFromCSV()
# print(mixture_values)
# print(csv_mix)

plt.plot(mixture_ppm_axis, mixture_values)
plt.savefig("1r_graph")
# plt.plot(csv_ppms[:7000], csv_mix[:7000])
# plt.savefig("csv_graph")
