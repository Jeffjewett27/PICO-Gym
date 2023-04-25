import json
import threading
import cv2

import numpy as np
from pico8gym.envs.pico_env_pool import PicoEnvPool
from pico8gym.components.reward_component import RewardComponent
from pico8gym.util.img_util import fancy_print_image, save_image
from pico8gym.server.eventlet import SocketServer
from pico8gym.components.pico_output import PicoOutput
from pico8gym.components.pico_controls import PicoControls
import gymnasium as gym
import gymnasium.spaces as spaces
# import subprocess
# import asyncio

class PicoEnv(gym.Env):
    render_modes = ["terminal", "human"]
    def __init__(self, controls: PicoControls=PicoControls(PicoControls.ALL_CONFIG), rewardComponent: RewardComponent=RewardComponent(), 
        outputClass=PicoOutput, render_mode=None) -> None:
        
        # Setup PICO-8 environment
        SocketServer.ensure_instance()
        PicoEnvPool.get_instance().add(self)

        # Communication with PICO-8
        self.connection = None
        self.isInitialized = False
        self.initializedEvent = threading.Event()
        self.picoMessageEvent = threading.Event()

        self.stepNum = 0
        self.render_mode = render_mode
        self.debug = False

        # Spaces and components
        self.outputClass = outputClass
        self.rewardComponent = rewardComponent
        self.controls = controls
        self.action_space = controls.action_space
        self.observation_space = spaces.Box(low=0, high=255, shape=(128,128,3), dtype=np.uint8)

        # Rendering
        self.lastScreen = None

    def connect(self, socket):
        print(f'Connected env to {socket.environ["REMOTE_PORT"]}')
        self.connection = socket

    def initialize(self):
        print('PicoEnv initialized')
        self.isInitialized = True
        self.initializedEvent.set()

    def receive(self, output: dict):
        if self.isInitialized:
            self.picoOutput = self.outputClass(output)
            self.picoMessageEvent.set()

    def wait_message_event(self, event):
        pOut = None
        if self.debug:
            print(f'PicoEnv waiting for {event}')
        while pOut is None or pOut.event != event:
            self.picoMessageEvent.wait()
            self.picoMessageEvent.clear()
            pOut = self.picoOutput
            if self.debug:
                print(f'Received event {pOut.event}')
        if self.debug:
            print(f'PicoEnv recieved {pOut.event}. Continuing')
        return pOut


    def step(self, action: spaces.MultiBinary):
        if not self.isInitialized:
            # raise Exception("Cannot step orphan environment")
            print("PicoEnv waiting to be initialized in step")
            self.initializedEvent.wait()
            self.initializedEvent.clear()
        controllerInput = self.controls.action_to_controls(action)
        msgObj = {
            'step': self.stepNum,
            'input': controllerInput
        }
        self.connection.send(json.dumps(msgObj))
        self.isBlocking = True
        
        pout = self.wait_message_event('step')
        # cv2.imwrite("testing.jpg", pout.observation['screen'])
        # fancy_print_image(pout.observation['screen'])
        reward = self.rewardComponent.step_reward(pout)

        self.lastScreen = pout.screen
        # img = self.rewardComponent.render(pout.screen)
        # fancy_print_image(img)
        # save_image(f"screen.jpg", pout.screen)

        if pout.terminated or pout.truncated:
            print(f'Done: reward={reward}, info={pout.info}, term={pout.terminated}, trunc={pout.truncated}, step={self.stepNum}')
        self.stepNum += 1
        return pout.get_observation(), reward, pout.terminated, pout.truncated, pout.info
    
    def reset(self, seed = None, options = {}):
        if not self.isInitialized:
            # raise Exception("Cannot step orphan environment")
            print("PicoEnv waiting to be initialized in reset")
            self.initializedEvent.wait()
            self.initializedEvent.clear()
        
        super().reset(seed=seed)
        self.rewardComponent.reset_reward(**options)
        command = {
            'type': 'reset',
            **options
        }
        msgObj = {
            'commands': [ command ]
        }
        msg = json.dumps(msgObj)
        self.connection.send(msg)
        pout = self.wait_message_event('reset')

        # img = self.rewardModel.render(pout.observation['screen'])
        # fancy_print_image(img)
        # save_image("testing.jpg", img)
        # print(f'Reset on step {self.stepNum}')
        self.stepNum = 0
        return pout.get_observation(), pout.info
    
    def render(self):
        if self.render_mode == "terminal":
            fancy_print_image(self.lastScreen)
    
    def close(self):
        self.connection = None
        SocketServer.check_active_connections()
