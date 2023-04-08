from Agent import Classical_q_learning,Dynamic_q_learning
from game import play_game
from environement import Environement


def experiance_template(): # DO NOT RUN
    """
    Experiment template, do not use !!! juste for copy paste with != values
    """
    # ----------------------------------------  INIT Environement ---------------------------------------------
    PATH = ...
    TYPE_PARSING = ...
    environement = Environement(PATH,TYPE_PARSING)

    # ----------------------------------------  INIT AGENT ---------------------------------------------

    NUMBER_SEQUENCE = environement.get_number_sequence()
    NUMBER_STATE  = int((NUMBER_SEQUENCE**(NUMBER_SEQUENCE+1) -1) / (NUMBER_SEQUENCE-1))
    GAMMA = ...
    ALPHA = ...
    EPSILON = ...
    LIST_POSSIBLE_ACTION = [*range(1,NUMBER_SEQUENCE+1)]
    agent = Classical_q_learning(LIST_POSSIBLE_ACTION, NUMBER_STATE, GAMMA, ALPHA, EPSILON)

    # ----------------------------------------  INIT GAME ---------------------------------------------

    NUMBER_TRAINING_EPISODE = ...
    NUMBER_TEST_EPISODE = ...

    # ----------------------------------------  RUN experiment ---------------------------------------------

    play_game(environement,agent,NUMBER_TRAINING_EPISODE,NUMBER_TEST_EPISODE)

def experiment_1():
    """
    Experiment 1 : Hepatite C
    """
    # ----------------------------------------  INIT Environement ---------------------------------------------
    PATH = "../Dataset/Hepatitis_C"
    TYPE_PARSING = "fasta"
    environement = Environement(PATH,TYPE_PARSING)

    # ----------------------------------------  INIT AGENT ---------------------------------------------

    NUMBER_SEQUENCE = environement.get_number_sequence()
    NUMBER_STATE  = int((NUMBER_SEQUENCE**(NUMBER_SEQUENCE+1) -1) / (NUMBER_SEQUENCE-1))
    GAMMA = 0.9
    ALPHA = 0.8
    EPSILON = 0.8
    LIST_POSSIBLE_ACTION = [*range(NUMBER_SEQUENCE)]
    agent = Dynamic_q_learning(LIST_POSSIBLE_ACTION, NUMBER_STATE, GAMMA, ALPHA, EPSILON)

    # ----------------------------------------  INIT GAME ---------------------------------------------

    NUMBER_TRAINING_EPISODE = 10**4
    NUMBER_TEST_EPISODE = 1

    # ----------------------------------------  RUN experiment ---------------------------------------------
    play_game(environement,agent,NUMBER_TRAINING_EPISODE,NUMBER_TEST_EPISODE,True)
def experiment_2():
    """
    Experiment 2 : Papio Anubis
    """
    # ----------------------------------------  INIT Environement ---------------------------------------------
    PATH = "../Dataset/Papio_Anubis"
    TYPE_PARSING = "fasta"
    environement = Environement(PATH,TYPE_PARSING)

    # ----------------------------------------  INIT AGENT ---------------------------------------------

    NUMBER_SEQUENCE = environement.get_number_sequence()
    NUMBER_STATE  = int((NUMBER_SEQUENCE**(NUMBER_SEQUENCE+1) -1) / (NUMBER_SEQUENCE-1))
    GAMMA = 0.9
    ALPHA = 0.8
    EPSILON = 0.8
    LIST_POSSIBLE_ACTION = [*range(NUMBER_SEQUENCE)]
    agent = Classical_q_learning(LIST_POSSIBLE_ACTION, NUMBER_STATE, GAMMA, ALPHA, EPSILON)

    # ----------------------------------------  INIT GAME ---------------------------------------------

    NUMBER_TRAINING_EPISODE = 10**4
    NUMBER_TEST_EPISODE = 1

    # ----------------------------------------  RUN experiment ---------------------------------------------
    play_game(environement,agent,NUMBER_TRAINING_EPISODE,NUMBER_TEST_EPISODE)

