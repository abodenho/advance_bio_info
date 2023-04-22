import os
import math
import random

from needleman_wunsch import *
from tree import *
from copy import deepcopy
INFINITY = float("inf")

class Environement:

    class calculator_needleman_wunsch:
        def __init__(self):
            self.actual_sequences_encounter = []
            self.actual_sequences_aligned = []
            self.known_alignement_sequence = {}
            self.known_alignement_sequence_score = {}

        def renitialise(self):
            self.actual_sequences_encounter = []
            self.actual_sequences_aligned = []


        def get_sequence_alignement(self):
            return self.actual_sequences_aligned


        def calculate(self,sequence,action_list):
            action_list = tuple(action_list)
            self.actual_sequences_encounter.append(sequence)
            if len(self.actual_sequences_encounter) == 1:
                score = 0
            else: #TODO optimization "1 2" == "2 1" , "1 2 3" == "2 1 3"
                if action_list in self.known_alignement_sequence_score: # case we kno the values
                    score = self.known_alignement_sequence_score[action_list]
                    self.actual_sequences_aligned = self.known_alignement_sequence[action_list]
                else: # case we do not know value and need to be calculate
                    if len(self.actual_sequences_encounter) == 2: #simple alignement
                        seq1 = self.actual_sequences_encounter[0]
                        seq2 = self.actual_sequences_encounter[1]

                        #Calculate info
                        self.actual_sequences_aligned = needleman_wunsch(deepcopy(seq1),deepcopy(seq2)) # TODO opti nécéssaire
                        score = compute_score(self.actual_sequences_aligned)
                        ## Update info
                        self.known_alignement_sequence_score[action_list] = score
                        self.known_alignement_sequence[action_list] = deepcopy(self.actual_sequences_aligned)


                    else:  # multiple alignement
                        self.actual_sequences_aligned = needleman_wunsch(deepcopy(self.actual_sequences_aligned),deepcopy(sequence))
                        score = compute_score(self.actual_sequences_aligned)
                        self.known_alignement_sequence_score[action_list] = score
                        self.known_alignement_sequence[action_list] = deepcopy(self.actual_sequences_aligned)
            return score


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
        self.NeedWunsch = self.calculator_needleman_wunsch()

    def step(self,choice_agent):
        self.__list_action.append(choice_agent)
        truncated = self.__has_multiple_same_action
        self.finish = (len(self.__list_action) ==  self.number_sequence)
        reward, alignement = self.__calculate_reward()
        new_state = self.__calculate_obs()
        info = (deepcopy(self.__list_action), new_state,alignement)

        return  new_state,reward,self.finish,truncated,info

    def reset(self):
        self.__list_action = []
        self.__has_multiple_same_action = False
        self.NeedWunsch.renitialise()
        return 0
    def __calculate_obs(self):
        return (self.__tree_state.get_state(self.__list_action) - 1) #-1 because tree go from 1 to n**(n-1)-1/n-1 and q table begin at 0

    def __calculate_reward(self):
        if self.__has_reapeate_action():
            reward = - INFINITY
            self.__has_multiple_same_action = True
        else:
            player_choice = self.__list_action[-1]
            sequence_choice = self.__dico_sequence[player_choice]
            reward = self.NeedWunsch.calculate(sequence_choice,self.__list_action)

        return reward, self.NeedWunsch.get_sequence_alignement()

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
