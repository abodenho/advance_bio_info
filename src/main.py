from EXPERIMENTS import *
from data_plotter import *
if __name__ == "__main__":
    data = experiment_5()

    STOP_TO = 60
    plot_best_score(data.get_best_score_average_serie(),STOP_TO)
    plot_time(data.get_time_average_serie(),STOP_TO)
