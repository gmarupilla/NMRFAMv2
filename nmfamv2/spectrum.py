import sys
from statistics import mean


# from MethodErrors import shiftError


class DataError(Exception):
    # Base class for data exceptions in this module
    pass


class PPMError(DataError):
    def __init__(self):
        self.description = "ERROR in Spectrum instance: 'ppm' is not of type 'list'"


class ValueError(DataError):
    def __init__(self):
        self.description = "ERROR in Spectrum instance: 'values' is not of type 'list'"


class PeakPPMError(DataError):
    def __init__(self):
        self.description = "ERROR in Spectrum instance: 'peak_ppms' exists, but it is not of type 'list'"


class PeakIndsError(DataError):
    def __init__(self):
        self.description = "ERROR in Spectrum instance: 'peak_inds' exists, but it is not of type 'list'"


class UnequalLengthsError(DataError):
    def __init__(self):
        self.description = "ERROR in Spectrum instance: length of ppms does not equal length of values"


class ZeroLengthError(DataError):
    def __init__(self):
        self.description = "ERROR in Spectrum instance: length of ppms or values is 0, but you cannot initialize a spectrum if length is 0"


class InvalidPeaksError(DataError):
    def __init__(self, offending_peak_index_value):
        self.description = "ERROR in Spectrum instance: peak value cannot be reconciled with given Values"
        self.offending_peak_index_value = offending_peak_index_value


# Spectrum vs metabolite
# - Spectrum simply contains the values and simple shift functions


# RULES: 
#   - Cannot initialize an empty Spectrum (ie [] for ppms or values)
#   - Any time you do anything with peaks, check if it has been already shifted
class Spectrum:
    # To initialize a spectrum, at the bare minimum, one must have a ppm list and a values list
    def __init__(self, ppms, values, peak_ppms=None, peak_inds=None):
        self.ppms = ppms
        self.values = values
        self.peak_ppms = peak_ppms
        self.peak_inds = peak_inds
        self.shifted = False
        self.__check_class_data()

    def convert_peak_ppms_to_peak_inds(self):
        self.__check_class_data()

        if self.peak_ppms is None:
            print("Error: Conversion error: Cannot convert peak to peak inds because no peak ppms exist")
            sys.exit()

        metab_peak_inds = []
        # i iterates through peak lists
        for i in range(len(self.peak_ppms)):
            # j iterates through ppms
            for j in range(len(self.ppms)):
                if self.peak_ppms[i] - self.ppms[j] <= 0:
                    metab_peak_inds.append(j - 1)
                    break

        self.peak_inds = metab_peak_inds

        self.__check_class_data()

    def find_zero_ind(self):
        for i in range(len(self.ppms)):
            if self.ppms[i] > 0:
                return i
        print("Error: No zero in found")

    def find_dss_shift_amount(self, zero_ind):
        print(zero_ind)
        # Find baseline
        baseline = mean([mean(self.values[:100]), mean(self.values[:len(self.values) - 100])])
        # baseline = median(self.values)

        left = zero_ind - 1
        right = zero_ind + 1
        while left > 1 and right < len(self.ppms) - 1:
            print("hi")
            if self.values[left] > baseline * 2 and self.values[left - 1] < self.values[left] and self.values[
                left + 1] < self.values[left]:
                return zero_ind - left
            left = left - 1
            if self.values[right] > baseline * 2 and self.values[right - 1] < self.values[right] and self.values[
                right + 1] < self.values[right]:
                return right - zero_ind
            right = right + 1
        print("No DSS was found")

    def center_dss_at_zero(self):
        zero_ind = self.find_zero_ind()
        dss_shift_amount = self.find_dss_shift_amount(zero_ind)
        print("zero at: ")
        print(zero_ind)
        print("shift amount is: ")
        print(dss_shift_amount)

        if dss_shift_amount < 0:
            # shift right
            self.shift_right(-1 * dss_shift_amount)
        elif dss_shift_amount > 0:
            # shift left
            self.shift_left(dss_shift_amount)

    # shift_left -> inputs: shift_ammo
    # 	Functionality: shifts the entire spectrum to the left by 'x' amount 
    # 	Special Features: none
    def shift_left(self, shift_amount):
        self.__check_class_data()

        # if (shift_amount >= len(self.values)):
        #    raise shiftError(len(self.values), shift_amount)

        shift_vals = self.values[:shift_amount]
        self.values = self.values[shift_amount:]
        self.values.extend(shift_vals)
        self.shifted = True

        self.__check_class_data()

    # shift_right -> inputs: 
    #   Functionality: shifts the entire spectrum to the right by 'x' amount 
    #   Special Features: none
    def shift_right(self, shift_amount):
        self.__check_class_data()

        # if (shift_amount >= len(self.values)):
        #    raise shiftError(len(self.values), shift_amount)

        shift_vals = self.values[:len(self.values) - shift_amount]
        self.values = self.values[len(self.values) - shift_amount:]
        self.values.extend(shift_vals)

        self.shifted = True

        self.__check_class_data()

    def getLogData(self):
        logData = {
            "start_ppm": self.ppms[0],
            "end_ppm": self.ppms[len(self.ppms) - 1],
            "ppms_length": len(self.ppms),
            "values_length": len(self.values),
            "peak_ppms": self.peak_ppms,
            "peak_inds": self.peak_inds,
            "shifted_from_original_position": self.shifted
        }
        return logData

    def __check_class_data(self):

        if type(self.ppms) != list:
            raise PPMError()
        if type(self.values) != list:
            raise ValueError()
        if self.peak_ppms is not None and type(self.peak_ppms) != list:
            raise PeakPPMError()
        if self.peak_inds is not None and type(self.peak_inds) != list:
            raise PeakIndsError()
        if len(self.ppms) == 0 or len(self.values) == 0 or (
                (self.peak_ppms is not None) and (len(self.peak_ppms) == 0)):
            raise ZeroLengthError()

        if len(self.ppms) != len(self.values):
            raise UnequalLengthsError()
        """
        if (self.peaks != None):
            for i in range(len(self.peaks)):
                if (self.peaks[i] < 0):
                    raise InvalidPeaksError(self.peaks[i])
                try:
                    self.values[self.peaks[i]]
                except:
                    raise InvalidPeaksError(self.peaks[i])
        """


