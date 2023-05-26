from EXPERIMENTS import *
from data_analyzer import *
import os
from plotting import plot_all
from enum import Enum
from brute_force import run_brute_force

PATH_SAVE_DATA = "../data_experiment/"

STOP_TO = { # COPY of article information
    1 : 150,
    2 : 210,
    3 : 150,
    4 : 150,
    5 : 250
}


class test_class(Enum):
    VANILLA = 0
    BRUTE_FORCE = -1
    EPSILON_DECAY_Q = 1
    WITHOUT_TRUNCATURE_Q = 2
    EXTEND_GAP_MSA = 3
    DIFFENT_VALUE_MSA = 4
    PRIORITY_ORDER_MSA = 5




def get_experiment_values(test_number):
    TRONCATE = True
    EPSILON = 0.2
    ESPILON_DECAY = None
    ESPILON_MIN = None
    NW_MODE = 0
    if test_number == test_class.EPSILON_DECAY_Q:
        EPSILON = 1
        ESPILON_DECAY = 0.95
        ESPILON_MIN = 0.01

    elif test_number == test_class.WITHOUT_TRUNCATURE_Q:
        TRONCATE = False

    elif test_number == test_class.EXTEND_GAP_MSA:
        NW_MODE = 1

    elif test_number == test_class.DIFFENT_VALUE_MSA:
        NW_MODE = 2

    elif test_number == test_class.PRIORITY_ORDER_MSA:
        NW_MODE = 3

    return TRONCATE, EPSILON, ESPILON_DECAY, ESPILON_MIN, NW_MODE


def run_all_experimnet(gather_data = True,test_number = test_class.VANILLA):


    if test_number != test_class.BRUTE_FORCE:
        if gather_data and not os.path.isdir(PATH_SAVE_DATA):
            os.mkdir(PATH_SAVE_DATA)

        #PARAMETER TO PLAY WITH

        TRONCATE, EPSILON, ESPILON_DECAY, ESPILON_MIN, NW_MODE = get_experiment_values(test_number)

        for i in range(1,6):
            print("--"*30,"Begin experiment :",i)
            data = eval("experiment_{}(TRONCATE,EPSILON,ESPILON_DECAY,ESPILON_MIN,NW_MODE)".format(i))
            name_experimnet = data.get_name()
            experiment_info = data.get_parameter_experiment_text()
            path_experiment = PATH_SAVE_DATA + name_experimnet + "_" + experiment_info

            print("END experiment ",name_experimnet ,"--"*30)
            if gather_data and not os.path.isdir(path_experiment):
                os.mkdir(path_experiment)
            experiment_analyzer(data,PATH_SAVE_DATA)
            data.save(PATH_SAVE_DATA)
            stop_to = STOP_TO[i]
            plot_all(path_experiment,stop_to)

    else:
        run_brute_force()



if __name__ == "__main__":
    VSCODE = False
    if VSCODE:
        if os.getcwd().split('/')[-1] == "advance_bio_info": # When running on VSCode instead of Pycharm
            os.chdir("src")

    run_all_experimnet()
