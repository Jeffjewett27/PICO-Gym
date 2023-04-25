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

    def step_reward(self, output: PicoOutput):
        posStr = output.info.get(self.infoKey, None)
        if posStr is None:
            return output.reward
        roompoints = self.waypoints[self.room]
        x, y = [float(v) for v in posStr.split(',')]
        for i in range(self.idx, len(roompoints)):
            tx, ty = roompoints[i]
            if (x - tx)**2 + (y - ty)**2 < self.radiusSqr:
                diff = i - self.idx + 1
                self.idx = i + 1
                return output.reward + diff * self.waypointReward
        return output.reward
    
    def reset_reward(self, **kwargs):
        self.idx = 0
        self.room = kwargs.get('room', 0)

    def render(self, img: np.array):
        roompoints = self.waypoints[self.room]
        for i in range(self.idx, len(roompoints)):
            tx, ty = roompoints[i]
            cv2.drawMarker(img, (tx, ty), (12, 255, 0), cv2.MARKER_DIAMOND, markerSize=15)
        return img

