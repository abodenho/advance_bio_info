import copy
import random

import numpy as np

class Agent_q_learning:
    def __init__(self,list_action,univers,gamma,alpha,epsilon,decrease_espilon = None):
        """
        :param list_action: liste des différents actions (int)
        :param state_shape: tuple of the state different maximal state per dim  exemple (5,6,3)
        :param gamma: discount value, entre 0 et 1
        :param alpha: learning rate, entre 0 et 1
        :param epsilon: for gready espilon, entre 0 et 1
        :param decrease_espilon: for espilon gready decrease, entre 0 et 1 si None désactive la fonctionalité
        """
        self.list_action = list_action
        self.univers = univers
        self.gamme = gamma
        self.alpha = alpha
        self.epsilon = epsilon
        self.decrease_espilon = decrease_espilon
        self.number_action = len(list_action)
        self._create_q_table()


    def _create_q_table(self):
        tmp = []
        for elem in self.univers:
            tmp.append(elem)
        tmp.append(self.number_action)
        self.q_table = np.zeros(tuple(tmp))

    def make_choice(self,current_state):
        current_state = self.convert_state(current_state)
        random_value = random.random()
        if  random_value < self.epsilon:
            action = [random.choice(self.list_action)]
        else:
            best_action = None
            best_value = None
            for i in range(self.number_action):
                if best_action == None:
                    best_action = i
                    best_value = self._go_through_state(current_state)[i]
                    action = [i]
                elif self._go_through_state(current_state)[i] > best_value:
                    best_action = i
                    best_value = self._go_through_state(current_state)[i]
                    action = [i]
                elif self._go_through_state(current_state)[i] == best_value:
                    action.append(i)

        self.epsilon = self.epsilon * self.decrease_espilon
        rep = random.choice(action)

        return rep

    def learn(self,current_state,new_state,action,reward,done):
        current_state = self.convert_state(current_state)
        new_state = self.convert_state(new_state)
        if done :
            self._go_through_state(current_state)[action] = (1-self.alpha) * self._go_through_state(current_state)[action] \
                                              + self.alpha * (reward)
        else:
            self._go_through_state(current_state)[action] = (1-self.alpha) * self._go_through_state(current_state)[action] \
                                                  + self.alpha * (reward + self.gamme * self._maxQ(new_state))


    def _maxQ(self,new_state):
        best_q = float('-inf')
        for i in range(self.number_action):
            if self._go_through_state(new_state)[i] > best_q:
                best_q = self._go_through_state(new_state)[i]
        return best_q

    def _go_through_state(self,tuple_state):
        rep = self.q_table
        for elem in tuple_state:
            rep = rep[int(elem)]
        return rep

    def convert_state(self,state):
        if type(state) != tuple and type(state) != list:
            state = [state]

        return state