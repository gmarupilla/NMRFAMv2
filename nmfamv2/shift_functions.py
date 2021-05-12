import copy
import sys


def shift_peaks_one(indexes, direction):
    direction_integer = None
    if direction == "left":
        direction_integer = -1
    elif direction == "right":
        direction_integer = 1
    else:
        print("Error: shift_peaks_one has faulty direction (not 'left' or 'right')")
        sys.exit()

    for i in range(len(indexes)):
        indexes[i] = indexes[i] + direction_integer
    return indexes


def shift_values_one(values, direction):
    if direction == "left":
        val = values.pop(0)
        values.append(val)
    elif direction == "right":
        val = values.pop(len(values) - 1)
        values.insert(0, val)
    else:
        print("Error: shift_values_one has faulty direction (not 'left' or 'right')")
        sys.exit()

    return values


def get_shift_score(metaboltie_values, metabolite_peak_indexes, mixture_values):
    shift_score = 0
    for peak_ind in metabolite_peak_indexes:
        shift_score = shift_score + (metaboltie_values[peak_ind] * mixture_values[peak_ind])
    return shift_score


def check_metabolite_shift(metabolite_values, metabolite_peak_indexes, mixture_values, shift_steps=400):
    max_score = get_shift_score(metabolite_values, metabolite_peak_indexes, mixture_values)
    best_shift_index = 0
    best_shift_direction = "right"

    for direction in ["left", "right"]:
        copy_metabolite_peak_indexes = copy.deepcopy(metabolite_peak_indexes)
        copy_metabolite_values = copy.deepcopy(metabolite_values)
        i = 1
        while i <= shift_steps:
            shift_peaks_one(copy_metabolite_peak_indexes, direction)
            shift_values_one(copy_metabolite_values, direction)

            shift_score = get_shift_score(copy_metabolite_values, copy_metabolite_peak_indexes, mixture_values)

            if max_score < shift_score:
                max_score = shift_score
                best_shift_index = i
                best_shift_direction = direction
            i = i + 1

    if best_shift_direction == "left":
        return best_shift_index * -1, max_score
    return best_shift_index, max_score

