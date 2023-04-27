import warnings
from collections import OrderedDict
from copy import deepcopy
from typing import Any, Callable, List, Optional, Sequence, Type, Union

import gymnasium as gym
from gymnasium.vector import VectorEnv
import numpy as np

from stable_baselines3.common.vec_env.base_vec_env import VecEnv, VecEnvIndices, VecEnvObs, VecEnvStepReturn
from stable_baselines3.common.vec_env.patch_gym import _patch_env
from stable_baselines3.common.vec_env.util import copy_obs_dict, dict_to_obs, obs_space_info


class SB3VecEnvWrapper(VecEnv):
    """
    Wraps a Gymnasium VectorEnv into a Stable Baselines3 VecEnv. Modified from DummyVecEnv
    :param venv: a `gymnasium.VectorEnv` instance to be wrapped
    """

    def __init__(self, venv: VectorEnv):
        self.venv = venv
        if len(venv.envs) == 0:
            raise ValueError("The provided VectorEnv has 0 envs")
        env = self.venv.envs[0]
        VecEnv.__init__(self, len(venv.envs), env.observation_space, env.action_space, env.render_mode)
        
        self.metadata = env.metadata
        self.venv.isInfoRecords = True

    def step_async(self, actions: np.ndarray) -> None:
        self.venv.step_async(actions)

    def step_wait(self) -> VecEnvStepReturn:
        observations, rewards, terminateds, truncateds, infos = self.venv.step_wait()
        dones = terminateds | truncateds
        for i in range(len(dones)):
            if dones[i]:
                observations[i], _ = self.venv.envs[i].reset()
        return observations, rewards, dones, infos

    def seed(self, seed: Optional[int] = None) -> List[Union[None, int]]:
        # Avoid circular import
        from stable_baselines3.common.utils import compat_gym_seed

        if seed is None:
            seed = np.random.randint(0, 2**32 - 1)
        seeds = []
        for idx, env in enumerate(self.venv.envs):
            seeds.append(compat_gym_seed(env, seed=seed + idx))
        return seeds

    def reset(self) -> VecEnvObs:
        observations, _ = self.venv.reset()
        return observations

    def close(self) -> None:
        for env in self.venv.envs:
            env.close()

    def get_images(self) -> Sequence[Optional[np.ndarray]]:
        if self.render_mode != "rgb_array":
            warnings.warn(
                f"The render mode is {self.render_mode}, but this method assumes it is `rgb_array` to obtain images."
            )
            return [None for _ in self.venv.envs]
        return [env.render() for env in self.venv.envs]

    def render(self, mode: Optional[str] = None) -> Optional[np.ndarray]:
        """
        Gym environment rendering. If there are multiple environments then
        they are tiled together in one image via ``BaseVecEnv.render()``.
        :param mode: The rendering type.
        """
        # return super().render(mode=mode)
        return self.venv.render()

    def get_attr(self, attr_name: str, indices: VecEnvIndices = None) -> List[Any]:
        """Return attribute from vectorized environment (see base class)."""
        target_envs = self._get_target_envs(indices)
        return [getattr(env_i, attr_name) for env_i in target_envs]

    def set_attr(self, attr_name: str, value: Any, indices: VecEnvIndices = None) -> None:
        """Set attribute inside vectorized environments (see base class)."""
        target_envs = self._get_target_envs(indices)
        for env_i in target_envs:
            setattr(env_i, attr_name, value)

    def env_method(self, method_name: str, *method_args, indices: VecEnvIndices = None, **method_kwargs) -> List[Any]:
        """Call instance methods of vectorized environments."""
        target_envs = self._get_target_envs(indices)
        return [getattr(env_i, method_name)(*method_args, **method_kwargs) for env_i in target_envs]

    def env_is_wrapped(self, wrapper_class: Type[gym.Wrapper], indices: VecEnvIndices = None) -> List[bool]:
        """Check if worker environments are wrapped with a given wrapper"""
        target_envs = self._get_target_envs(indices)
        # Import here to avoid a circular import
        from stable_baselines3.common import env_util

        return [env_util.is_wrapped(env_i, wrapper_class) for env_i in target_envs]

    def _get_target_envs(self, indices: VecEnvIndices) -> List[gym.Env]:
        indices = self._get_indices(indices)
        return [self.venv.envs[i] for i in indices]