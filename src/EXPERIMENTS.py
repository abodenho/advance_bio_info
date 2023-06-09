from Agent import Classical_q_learning,Dynamic_q_learning
from game import play_game
from environement import Environement
from data_garbage import Data_garbage

def experiment_1(TRONCATE,EPSILON,ESPILON_DECAY,ESPILON_MIN,NW_MODE):
    """
    Experiment 1 : Hepatite C
    """
    # ----------------------------------------  INIT Environement ---------------------------------------------
    PATH = "../Dataset/Hepatitis_C"
    TYPE_PARSING = "fasta"

    data = experiment(PATH,TYPE_PARSING,EPSILON=EPSILON,
                      TRONCATE= TRONCATE,ESPILON_DECAY=ESPILON_DECAY, ESPILON_MIN=ESPILON_MIN,NW_MODE=NW_MODE)

    data.set_name_experiment("Hepatitis_C")
    return data

def experiment_2(TRONCATE,EPSILON,ESPILON_DECAY,ESPILON_MIN,NW_MODE):
    """
    Experiment 2 : Papio Anubis
    """
    # ----------------------------------------  INIT Environement ---------------------------------------------
    PATH = "../Dataset/Papio_Anubis"
    TYPE_PARSING = "fasta"

    data = experiment(PATH,TYPE_PARSING,EPSILON=EPSILON,
                      TRONCATE= TRONCATE,ESPILON_DECAY=ESPILON_DECAY, ESPILON_MIN=ESPILON_MIN,NW_MODE=NW_MODE)

    data.set_name_experiment("Papio_Anubis")
    return data

def experiment_3(TRONCATE,EPSILON,ESPILON_DECAY,ESPILON_MIN,NW_MODE):
    """
    Experiment 3 Dataset 1
    """
    # ----------------------------------------  INIT Environement ---------------------------------------------
    PATH = "../Dataset/Dataset_1.txt"
    TYPE_PARSING = "txt"

    data = experiment(PATH,TYPE_PARSING,EPSILON=EPSILON,
                      TRONCATE= TRONCATE,ESPILON_DECAY=ESPILON_DECAY, ESPILON_MIN=ESPILON_MIN,NW_MODE=NW_MODE)


    data.set_name_experiment("Dataset_1")
    return data


def experiment_4(TRONCATE,EPSILON,ESPILON_DECAY,ESPILON_MIN,NW_MODE):
    """
    Experiment 4 : Lemur gorilla mouse
    """
    # ----------------------------------------  INIT Environement ---------------------------------------------
    PATH = "../Dataset/Lemur_gorilla_mouse.txt"
    TYPE_PARSING = "txt"

    data = experiment(PATH,TYPE_PARSING,EPSILON=EPSILON,
                      TRONCATE= TRONCATE,ESPILON_DECAY=ESPILON_DECAY, ESPILON_MIN=ESPILON_MIN,NW_MODE=NW_MODE)

    data.set_name_experiment("Lemur_gorilla_mouse")

    return data


def experiment_5(TRONCATE,EPSILON,ESPILON_DECAY,ESPILON_MIN,NW_MODE):
    """
    Experiment 5 : Rat lemur opossum
    """
    # ----------------------------------------  INIT Environement ---------------------------------------------
    PATH = "../Dataset/Rat_lemur_opossum.txt"
    TYPE_PARSING = "txt"

    data = experiment(PATH,TYPE_PARSING,EPSILON=EPSILON,
                      TRONCATE= TRONCATE,ESPILON_DECAY=ESPILON_DECAY, ESPILON_MIN=ESPILON_MIN,NW_MODE=NW_MODE)
    data.set_name_experiment("Rat_lemur_opossum")

    return data


def experiment(PATH,TYPE_PARSING, GAMMA = 0.9, ALPHA = 0.8, EPSILON = 0.2, NUMBER_TRAINING_EPISODE = 10**3 ,NUMBER_REPITION_EXPERIMENT = 20,
               USE_DYNAMIC_AGENT = True, TREE_CHOICE = 1,TRONCATE = True,VERBOSE = False, ESPILON_DECAY = None , ESPILON_MIN = None, NW_MODE = 0) : # NUMBER_TRAINING_EPISODE = 10**4


    # ----------------------------------------  INIT Environement ---------------------------------------------
    environement = Environement(PATH,TYPE_PARSING,TREE_CHOICE,NW_MODE)

    # ----------------------------------------  INIT AGENT ---------------------------------------------

    NUMBER_SEQUENCE = environement.get_number_sequence()
    NUMBER_STATE  = int((NUMBER_SEQUENCE**(NUMBER_SEQUENCE+1) -1) / (NUMBER_SEQUENCE-1))
    LIST_POSSIBLE_ACTION = [*range(NUMBER_SEQUENCE)]

    # ----------------------------------------  RUN experiment ---------------------------------------------
    data_keeper = Data_garbage()
    data_keeper.add_info_experiment(GAMMA, ALPHA, EPSILON, NUMBER_TRAINING_EPISODE,NUMBER_REPITION_EXPERIMENT,
                                    USE_DYNAMIC_AGENT, TREE_CHOICE,TRONCATE,ESPILON_DECAY,ESPILON_MIN,NW_MODE)
    for experiment in range(NUMBER_REPITION_EXPERIMENT):
        environement = Environement(PATH, TYPE_PARSING, TREE_CHOICE, NW_MODE)
        if USE_DYNAMIC_AGENT:
            agent = Dynamic_q_learning(LIST_POSSIBLE_ACTION, NUMBER_STATE, GAMMA, ALPHA, EPSILON,ESPILON_DECAY,ESPILON_MIN)
        else:
            agent = Classical_q_learning(LIST_POSSIBLE_ACTION, NUMBER_STATE, GAMMA, ALPHA, EPSILON,ESPILON_DECAY,ESPILON_MIN)

        print("Repetion ",experiment)
        data_keeper.begin_new_experiment()
        play_game(environement,agent,NUMBER_TRAINING_EPISODE,data_keeper,TRONCATE,VERBOSE)
        environement = Environement(PATH, TYPE_PARSING, TREE_CHOICE, NW_MODE)
        print("*"*50)
    return data_keeper

