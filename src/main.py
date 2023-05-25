from EXPERIMENTS import *
from data_analyzer import *
import os



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

    for i in range(5,6):
        print("--"*30,"Begin experiment :",i)
        data = eval("experiment_{}()".format(i))
        name_experimnet = data.get_name()
        experiment_info = data.get_parameter_experiment()
        print("END experiment ",name_experimnet ,"--"*30)
        if gather_data and not os.path.isdir(PATH_SAVE_DATA + name_experimnet + "_" + experiment_info):
            os.mkdir(PATH_SAVE_DATA + name_experimnet + "_" + experiment_info)
        stop_to = STOP_TO[i]
        experiment_analyzer(data,PATH_SAVE_DATA,stop_to)
        data.save(PATH_SAVE_DATA)


if __name__ == "__main__":
    VSCODE = False
    if VSCODE:
        if os.getcwd().split('/')[-1] == "advance_bio_info": # When running on VSCode instead of Pycharm
            os.chdir("src")

    run_all_experimnet()
