import itertools
from copy import deepcopy
class Stupid_tree:
    """
    Creating state when encounter a new action path
    """
    def __init__(self):
        self.__tree = {}
        self.__state_number = 0
    def get_state(self,action_list):
        key = tuple(action_list)
        if not (key in self.__tree):
            self.__state_number += 1
            self.__tree[key] = self.__state_number

        return self.__tree[key]


class Soft_tree:
    """
    Soft tree more quicker to create and travel

    action == state
    """

    def __init__(self, number_sequence):
        self.__tree = {}
        self.__number_state = 0
        self.__number_sequence = number_sequence
        self.__list_sequence = [*range(number_sequence)]
        self.__create_tree()
        print(self.__tree)


    def __str__(self):
        return repr(self.__tree)

    def __create_tree(self):
        self.__number_state += 1
        self.__tree[()] = self.__number_state
        maximal_height = self.__number_sequence
        for height in range(1, maximal_height+1):
            list_state = self.__create_height(height)
            for key in list_state:
                self.__number_state += 1
                self.__tree[key] = self.__number_state

    def __create_height(self, height):
        return [p for p in itertools.product(self.__list_sequence, repeat=height)]

    def get_state(self, path_action_list):
        return self.__tree[tuple(path_action_list)]


class Hard_tree:
    """
    Tree of state exactly like the article
    """
    STATE = 0
    NUMBER_SEQUENCE = 0

    class _Node:
        def __init__(self, path_to_reach, state_number):
            self.state = state_number
            self.info = path_to_reach
            self.is_leaf = True

        def add_level(self):
            if self.is_leaf:
                self.__create_sons()
            else:
                for son in self.sons:
                    son.add_level()

        def __create_sons(self):
            self.is_leaf = False
            self.sons = []
            for seq in range(1, Hard_tree.NUMBER_SEQUENCE + 1):
                son_state = Hard_tree.STATE
                Hard_tree.STATE += 1
                path_son = deepcopy(self.info) + seq
                self.sons.append(Hard_tree._Node(path_son, son_state))

        def get_son(self, i):
            return self.sons[i]
    def __init__(self,number_sequence):
        Hard_tree.NUMBER_SEQUENCE = number_sequence
        self.__create_tree()

    def __str__(self):
        return "One day maybe" #TODO LATEX
    def __create_tree(self):
        Hard_tree.STATE += 1
        self.root = self._Node([], Hard_tree.STATE)
        for _ in range(Hard_tree.NUMBER_SEQUENCE):
            self.root.add_level()


    def get_state(self,path_action_list):
        node = self.root
        for action in path_action_list :
            node.get_son(action-1)

        return node.state