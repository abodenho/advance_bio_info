from agent_q_learning import Agent_q_learning
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
    NUMBER_STATE  = (NUMBER_SEQUENCE**(NUMBER_SEQUENCE-1) -1) / (NUMBER_SEQUENCE-1)
    GAMMA = ...
    ALPHA = ...
    EPSILON = ...
    agent = Agent_q_learning(NUMBER_SEQUENCE,(NUMBER_STATE),GAMMA,ALPHA,EPSILON)

    # ----------------------------------------  INIT GAME ---------------------------------------------

    NUMBER_TRAINING_EPISODE = ...
    NUMBER_TEST_EPISODE = ...

    # ----------------------------------------  RUN experiment ---------------------------------------------

    play_game(environement,agent,NUMBER_TRAINING_EPISODE,NUMBER_TEST_EPISODE)

def experiance_1():
    """
    Experiment 1 Hepatite C
    """
    # ----------------------------------------  INIT Environement ---------------------------------------------
    PATH = "../Dataset/Hepatitis_C"
    TYPE_PARSING = "fasta"
    environement = Environement(PATH,TYPE_PARSING)

    # ----------------------------------------  INIT AGENT ---------------------------------------------

    NUMBER_SEQUENCE = environement.get_number_sequence()
    NUMBER_STATE  = (NUMBER_SEQUENCE**(NUMBER_SEQUENCE-1) -1) / (NUMBER_SEQUENCE-1)
    GAMMA = 0.9
    ALPHA = 0.8
    EPSILON = 0.8
    agent = Agent_q_learning(NUMBER_SEQUENCE,(NUMBER_STATE),GAMMA,ALPHA,EPSILON)

    # ----------------------------------------  INIT GAME ---------------------------------------------

    NUMBER_TRAINING_EPISODE = 10**4
    NUMBER_TEST_EPISODE = 1

    # ----------------------------------------  RUN experiment ---------------------------------------------

    play_game(environement,agent,NUMBER_TRAINING_EPISODE,NUMBER_TEST_EPISODE)

