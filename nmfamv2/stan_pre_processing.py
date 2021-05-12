import random

from .stan_pre_processing_functions import (
    get_names, get_metabolite_dot_products,
    get_area_factors, get_mixture_dot_products
)


def stan_data_preparation(mixture, metabolites):
    pass


def get_zeros(metabolite_count):
    zeros = []
    for i in range(0, metabolite_count):
        x = random.uniform(0, 0.00000001)
        zeros.append(x)
    return zeros


def get_sigmas(metabolite_count):
    return [0.1] * metabolite_count


def get_scales_sigma(scales_mean):
    return [x / 2 for x in scales_mean]


def stan_pre_process(mixture, metabolites, stan_parameters, initial_estimates):
    names = get_names(metabolites)
    area_factors = get_area_factors(metabolites)
    # initial_estimates = [10] * len(metabolites)
    is_it_final = 0
    num_time_points = stan_parameters["num_time_points"]
    metaboliteDotProducts = get_metabolite_dot_products(metabolites)
    mixtureDotProducts = get_mixture_dot_products(mixture, metabolites)

    zeros = get_zeros(len(names))
    sigmas = get_sigmas(len(names))

    scales_sigma = get_scales_sigma(sigmas)
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
