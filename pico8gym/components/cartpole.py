from pico8gym.util.img_util import b64_decode_img
from .pico_output import PicoOutput

import numpy as np

class CartPoleOutput(PicoOutput):
    def __init__(self, data: dict={}):
        super().__init__(data)

    def get_observation(self):
        keys = ['x','x_dot','theta','theta_dot']
        values = [self.info.get(key, 0) for key in keys]
        return np.array(values, dtype=np.float32)
