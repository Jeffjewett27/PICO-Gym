import gymnasium as gym
from stable_baselines3 import PPO
from pico8gym.envs import CelesteEnv, PicoVecEnv, SB3VecEnvWrapper
from stable_baselines3.common.callbacks import CheckpointCallback, EvalCallback, CallbackList
from stable_baselines3.common.vec_env import VecFrameStack, VecMonitor, VecTransposeImage

test='4b'
numenvs = 12

def makeEnv():
    return gym.make('pico8gym/celeste-v0')
env = SB3VecEnvWrapper(PicoVecEnv([makeEnv] * numenvs))
env = VecFrameStack(env, n_stack=4)
env = VecMonitor(env, filename=f'logs/celeste_t{test}', info_keywords=('tag',))
env = VecTransposeImage(env)

checkpoint_callback = CheckpointCallback(
  save_freq=2e5//numenvs,
  save_path="./logs/",
  name_prefix=f"celeste_t{test}"
)

eval_callback = EvalCallback(env, best_model_save_path="./logs/",
                             log_path="./logs/", eval_freq=1e5,
                             deterministic=True, render=False)

callback = CallbackList([checkpoint_callback, eval_callback])

# model = PPO("CnnPolicy", env, verbose=1, learning_rate=2.5e-4, clip_range=0.1, vf_coef=0.5, ent_coef=0.01)
model = PPO.load("logs/best_model", env=env)
# model = PPO.load('logs')
model.learn(total_timesteps=1.0e7, callback=callback, progress_bar=True)

model.save(f'models/best_celeste_t{test}')