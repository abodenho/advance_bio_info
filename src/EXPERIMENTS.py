from Agent import Classical_q_learning,Dynamic_q_learning
from game import play_game
from environement import Environement
from data_garbage import Data_garbage

def experiment_1():
    """
    Experiment 1 : Hepatite C
    """
    # ----------------------------------------  INIT Environement ---------------------------------------------
    PATH = "../Dataset/Hepatitis_C"
    TYPE_PARSING = "fasta"

    data =  experiment(PATH,TYPE_PARSING, USE_DYNAMIC_AGENT=True,VERBOSE=True)
    data.set_name("Hepatitis_C")

    return data

def experiment_2():
    """
    Experiment 2 : Papio Anubis
    """
    # ----------------------------------------  INIT Environement ---------------------------------------------
    PATH = "../Dataset/Papio_Anubis"
    TYPE_PARSING = "fasta"

    data =  experiment(PATH,TYPE_PARSING,VERBOSE=True)
    data.set_name("Papio_Anubis")
    return data

def experiment_3():
    """
    Experiment 3 Dataset 1
    """
    # ----------------------------------------  INIT Environement ---------------------------------------------
    PATH = "../Dataset/Dataset_1.txt"
    TYPE_PARSING = "txt"

    data =  experiment(PATH, TYPE_PARSING)
    data.set_name("Dataset_1")
    return data


def experiment_4():
    """
    Experiment 4 : Lemur gorilla mouse
    """
    # ----------------------------------------  INIT Environement ---------------------------------------------
    PATH = "../Dataset/Lemur_gorilla_mouse.txt"
    TYPE_PARSING = "txt"

    data =  experiment(PATH,TYPE_PARSING)
    data.set_name("Lemur_gorilla_mouse")

    return data


def experiment_5():
    """
    Experiment 5 : Rat lemur opossum
    """
    # ----------------------------------------  INIT Environement ---------------------------------------------
    PATH = "../Dataset/Rat_lemur_opossum.txt"
    TYPE_PARSING = "txt"

    data = experiment(PATH,TYPE_PARSING)
    data.set_name("Rat_lemur_opossum")
    return data


def experiment(PATH,TYPE_PARSING, GAMMA = 0.9, ALPHA = 0.8, EPSILON = 0.01, NUMBER_TRAINING_EPISODE = 10**4 ,NUMBER_REPITION_EXPERIMENT = 5, USE_DYNAMIC_AGENT = False, TREE_CHOICE = 1,TRONCATE = True,VERBOSE = False) :


    # ----------------------------------------  INIT Environement ---------------------------------------------
    environement = Environement(PATH,TYPE_PARSING,TREE_CHOICE)

    # ----------------------------------------  INIT AGENT ---------------------------------------------

    NUMBER_SEQUENCE = environement.get_number_sequence()
    NUMBER_STATE  = int((NUMBER_SEQUENCE**(NUMBER_SEQUENCE+1) -1) / (NUMBER_SEQUENCE-1))
    LIST_POSSIBLE_ACTION = [*range(NUMBER_SEQUENCE)]

    # ----------------------------------------  RUN experiment ---------------------------------------------
    data_keeper = Data_garbage()
    data_keeper.add_info_experiment(GAMMA, ALPHA, EPSILON, NUMBER_TRAINING_EPISODE,NUMBER_REPITION_EXPERIMENT, USE_DYNAMIC_AGENT, TREE_CHOICE,TRONCATE)
    for experiment in range(NUMBER_REPITION_EXPERIMENT):
        if USE_DYNAMIC_AGENT:
            agent = Dynamic_q_learning(LIST_POSSIBLE_ACTION, NUMBER_STATE, GAMMA, ALPHA, EPSILON)
        else:
            agent = Classical_q_learning(LIST_POSSIBLE_ACTION, NUMBER_STATE, GAMMA, ALPHA, EPSILON)

        print("Repetion ",experiment)
        data_keeper.begin_new_experiment()
        play_game(environement,agent,NUMBER_TRAINING_EPISODE,data_keeper,TRONCATE,VERBOSE)
        print("*"*50)
    return data_keeper