def experiment_3():
    """
    Experiment 3 Dataset 1
    """
    # ----------------------------------------  INIT Environement ---------------------------------------------
    PATH = "../Dataset/Dataset_1.txt"
    TYPE_PARSING = "txt"
    environement = Environement(PATH,TYPE_PARSING)

    # ----------------------------------------  INIT AGENT ---------------------------------------------

    NUMBER_SEQUENCE = environement.get_number_sequence()
    NUMBER_STATE  = int((NUMBER_SEQUENCE**(NUMBER_SEQUENCE+1) -1) / (NUMBER_SEQUENCE-1))
    GAMMA = 0.9
    ALPHA = 0.8
    EPSILON = 0.8
    LIST_POSSIBLE_ACTION = [*range(NUMBER_SEQUENCE)]
    agent = Classical_q_learning(LIST_POSSIBLE_ACTION, NUMBER_STATE, GAMMA, ALPHA, EPSILON)

    # ----------------------------------------  INIT GAME ---------------------------------------------

    NUMBER_TRAINING_EPISODE = 10**4
    NUMBER_TEST_EPISODE = 1

    # ----------------------------------------  RUN experiment ---------------------------------------------
    play_game(environement,agent,NUMBER_TRAINING_EPISODE,NUMBER_TEST_EPISODE)

def experiment_4():
    """
    Experiment 4 : Lemur gorilla mouse
    """
    # ----------------------------------------  INIT Environement ---------------------------------------------
    PATH = "../Dataset/Lemur_gorilla_mouse.txt"
    TYPE_PARSING = "txt"
    environement = Environement(PATH,TYPE_PARSING)

    # ----------------------------------------  INIT AGENT ---------------------------------------------

    NUMBER_SEQUENCE = environement.get_number_sequence()
    NUMBER_STATE  = int((NUMBER_SEQUENCE**(NUMBER_SEQUENCE+1) -1) / (NUMBER_SEQUENCE-1))
    GAMMA = 0.9
    ALPHA = 0.8
    EPSILON = 0.8
    LIST_POSSIBLE_ACTION = [*range(NUMBER_SEQUENCE)]
    agent = Classical_q_learning(LIST_POSSIBLE_ACTION, NUMBER_STATE, GAMMA, ALPHA, EPSILON)

    # ----------------------------------------  INIT GAME ---------------------------------------------

    NUMBER_TRAINING_EPISODE = 10**4
    NUMBER_TEST_EPISODE = 1

    # ----------------------------------------  RUN experiment ---------------------------------------------
    play_game(environement,agent,NUMBER_TRAINING_EPISODE,NUMBER_TEST_EPISODE)


def experiment_5():
    """
    Experiment 5 : Rat lemur opossum
    """
    # ----------------------------------------  INIT Environement ---------------------------------------------
    PATH = "../Dataset/Rat_lemur_opossum.txt"
    TYPE_PARSING = "txt"
    environement = Environement(PATH,TYPE_PARSING)

    # ----------------------------------------  INIT AGENT ---------------------------------------------

    NUMBER_SEQUENCE = environement.get_number_sequence()
    NUMBER_STATE  = int((NUMBER_SEQUENCE**(NUMBER_SEQUENCE+1) -1) / (NUMBER_SEQUENCE-1))
    GAMMA = 0.9
    ALPHA = 0.8
    EPSILON = 0.8
    LIST_POSSIBLE_ACTION = [*range(NUMBER_SEQUENCE)]
    agent = Classical_q_learning(LIST_POSSIBLE_ACTION, NUMBER_STATE, GAMMA, ALPHA, EPSILON)

    # ----------------------------------------  INIT GAME ---------------------------------------------

    NUMBER_TRAINING_EPISODE = 10**4
    NUMBER_TEST_EPISODE = 1

    # ----------------------------------------  RUN experiment ---------------------------------------------
    play_game(environement,agent,NUMBER_TRAINING_EPISODE,NUMBER_TEST_EPISODE)