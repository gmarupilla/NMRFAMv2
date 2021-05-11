from ShiftFunctions import shift_peaks_one
from ShiftFunctions import shift_values_one
from ShiftFunctions import getShiftScore
from ShiftFunctions import check_metabolite_shift





#######   SHIFT_PEAKS   #######
def shift_peaks_left_one():
    peaks = [3, 4, 7, 9]
    assert (shift_peaks_one(peaks, "left") == [2, 3, 6, 8])


def shift_peaks_right_one():
    peaks = [3, 4, 7, 9]
    assert (shift_peaks_one(peaks, "right") == [4, 5, 8, 10])


#######   SHIFT_VALUES   #######
def shift_vals_left_one():
    vals = [0, 0, 0, 1, 2, 3, 4, 5, 0, 0, 0]
    assert (shift_values_one(vals, "left") == [0, 0, 1, 2, 3, 4, 5, 0, 0, 0, 0])


def shift_vals_right_one():
    vals = [0, 0, 0, 1, 2, 3, 4, 5, 0, 0, 0]
    assert (shift_values_one(vals, "right") == [0, 0, 0, 0, 1, 2, 3, 4, 5, 0, 0])


#######   SHIFT_SCORE   #######
def test_zero_shift_score():
    peaks = [3, 7]
    vals = [0, 0, 0, 1, 0, 1, 2, 3, 2, 1, 0, 0, 0]
    mixture = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    assert (getShiftScore(vals, peaks, mixture) == 0)


def test_shift_score():
    peaks = [3, 7]
    vals = [0, 0, 0, 1, 0, 1, 2, 3, 2, 1, 0, 0, 0]
    mixture = [0, 0, 0, 3, 0, 3, 7, 15, 7, 3, 0, 0, 0]
    assert (getShiftScore(vals, peaks, mixture) == 48)


#######   CHECK_SHIFTS   #######
def test_check_shift_left_simple():
    metabolite_array = [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]  # len 15
    peaks = [6]
    mixture = [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    shift_tuple = check_metabolite_shift(metabolite_array, peaks, mixture, shift_steps=3)
    assert (shift_tuple[0] == -3)


def test_check_shift_right_simple():
    metabolite_array = [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]  # len 15
    peaks = [6]
    mixture = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
    shift_tuple = check_metabolite_shift(metabolite_array, peaks, mixture, shift_steps=3)
    assert (shift_tuple[0] == 3)


def test_check_better_outside_range_left():
    metabolite_array = [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]  # len 15
    peaks = [6]
    mixture = [0, 0, 15, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    shift_tuple = check_metabolite_shift(metabolite_array, peaks, mixture, shift_steps=3)
    assert (shift_tuple[0] == -3)


def test_check_better_outside_range_right():
    metabolite_array = [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]  # len 15
    peaks = [6]
    mixture = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 15, 0, 0, 0, 0]
    shift_tuple = check_metabolite_shift(metabolite_array, peaks, mixture, shift_steps=3)
    assert (shift_tuple[0] == 3)




# if __name__ == "__main__":
#     test()
