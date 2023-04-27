import pico8gym
import gymnasium as gym
from pico8gym.envs import CelesteEnv

# waypointModel = WaypointReward('player', [
#     (40,100),
#     (70,105),
#     (105,95),
#     (120,80),
#     (95,65),
#     (105,40),
#     (70,20),
#     (55,10),
# ], 8, 10)
# env = gym.make('pico8gym/default-v0', render_mode="terminal", rewardModel=waypointModel)
env = CelesteEnv()
observation, info = env.reset()

for _ in range(10000):
    action = env.action_space.sample()  # agent policy that uses the observation and info
    observation, reward, terminated, truncated, info = env.step(action)

    if terminated or truncated:
        observation, info = env.reset()
    env.render()

env.close()