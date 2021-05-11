from StanPreProcessingFunctions import *

import random


def stanDataPreparation(mixture, metabolites):
    pass


def getZeros(metabolite_count):
    zeros = []
    for i in range(0, metabolite_count):
        x = random.uniform(0, 0.00000001)
        zeros.append(x)
    return zeros


def getSigmas(metabolite_count):
    return [0.1] * metabolite_count


def getScalesSigma(scales_mean):
    return [x / 2 for x in scales_mean]


def stanPreProcess(mixture, metabolites, stan_parameters, initial_estimates):
    names = getNames(metabolites)
    area_factors = getAreaFactors(metabolites)
    # initial_estimates = [10] * len(metabolites)
    is_it_final = 0
    num_time_points = stan_parameters["num_time_points"]
    metaboliteDotProducts = getMetaboliteDotProducts(metabolites)
    mixtureDotProducts = getMixtureDotProducts(mixture, metabolites)

    zeros = getZeros(len(names))
    sigmas = getSigmas(len(names))

    scales_sigma = getScalesSigma(sigmas)
    print("Metabolite Dot Products: ")
    print(metaboliteDotProducts)
    print("Mixture Dot Products:")
    print(mixtureDotProducts)

    stanPreprocess = {
        'is_it_final': is_it_final,
        'LENGTH': num_time_points,
        'final_size': len(names),
        'scales_mat_est': initial_estimates,
        'temps_square_dots': metaboliteDotProducts,
        'temps_mixture_dots': mixtureDotProducts,
        'zeros': zeros,
        'sigma': sigmas,
        'scales_mean': initial_estimates,
        'scales_sigma': scales_sigma
    }

    print("is_it_final: {is_it_final}".format(is_it_final=is_it_final))
    print("LENGTH: {LENGTH}".format(LENGTH=num_time_points))
    print("final_size: {final_size}".format(final_size=len(names)))
    print("scales_mat_est: {len}".format(len=initial_estimates))
    print("temps_square_dots: {len}".format(len=metaboliteDotProducts))
    print("temps_mixture_dots: {len}".format(len=mixtureDotProducts))
    print("zeros: {len}".format(len=zeros))
    print("sigma: {len}".format(len=sigmas))
    print("scales_mean: {len}".format(len=initial_estimates))
    print("scales_sigma: {len}".format(len=scales_sigma))

    return stanPreprocess
