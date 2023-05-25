from EXPERIMENTS import *
from data_analyzer import *
import os
from plotting import plot_all


PATH_SAVE_DATA = "../data_experiment/"

STOP_TO = { # COPY of article information
    1 : 150,
    2 : 210,
    3 : 150,
    4 : 150,
    5 : 250
}



def run_all_experimnet(gather_data = True):

    if gather_data and not os.path.isdir(PATH_SAVE_DATA):
        os.mkdir(PATH_SAVE_DATA)

    #PARAMETER TO PLAY WITH

    USE_DYNAMIC_AGENT = True
    TRONCATE = True
    EPSILON = 0.8
    ESPILON_DECAY = None
    ESPILON_MIN = None
    NW_MODE = 0

    for i in range(5,6):
        print("--"*30,"Begin experiment :",i)
        data = eval("experiment_{}(USE_DYNAMIC_AGENT,TRONCATE,EPSILON,ESPILON_DECAY,ESPILON_MIN,NW_MODE)".format(i))
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



if __name__ == "__main__":
    VSCODE = False
    if VSCODE:
        if os.getcwd().split('/')[-1] == "advance_bio_info": # When running on VSCode instead of Pycharm
            os.chdir("src")

    run_all_experimnet()
