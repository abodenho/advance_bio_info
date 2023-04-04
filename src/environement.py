import os
import math
from copy import deepcopy
INFINITY = math.inf

class Environement:
    def __init__(self,path_folder,type_parsing):
        ### Static information
        type_parsing = type_parsing.lower()
        self.__dico_sequence = self.__parse(path_folder,type_parsing)
        ### Dynamic information
        self.__list_key_sequence_choice = []
        self.__has_multiple_same_action = False
        self.finish = False

    def step(self,choice_agent):
        self.__list_key_sequence_choice.append(choice_agent)
        truncated = self.__has_multiple_same_action
        self.finish = (len(self.__list_key_sequence_choice) == len(self.__dico_sequence))
        reward = self.__calculate_reward()
        new_state = self.__calculate_obs()
        info = (deepcopy(self.__list_key_sequence_choice),new_state)

        return  new_state,reward,self.finish,truncated,info

    def reset(self):
        self.__list_key_sequence_choice = []
        self.__has_multiple_same_action = False
        return 0
    def __calculate_obs(self):
        depth = len(self.__list_key_sequence_choice)
        #TODO A FAIRE !!!!

    def __calculate_reward(self):
        if len(self.__list_key_sequence_choice) == 1:
            reward = 0
        elif self.__has_reapeate_action():
            reward = - INFINITY
            self.__has_multiple_same_action = True

        else:
            reward = +10 #TODO ADD PART HO RAIE LIEN

        return reward

    def __has_reapeate_action(self):
        last_action = self.__list_key_sequence_choice[-1]
        rep = False
        if last_action in self.__list_key_sequence_choice[:-1]:
            rep = True
        return rep


    def __parse(self,path_folder,type_parsing):
        """
        Parse all the files
        """
        dico_sequence = {}
        cmpt = 0

        if path_folder[-1] == "/" or path_folder[-1] == "\\": # any one have this problem
            path_folder = path_folder[:-1]

        if type_parsing == "fasta":
            for file in os.listdir(path_folder):
                path_file = path_folder + "/" + file
                dico_sequence[cmpt] = self.__parse_fasta(path_file)
                cmpt += 1


        return dico_sequence
    def __parse_fasta(self,path):
        """
        Parse the fasta file
        """
        sequence = ""
        file = open(path, 'r')
        line =file.readline()
        while line:
            line = file.readline()
            if line :
                if line[-1] == "\n":
                    line = line[:-1]
                sequence += line

        file.close()

        return sequence

    def get_number_sequence(self):
        return len(self.__dico_sequence)