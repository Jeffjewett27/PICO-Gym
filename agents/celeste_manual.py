import pico8gym
import gymnasium as gym
from pico8gym.envs import CelesteEnv
from pygame import key
import pygame
import numpy as np

env = CelesteEnv()
observation, info = env.reset()
env.render()

for _ in range(10000):
    keys = key.get_pressed()
    action = env.action_space.from_jsonable([
        keys[pygame.K_LEFT],
        keys[pygame.K_RIGHT],
        keys[pygame.K_UP],
        keys[pygame.K_DOWN],
        keys[pygame.K_z],
        keys[pygame.K_x]
    ])
    
    # action = env.action_space.sample()  # agent policy that uses the observation and info
    observation, reward, terminated, truncated, info = env.step(action)
    # print(info)
    if terminated or truncated:
        observation, info = env.reset()
    env.render()
    
env.close()