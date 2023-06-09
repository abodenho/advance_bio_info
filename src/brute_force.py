from environement import Environement
from  itertools import permutations
from time import time
from needleman_wunsch import compute_score, needleman_wunsch
import os

ALL_DATA = {
    "Hepatitis_C": ("../Dataset/Hepatitis_C", "fasta"),
    "Papio_Anubis": ("../Dataset/Papio_Anubis", "fasta"),
    "Dataset_1": ("../Dataset/Dataset_1.txt", "txt"),
    "Lemur_gorilla_mouse": ("../Dataset/Lemur_gorilla_mouse.txt", "txt"),
    "Rat_lemur_opossum": ("../Dataset/Rat_lemur_opossum.txt", "txt"),
}

def get_AL(list_alignement):
    return len(list_alignement[0])

def get_EM(list_alignement):
    lenght = get_AL(list_alignement)
    number_exact_match = 0
    for column in range(lenght):
        is_same = True
        base = list_alignement[0][column] #take the char of the first alignement as referencement
        for alignement in list_alignement:
            if alignement[column] != base:
                is_same = False
                break
        if is_same:
            number_exact_match += 1

    return number_exact_match

def get_CS(list_alignement):
    AL = get_AL(list_alignement)
    EM = get_EM(list_alignement)
    return EM/AL

def _brut_force(all_sequences):
    all_permutation  = list(permutations(range(len(all_sequences))))
    NUMBER_PERMUTATION = len(all_permutation)
    list_best_index_alignement, list_best_alignement, best_score = [], [], 0

    for permutation in all_permutation: #journey throught all permutation
        current_alignement = []
        for index_sequence in permutation: # create the alignement
            sequence = all_sequences[index_sequence]
            if len(current_alignement) != 0:
                current_alignement = needleman_wunsch(current_alignement,sequence, version=0)
            else:
                current_alignement.append(sequence)

        current_score = compute_score(current_alignement)
        if current_score == best_score:
            list_best_alignement.append(current_alignement)
            list_best_index_alignement.append(permutation)

        elif best_score < current_score:
            list_best_alignement = [current_alignement]
            list_best_index_alignement = [permutation]
            best_score = current_score


    return list_best_index_alignement,list_best_alignement, best_score,NUMBER_PERMUTATION


def _get_name(path_data):
    tmp = path_data.split("/")
    name = tmp[-1]
    if "txt" in name: #remove .txt
        name = name.split(".")[0]
    return name

def _write_data(path,list_best_index_alignement,list_best_alignement,score,number_permutation,time):
    f = open(path + "/"+"data.txt", "w")

    f.write("Numbre total different permutation : " + str(number_permutation) + "\n")
    f.write("Best score : " + str(score) +" \n")
    f.write("Number alignement with this score : " + str(len(list_best_alignement)) + "\n")
    f.write("Time taken (in second) to run all permutation : " + str(time) + "\n" )
    f.write("\n")
    f.write("List index of those sequences : \n")
    for elem in list_best_index_alignement :
        f.write(str(elem) + "\n")

    f.write("\n")

    f.write("Alignement for those sequences : " + "\n")
    for elem_index in range(len(list_best_alignement)) :
        index_list = list_best_index_alignement[elem_index]
        alignement = list_best_alignement[elem_index]

        f.write("-> for the seq " + str(index_list) + " : \n")
        for sequence in alignement:
            f.write("\t" + str(sequence) + "\n")
        f.write("\t -> value AL " + str(get_AL(alignement)) + "\n")
        f.write("\t -> value EM " + str(get_EM(alignement)) + "\n")
        f.write("\t -> value CS " + str(get_CS(alignement)) + "\n")


        f.write("\n ")

    f.close()


def run_brute_force(experiment,setting_value,setting_name):
    key = list(ALL_DATA.keys())[experiment-1]
    path, format_file = ALL_DATA[key]

    # retrive datas
    sequences = Environement(path, format_file).get_dico_sequence()

    # begin experiment
    begin = time()
    list_best_index_alignement, list_best_alignement, best_score, number_permutation = _brut_force(sequences)
    end = time() - begin


    # save inforamtion
    name_experiment = _get_name(path)
    path_saving = "../data_experiment/" + str(setting_value) +"_" + setting_name + "/" + name_experiment

    if not os.path.isdir("../data_experiment"):
        os.mkdir("../data_experiment")
    if not os.path.isdir("../data_experiment/" + str(setting_value) +"_" + setting_name + "/"):
        os.mkdir("../data_experiment/" + str(setting_value) +"_" + setting_name + "/")
    if not os.path.isdir(path_saving):
        os.mkdir(path_saving)

    _write_data(path_saving, list_best_index_alignement, list_best_alignement, best_score, number_permutation,end)


