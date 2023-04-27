import gymnasium as gym
import gymnasium.spaces as spaces
from pico8gym.envs import PicoEnv
from pico8gym.components import PicoControls, CartPoleOutput

import math
import numpy as np

class CartPoleEnv(PicoEnv):
    def __init__(self, render_mode=None) -> None:
        controllerInput = PicoControls([PicoControls.NONE, PicoControls.RIGHT], isDiscrete=True)
        super().__init__(
            cart='cartpole',
            controls=controllerInput,
            outputClass=CartPoleOutput,
            render_mode=render_mode
        )

        # Angle at which to fail the episode
        self.theta_threshold_radians = 12 * 2 * math.pi / 360
        self.x_threshold = 2.4

        # Angle limit set to 2 * theta_threshold_radians so failing observation
        # is still within bounds.
        high = np.array(
            [
                self.x_threshold * 2,
                np.finfo(np.float32).max,
                self.theta_threshold_radians * 2,
                np.finfo(np.float32).max,
            ],
            dtype=np.float32,
        )
        self.observation_space = spaces.Box(-high, high, dtype=np.float32)

