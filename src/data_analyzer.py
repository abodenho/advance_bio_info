import numpy as np

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

def title(string):
    return "-"*10 + string + "-"*10 + "\n \n"
def experiment_analyzer(data,SAVE_TO):
    average_score,std_score, lowest_score, biggest_score, best_alignement, worst_alignement,action_list_best, action_list_worst = data.get_all_result()
    best_AL, best_EM, best_CS = get_AL(best_alignement),get_EM(best_alignement),get_CS(best_alignement)
    words_AL, words_EM, words_CS = get_AL(worst_alignement),get_EM(worst_alignement),get_CS(worst_alignement)



    running_info = data.get_info_experiment()

    mean_episode, mean_time, std_episode, std_time  = get_best_info(data)
    with open(SAVE_TO + data.get_name() + '.txt', 'w') as f:

        f.write(title("Score result"))

        f.write("Average score : {} \t | STD score : {}  \n".format(average_score,std_score))
        f.write("Biggest score encounter : {} \t | lowest score encounter : {} \n \n".format(biggest_score,lowest_score))

        f.write(title("AL, EM , CS"))
        f.write("From the best alignement encounter : \n \t - AL : {} \n \t - EM : {} \n \t - CS : {} \n".format(best_AL,best_EM,best_CS))
        f.write("From the worst alignement encounter : \n \t - AL : {} \n \t - EM : {} \n \t - CS : {} \n \n".format(words_AL,words_EM,words_CS))

        f.write(title("Reach best score"))
        f.write("Average episode to best score : " + str(mean_episode) + "\n")
        f.write("Average time to best score : " + str(mean_time) + "\n")
        f.write("STD episode to best score : " + str(std_episode) + "\n")
        f.write("STD  time to best score : " + str(std_time) + "\n \n")

        f.write(title("Experiment info"))
        for key in running_info:
            string = key + " : "+str(running_info[key]) + "\n"
            f.write(string)

        f.write("\n")

        f.write(title("Alignement"))
        f.write("BEST ENCOUNTER : {}\n".format(str(action_list_best)))
        for alignement in best_alignement:
            f.write("\t " + str(alignement) + "\n")
        f.write("\n \n \n")
        f.write("Worst ENCOUNTER : {} \n ".format(str(action_list_worst)))
        for alignement in worst_alignement:
            f.write("\t " + str(alignement) + "\n")

    f.close()


def get_best_info(data):
    list_time_best_score = []
    list_episode_best_score = []
    for expirement in range(data.get_number_experiment()):
        best_score_average = data.get_best_score_serie(expirement)
        time_series = data.get_time_serie(expirement)
        best_score = best_score_average[-1]
        for episode in range(len(best_score_average)):
            if best_score_average[episode] == best_score:
                list_episode_best_score.append(episode + 1) # +1 because we count at 1
                list_time_best_score.append(time_series[episode])
                break

    mean_episode = np.mean(list_episode_best_score)
    mean_time = np.mean(list_time_best_score)
    std_episode = np.std(list_episode_best_score)
    std_time = np.std(list_time_best_score)


    return mean_episode, mean_time, std_episode, std_time