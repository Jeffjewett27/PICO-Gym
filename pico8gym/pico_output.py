class PicoOutput:
    @staticmethod
    def from_dict(dict):
        step = dict['step'] if 'step' in dict else -1
        obs = dict['observation'] if 'observation' in dict else {}
        reward = dict['reward'] if 'reward' in dict else 0
        term = dict['terminated'] if 'terminated' in dict else False
        trunc = dict['truncated'] if 'truncated' in dict else False
        info = dict['info'] if 'info' in dict else {}
        return PicoOutput(step, obs, reward, term, trunc, info)

    def __init__(self, step: int = 0, observation: dict = {}, reward: float = 0, 
        terminated: bool = False, truncated: bool = False, info: dict = {}):
        self.step = step
        self.observation = observation
        self.reward = reward
        self.terminated = terminated
        self.truncated = truncated
        self.info = info
