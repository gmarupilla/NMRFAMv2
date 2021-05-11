import time
import sys
import os

from ReadUserData import readMetadata
from ReadUserData import readMixture
from ReadUserData import readMetaboliteList
from PreProcessing import preProcess
from PreEstimate import preEstimate
from PreEstimate import getPreEstimates
from PreEstimate import logPreEstimate

from StanPreProcessing import stanPreProcess

from StanEstimation import getStanModel
from StanEstimation import stanEstimation
from SaveEstimates import saveEstimates

from RunLog import RunLog
from RunResultsWriter import RunResultsWriter


def main(mixture_path, runLog, resultsWriter):
    # READ
    init_time = float(time.time())
    # metadata = readMetadata() #
    mixture = readMixture(mixture_path)  # Mixture will be a Spectrum object
    metabolite_list = readMetaboliteList()  # Metabolite list will be an array of Metabolite Objects
    end_time = float(time.time())
    mixture.center_dss_at_zero()
    # Log
    runLog.log_mixture(mixture, "original")
    runLog.log_metab_list(metabolite_list, "original")

    print("Read time: " + str(end_time - init_time))
    #######################

    # PREPROCESS
    """
    PreProcess will change the mixture Spectrum and metabolite list Metabolites.
    Nothing is returned, the data is changed in-line
    """
    init_time = float(time.time())
    preProcess(mixture, metabolite_list)
    end_time = float(time.time())

    runLog.log_mixture(mixture, "resized")
    runLog.log_metab_list(metabolite_list, "shifted")

    print("PreProcess time: " + str(end_time - init_time))
    ########################    

    # PREESTIMATE
    init_time = float(time.time())
    preEstimate(mixture, metabolite_list)
    pre_estimates = getPreEstimates(mixture, metabolite_list)
    # pre_estimates = [30] * len(metabolite_list)
    end_time = float(time.time())
    # logPreEstimate(mixture, metabolite_list)
    # print("pre estimates:")
    # print(pre_estimates)
    runLog.log_fitted_all_metabs(metabolite_list, mixture, pre_estimates, "/preestimates")
    runLog.log_fitted_metabs(metabolite_list, mixture, pre_estimates, "/preestimates")
    print("PreEstimate time: " + str(end_time - init_time))
    ########################

    # STAN PREPRECESSING
    init_time = float(time.time())
    stan_parameters = parameters["stan"]
    stan_pre_process_dict = stanPreProcess(mixture, metabolite_list, stan_parameters, pre_estimates)
    end_time = float(time.time())
    print("StanPreprocessing time: " + str(end_time - init_time))
    ########################

    # STAN ESTIMATION
    init_time = int(time.time())
    # checkDataCompatibleWithStan() # TODO: Ensure that none of the means are zero
    stan_estimates = stanEstimation(mixture, metabolite_list, stan_pre_process_dict, stan_parameters, runLog)
    end_time = int(time.time())
    print("Stan Estimation time: " + str(end_time - init_time))
    ########################

    print(stan_estimates)

    # print(stan_estimates)
    # init_time = int(time.time())
    # saveEstimates(stan_estimates)
    # end_time = int(time.time())
    # print("Data save time: " + str(end_time - init_time))
    ########################


def checkArgsForErrors(args):
    if len(args) == 0: return "ERROR: Must include a path to a user directory path as an arg"
    if len(args) > 1: return "ERROR: Too many args provided. Must only provide a user directory path"

    if not os.path.isdir(args[0]): return "ERROR: Provided path DNE or is not a direcotry"

    return None


if __name__ == "__main__":
    parameters = {
        "metadata": {
            "correction_factors": [1] * 50,
            "outputPath": "./run/Results"
        },

        "stan": {
            "num_time_points": 16384,
            "run_parameters": [
                {
                    "modeltype": "ADJUSTING",
                    "num_iterations": 10000,
                    "num_chains": 8,
                    "max_treedepth": 16
                },
                {
                    "modeltype": "ADJUSTING",
                    "num_iterations": 10000,
                    "num_chains": 8,
                    "max_treedepth": 16
                },
                {
                    "modeltype": "ADJUSTING",
                    "num_iterations": 10000,
                    "num_chains": 8,
                    "max_treedepth": 16
                },
                {
                    "modeltype": "ADJUSTING",
                    "num_iterations": 10000,
                    "num_chains": 8,
                    "max_treedepth": 16
                }
            ]
        }
    }
    args = sys.argv[1:]
    error = checkArgsForErrors(args)
    if error:
        print(error)

    else:
        mixture_path = args[0] + "/pdata/3"
        runLog = RunLog("test_dir")
        resultsWriter = RunResultsWriter("test_dir")
        main(mixture_path, runLog, resultsWriter)
