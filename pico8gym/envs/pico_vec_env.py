from pico8gym.envs.pico_env_pool import PicoEnvPool
from .pico_env import PicoEnv
import gymnasium as gym
from gymnasium.vector.utils import iterate
import numpy as np

class PicoVecEnv(gym.vector.VectorEnv):
    def __init__(self, env_fns, num_envs: int = -1, observation_space: gym.Space = None, action_space: gym.Space = None):
        self.num_envs = max(len(env_fns), num_envs)
        assert self.num_envs > 0
        self.envs = []
        for i in range(self.num_envs):
            self.envs.append(env_fns[i%len(env_fns)]())

        super().__init__(self.num_envs, self.envs[0].observation_space, self.envs[0].action_space)

    def step_async(self, actions):
        actionIterable = iterate(self.action_space, actions)
        for (env, action) in zip(self.envs, actionIterable):
            env.step_async(action)
    
    def step_wait(self):
        observations_list, rewards, terminateds, truncateds = [], [], [], []
        if self.isInfoRecords:
            infos = []
        else:
            infos = {}
        for i in range(len(self.envs)):
            obs, rew, terminated, truncated, info = self.envs[i].step_wait()
            observations_list.append(obs)
            rewards.append(rew)
            terminateds.append(terminated)
            truncateds.append(truncated)
            if self.isInfoRecords:
                infos.append(info)
            else:
                infos = self._add_info(infos, info, i)

        return (
            np.array(observations_list),
            np.array(rewards),
            np.array(terminateds, dtype=np.bool_),
            np.array(truncateds, dtype=np.bool_),
            infos,
        )

    def step(self, actions):
        self.step_async(actions)
        return self.step_wait(actions)

    def reset_async(self, seed = None, options = {}):
        if seed is None:
            seed = [None for _ in range(self.num_envs)]
        if isinstance(seed, int):
            seed = [seed + i for i in range(self.num_envs)]
        assert len(seed) == self.num_envs

        for i, (env, single_seed) in enumerate(zip(self.envs, seed)):
            kwargs = {}
            if single_seed is not None:
                kwargs["seed"] = single_seed
            if options is not None:
                kwargs["options"] = options

            env.reset_async(**kwargs)

    def reset_wait(self, seed = None, options = {}):
        observations = []
        infos = {}
        for i, env in enumerate(self.envs):
            observation, info = env.reset_wait()
            observations.append(observation)
            infos = self._add_info(infos, info, i)
        return np.array(observations), infos

    def reset(self, seed = None, options = {}):
        super().reset(seed=seed)
        self.reset_async(seed, options)
        return self.reset_wait()

    def render(self):
        self.envs[0].render()

    def close(self, **kwargs):
        pass