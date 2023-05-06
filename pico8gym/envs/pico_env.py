import json
import threading
import cv2

import numpy as np
from pico8gym.envs.pico_env_pool import PicoEnvPool
from pico8gym.components.reward_component import RewardComponent
from pico8gym.server.process_management import ProcessManagement
from pico8gym.util.img_util import draw_controls, fancy_print_image, save_image
from pico8gym.server.eventlet import SocketServer
from pico8gym.components.pico_output import PicoOutput
from pico8gym.components.pico_controls import PicoControls
import gymnasium as gym
import gymnasium.spaces as spaces
from gymnasium.error import DependencyNotInstalled
import subprocess
import atexit
# import asyncio

class PicoEnv(gym.Env):
    totalSteps = 0
    metadata = {
        "render_modes": ["human", "rgb_array"],
        "render_fps": 30,
    }
    def __init__(self, cart, controls: PicoControls=PicoControls(PicoControls.ALL_CONFIG), rewardComponent: RewardComponent=RewardComponent(), 
        outputClass=PicoOutput, infoLoggingDefaults={}, max_episode_steps = None, resolution = (128, 128), frameskip = 0, render_mode=None) -> None:
        
        self.cart = cart

        # Setup PICO-8 environment
        SocketServer.ensure_instance()
        PicoEnvPool.get_instance().add(self)
        ProcessManagement.get_instance().spawn_process(cart)

        # Communication with PICO-8
        self.connection = None
        self.isInitialized = False
        self.initializedEvent = threading.Event()
        self.picoMessageEvent = threading.Event()

        self.stepNum = 0
        self.render_mode = render_mode
        self.max_episode_steps = max_episode_steps
        self.frameskip = frameskip
        self.debug = False

        # Spaces and components
        self.resolution = resolution
        self.outputClass = outputClass
        self.infoLoggingDefaults = infoLoggingDefaults
        self.rewardComponent = rewardComponent
        self.controls = controls
        self.action_space = controls.action_space
        self.observation_space = spaces.Box(low=0, high=255, shape=(*resolution,3), dtype=np.uint8)
        print('PICO_ENV OBS SHAPE', self.observation_space.shape)    

        # Rendering
        self.lastScreen = None
        self.lastControls = 0
        self.screen_width = 600
        self.screen_height = 600
        self.screen = None
        self.clock = None

    def connect(self, socket):
        print(f'Connected env to {socket.environ["REMOTE_PORT"]}')
        self.connection = socket

    def initialize(self):
        print('PicoEnv initialized')
        self.isInitialized = True
        self.initializedEvent.set()

    def receive(self, output: dict):
        if self.isInitialized:
            self.picoOutput = self.outputClass(output, self.infoLoggingDefaults)
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

    def step_async(self, action: spaces.MultiBinary):
        self.lastAction = action
        self.lastControls = self.controls.action_to_controls(action)
        msgObj = {
            'step': self.stepNum,
            'input': self.lastControls,
            'skipframes': self.frameskip,
        }
        self.connection.send(json.dumps(msgObj))

    def step_wait(self):
        pout = self.wait_message_event('step')
        # cv2.imwrite("testing.jpg", pout.observation['screen'])
        # fancy_print_image(pout.observation['screen'])
        reward = self.rewardComponent.step_reward(pout)

        self.lastScreen = pout.screen
        # img = self.rewardComponent.render(pout.screen)
        # fancy_print_image(img)
        # save_image(f"screen.jpg", pout.get_observation(self.observation_space))
        # if pout.terminated or pout.truncated:
        #     print(f'Done: reward={reward}, info={pout.info}, term={pout.terminated}, trunc={pout.truncated}, step={self.stepNum}')
        self.stepNum += 1
        PicoEnv.totalSteps += 1
        truncated = bool(self.max_episode_steps) and self.stepNum >= self.max_episode_steps
        return pout.get_observation(self.observation_space), reward, pout.terminated, pout.truncated or truncated, pout.info

    def step(self, action: spaces.MultiBinary):
        if not self.isInitialized:
            # raise Exception("Cannot step orphan environment")
            print("PicoEnv waiting to be initialized in step")
            self.initializedEvent.wait()
            self.initializedEvent.clear()
        self.step_async(action)
        
        return self.step_wait()

    def reset_async(self, seed = None, options = {}):
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

    def reset_wait(self):
        pout = self.wait_message_event('reset')
        # img = self.rewardModel.render(pout.observation['screen'])
        # fancy_print_image(img)
        # save_image("testing.jpg", img)
        # print(f'Reset on step {self.stepNum}')
        self.stepNum = 0
        return pout.get_observation(self.observation_space), pout.info
    
    def reset(self, seed = None, options = {}):
        self.reset_async(seed, options)

        return self.reset_wait()
    
    def render(self):
        if self.render_mode is None:
            assert self.spec is not None
            gym.logger.warn(
                "You are calling render method without specifying any render mode. "
                "You can specify the render_mode at initialization, "
                f'e.g. gym.make("{self.spec.id}", render_mode="rgb_array")'
            )
            return

        try:
            import pygame
        except ImportError as e:
            raise DependencyNotInstalled(
                "pygame is not installed, run `pip install gymnasium[classic-control]`"
            ) from e

        if self.screen is None:
            pygame.init()
            if self.render_mode == "human":
                pygame.display.init()
                self.screen = pygame.display.set_mode(
                    (self.screen_width, self.screen_height)
                )
            else:  # mode == "rgb_array"
                self.screen = pygame.Surface((self.screen_width, self.screen_height))
        if self.clock is None:
            self.clock = pygame.time.Clock()

        if self.lastScreen is not None:
            npimg = self.lastScreen
            # npimg = self.rewardComponent.render(self.lastScreen)
            draw_controls(npimg, self.lastControls)
            # npimg = cv2.resize(npimg, (48,48), interpolation=cv2.INTER_NEAREST)
            npimg = cv2.resize(cv2.cvtColor(np.transpose(npimg, axes=(1, 0, 2)), cv2.COLOR_RGB2BGR), (self.screen_width, self.screen_width), interpolation=cv2.INTER_AREA)
            surf = pygame.surfarray.make_surface(npimg)
            self.screen.blit(surf, (0, 0))

        if self.render_mode == "human":
            pygame.event.pump()
            self.clock.tick(self.metadata["render_fps"] / (1+self.frameskip))
            pygame.display.flip()

        elif self.render_mode == "rgb_array":
            return np.transpose(
                np.array(pygame.surfarray.pixels3d(self.screen)), axes=(1, 0, 2)
            )
    
    def close(self):
        self.connection = None
        SocketServer.check_active_connections()
