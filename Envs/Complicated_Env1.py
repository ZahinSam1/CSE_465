from gymnasium.spaces import Discrete, Box, Dict
from gymnasium import Env

import pygame

# env essentials import
from Agents.agent import Agent


import os
import sys
import time
sys.path.insert(1, os.path.join(sys.path[0], '..'))


class GameEnv(Env):
    def __init__(self, screen_width=400, screen_height=400, render_mode='human'):
        super(GameEnv, self).__init__()

        # defining the screen dimension for render purpose
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.render_mode = render_mode

        # defining the observation and action spaces for all the agents
        self.observation_space = Dict()

        # defining the action space based on total number of predator and prey
        # since we are training only one agent so, defining only the necessary number of actions
        self.action_space = Discrete(5)
        # 5 for rotate
        # clockwise, anti-clock
        # move front, move back and wait

        self.total_steps = 0

        self.number_of_prey = 1
        self.number_of_predator = 1
        self.prey_agent = None
        self.predator_agent = None
        self.predator_i_position = None
        self.initial_distance = None
        self.current_distance = None
        self.previous_distance = None
        self.predator_total_reward = 0
        self.number_of_agents = self.number_of_prey + self.number_of_prey

        self.obs = None

        # the pygame window should be initialized in the render function
        # initializing the pygame
        pygame.init()

        # setting the screen size
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Multi Agent Environment(simple)')

        # *it is set in mily second format (time is sec is time/1000)
        self.total_running_time = 10

        # start the tick timer
        self.start_time = 0

        # initializing the font
        pygame.font.init()
        self.font = pygame.font.Font(None, 18)

    def agent_init(self):
        prey_agents = Agent('prey', 0)

        predator_agents = Agent('predator', 0)

        self.prey_agent = prey_agents
        self.predator_agent = predator_agents

    def set_agent_number(self, prey_number, predator_number):
        self.number_of_predator = predator_number
        self.number_of_prey = prey_number

    # the usual reset function
    def reset(self, seed=0):
        self.start_time = time.time()

        self.agent_init()

        self.total_steps = 0
        self.predator_total_reward = 0

        predator = self.predator_agent

        # for predator in self.predator_agents:
        predator.agent_reset(width=self.screen_width, height=self.screen_height)
        # observation.append([predator.index, predator.agent, predator.current_position])

        # setting the predator and prey to their initial position

        self.predator_agent = predator

        # all the variable values inside the observation space needs to be sent inside the observation variable
        # for this level purpose we decided to add the dictionary observation
        # set the observation to a dictionary
        observation = None
        self.obs = observation

        return observation, seed

    def step(self, action):
        # initializing the return variables
        done = False
        reward = 0
        truncated = False
        info = {}
        current_time = time.time()

        elapsed_time = current_time - self.start_time
        # handles the pygame window event when closing
        # !if the window still crashes pygame.event needs to be managed properly
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                pygame.quit()

        predator = self.predator_agent

        # observation needs to be set a dictionary
        observation = None

        self.total_steps += 1

        self.render()

        # it will update the total reward every step
        self.predator_total_reward = reward
        self.obs = observation

        return observation, reward, done, truncated, info

    def render(self):
        if self.render_mode == 'human':
            pass

    def close(self):
        pygame.quit()
