import numpy as np

class JacksCarRentalEnvironment(object):

    MAX_CAPACITY = 20
    TRANSFER_COST = 2
    REQUEST_RATE = [3, 4]
    RETURN_RATE = [3, 2]

    def step(self, action):
        done = False
        reward = 0
        info = ''

        if(np.min(observation) <= 0):
            done = True
            info = 'No cars!'
        
        if(not done):
            cars_requested_1 = np.random.poisson(REQUEST_RATE[0])
            cars_requested_2 = np.random.poisson(REQUEST_RATE[1])
            observation[0] = observation[0] - cars_requested_1
            observation[1] = observation[1] - cars_requested_2

        if(np.min(observation) <= 0 and not done):
            done = True
            info = 'Not enought cars to fulfill requests!'

        if (not done):
            reward = (cars_requested_1 + cars_requested_2) * 10 - (abs(action) * TRANSFER_COST)
        else:
            reward = -(abs(action) * 2)
            observation[0] = observation[0] - action
            observation[1] = observation[1] + action
        
        if(not done):
            if(observation[0] - action < 0 and observation[1] + action < 0):
                done = True
                info = 'Not enough cars to move!'
            else:
                observation[0] = observation[0] - action
                observation[1] = observation[1] + action

        cars_returned_1 = np.random.poisson(RETURN_RATE[0])
        cars_returned_2 = np.random.poisson(RETURN_RATE[1])
        observation[0] = observation[0] + cars_returned_1
        observation[1] = observation[1] + cars_returned_2
        np.clip(observation, None, MAX_CAPACITY)

        return observation, reward, False, info

    def reset(self, param=10):
        global observation
        observation = np.array([param, param])
        return observation

    @property
    def action_space(self):
        """
        Returns a Space object
        """
        raise NotImplementedError

    @property
    def observation_space(self):
        """
        Returns a Space object
        """
        raise NotImplementedError