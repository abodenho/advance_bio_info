import time
import numpy as np


class Data_garbage:
    def __init__(self):
        self.experiment = -1
        self.experiment_info = {}


    def begin_new_experiment(self):
        self.experiment += 1
        self.experiment_info[self.experiment]= {}
        self.experiment_info[self.experiment]["training"] = {}
        self.experiment_info[self.experiment]["result"] = {}

        self.best_score_encounter = float("-inf")

        self.initial_time = time.time()


    def add_data_experiment_training(self, score, episode):
        time_from_begining = time.time() - self.initial_time
        self.best_score_encounter = max(self.best_score_encounter, score)
        self.experiment_info[self.experiment]["training"][episode] = Data_episode(score,self.best_score_encounter,time_from_begining)

    def add_data_experiment_testing(self,score,alignement):
        self.experiment_info[self.experiment]["result"]["score"] = score
        self.experiment_info[self.experiment]["result"]["alignement"] = alignement


    def get_time_serie(self,experiment):
        rep = []
        for epidode in self.experiment_info[experiment]["training"]:
            data = self.experiment_info[experiment]["training"][epidode]
            rep.append(data.time)
        return rep

    def get_time_average_serie(self):
        all_experiment_time_result = []
        for experiment in range(self.experiment):
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
        for experiment in range(self.experiment):
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
        for experiment in range(self.experiment):
            all_experiment_best_score_result.append(self.get_best_score_serie(experiment))
        return np.mean(all_experiment_best_score_result,axis=0)

    def get_result(self,experiment):
        score = self.experiment_info[experiment]["result"]["score"]
        alignement = self.experiment_info[experiment]["result"]["alignement"]
        return (score,alignement)

    def get_number_experiment(self):
        return self.experiment


    def __repr__(self):
        return repr(self.experiment_info)

class Data_episode:
    def __init__(self,score,best_score_encounter,time):
        self.score = score
        self.time = time
        self.best_score_encounter = best_score_encounter

    def __repr__(self):
        return "Best Score : " + str(self.best_score_encounter)  + "\t | Time : " + str(self.time) + "\t | Real score : " + str(self.score)