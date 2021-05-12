import numpy as np


def get_names(metabolites):
    names = []
    for metab in metabolites:
        names.append(metab.name)
    return names


def get_area_factors(metabolites):
    area_factors = []
    for metab in metabolites:
        metab.calc_riemann_sum()
        area_factors.append(metab.riemannSum)
    return area_factors


def get_initial_estimates(metabolites):
    initial_estimates = []
    for metab in metabolites:
        initial_estimates.append(metab.max_scale)
    return initial_estimates


def get_metabolite_dot_products(metabolites):
    metabolite_dot_products = []
    for metab_outer in metabolites:
        row = []
        for metab_inner in metabolites:
            row.append(np.dot(metab_outer.values, metab_inner.values))
        metabolite_dot_products.append(row)
    return metabolite_dot_products


def get_mixture_dot_products(mixture, metabolites):
    mixture_dot_products = []
    for metab in metabolites:
        mixture_dot_products.append(np.dot(metab.values, mixture.values))
    return mixture_dot_products
