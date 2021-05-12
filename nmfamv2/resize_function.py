import sys

import numpy as np
from scipy import interpolate


def generate_ppm_axis(size, lower_bound, upper_bound):
    ppm_axis = []
    total_range = upper_bound - lower_bound
    step = total_range / size
    curr_index_value = lower_bound
    for i in range(size):
        ppm_axis.append(curr_index_value)
        curr_index_value = curr_index_value + step
    return ppm_axis


def extend_ppm(ppm_vals, vals, boundaries):
    window = ppm_vals[len(ppm_vals) - 1] - ppm_vals[0]
    step = window / (len(ppm_vals) - 1)
    start_point = ppm_vals[0]
    end_point = ppm_vals[len(ppm_vals) - 1]
    pointer = start_point

    front_ppm_extension = []
    front_val_extension = []
    while pointer > boundaries[0]:
        pointer = pointer - step
        front_ppm_extension.append(pointer)
        front_val_extension.append(0)

    front_ppm_extension.reverse()

    ppm_vals = front_ppm_extension + ppm_vals
    vals = front_val_extension + vals

    pointer = end_point
    while pointer < boundaries[1]:
        pointer = pointer + step
        ppm_vals.append(pointer)
        vals.append(0)

    if len(ppm_vals) != len(vals):
        print("ERROR: extend_ppm failed")
        sys.exit(1)
    return ppm_vals, vals


def resizer(ppm, val, num, newppmtuple):
    f = interpolate.interp1d(ppm, val)
    new_ppm = np.linspace(newppmtuple[0], newppmtuple[1], num)
    new_vals = f(new_ppm)
    return new_ppm, new_vals


def get_peaks(input_mixture, num_peaks):
    peaks_indexes = []
    threshold = .02
    for i in range(len(input_mixture)):
        if i != 1 and i != len(input_mixture) - 2 and i != 0 and i != len(input_mixture) - 1 and input_mixture[
            i] > threshold and input_mixture[i - 1] < input_mixture[i] and input_mixture[i + 1] < input_mixture[i] and \
                input_mixture[i - 2] <= input_mixture[i - 1] and input_mixture[i + 2] <= input_mixture[i + 1]:
            peaks_indexes.append(i)
    return peaks_indexes


def resize(mixture, newsize):
    # original_time_domain_mixture = np.fft.ifft(mixture)
    # original_length = len(original_time_domain_mixture)
    time_domain_resize = np.fft.ihfft(mixture)
    # resize_time_domain_size = len(time_domain_resize)
    # print(type(time_domain_resize))
    frequency_domain_resize = np.fft.hfft(time_domain_resize, newsize)
    return frequency_domain_resize


def locate_index(list_, value):
    for i in range(len(list_)):
        if i != 0 and list_[i - 1] <= value <= list_[i]:
            return i


def trim_spectrum(ppm_list, value_list, lower_bound, upper_bound):
    if len(ppm_list) != len(value_list):
        print("PPM List and Value List are not the same size")
        exit()
    lower_index = locate_index(ppm_list, lower_bound)
    upper_index = locate_index(ppm_list, upper_bound)
    new_value_list = value_list[lower_index:upper_index]
    return new_value_list


def mixture_template_size_synchronization(template_names, template_ppms_list, template_values_list, mixture_values):
    OFFSET = 12.78661
    SWP = 16.0252988219442
    mixture_ppms = generate_ppm_axis(len(mixture_values), OFFSET - SWP, OFFSET)
    # ***** PRE CHECKS ******
    if len(mixture_ppms) == 0:
        print("[mixture_template_size_synchronization] ERROR: Mixture ppms are empty")
        sys.exit()
    if len(template_ppms_list) == 0:
        print("[mixture_template_size_synchronization] ERROR: No template ppms were passed")
        sys.exit()
    if len(template_values_list) == 0:
        print("[mixture_template_size_synchronization] ERROR: No template values were passed")
        sys.exit()
    if len(template_names) != len(template_values_list):
        print("[mixture_template_size_synchronization] ERROR: Names size is not equal to template values size")
        sys.exit()
    if len(template_ppms_list) != len(template_values_list):
        print(
            "[mixture_template_size_synchronization] ERROR: template_ppms_list length does not equal template_values_list")
        sys.exit()
    if len(mixture_ppms) != len(mixture_values):
        print("[mixture_template_size_synchronization] ERROR: mixture_ppms length does not equal mixture_values length")
        sys.exit()
    # ********************

    # Cycle through template names
    for t in range(len(template_names)):
        template_ppms_list[t], template_values_list[t] = extend_ppm(template_ppms_list[t], template_values_list[t], (
            mixture_ppms[0], mixture_ppms[len(mixture_ppms) - 1]))
        # Resize metabolites
        template_ppms_list[t], template_values_list[t] = resizer(template_ppms_list[t], template_values_list[t],
                                                                 len(mixture_values), (template_ppms_list[t][0],
                                                                                       template_ppms_list[t][len(
                                                                                           template_ppms_list[t]) - 1]))

    # ****** POST CHECKS *********
    if len(template_ppms_list[0]) != len(mixture_ppms):
        print("[mixture_template_size_synchronization] ERROR: template size not the same as the mixture size")
        sys.exit()
    # First template ppm serves as the benchmark for the rest of the templates to be equivalent to
    first_template_ppm_length = len(template_ppms_list[0])
    for i in range(len(template_ppms_list)):
        if len(template_ppms_list[i]) != first_template_ppm_length:
            print("[mixture_template_size_synchronization] ERROR: template with index " + str(i) + " and name " +
                  template_names[i] + " has ppms that do not equal the first template's ppm length")
            sys.exit()
        if len(template_ppms_list[i]) != len(template_values_list[i]):
            print("[mixture_template_size_synchronization] ERROR: template with index " + str(i) + " and name " +
                  template_names[i] + " has ppm length that does not equal the values list")
            sys.exit()
    # *****************************

    return template_ppms_list, template_values_list


# OFFSET:  12.78661
# SWP:  16.0252988219442

def resize_ppms_and_values(ppms, values, mixture_ppm_left_bound, mixture_ppm_right_bound, new_size_length):
    # Extend the ppms
    new_ppms, new_values = extend_ppm(ppms, values, (mixture_ppm_left_bound, mixture_ppm_right_bound))
    # Resize metabolites
    new_ppms, new_values = resizer(ppms, values, new_size_length, (mixture_ppm_left_bound, mixture_ppm_right_bound))

    if new_size_length != len(new_ppms):
        print("ERROR: target resize length does not equal actual length of resized ppms")
        print("Target length: " + str(new_size_length))
        print("Actual ppm length: " + str(len(new_ppms)))
        sys.exit()
    if new_size_length != len(new_values):
        print("ERROR: target resize length does not equal actual length of resized values")
        print("Target length: " + str(new_size_length))
        print("Actual values length: " + str(len(new_values)))
        sys.exit()

    return new_ppms, new_values


