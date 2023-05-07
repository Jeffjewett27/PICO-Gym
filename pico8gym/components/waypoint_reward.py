import cv2
import numpy as np
from .pico_output import PicoOutput
from .reward_component import RewardComponent

class WaypointReward(RewardComponent):
    def __init__(self, infoKey, waypoints, radius, waypointReward):
        super().__init__()
        self.infoKey = infoKey
        self.waypoints = waypoints
        self.radius = radius
        self.radiusSqr = self.radius**2
        self.idx = 0
        self.waypointReward = waypointReward
        self.allowSkips = False
        self.waypointEnergy = 45
        self.energy = self.waypointEnergy
        self.dashReward = 0.4
        self.drawMarkers = True

    def step_reward(self, output: PicoOutput):
        reward = output.reward
        output.screen = self.render(output.screen)
        tag = output.info.get('tag', '')
        if tag == 'goal':
            reward += 4 * self.waypointReward
        elif tag == 'died':
            reward -= 0.6 * self.waypointReward
        self.energy -= 1
        posStr = output.info.get(self.infoKey, None)
        djumps = int(output.info.get('dash', 0))
        if posStr is None:
            return output.reward
        roompoints = self.waypoints[self.room]
        x, y = [float(v) for v in posStr.split(',')]
        for i in range(self.idx, len(roompoints)):
            if not self.allowSkips and i > self.idx and len(roompoints[i]) < 3:
                continue
            tx = roompoints[i][0]
            ty = roompoints[i][1]
            if (x - tx)**2 + (y - ty)**2 < self.radiusSqr:
                diff = i - self.idx + 1
                self.idx = i + 1
                self.energy = self.waypointEnergy * diff
                # print('dash', djumps, 'reward', output.reward, 'diff', diff, 'wrew', self.waypointReward, 'dashrew', self.dashReward)
                # print('dash', djumps, 'reward', (1 + self.dashReward * djumps))
                return reward + diff * self.waypointReward * (1 + self.dashReward * djumps)
        if self.energy <= 0:
            output.terminated = True
        return reward
    
    def reset_reward(self, **kwargs):
        self.idx = 0
        self.room = kwargs.get('room', 0)
        self.energy = self.waypointEnergy

    def render(self, img: np.array):
        roompoints = self.waypoints[self.room]
        yellow = (0, 255, 255)
        purple = (255, 12, 255)
        for i in range(self.idx, len(roompoints)):
            tx = roompoints[i][0]
            ty = roompoints[i][1]
            milestone = len(roompoints[i]) > 2
            cv2.drawMarker(img, (tx, ty), purple if milestone else yellow, cv2.MARKER_DIAMOND, markerSize=8, thickness=3)
        return img

