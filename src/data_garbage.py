import time
import numpy as np


class Data_garbage:
    def __init__(self):
        self.last_experiment_saved = None
        self.experiment_info = {}
        self.name = None
        self.dico_info_running = {}
    def set_name(self,new_name):
        self.name = new_name

    def get_name(self):
        return self.name

    def begin_new_experiment(self):
        if self.last_experiment_saved != None:
            self.last_experiment_saved += 1
        else:
            self.last_experiment_saved = 0
        self.experiment_info[self.last_experiment_saved]= {}
        self.experiment_info[self.last_experiment_saved]["training"] = {}
        self.experiment_info[self.last_experiment_saved]["result"] = {}

        self.best_score_encounter = float("-inf")

        self.initial_time = time.time()


    def add_data_experiment_training(self, score, episode):
        time_from_begining = time.time() - self.initial_time
        self.best_score_encounter = max(self.best_score_encounter, score)
        self.experiment_info[self.last_experiment_saved]["training"][episode] = Data_episode(score, self.best_score_encounter, time_from_begining)

    def add_data_experiment_testing(self,score,alignement):
        self.experiment_info[self.last_experiment_saved]["result"]["score"] = score
        self.experiment_info[self.last_experiment_saved]["result"]["alignement"] = alignement


    def get_time_serie(self,experiment):
        rep = []
        for epidode in self.experiment_info[experiment]["training"]:
            data = self.experiment_info[experiment]["training"][epidode]
            rep.append(data.time)
        return rep

    def get_time_average_serie(self):
        all_experiment_time_result = []
        for experiment in range(self.get_number_experiment()):
            all_experiment_time_result.append(self.get_time_serie(experiment))
        return np.mean(all_experiment_time_result,axis=0)


    def get_score_serie(self,experiment):
        rep = []
        for epidode in self.experiment_info[experiment]["training"]:
            data = self.experiment_info[experiment]["training"][epidode]
            rep.append(data.score)
        return rep

    def get_score_average_serie(self):
        all_experiment_score_result = []
        for experiment in range(self.get_number_experiment()):
            all_experiment_score_result.append(self.get_score_serie(experiment))
        return np.mean(all_experiment_score_result,axis=0)

    def get_best_score_serie(self,experiment):
        rep = []
        for epidode in self.experiment_info[experiment]["training"]:
            data = self.experiment_info[experiment]["training"][epidode]
            rep.append(data.best_score_encounter)
        return rep

    def get_best_score_average_serie(self):
        all_experiment_best_score_result = []
        for experiment in range(self.get_number_experiment()):
            all_experiment_best_score_result.append(self.get_best_score_serie(experiment))
        return np.mean(all_experiment_best_score_result,axis=0)

    def __get_result(self, experiment):
        score = self.experiment_info[experiment]["result"]["score"]
        alignement = self.experiment_info[experiment]["result"]["alignement"]
        return (score,alignement)

    def get_all_result(self):
        best_alignement = None
        lowest_score = float("inf")
        biggest_score = float("-inf")
        worst_alignement = None
        list_score = []
        for i in range(self.get_number_experiment()):
            score,alignement = self.__get_result(i)
            list_score.append(score)
            if score > biggest_score:
                biggest_score = score
                best_alignement = alignement
            if score < lowest_score:
                lowest_score = score
                worst_alignement = alignement
        average_score = np.mean(list_score)
        std_score = np.std(list_score)
        return average_score,std_score, lowest_score, biggest_score, best_alignement, worst_alignement


    def get_number_experiment(self):
        return self.last_experiment_saved + 1


    def __repr__(self):
        return repr(self.experiment_info)


    def add_info_experiment(self,GAMMA, ALPHA, EPSILON, NUMBER_TRAINING_EPISODE,
                            NUMBER_REPITION_EXPERIMENT, USE_DYNAMIC_AGENT, TREE_CHOICE,TRONCATE):
        self.dico_info_running["GAMMA"] = GAMMA
        self.dico_info_running["ALPHA"] = ALPHA
        self.dico_info_running["EPSILON"] = EPSILON
        self.dico_info_running["NUMBER_TRAINING_EPISODE"] = NUMBER_TRAINING_EPISODE
        self.dico_info_running["NUMBER_REPITION_EXPERIMENT"] = NUMBER_REPITION_EXPERIMENT
        self.dico_info_running["USE_DYNAMIC_AGENT"] = USE_DYNAMIC_AGENT
        if TREE_CHOICE == 1:
            TREE_CHOICE = "stupid_tree"
        elif TREE_CHOICE == 2:
            TREE_CHOICE = "quick_tree"

        elif TREE_CHOICE == 3:
            TREE_CHOICE = "article_tree"
        self.dico_info_running["TREE_CHOICE"] = TREE_CHOICE
        self.dico_info_running["TRONCATE"] = TRONCATE

    def get_info_experiment(self):
        return self.dico_info_running


class Data_episode:
    def __init__(self,score,best_score_encounter,time):
        self.score = score
        self.time = time
        self.best_score_encounter = best_score_encounter

    def __repr__(self):
        return "Best Score : " + str(self.best_score_encounter)  + "\t | Time : " + str(self.time) + "\t | Real score : " + str(self.score)