import os

import matplotlib.pyplot as plt
from data_garbage import Data_garbage


PATH_BRUTE_FORCE = "../data_experiment/-1_BRUTE_FORCE"
PATH_VANILLA = "../data_experiment/0_VANILLA"
PATH_ESPILON_DECAY = "../data_experiment/1_EPSILON_DECAY"
PATH_WITHOUT_TRUNCATURE = "../data_experiment/2_WITHOUT_TRUNCATURE"
PATH_MSA_EXTENDED_GAP = "../data_experiment/3_MSA_EXTEND_GAP"
PATH_MSA_SCORING = "../data_experiment/4_MSA_SCORING"
PATH_MSA_PRIORITY = "../data_experiment/5_MSA_PRIORITY"

LIST_PATH_SETTINGS = [PATH_VANILLA,PATH_ESPILON_DECAY,PATH_WITHOUT_TRUNCATURE,PATH_MSA_EXTENDED_GAP,
                      PATH_MSA_SCORING,PATH_MSA_PRIORITY]

LIST_NAME_EXPERIMENT = ["Hepatitis_C","Papio_Anubis","Dataset_1","Lemur_gorilla_mouse","Rat_lemur_opossum"]

STOP_TO = { # COPY of article information + 50
    "Hepatitis_C" : 150,
    "Papio_Anubis" : 210,
    "Dataset_1" : 150,
    "Lemur_gorilla_mouse" : 150,
    "Rat_lemur_opossum" : 250
}



def load_data(FOLDER_DATA,experiment_name):
    data = Data_garbage()
    data.load_data(FOLDER_DATA,experiment_name)

    GAMMA, ALPHA, EPSILON, USE_DYNAMIC_AGENT, TRONCATE, MODE_NW, EPSILON_DECAY, EPSILON_MIN = data.get_parameter_experiment()
    time_series = data.get_time_average_serie()
    score_average = data.get_score_average_serie()
    best_score_average = data.get_best_score_average_serie()

    return time_series, score_average, best_score_average, GAMMA, ALPHA, EPSILON, USE_DYNAMIC_AGENT, TRONCATE, MODE_NW, EPSILON_DECAY, EPSILON_MIN


def get_key_dico(path):
    if "VANILLA" in path:
        key = "VANILLA"
    elif "DECAY" in path:
        key = "EPSILON_DECAY"
    elif "TRUNCATURE" in path:
        key = "WITHOUT_TRUNCATURE"
    elif "EXTEND" in path:
        key = "MSA_EXTEND_GAP"
    elif "MSA_SCORING" in path:
        key = "MSA_SCORING"
    elif "MSA_PRIORITY" in path:
        key = "MSA_PRIORITY"
    else:
        raise Exception

    return key

def get_info_brute_force(path_txt):
    f = open(path_txt, "r")
    number_permutation = int(f.readline().split(":")[-1])
    best_score = int(f.readline().split(":")[-1])
    f.readline()
    time = float(f.readline().split(":")[-1])
    f.close()
    return number_permutation,best_score,time


def gather_all_data(experiment_name):
    dico_data = {}
    for path_setting in LIST_PATH_SETTINGS: #recovery all but not brute force
        path_experiment_setting_data = path_setting + "/" + experiment_name
        time_series, score_average, best_score_average, GAMMA, ALPHA, EPSILON, USE_DYNAMIC_AGENT, \
        TRONCATE, MODE_NW, EPSILON_DECAY, EPSILON_MIN = load_data(path_experiment_setting_data,experiment_name)
        key = get_key_dico(path_setting)
        dico_data[key] = (time_series, best_score_average)



    ### Recover data from brute force
    if experiment_name == "Hepatitis_C": # we do not have any data
        dico_data["BRUTE_FORCE"] = (None,None,None)

    else:
        path_experiment_setting_data = PATH_BRUTE_FORCE + "/" +  experiment_name + "/" + "data.txt"
        dico_data["BRUTE_FORCE"]  = get_info_brute_force(path_experiment_setting_data)

    return dico_data


def normal_plot(data,stop_to,name_experiment):
    labels = []
    list_time_series = []
    list_best_score = []
    for setting in data:
        if setting != "BRUTE_FORCE":
            time_series, best_score_average = data[setting]
            labels.append(setting)
            list_time_series.append(time_series)
            list_best_score.append(best_score_average)

        else:
            number_permutation, best_score, time = data[setting]

    plt.grid(True)
    plt.xlabel("Episode")
    plt.ylabel("Time to reach episode average (seconds)")
    plt.title("Time evolution" + " "  + name_experiment)
    for index in range(len(list_time_series)):
        label = labels[index]
        time_series = list_time_series[index]
        plot(time_series,stop_to,label)
    plt.legend()

    plt.savefig("../ultimate_plot/"+ name_experiment + "_time_plot.png")
    plt.clf()

    plt.grid(True)
    plt.xlabel("Episode")
    plt.ylabel("Best score average")
    plt.title("Best score evolution" + " "  + name_experiment)
    for index in range(len(list_best_score)):
        label = labels[index]
        best_score = list_best_score[index]
        plot(best_score,stop_to,label)
    plt.legend()
    plt.savefig("../ultimate_plot/"+ name_experiment + "_best_score_plot.png")
    plt.clf()



def hepatitis_plot(data,stop_to,name_experiment):
    labels = []
    list_time_series = []
    list_best_score = []
    for setting in data:
        if setting != "BRUTE_FORCE":
            time_series, best_score_average = data[setting]
            labels.append(setting)
            list_time_series.append(time_series)
            list_best_score.append(best_score_average)

    plt.grid(True)
    plt.xlabel("Episode")
    plt.ylabel("Time to reach episode average (seconds)")
    plt.title("Time evolution" + " " + name_experiment)
    for index in range(len(list_time_series)):
        label = labels[index]
        time_series = list_time_series[index]
        plot(time_series, stop_to, label)
    plt.legend()

    plt.savefig("../ultimate_plot/" + name_experiment + "_time_plot.png")
    plt.clf()

    plt.grid(True)
    plt.xlabel("Episode")
    plt.ylabel("Best score average")
    plt.title("Best score evolution")
    for index in range(len(list_best_score)):
        label = labels[index]
        best_score = list_best_score[index]
        plot(best_score, stop_to, label)
    plt.legend()
    plt.savefig("../ultimate_plot/" + name_experiment + "_best_score_plot.png")
    plt.clf()






def plot(data ,stop_to,label):

    if stop_to:
        number_episode = stop_to
        data = data[:stop_to]
    else:
        number_episode = len(data)

    plt.plot([*range(number_episode)],data,label=label)




def plot_experiment():
    if  not os.path.isdir("../ultimate_plot"):
        os.mkdir("../ultimate_plot")

    all_data = {}
    for experiment in LIST_NAME_EXPERIMENT:
        all_data[experiment] = gather_all_data(experiment)



    #Key :  experiment name | value : dictionnary -> key : setting | value : datas

    for experiment in LIST_NAME_EXPERIMENT:
        if experiment != "Hepatitis_C":
            normal_plot(all_data[experiment],STOP_TO[experiment],experiment)
        else:
            hepatitis_plot(all_data[experiment],STOP_TO[experiment],experiment)

plot_experiment()