def play_game(environement,agent,NUMBER_EPISODE,NUMBER_TEST):
    print("Begin training")
    for episode in range(NUMBER_EPISODE):
        finish = False
        observation = environement.reset()

        if (episode % 100 == 0):
            print("pourcentage ", round(episode / NUMBER_EPISODE, 3),"%")

        while not finish:
            choice = agent.make_choice(observation)
            old_obs = observation
            observation, reward, finish, truncated,info = environement.step(choice)
            agent.learn(old_obs, observation, choice, reward, finish)

    print("Begin testing")
    agent.epsilon = 0
    for i in range(NUMBER_TEST):
        finish = False
        observation = environement.reset()
        while not finish:
            choice = agent.make_choice(observation)
            observation, reward, finish, truncated,info = environement.step(choice)
