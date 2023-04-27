from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple, Type, Union

from stable_baselines3.common.vec_env import VecEnv, VecEnvObs
from gymnasium.vector import VectorEnv
from gymnasium import spaces

import numpy as np

class SB3VecEnvWrapper(VecEnv):
    def __init__(
        self,
        venv: VectorEnv,
        observation_space: Optional[spaces.Space] = None,
        action_space: Optional[spaces.Space] = None,
        render_mode: Optional[str] = None,
    ):
        self.venv = venv
        VecEnv.__init__(
            self,
            num_envs=venv.num_envs,
            observation_space=observation_space or venv.observation_space,
            action_space=action_space or venv.action_space,
            render_mode=render_mode or venv.render_mode,
        )
        
    def step_async(self, actions: np.ndarray) -> None:
        self.venv.step_async(actions)

    def step_wait(self):
        # TODO reset if done
        for env_idx in range(self.num_envs):
            obs, self.buf_rews[env_idx], terminated, truncated, self.buf_infos[env_idx] = self.envs[env_idx].step(
                self.actions[env_idx]
            )
            # convert to SB3 VecEnv api
            self.buf_dones[env_idx] = terminated or truncated
            # See https://github.com/openai/gym/issues/3102
            # Gym 0.26 introduces a breaking change
            self.buf_infos[env_idx]["TimeLimit.truncated"] = truncated and not terminated

            if self.buf_dones[env_idx]:
                # save final observation where user can get it, then reset
                self.buf_infos[env_idx]["terminal_observation"] = obs
                obs, self.reset_infos[env_idx] = self.envs[env_idx].reset()
            self._save_obs(env_idx, obs)
        return (self._obs_from_buf(), np.copy(self.buf_rews), np.copy(self.buf_dones), deepcopy(self.buf_infos))

    def reset(self, seed = None, options = {}):
        self.venv.reset_async(seed, options)
        self.venv.reset_wait(seed, options)

    def close(self):
        self.venv.close()

    #Duplicate DummyVecEnv behavior
    def seed(self, seed: Optional[int] = None) -> List[Union[None, int]]:
        # Avoid circular import
        from stable_baselines3.common.utils import compat_gym_seed

        if seed is None:
            seed = np.random.randint(0, 2**32 - 1)
        seeds = []
        for idx, env in enumerate(self.envs):
            seeds.append(compat_gym_seed(env, seed=seed + idx))
        return seeds

    