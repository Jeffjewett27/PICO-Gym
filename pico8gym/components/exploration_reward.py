from pico8gym.components.pico_output import PicoOutput
from .reward_component import RewardComponent
import numpy as np
import cv2

class ExplorationReward(RewardComponent):
    def __init__(self):
        self.gridSize = 8
        self.verticalFactor = 4
        self.loopbackPenalty = 0.2 # fraction remaining after looping
        self.gridDecay = 0.6 # fraction recovered for continuing
        self.cumReward = 0
        self.reset_reward()

    def verticalReward(self, idx):
        row = idx // self.gridSize
        rowFrac = 1 - row / self.gridSize
        return rowFrac * self.verticalFactor + self.loopbackPenalty

    def step_reward(self, output: PicoOutput):
        reward = 0
        tag = output.info.get('tag', '')
        if tag == 'goal':
            reward += self.verticalFactor * max(80 - self.dist, 10)
        elif tag == 'died':
            reward -= self.verticalFactor * 3
        posStr = output.info.get('player', None)
        if posStr is None:
            return 0
        x, y = [float(v) for v in posStr.split(',')]
        sx, sy = max(0,min((x * self.gridSize) // 128, self.gridSize-1)), max(min((y * self.gridSize) // 128, self.gridSize-1),0)
        curIdx = int(sx + sy * self.gridSize)
        if curIdx > len(self.path) or curIdx == self.prevIdx:
            return 0
        if self.prevIdx is None:
            self.prevIdx = curIdx
            self.cumReward += reward
            self.startIdx = curIdx
            return reward
        if self.path[curIdx] != curIdx or curIdx == self.startIdx:
            self.loopCounts[curIdx] += 1
            if self.loopCounts[curIdx] > 2:
                print('Looped too many times')
                output.terminated = True
            # visited before. Erase path and penalize
            idx = self.prevIdx
            while idx != curIdx:
                if self.path[idx] == idx:
                    print("WARNING bad path")
                    print(self.path)
                    print(idx)
                    print(curIdx)
                    print(self.prevIdx)
                    break
                oldColl = self.collRewards[idx]
                self.collRewards[idx] *= self.loopbackPenalty
                diff = oldColl - self.collRewards[idx]
                reward -= diff
                self.path[idx], idx = idx, self.path[idx]
        elif self.path[curIdx] != self.startIdx:
            # point back to maintain path
            self.path[curIdx] = self.prevIdx
            self.collRewards[curIdx] = self.gridRewards[curIdx]
            reward += self.gridRewards[curIdx]
            self.gridRewards[curIdx] *= self.gridDecay
            
        self.cumReward += reward
        self.dist += 1
        self.prevIdx = curIdx
        return reward                

    def reset_reward(self, **kwargs):
        # if self.cumReward != 0:
        #     print(f'CUMULATIVE: {self.cumReward}, DIST: {self.dist}, FRAC: {self.cumReward / self.dist}, SCORE: {self.cumReward * (1+self.cumReward/self.dist)}')
        self.path = [i for i in range(self.gridSize**2)]
        self.gridRewards = [self.verticalReward(i) for i in range(self.gridSize**2)]
        self.collRewards = [0 for _ in range(self.gridSize**2)]
        self.loopCounts = [0 for _ in range(self.gridSize**2)]
        self.prevIdx = None
        self.cumReward = 0
        self.dist = 0

    def render(self, img: np.ndarray):
        grid = np.array(self.collRewards).reshape((self.gridSize, self.gridSize))
        grid = cv2.resize(grid * (255 / self.verticalFactor), img.shape[:2], interpolation=cv2.INTER_AREA)
        grid = cv2.merge((np.zeros_like(grid), grid, np.zeros_like(grid)))
        return np.uint8(img + grid)
