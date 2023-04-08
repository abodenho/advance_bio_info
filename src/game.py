def play_game(environement,agent,NUMBER_EPISODE,NUMBER_TEST,stop_to_truncated = False):
    print("Begin training")
    for episode in range(NUMBER_EPISODE):
        end = False
        observation = environement.reset()

        if (episode % 100 == 0):
            print("pourcentage ", round(episode / NUMBER_EPISODE *100, 3),"%")

        while not end:
            choice = agent.make_choice(observation)
            old_obs = observation
            observation, reward, finish, truncated,info = environement.step(choice)
            agent.learn(old_obs, observation, choice, reward, finish)

            if stop_to_truncated:
                end = finish or truncated
            else:
                end = finish

    print("Begin testing")
    agent.epsilon = 0
    for i in range(NUMBER_TEST):
        end = False
        observation = environement.reset()
        while not end:
            choice = agent.make_choice(observation)
            observation, reward, finish, truncated,info = environement.step(choice)
            if stop_to_truncated:
                end = finish or truncated
            else:
                end = finish
        print("TESTING : ",i, "\t | Choice list : ",info[0])