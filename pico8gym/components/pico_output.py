from pico8gym.util.img_util import b64_decode_img
from gymnasium import spaces
import cv2

class PicoOutput:
    @staticmethod
    def parse_bool(val):
        if type(val) == str:
            return val == 'true'
        elif type(val) == int:
            return val != 0
        return False
    
    def __init__(self, data: dict={}, infoDefaults: dict={}):
        self.event = data.pop('event', 'default')
        self.step = data.pop('step', -1)
        self.screenStr = data.pop('screen', None)
        try:
            self.reward = float(data.pop('reward', 0))
        except:
            self.reward = 0
        self.terminated = PicoOutput.parse_bool(data.pop('terminated', False))
        self.truncated = PicoOutput.parse_bool(data.pop('truncated', False))
        self.info = {
            **infoDefaults,
            **data, #remaining keys
        }

        self.screen = None
        if self.screenStr is not None and len(self.screenStr) > 0:
            self.screen = b64_decode_img(self.screenStr)
            # print('Screen transformation')
            # print(self.observation['screen'])

    def get_observation(self, observation_space: spaces.Space = None):
        # print('GET_OBS', observation_space, observation_space.shape)
        if observation_space is not None and isinstance(observation_space, spaces.Box):
            return cv2.resize(self.screen, observation_space.shape[:2], interpolation=cv2.INTER_NEAREST)
        return self.screen
    
