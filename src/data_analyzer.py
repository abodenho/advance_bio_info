import matplotlib.pyplot as plt
import os
def plot_time(list_time, name,stop_to = None):

    if stop_to:
        number_episode = stop_to
        list_time = list_time[:stop_to]
    else:
        number_episode = len(list_time)

    plt.grid(True)
    plt.xlabel("Episode")
    plt.ylabel("Time to reach episode average (seconde)")
    plt.title("Time evolution")
    plt.plot([*range(number_episode)],list_time)
    plt.savefig(name + "_time_plot.png")
    plt.show()


def plot_best_score(list_score,name, stop_to = None):
    if stop_to:
        number_episode = stop_to
        list_score = list_score[:stop_to]
    else:
        number_episode = len(list_score)

    plt.grid(True)
    plt.xlabel("Episode")
    plt.ylabel("Best score average")
    plt.title("Best score evolution")
    plt.plot([*range(number_episode)], list_score)
    plt.savefig(name + "_best_score_plot.png")
    plt.show()

def plot_score(list_score,name,stop_to = None):

    if stop_to:
        number_episode = stop_to
        list_score = list_score[:stop_to]
    else:
        number_episode = len(list_score)

    plt.grid(True)
    plt.xlabel("Episode")
    plt.ylabel("Score average")
    plt.title("Score evolution")
    plt.plot([*range(number_episode)], list_score)
    plt.savefig(name + "_score_plot.png")
    plt.show()


def get_AL(list_alignement):
    return len(list_alignement[0])

def get_EM(list_alignement):
    lenght = get_AL(list_alignement)
    number_exact_match = 0
    for column in range(lenght):
        is_same = True
        base = list_alignement[0][column] #take the char of the first alignement as referencement
        for alignement in list_alignement:
            if alignement[column] != base:
                is_same = False
                break
        if is_same:
            number_exact_match += 1

    return number_exact_match

def get_CS(list_alignement):
    AL = get_AL(list_alignement)
    EM = get_EM(list_alignement)
    return EM/AL


def experiment_analyzer(data,SAVE_TO,stop_to = 100):
    score, list_alignement = data.get_result(0)
    time_series = data.get_time_average_serie()
    score_average = data.get_score_average_serie()
    best_score_average = data.get_best_score_average_serie()
    AL, EM, CS = get_AL(list_alignement),get_EM(list_alignement),get_CS(list_alignement)
    name = SAVE_TO + data.get_name() + "/" + data.get_name()


    running_info = data.get_info_experiment()

    number_episode_before_reach_best_score, time_to_reach_best_score  = get_best_info(time_series,best_score_average)
    with open(name + '.txt', 'w') as f:
        string_info = "SCORE : " + str(score) + "\nAL : " \
                      + str(AL) + "\nEM : " + str(EM) + "\nCS : " + str(CS) + "\n"
        f.write(string_info)
        f.write("Number episode before reach best score : " + str(number_episode_before_reach_best_score) + "\n")
        f.write("Time to reach best score : " + str(time_to_reach_best_score) + "\n")
        for key in running_info:
            string = key + " : "+str(running_info[key]) + "\n"
            f.write(string)
    f.close()
    plot_time(time_series,name,stop_to)
    plot_score(score_average,name,stop_to)
    plot_best_score(best_score_average,name,stop_to)

def get_best_info(time_series,best_score_average):
    best_score = best_score_average[-1]
    number_episode_to_reach_best_score = "error"
    time_to_reach_best_score = "error"
    for episode in range(len(best_score_average)):
        if best_score_average[episode] == best_score:
            number_episode_to_reach_best_score = episode + 1 # +1 because we count at 1
            time_to_reach_best_score = time_series[episode]
            break

    return number_episode_to_reach_best_score, time_to_reach_best_score