import json

import numpy as np
from pico8gym.server.eventlet import SocketServer
from pico8gym.pico_output import PicoOutput
import gymnasium as gym
import gymnasium.spaces as spaces

class PicoEnv(gym.Env):
    def __init__(self) -> None:
        SocketServer.ensure_instance()
        self.connection = None
        self.isInitialized = False
        self.stepNum = 0
        self.isBlocking = False

        self.action_space = spaces.MultiBinary(6)
        self.observation_space = spaces.Dict({
            'screen': spaces.Box(low=0, high=255, shape=(128,128,3), dtype=np.uint8)
        })

    def connect(self, socket):
        print(f'Connected env to {socket.environ["REMOTE_PORT"]}')
        self.connection = socket
        self.isInitialized = True

    def receive(self, output: PicoOutput):
        print(f'Received {output.screen}')
        if self.isInitialized and self.stepNum <= output.step:
            self.picoOutput = output
            self.isBlocking = False

    def step(self, action: spaces.MultiBinary):
        if self.connection is None:
            raise Exception("Cannot step orphan environment")
        msgObj = {
            'step': self.stepNum,
            'input': spaces.MultiBinary.to_jsonable(action),
        }
        self.connection.send(json.dumps(msgObj))
        self.isBlocking = True
        while self.isBlocking:
            pass
        pout = self.picoOutput
        if pout is None:
            raise Exception('No output received')
        return pout.observation, pout.reward, pout.terminated, pout.truncated, pout.info
    
    def reset(self, seed = None, options = None):
        if self.connection is None:
            raise Exception("Cannot reset orphan environment")
        
        super().reset(seed=seed)
        command = {
            'type': 'reset',
            **options
        }
        msgObj = {
            'commands': [ command ]
        }
        msg = json.dumps(msgObj)
        self.connection.send(msg)
