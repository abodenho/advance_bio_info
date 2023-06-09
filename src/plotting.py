import os

import matplotlib.pyplot as plt
from data_garbage import Data_garbage


PATH_BRUTE_FORCE = "../data_experiment/-1_BRUTE_FORCE"
PATH_VANILLA = "../data_experiment/0_VANILLA"
PATH_ESPILON_DECAY = "../data_experiment/1_EPSILON_DECAY_Q"
PATH_WITHOUT_TRUNCATURE = "../data_experiment/2_WITHOUT_TRUNCATURE_Q"
PATH_MSA_EXTENDED_GAP = "../data_experiment/3_EXTEND_GAP_MSA"
PATH_MSA_SCORING = "../data_experiment/4_DIFFENT_VALUE_MSA"
PATH_MSA_PRIORITY = "../data_experiment/5_PRIORITY_ORDER_MSA"

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


def plot_time(list_time, PATH ,stop_to):

    if stop_to:
        number_episode = stop_to
        list_time = list_time[:stop_to]
    else:
        number_episode = len(list_time)

    plt.grid(True)
    plt.xlabel("Episode", fontsize=15)
    plt.ylabel("Time to reach episode average (seconde)", fontsize=15)
    plt.title("Time evolution", fontsize=16)
    plt.plot([*range(number_episode)],list_time)
    plt.savefig(PATH + "/"+ "time_plot.png")
    # plt.show()
    plt.clf()


def plot_best_score(list_score,PATH, stop_to):
    if stop_to:
        number_episode = stop_to
        list_score = list_score[:stop_to]
    else:
        number_episode = len(list_score)

    plt.grid(True)
    plt.xlabel("Episode", fontsize=15)
    plt.ylabel("Best score average", fontsize=15)
    plt.title("Best score evolution", fontsize=16)
    plt.plot([*range(number_episode)], list_score)
    plt.savefig(PATH +"/" + "best_score_plot.png")
    # plt.show()
    plt.clf()

def plot_score(list_score,PATH,stop_to):

    if stop_to:
        number_episode = stop_to
        list_score = list_score[:stop_to]
    else:
        number_episode = len(list_score)

    plt.grid(True)
    plt.xlabel("Episode", fontsize=15)
    plt.ylabel("Score average", fontsize=15)
    plt.title("Score evolution", fontsize=16)
    plt.plot([*range(number_episode)], list_score)
    plt.savefig(PATH +"/" +  "score_plot.png")
    # plt.show()
    plt.clf()


def get_name_experiment(FOLDER_NAME):
    tmp = FOLDER_NAME.split("EPSILON")
    tmp = tmp[0]
    tmp = tmp.split("/")
    name = tmp[-1]
    while name[-1] == "_": #remomove undersord at the end
        name = name[:-1]

    return name


def plot_all(FOLDER_DATA,experiment_name,STOP_TO):
    time_series, score_average, best_score_average, GAMMA, ALPHA, EPSILON, USE_DYNAMIC_AGENT, \
    TRONCATE, MODE_NW, EPSILON_DECAY, EPSILON_MIN = load_data(FOLDER_DATA,experiment_name)

    plot_best_score(best_score_average,FOLDER_DATA,STOP_TO)
    plot_score(score_average,FOLDER_DATA,STOP_TO)
    plot_time(time_series,FOLDER_DATA,STOP_TO)





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
        key = "EPSILON DECAY"
    elif "TRUNCATURE" in path:
        key = "WITHOUT PRUNING"
    elif "EXTEND" in path:
        key = "MSA EXTEND GAP"
    elif "DIFFENT_VALUE" in path:
        key = "MSA SCORING"
    elif "PRIORITY" in path:
        key = "MSA PRIORITY"
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
            bf_number_permutation, bf_best_score, bf_time = data[setting]

    plt.grid(True)
    plt.xlabel("Episode", fontsize=15)
    plt.ylabel("Time (seconds)", fontsize=15)
    plt.title("Execution time on " + name_experiment + " dataset", fontsize=16)
    for index in range(len(list_time_series)):
        label = labels[index]
        time_series = list_time_series[index]
        plot(time_series,stop_to,label)

    if not "Hepatitis" in name_experiment:
        plt.scatter(bf_number_permutation,bf_time,s=75,label="BRUTE_FORCE", color='black')

    plt.legend(fontsize=12)
    plt.savefig("../ultimate_plot/"+ name_experiment + "_time_plot.png")
    plt.clf()

    plt.grid(True)
    plt.xlabel("Episode", fontsize=15)
    plt.ylabel("Best score", fontsize=15)
    plt.title("Best score evolution on " + name_experiment + " dataset", fontsize=16)
    for index in range(len(list_best_score)):
        label = labels[index]
        best_score = list_best_score[index]
        plot(best_score,stop_to,label)

    if not "Hepatitis" in name_experiment:
        plt.scatter(bf_number_permutation, bf_best_score, s=75, label="BRUTE_FORCE", color='black')
    plt.legend(fontsize=12)
    plt.savefig("../ultimate_plot/"+ name_experiment + "_best_score_plot.png")
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
        normal_plot(all_data[experiment],STOP_TO[experiment],experiment)

