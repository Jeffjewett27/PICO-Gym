from pico8gym.components.pico_output import PicoOutput

class RewardComponent:
    def __init__(self):
        pass

    def step_reward(self, output: PicoOutput):
        return output.reward
    
    def reset_reward(self, **kwargs):
        pass

    def render(self, img):
        return img