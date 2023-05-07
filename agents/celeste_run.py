import gymnasium as gym
from stable_baselines3 import PPO
from pico8gym.envs import CelesteEnv, PicoVecEnv, SB3VecEnvWrapper
from stable_baselines3.common.callbacks import CheckpointCallback, EvalCallback, CallbackList
from stable_baselines3.common.vec_env import VecFrameStack

def makeEnv():
    return gym.make('pico8gym/celeste-v0')
env = SB3VecEnvWrapper(PicoVecEnv([makeEnv] * 1))
env = VecFrameStack(env, n_stack=4)

# model = PPO.load("logs/best_model", env=env)
# model = PPO.load("models/best_celeste_t3", env=env)
model = PPO.load("logs/celeste_t5_399960_steps", env=env)
vec_env = model.get_env()
obs = vec_env.reset()
for i in range(10000):
    action, _state = model.predict(obs, deterministic=True)
    obs, reward, done, info = vec_env.step(action)
    vec_env.render()

env.close()