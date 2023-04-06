import itertools
from copy import deepcopy

class Soft_tree:
    """
    Soft tree more quicker to create and travel
    """

    def __init__(self, number_sequence):
        self.__tree = {}
        self.__number_state = 0
        self.__number_sequence = number_sequence
        self.__list_sequence = [*range(1, number_sequence + 1)]

    def __create_tree(self):
        self.__number_state += 1
        self.__tree[()] = self.__number_state
        maximal_height = self.__number_sequence
        for height in range(1, maximal_height):
            list_state = self.__create_height(height)
            for key in list_state:
                self.__number_state += 1
                self.__tree[key] = self.__number_state

    def __create_height(self, height):
        return [p for p in itertools.product(self.__list_sequence, repeat=height)]

    def get_state(self, path_action):
        return self.__tree[path_action]

    def print_tree(self):
        print(self.__tree)


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
                Hard_tree.STATE += 1
                son_state = Hard_tree.STATE
                path_son = deepcopy(self.info) + seq
                self.sons.append(Hard_tree._Node(path_son, son_state))

        def get_son(self, i):
            return self.sons[i]
    def __init__(self,number_sequence):
        Hard_tree.NUMBER_SEQUENCE = number_sequence
        self.__create_tree()
    def __create_tree(self):
        Hard_tree.STATE += 1
        self.root = self._Node([], Hard_tree.STATE)
        for _ in range(Hard_tree.NUMBER_SEQUENCE):
            self.root.add_level()


    def get_state(self,path_action):
        node = self.root
        for action in path_action :
            node.get_son(action-1)

        return node.state