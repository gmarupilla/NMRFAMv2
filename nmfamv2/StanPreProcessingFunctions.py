import numpy as np


def getNames(metabolites):
    names = []
    for metab in metabolites:
        names.append(metab.name)
    return names


def getAreaFactors(metabolites):
    areaFactors = []
    for metab in metabolites:
        metab.calc_riemann_sum()
        areaFactors.append(metab.riemannSum)
    return areaFactors


def getInitialEstimates(metabolites):
    initialEstimates = []
    for metab in metabolites:
        initialEstimates.append(metab.max_scale)
    return initialEstimates


def getMetaboliteDotProducts(metabolites):
    metabDotProducts = []
    for metab_outer in metabolites:
        row = []
        for metab_inner in metabolites:
            row.append(np.dot(metab_outer.values, metab_inner.values))
        metabDotProducts.append(row)
    return metabDotProducts


def getMixtureDotProducts(mixture, metabolites):
    mixtureDotProducts = []
    for metab in metabolites:
        mixtureDotProducts.append(np.dot(metab.values, mixture.values))
    return mixtureDotProducts
