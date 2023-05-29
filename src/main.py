from EXPERIMENTS import *
from data_analyzer import *
import os
from plotting import plot_all,plot_experiment
from enum import Enum
from brute_force import run_brute_force

PATH_SAVE_DATA = "../data_experiment/"

VANILLA = 0
BRUTE_FORCE = -1
EPSILON_DECAY_Q = 1
WITHOUT_TRUNCATURE_Q = 2
EXTEND_GAP_MSA = 3
DIFFENT_VALUE_MSA = 4
PRIORITY_ORDER_MSA = 5

HEPATITIS_C = 1
PAPIO_ANUBIS = 2
DATASET_1 = 3
LEMUR_GORILLA_MOUSE = 4
RAT_LEMUR_OPOSSUM = 5


STOP_TO = { # COPY of article information + 50
    HEPATITIS_C : 150,
    PAPIO_ANUBIS : 210,
    DATASET_1 : 150,
    LEMUR_GORILLA_MOUSE : 150,
    RAT_LEMUR_OPOSSUM : 250
}





def get_experiment_values(test_number):
    TRONCATE = True
    EPSILON = 0.2
    ESPILON_DECAY = None
    ESPILON_MIN = None
    NW_MODE = 0
    if test_number == EPSILON_DECAY_Q:
        EPSILON = 1
        ESPILON_DECAY = 0.95
        ESPILON_MIN = 0.01

    elif test_number == WITHOUT_TRUNCATURE_Q:
        TRONCATE = False

    elif test_number == EXTEND_GAP_MSA:
        NW_MODE = 1

    elif test_number == DIFFENT_VALUE_MSA:
        NW_MODE = 2

    elif test_number == PRIORITY_ORDER_MSA:
        NW_MODE = 3

    return TRONCATE, EPSILON, ESPILON_DECAY, ESPILON_MIN, NW_MODE

def get_setting_name(setting):
    if setting == VANILLA :
        rep = "VANILLA"
    elif setting == BRUTE_FORCE:
        rep = "BRUTE_FORCE"
    elif setting == EPSILON_DECAY_Q:
        rep = "EPSILON_DECAY_Q"
    elif setting == WITHOUT_TRUNCATURE_Q:
        rep = "WITHOUT_TRUNCATURE_Q"
    elif setting == EXTEND_GAP_MSA:
        rep = "EXTEND_GAP_MSA"
    elif setting == DIFFENT_VALUE_MSA:
        rep = "DIFFENT_VALUE_MSA"
    elif setting == PRIORITY_ORDER_MSA:
        rep = "PRIORITY_ORDER_MSA"

    return rep

def run_experimnet(setting, experiment):

    if setting != BRUTE_FORCE:
        print(f"\n## TEST CONFIG: {setting}\n ##")
        if not os.path.isdir(PATH_SAVE_DATA):
            os.mkdir(PATH_SAVE_DATA)

        #PARAMETER TO PLAY WITH

        TRONCATE, EPSILON, ESPILON_DECAY, ESPILON_MIN, NW_MODE = get_experiment_values(setting)

        print("--"*30,"Begin experiment :",experiment)
        data = eval("experiment_{}(TRONCATE,EPSILON,ESPILON_DECAY,ESPILON_MIN,NW_MODE)".format(experiment))
        name_experimnet = data.get_name()
        if  not os.path.isdir(PATH_SAVE_DATA + str(setting)  + "_" + get_setting_name(setting)):
            os.mkdir(PATH_SAVE_DATA + str(setting)  + "_" + get_setting_name(setting))
        path_experiment_folder = PATH_SAVE_DATA + str(setting)  + "_" + get_setting_name(setting) +"/" + name_experimnet +"/"
        print("END experiment ",name_experimnet ,"--"*30)
        if  not os.path.isdir(path_experiment_folder):
            os.mkdir(path_experiment_folder)

        experiment_analyzer(data,path_experiment_folder)
        data.save(path_experiment_folder)
        #stop_to = STOP_TO[experiment]
        #plot_all(path_experiment_folder,name_experimnet,stop_to)
    else:
        run_brute_force(experiment,setting,get_setting_name(setting))


def run_all_experiment():
    for setting in [VANILLA,EPSILON_DECAY_Q,WITHOUT_TRUNCATURE_Q,EXTEND_GAP_MSA,DIFFENT_VALUE_MSA,PRIORITY_ORDER_MSA]: # run normal settings
        for experiment in [HEPATITIS_C,PAPIO_ANUBIS,DATASET_1,LEMUR_GORILLA_MOUSE,RAT_LEMUR_OPOSSUM]:
            run_experimnet(setting, experiment)
    setting = BRUTE_FORCE # special case brute force
    for experiment in [DATASET_1, LEMUR_GORILLA_MOUSE, RAT_LEMUR_OPOSSUM,PAPIO_ANUBIS]:
        run_experimnet(setting, experiment)

if __name__ == "__main__":
    VSCODE = False
    if VSCODE:
        if os.getcwd().split('/')[-1] == "advance_bio_info": # When running on VSCode instead of Pycharm
            os.chdir("src")

    RUN_ALL_EXPERIMENT = False # you can change it
    PLOT_GRAPH = True # you can change it

    if RUN_ALL_EXPERIMENT:
        run_all_experiment()

    if PLOT_GRAPH:
        plot_experiment()