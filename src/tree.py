import itertools

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