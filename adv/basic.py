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
DIRECTION_MAP = dict([
    ("NORTH", DIRECTION_NORTH),
    ("SOUTH", DIRECTION_SOUTH),
    ("EAST", DIRECTION_EAST),
    ("WEST", DIRECTION_WEST),
    ("UP", DIRECTION_UP),
    ("DOWN", DIRECTION_DOWN)
    ])


def get_direction(dir):
    return DIRECTION_MAP[dir.upper()]


def get_dir_index(dir):
    d = get_direction(dir)
    return DIRECTION.index(d)


def get_opposite_direction(dir):
    index = DIRECTION.index(dir)
    if index < 4:
        index += 2
        if index > 3:
            index -=4
    else:
        index = 4 if (index == 5) else 5
    return DIRECTION[index]