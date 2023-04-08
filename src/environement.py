import os
import math
import random

from tree import *
from copy import deepcopy
INFINITY = math.inf

class Environement:
    def __init__(self,path_folder,type_parsing,tree_choice = 1):
        ### Static information
        type_parsing = type_parsing.lower()
        self.__dico_sequence = self.__parse(path_folder,type_parsing)
        self.number_sequence = self.__number_action = len(self.__dico_sequence)
        if tree_choice == 1:
            self.__tree_state = Stupid_tree()
        elif tree_choice == 2:
            self.__tree_state = Soft_tree(self.number_sequence)
        elif tree_choice == 3:
            self.__tree_state = Hard_tree(self.number_sequence)

        ### Dynamic information
        self.__list_action = []
        self.__has_multiple_same_action = False
        self.finish = False

    def step(self,choice_agent):
        self.__list_action.append(choice_agent)
        truncated = self.__has_multiple_same_action
        self.finish = (len(self.__list_action) ==  self.number_sequence)
        reward = self.__calculate_reward()
        new_state = self.__calculate_obs()
        info = (deepcopy(self.__list_action), new_state)

        return  new_state,reward,self.finish,truncated,info

    def reset(self):
        self.__list_action = []
        self.__has_multiple_same_action = False
        return 0
    def __calculate_obs(self):
        return (self.__tree_state.get_state(self.__list_action) - 1) #-1 because tree go from 1 to n**(n-1)-1/n-1 and q table begin at 0

    def __calculate_reward(self):
        if len(self.__list_action) == 1:
            reward = 0
        elif self.__has_reapeate_action():
            reward = - INFINITY
            self.__has_multiple_same_action = True

        else:
            reward = random.randint(1,100) #TODO ADD PART HO RAIE LIEN

        return reward

    def __has_reapeate_action(self):
        last_action = self.__list_action[-1]
        rep = False
        if last_action in self.__list_action[:-1]:
            rep = True
        return rep


    def __parse(self, path, type_parsing):
        """
        Parse all the files
        """
        dico_sequence = {}
        cmpt = 0

        if path[-1] == "/" or path[-1] == "\\": # anyone have this problem
            path = path[:-1]

        if type_parsing == "fasta":
            for file in os.listdir(path):
                path_file = path + "/" + file
                dico_sequence[cmpt] = self.__parse_fasta(path_file)
                cmpt += 1
        elif type_parsing == "txt":
            list_sequence = self.__parse_txt(path)
            for seq in list_sequence:
                dico_sequence[cmpt] = seq
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
    def __parse_txt(self,path):
        list_sequence = []
        file = open(path, 'r')
        line =file.readline()
        while line != "\n":
            line = file.readline()
            if line != "\n" :
                idx_begin_seqence = line.index(":") + 1
                list_sequence.append(line[idx_begin_seqence:-1])
        file.close()
        return list_sequence

    def get_number_sequence(self):
        return len(self.__dico_sequence)