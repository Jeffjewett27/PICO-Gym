from gymnasium.envs.registration import register

register(
     id="pico8gym/default-v0",
     entry_point="pico8gym.envs:PicoEnv",
     max_episode_steps=300,
)

register(
     id="pico8gym/celeste-v0",
     entry_point="pico8gym.envs:CelesteEnv",
     max_episode_steps=600,
     order_enforce=False
)

register(
     id="pico8gym/cartpole-v0",
     entry_point="pico8gym.envs:CartPoleEnv",
     max_episode_steps=1000,
     order_enforce=False
)