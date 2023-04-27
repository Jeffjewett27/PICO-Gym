import gymnasium as gym
from stable_baselines3 import A2C
from pico8gym.envs.cartpole import CartPoleEnv
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.vec_env import DummyVecEnv, VecMonitor
from stable_baselines3.common.env_util import make_vec_env
import time
from pico8gym.envs.pico_vec_env import PicoVecEnv
from pico8gym.envs.sb3_vec_wrapper import SB3VecEnvWrapper

from pico8gym.envs.pico_env import PicoEnv

# env = CartPoleEnv(render_mode="terminal")
def makeEnv():
    env = gym.make('pico8gym/cartpole-v0', render_mode='human')
    # return Monitor(env, filename="logs/cartpole.log")
    return env
env = SB3VecEnvWrapper(PicoVecEnv([makeEnv] * 4))
# print(env.observation_space)
# print(env.action_space)

observation = env.reset()

# for _ in range(10000):
#     action = env.action_space.sample()  # agent policy that uses the observation and info
#     observation, reward, terminated, truncated, info = env.step(action)

#     if terminated or truncated:
#         observation, info = env.reset()
#     env.render()

# env.close()

# env = VecMonitor(DummyVecEnv([makeEnv, makeEnv, makeEnv, makeEnv]))
# env = make_vec_env('pico8gym/cartpole-v0', n_envs=8, env_kwargs={ 'render_mode': 'human' })
model = A2C("MlpPolicy", env, verbose=1)
# model.learn(total_timesteps=40_000, progress_bar=True)
# model.save("models/cart3")
# print(f'NUM PICOENV STEPS: {PicoEnv.totalSteps}')
model = A2C.load("models/cart3", env=env)
vec_env = model.get_env()
obs = vec_env.reset()
for i in range(10000):
    action, _state = model.predict(obs, deterministic=True)
    obs, reward, done, info = vec_env.step(action)
    vec_env.render()

env.close()