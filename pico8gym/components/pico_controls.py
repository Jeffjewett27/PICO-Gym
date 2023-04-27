import functools

import gymnasium.spaces as spaces

class PicoControls:
    NONE = 0x00
    LEFT = 0x01
    RIGHT = 0x02
    UP = 0x04
    DOWN = 0x08
    BTN_O = 0x10
    BTN_X = 0x20
    MENU = 0x40

    ALL_CONFIG = [LEFT, RIGHT, UP, DOWN, BTN_O, BTN_X]
    DIR_CONFIG = [LEFT, RIGHT, UP, DOWN]
    ALL_WITH_MENU_CONFIG = [LEFT, RIGHT, UP, DOWN, BTN_O, BTN_X, MENU]

    def __init__(self, buttonList: list, isDiscrete=False):
        self.buttonList = buttonList
        self.isDiscrete = isDiscrete
        self.action_space = spaces.Discrete(len(buttonList)) \
            if isDiscrete else spaces.MultiBinary(len(buttonList))

    def action_to_controls(self, action):
        if self.isDiscrete:
            return self.buttonList[action]
        buttonVals = [v*a for v, a in zip(self.buttonList, action)]
        return int(functools.reduce(lambda a, b: a | b, buttonVals))