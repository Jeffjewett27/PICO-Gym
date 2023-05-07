import os
import numpy as np
dirname = os.path.dirname(__file__)

rooms = {}

def read_room(roomId):
    filename = os.path.join(dirname, f'rooms/room{roomId}_spawn.txt')
    with open(filename) as file:
        lines = file.readlines()
        if len(lines) < 16:
            raise ValueError(f'Room spawn file must be a 16x16 grid: {filename}')
        for i in range(16):
            if len(lines[i].strip()) < 16:
                raise ValueError(f'Room spawn file must be a 16x16 grid: {filename}')
        spawning = [
            [int(v == '1') for v in line.strip()]
            for line in lines
        ]
        # print(spawning)
        # print([len(line) for line in spawning])
        return np.array(spawning).flatten()

def sample_room(roomId):
    if roomId not in rooms:
        rooms[roomId] = read_room(roomId)
    room = rooms[roomId]
    spawn_idx, = np.nonzero(room)

    point = np.random.choice(spawn_idx)
    x = (point % 16) * 8
    y = (point // 16) * 8
    return int(x), int(y)
    # return 70, 80