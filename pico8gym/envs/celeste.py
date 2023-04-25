import gymnasium as gym
from pico8gym.envs import PicoEnv
from pico8gym.components.waypoint_reward import WaypointReward

class CelesteEnv(PicoEnv):
    def __init__(self) -> None:
        waypointReward = WaypointReward('player', [
            [
                (65,80),
                (105,65),
                (35,40),
                (60,25),
                (95,25),
                (112,10),
            ],
            [
                (30,48),
                (73,45),
                (104,72),
                (113,40),
                (110,7),
            ],
            [
                (60,81),
                (88,81),
                (114,57),
                (54,30),
                (75,6),
            ],
            [
                (40,100),
                (105,95),
                (120,80),
                (95,65),
                (105,40),
                (70,20),
                (55,10),
            ],
            [
                (48,42),
                (91,95),
                (103,55),
                (74,19),
                (46,19),
            ],
            [
                (53,96),
                (76,68),
                (104,39),
                (104,11),
            ],
            [
                (38,54),
                (57,30),
                (60,7),
            ],
            [
                (64,103),
                (99,102),
                (68,43),
                (15,14),
            ],
        ], 8, 10)
        controllerInput = PicoControls(PicoControls.ALL_CONFIG)
        super().__init__(
            controls=controllerInput,
            rewardComponent=waypointReward,
            render_mode=None, 
        )

    def reset(self, seed = None, options = {}):
        self.room = np.random.randint(8)
        options = {
            'room': self.room,
            **options,
        }
        super().reset(seed, options)