def test():
    """Init Exception Tests"""
    # Test #1: Check that the class catches when ppms is not a list
    try:
        Spectrum(1, [])
        print("Failed Exception Test #1")
        sys.exit()
    except PPMError:
        pass
    except:
        print("Failed Exception Test #1: Wrong error thrown")

    # Test #2: Check that the class catches when values is not a list
    try:
        Spectrum([1, 2, 3], "a")
        print("Failed Exception Test #2")
        sys.exit()
    except ValueError:
        pass
    except:
        print("Failed Exception Test #2: Wrong error thrown")

    # Test #3: Check that the class catches when peaks is given, but is not a list
    try:
        Spectrum([1, 2, 3], [1, 2, 3], "a")
        print("Failed Exception Test #3")
        sys.exit()
    except:
        print("Failed Exception Test #3: Wrong error thrown")

    # Test #4: Check that the class catches when length of ppms or value is zero
    try:
        Spectrum([], [])
        print("Failed Exception Test #4")
        sys.exit()
    except ZeroLengthError:
        pass
    except:
        print("Failed Exception Test #4: Wrong error thrown")

    # Test #5: Check that the class catches when length of peaks is not None but has zero length
    try:
        Spectrum([1, 2, 3, 4], [1, 2, 3, 4], [])
        print("Failed Exception Test #5")
        sys.exit()
    except ZeroLengthError:
        pass
    except:
        print("Failed Exception Test #5: Wrong error thrown")

    # Test #6: Check that the class catches when length of ppms does not equal the length of value
    try:
        Spectrum([1, 2, 3, 4], [1, 2])
        print("Failed Exception Test #6")
        sys.exit()
    except UnequalLengthsError:
        pass
    except:
        print("Failed Exception Test #6: Wrong error thrown")

    # Test #7: Pass a peak value that is negative
    try:
        Spectrum([1, 2, 3, 4], [1, 2, 3, 4], [-1])
        print("Failed Exception Test #7")
        sys.exit()
    except InvalidPeaksError as err:
        if err.offending_peak_index_value != -1:
            print("Failed Exception Test #7")
            print("Expected failing peak index to be -1")
            print("Actual: " + err.offending_peak_index_value)
            sys.exit()
    except:
        print("Failed Exception Test #7: Wrong error thrown")

    # Test #8: Pass a peak value that is higher than the length of value
    try:
        # 5 is outside the bouds of index
        #   [1,2,3,4]
        #    0 1 2 3   ---> 5 is beyond 3
        Spectrum([1, 2, 3, 4], [1, 2, 3, 4], [5])
        print("Failed Exception Test #8")
        sys.exit()
    except InvalidPeaksError as err:
        if err.offending_peak_index_value != 5:
            print("Failed Exception Test #8")
            print("Expected failing peak index to be 5")
            print("Actual: " + err.offending_peak_index_value)
            sys.exit()
    except:
        print("Failed Exception Test #8: Wrong error thrown")

    # Test #9: Pass a peak value that is of type float
    try:
        Spectrum([1, 2, 3, 4], [1, 2, 3, 4], [1.0])
        print("Failed Exception Test #9")
        sys.exit()
    except InvalidPeaksError as err:
        if err.offending_peak_index_value != 1.0:
            print("Failed Exception Test #9")
            print("Expected failing peak index to be 1.0")
            print("Actual: " + err.offending_peak_index_value)
            sys.exit()
    except:
        print("Failed Exception Test #9: Wrong error thrown")

