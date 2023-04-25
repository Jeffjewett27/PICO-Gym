import gymnasium as gym
from stable_baselines3 import A2C
from pico8gym.envs.cartpole import CartPoleEnv
from stable_baselines3.common.monitor import Monitor
import time

# env = CartPoleEnv(render_mode="terminal")
env = gym.make('pico8gym/cartpole-v0')
env = Monitor(env, filename="logs/cartpole.log")

print(env.observation_space)
print(env.action_space)

# observation, info = env.reset()

# for _ in range(10000):
#     action = env.action_space.sample()  # agent policy that uses the observation and info
#     observation, reward, terminated, truncated, info = env.step(action)

#     if terminated or truncated:
#         observation, info = env.reset()
#     env.render()

# env.close()

model = A2C("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=10_000, progress_bar=True)

vec_env = model.get_env()
obs = vec_env.reset()
for i in range(1000):
    action, _state = model.predict(obs, deterministic=True)
    obs, reward, done, info = vec_env.step(action)
    vec_env.render()
    time.sleep(0.05)

env.close()