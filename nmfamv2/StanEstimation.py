import StanModelConstants
import numpy as np
# Upgrading pystan to 3.0 (https://github.com/stan-dev/pystan/blob/c1fda8a2545c322db8efb571be1923ef8cfec275/doc/upgrading.rst)
import stan

import RunLog as log

import sys


def getStanModel(modelNameString):
    if modelNameString == "BASIC":
        return StanModelConstants.STAN_MODEL_BASIC
    elif modelNameString == "ADJUSTING":
        return StanModelConstants.STAN_MODEL_ADJUSTING
    elif modelNameString == "BAD_ESTIMATES":
        return StanModelConstants.STAN_MODEL_BAD_ESTIMATES
    elif modelNameString == "OK_ESTIMATES":
        return StanModelConstants.STAN_MODEL_OK_ESTIMATES


def stanEstimation(mixture, metabolite_list, stanPreprocessParameters, stan_parameters, runLog):
    global results
    last_estimates = None
    new_sigmas = None
    run_number = 1
    for params in stan_parameters["run_parameters"]:
        if last_estimates is not None:
            stanPreprocessParameters["scales_mat_est"] = last_estimates
            stanPreprocessParameters["scales_mean"] = last_estimates
            stanPreprocessParameters["scales_sigma"] = new_sigmas

        stan_model_string = getStanModel(params["modeltype"])
        stan_model = stan.build(model_code=stan_model_string, verbose=False)
        print("about to run stan fit")
        stan_fit = stan_model.sampling(data=stanPreprocessParameters, iter=params["num_iterations"],
                                       chains=params["num_chains"], control={'max_treedepth': params["max_treedepth"]})

        # print(type(stan_fit.summary()))
        results = stan_fit.extract()
        scales = list(map(list, zip(*results["scales"])))

        # names = list(map(list, zip(*scales)))
        final_scale = []
        final_scale_mean = []
        final_scale_30 = []
        final_scale_50 = []
        final_scale_70 = []
        final_scale_10 = []
        final_scale_90 = []
        names = []
        new_sigmas = []
        for i in range(len(metabolite_list)):
            names.append(metabolite_list[i].name)
            SCS = scales[i]
            # final_scale.append(SCS)
            final_scale_mean.append(sum(SCS) / len(SCS))
            final_scale_30.append(np.percentile(SCS, 30))
            final_scale_50.append(np.percentile(SCS, 50))
            final_scale_70.append(np.percentile(SCS, 70))
            final_scale_10.append(np.percentile(SCS, 10))
            final_scale_90.append(np.percentile(SCS, 90))
            new_sigmas.append(abs(np.percentile(SCS, 10) - np.percentile(SCS, 90)) * 1.5)
        results = {
            "names": names,
            "means": final_scale_mean,
            "scale_10": final_scale_10,
            "scale_30": final_scale_30,
            "scale_50": final_scale_50,
            "scale_70": final_scale_70,
            "scale_90": final_scale_90
        }
        last_estimates = final_scale_mean

        runLog.log_fitted_all_metabs(metabolite_list, mixture, final_scale_mean, "/{num}".format(num=run_number))
        runLog.log_fitted_metabs(metabolite_list, mixture, final_scale_mean, "/{num}".format(num=run_number))

        run_number = run_number + 1

    return results
