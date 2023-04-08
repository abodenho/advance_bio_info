def play_game(environement,agent,NUMBER_EPISODE,NUMBER_TEST,stop_to_truncated = False):
    print("Begin training")
    for episode in range(NUMBER_EPISODE):
        end = False
        observation = environement.reset()


        while not end:
            choice = agent.make_choice(observation)
            old_obs = observation
            observation, reward, finish, truncated,info = environement.step(choice)
            agent.learn(old_obs, observation, choice, reward, end)
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

        for seq_aling in info[2]:
            print(seq_aling)

        print("*"*50)
