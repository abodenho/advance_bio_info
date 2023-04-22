from needleman_wunsch import compute_score

def play_game(environement,agent,NUMBER_EPISODE,data_keeper,stop_to_truncated = False,VERBOSE = False):
    for episode in range(NUMBER_EPISODE):
        end = False
        observation = environement.reset()

        if (episode % 100 == 0 and VERBOSE):
            print("pourcentage ", round((episode / NUMBER_EPISODE)*100, 1),"%")

        while not end:
            choice = agent.make_choice(observation)
            old_obs = observation
            observation, reward, finish, truncated,info = environement.step(choice)
            if stop_to_truncated:
                end = finish or truncated
            else:
                end = finish
            agent.learn(old_obs, observation, choice, reward, end)


        data_keeper.add_data_experiment_training(compute_score(info[2]), episode)

    agent.epsilon = 0
    end = False
    observation = environement.reset()
    while not end:
        choice = agent.make_choice(observation)
        observation, reward, finish, truncated,info = environement.step(choice)
        if stop_to_truncated:
            end = finish or truncated
        else:
            end = finish

    data_keeper.add_data_experiment_testing(compute_score(info[2]), info[2])

    if VERBOSE:
        print("SCORE : ", compute_score(info[2]), "\t | Choice list : ",info[0])
        for seq_aling in info[2]:
            print(seq_aling)

