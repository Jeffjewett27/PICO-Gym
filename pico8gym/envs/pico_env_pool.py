from __future__ import annotations
import pico8gym.envs.pico_env as pico_env

class PicoEnvPool:
    instance = None

    @staticmethod
    def get_instance():
        if (PicoEnvPool.instance is None):
            PicoEnvPool.instance = PicoEnvPool()
        return PicoEnvPool.instance
    
    def __init__(self):
        self.envs = []

    def __getitem__(self, indices):
        return self.envs[indices]
    
    def add(self, env: pico_env.PicoEnv):
        self.envs.append(env)

    def get_orphan_env(self):
        for env in self.envs:
            if env.connection is None:
                return env
        env = pico_env.PicoEnv()
        self.add(env)
        return env