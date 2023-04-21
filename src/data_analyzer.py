import matplotlib.pyplot as plt

def plot_time(list_time, stop_to = None):

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
    plt.show()


def plot_best_score(list_score,stop_to = None):
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
    plt.show()

def plot_score(list_score,stop_to = None):

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


def experiment_analyzer(data,stop_to = 100):
    score, list_alignement = data.get_result()
    time_series = data.get_time_average_serie()
    score_average = data.get_score_average_serie()
    best_score_average = data.get_best_score_average_serie()
    AL, EM, CS = get_AL(list_alignement),get_EM(list_alignement),get_CS(list_alignement)
    print("SCORE : ", score,"\t | AL : ", AL, "\t | EM : ",EM, "\t | CS : ",CS)

    plot_time(time_series,stop_to)
    plot_score(score_average,stop_to)
    plot_best_score(best_score_average,stop_to)
