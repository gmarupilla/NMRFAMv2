# We want to pass a mixture object (just a spectrum) and a list 
# of metabolite objects. 

import matplotlib.pyplot as plt
import random
import sys
import math
from statistics import mean


###  MAXES  ###

def find_max_peak_val(metabolite_peak_inds, metabolite_values):
    highest_value = -1
    for ind in metabolite_peak_inds:
        if metabolite_values[ind] > highest_value:
            highest_value = metabolite_values[ind]
    return highest_value


# Max scale makes sure that all peaks are at least scaled to
def single_metabolite_seeding_max(metabolite_peak_inds, metabolite_values, mixture_values):
    # We want to find a number mutliple for the metabolite values such that scale * metab < mixture at each peak ind
    if len(metabolite_peak_inds) == 0: return 0

    highest_value = find_max_peak_val(metabolite_peak_inds, metabolite_values)

    scales = []
    for ind in metabolite_peak_inds:
        if metabolite_values[ind] == 0:
            print(
                "ERROR: [PreEstimate.py][find_metabolite_seeding_max] A supposed peak ind points to a zero value. Check logic of preprocessing and the validity of peak locations for this metabolite.")
            sys.exit()
        if metabolite_values[ind] > highest_value * .2:
            scales.append(mixture_values[ind] / metabolite_values[ind])
    return min(scales)


def find_seeding_maxes(metabolite_list, mixture):
    max_list = []
    for metabolite in metabolite_list:
        max_scale = single_metabolite_seeding_max(metabolite.peak_inds, metabolite.values, mixture.values)
        if max_scale > metabolite.min_scale:
            metabolite.max_scale = max_scale
        else:
            metabolite.max_scale = metabolite.min_scale


###  MINS  ###


def getOnlyPeaks(allPeakInds, window):
    if len(allPeakInds) <= 1:
        return allPeakInds
    # List is at least of length 2

    onlyDict = {}

    i = 1
    # Do right check of first peak
    if abs(allPeakInds[i] - allPeakInds[i + 1]) <= window:
        onlyDict[allPeakInds[i]] = False
    else:
        onlyDict[allPeakInds[i]] = True

    while i < len(allPeakInds) - 1:
        # Left check
        if abs(allPeakInds[i] - allPeakInds[i - 1]) <= window:
            onlyDict[allPeakInds[i]] = False
        elif abs(allPeakInds[i] - allPeakInds[i + 1]) <= window:
            onlyDict[allPeakInds[i]] = False
        else:
            onlyDict[allPeakInds[i]] = True

        i = i + 1
    # Check the final ind
    if abs(allPeakInds[len(allPeakInds) - 1] - allPeakInds[len(allPeakInds) - 2]) <= window:
        onlyDict[allPeakInds[len(allPeakInds) - 1]] = False
    else:
        onlyDict[allPeakInds[len(allPeakInds) - 1]] = True

    onlyPeaks = []
    for key in onlyDict.keys():
        if onlyDict[key]:
            onlyPeaks.append(key)

    return onlyPeaks


"""
# Combine all metabolite peaks in one list
# INPUT: a list of lists containing each metabolites peak indexes
# RETURNS: a single list of peak inds
def peakPreparation(peakIndsList): 
    foundPeaks = {}
    duplicatePeaks = []
    for peakInds in peakIndsList: 
        for ind in peakInds:
            if ind in foundPeaks:
                foundPeaks[ind] = None
                duplicatePeaks.append(ind)
            else:
                foundPeaks[ind] = ind

    allPeakInds = list(filter(lambda x: x != None, foundPeaks.values()))
    allPeakInds.sort()

    return allPeakInds, duplicatePeaks
"""


def extractPeakIndsList(metabolite_list):  # Returns a list of lists with peak_inds
    allPeakIndsList = []
    for metabolite in metabolite_list:
        allPeakIndsList.append(metabolite.peak_inds)
    return allPeakIndsList


# Min scale will determine if the metabolite contains a peak that only can be scaled by that metabolite
def find_seeding_mins(metabolite_list, mixture, window=15):
    # "only peaks" -> We will roughly define a peak that only belongs to only one metabolite if no other peaks are within 'window' indexes

    #   1st) We must determine each metabolite's 'only peaks' ie, it has peaks that can only be 'explained' by one metabolite
    #   2nd) We must run the 'only peaks' for each metabolite through the max seeding function to make sure all only peaks are covered

    seeding_min_scales = []

    # 1) Get 'only peaks'
    allPeakIndsList = extractPeakIndsList(metabolite_list)
    # print(allPeakIndsList)
    allPeakInds = []
    for peak_inds in allPeakIndsList:
        allPeakInds = allPeakInds + peak_inds
    allPeakInds.sort()

    # Only peaks is a 1D list of peaks that are exclusively held by one singular metabolite in the list
    onlyPeaks = getOnlyPeaks(allPeakInds, window)

    # 2) Record only peaks
    for metabolite in metabolite_list:
        metab_only_peaks = []
        # Cycle through only peaks
        for onlyPeak in onlyPeaks:
            if onlyPeak in metabolite.peak_inds:
                metab_only_peaks.append(onlyPeak)
        min_scale = 0
        metabolite.only_peaks = metab_only_peaks

        min_scale = single_metabolite_seeding_max(metabolite.only_peaks, metabolite.values, mixture.values)
        max_scale = single_metabolite_seeding_max(metabolite.peak_inds, metabolite.values, mixture.values)
        if min_scale < 0:
            metabolite.min_scale = 0
        elif min_scale > max_scale:
            metabolite.min_scale = max_scale
        else:
            metabolite.min_scale = min_scale


