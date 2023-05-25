import matplotlib.pyplot as plt
from data_garbage import Data_garbage

def plot_time(list_time, PATH ,stop_to):

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
    plt.savefig(PATH + "/"+ "time_plot.png")
    plt.show()


def plot_best_score(list_score,PATH, stop_to):
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
    plt.savefig(PATH +"/" + "best_score_plot.png")
    plt.show()

def plot_score(list_score,PATH,stop_to):

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
    plt.savefig(PATH +"/" +  "score_plot.png")
    plt.show()


def get_name_experiment(FOLDER_NAME):
    tmp = FOLDER_NAME.split("EPSILON")
    tmp = tmp[0]
    tmp = tmp.split("/")
    name = tmp[-1]
    while name[-1] == "_": #remomove undersord at the end
        name = name[:-1]

    return name


def load_data(FOLDER_DATA):
    data = Data_garbage()
    name_experimnet = get_name_experiment(FOLDER_DATA)
    data.load_data(FOLDER_DATA,name_experimnet)

    GAMMA, ALPHA, EPSILON, USE_DYNAMIC_AGENT, TRONCATE, MODE_NW, EPSILON_DECAY, EPSILON_MIN = data.get_parameter_experiment()
    time_series = data.get_time_average_serie()
    score_average = data.get_score_average_serie()
    best_score_average = data.get_best_score_average_serie()

    return time_series, score_average, best_score_average, GAMMA, ALPHA, EPSILON, USE_DYNAMIC_AGENT, TRONCATE, MODE_NW, EPSILON_DECAY, EPSILON_MIN

def plot_all(FOLDER_DATA,STOP_TO):
    time_series, score_average, best_score_average, GAMMA, ALPHA, EPSILON, USE_DYNAMIC_AGENT, \
    TRONCATE, MODE_NW, EPSILON_DECAY, EPSILON_MIN = load_data(FOLDER_DATA)

    plot_best_score(best_score_average,FOLDER_DATA,STOP_TO)
    plot_score(score_average,FOLDER_DATA,STOP_TO)
    plot_time(time_series,FOLDER_DATA,STOP_TO)
