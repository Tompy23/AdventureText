class Response:
    def __init__(self, source, text):
        self.source = source
        self.text = text


class Player:
    def __init__(self, name):
        self.name = name
        self.area = None

    def set_area(self, area):
        self.area = area


class Direction:
    def __init__(self, name):
        self.name = name


DIRECTION_NORTH = Direction("North")
DIRECTION_SOUTH = Direction("South")
DIRECTION_EAST = Direction("East")
DIRECTION_WEST = Direction("West")
DIRECTION_UP = Direction("Up")
DIRECTION_DOWN = Direction("Down")

DIRECTION = [DIRECTION_NORTH, DIRECTION_EAST, DIRECTION_SOUTH, DIRECTION_WEST, DIRECTION_UP, DIRECTION_DOWN]
DIRECTION_MAP = {
    "NORTH": DIRECTION_NORTH,
    "SOUTH": DIRECTION_SOUTH,
    "EAST": DIRECTION_EAST,
    "WEST": DIRECTION_WEST,
    "UP": DIRECTION_UP,
    "DOWN": DIRECTION_DOWN}


def get_direction(d):
    return DIRECTION_MAP[d.upper()]


def get_dir_index(d):
    di = get_direction(d)
    return DIRECTION.index(di)


def get_opposite_direction(d):
    i = DIRECTION.index(d)
    if i < 4:
        i += 2
        if i > 3:
            i -= 4
    else:
        i = 4 if (i == 5) else 5
    return DIRECTION[i]