def getOverlappingMetabolites(metabolite_list):
    overlapping_dict = {}

    for i in range(len(metabolite_list)):
        overlapping_dict[i] = []
        metab1 = metabolite_list[i]
        overlap_detector = {}
        for peak in metab1.peak_inds:
            overlap_detector[peak] = True

        j = i + 1
        while j < len(metabolite_list):
            metab2 = metabolite_list[j]
            for peak in metab2.peak_inds:
                if peak in overlap_detector:
                    overlapping_dict[i].append(j)
                    break
            j = j + 1
    return overlapping_dict


def preEstimate(mixture, metabolite_list):
    # First we want to get the minimum seedings for 
    find_seeding_mins(metabolite_list, mixture)

    find_seeding_maxes(metabolite_list, mixture)


def logPreEstimate(mixture, metabolite_list):
    pass


def getPreEstimates(mixture, metabolite_list):
    if len(metabolite_list) == 0:
        print("[PreEstimate.py] No metabolites")
        sys.exit()
    if len(metabolite_list) == 1: return [metabolite_list[0].max_scale]

    scale_possibilities = []
    for metab in metabolite_list:
        scale_possibilities.append([metab.max_scale])

    overlapping_dict = getOverlappingMetabolites(metabolite_list)

    for _ in range(10000):
        metab1_ind = random.randint(0, len(metabolite_list) - 1)
        if len(overlapping_dict[metab1_ind]) != 0:
            metab1 = metabolite_list[metab1_ind]
            metab2_ind = overlapping_dict[metab1_ind][random.randint(0, len(overlapping_dict[metab1_ind]) - 1)]
            metab2 = metabolite_list[metab2_ind]
            print(metab1.min_scale)
            print(metab1.max_scale)
            scale1 = random.randint(math.floor(metab1.min_scale), math.ceil(metab1.max_scale))

            # Get overlapping indexes
            overlapping_inds = []
            for ind1 in metab1.peak_inds:
                for ind2 in metab2.peak_inds:
                    if ind1 == ind2:
                        overlapping_inds.append(ind1)
                        break

            scale2 = None
            for o_ind in overlapping_inds:
                sub_mixture = mixture.values[o_ind] - (scale1 * metab1.values[o_ind])
                new_potential_scale = sub_mixture / metab2.values[o_ind]
                if scale2 == None:
                    scale2 = new_potential_scale
                elif scale2 > new_potential_scale:
                    scale2 = new_potential_scale
            if scale2 > 0:
                scale_possibilities[metab1_ind].append(scale1)
                scale_possibilities[metab2_ind].append(scale2)

    for i in range(len(scale_possibilities)):
        scale_possibilities[i] = mean(scale_possibilities[i])

    return scale_possibilities

# Tests (organize them)
def test_single_perfect_fit_seeding_max():
    # Max scale should equal 3
    max_scale = single_metabolite_seeding_max([7, 12], [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0],
                                              [0, 0, 0, 0, 0, 1, 2, 3, 2, 1, 0, 3, 9, 3, 0, 0, 0, 0])
    assert (max_scale == 3)


def test_single_over_fit_seeding_max():
    # Max scale should equal 4
    max_scale = single_metabolite_seeding_max([7, 12], [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0],
                                              [0, 0, 0, 0, 0, 1, 2, 4, 2, 1, 0, 3, 9, 3, 0, 0, 0, 0])
    assert (max_scale == 4)


def test_zero_only_peaks():
    assert (getOnlyPeaks([], 10) == [])


def test_one_only_peaks():
    assert (getOnlyPeaks([1], 10) == [1])


def test_none_only_peaks():
    assert (getOnlyPeaks([3, 10, 11], 10) == [])


def test_none_only_peaks_dups():
    assert (getOnlyPeaks([3, 10, 11, 90, 90], 10) == [])


def test_only_peaks_front_edge():
    assert (getOnlyPeaks([3, 4, 8, 14], 3) == [8, 14])


# def test_multiple_fit_seeding_max():
"""
def test_only_to_dups():
    assert(checkOnlyToDups(3, [0,6], 2) == True)

def test_not_only_to_dups():
    assert(checkOnlyToDups(3, [1,6], 2) == False)

def test_only_peaks_base_check():
    assert(getOnlyPeaks([], [1,2,3], 2) == [])
"""

"""
def test_collect_all_peaks():
    allPeaks = extractPeakIndsList([[0,1,2,3],[4,5],[6,7,8]])
    assert(allPeaks == [0,1,2,3,4,5,6,7,8])
"""

"""
def test_collect_all_peaks_with_duplicates():
    allPeaks = getAllPeakInds([[0,1,2,3],[3,4],[4,7,8]])
    assert(allPeaks == [0,1,2,3,4,7,8])

def test_collect_all_peaks_with_duplicates_unsorted():
    allPeaks = getAllPeakInds([[3,4],[0,1,2,3],[4,7,8]])
    assert(allPeaks == [0,1,2,3,4,7,8])
"""
