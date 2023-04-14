from needleman_wunsch import compute_score

def play_game(environement,agent,NUMBER_EPISODE,NUMBER_TEST,stop_to_truncated = False,VERBOSE = False):
    for episode in range(NUMBER_EPISODE):
        end = False
        observation = environement.reset()

        if (episode % 100 == 0 and VERBOSE):
            print("pourcentage ", round((episode / NUMBER_EPISODE)*100, 1),"%")

        while not end:
            choice = agent.make_choice(observation)
            old_obs = observation
            observation, reward, finish, truncated,info = environement.step(choice)
            agent.learn(old_obs, observation, choice, reward, end)
            if stop_to_truncated:
                end = finish or truncated
            else:
                end = finish

    agent.epsilon = 0
    for episode in range(NUMBER_TEST):
        end = False
        observation = environement.reset()
        while not end:
            choice = agent.make_choice(observation)
            observation, reward, finish, truncated,info = environement.step(choice)
            if stop_to_truncated:
                end = finish or truncated
            else:
                end = finish

        print("EPISODE TEST : ", episode+1)
        print("SCORE : ", compute_score(info[2]), "\t | Choice list : ",info[0])

        for seq_aling in info[2]:
            print(seq_aling)

