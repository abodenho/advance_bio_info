from EXPERIMENTS import *
from data_analyzer import *
import os

PATH_SAVE_DATA = "../data_experiment/"

def run_all_experimnet(gather_data = True):

    if gather_data and not os.path.isdir(PATH_SAVE_DATA):
        os.mkdir(PATH_SAVE_DATA)

    for i in range(3,6):
        data = eval("experiment_{}()".format(i))
        name_experimnet = data.get_name()
        if gather_data and not os.path.isdir(PATH_SAVE_DATA + name_experimnet):
            os.mkdir(PATH_SAVE_DATA + name_experimnet)

        experiment_analyzer(data,PATH_SAVE_DATA)

if __name__ == "__main__":
    run_all_experimnet()
