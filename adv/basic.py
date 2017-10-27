class Player:
    def __init__(self, name):
        self.name = name
        self.area = None
        self.inventory = list([])
        self.equipped = list([])

    def set_area(self, area):
        self.area = area

    def add_inventory(self, item):
        self.inventory.append(item)

    def equip(self, item):
        if len(self.equipped) <= 2 and self.inventory.__contains__(item):
            self.inventory.remove(item)
            self.equipped.append(item)

    def store(self, item):
        if self.equipped.__contains__(item):
            self.equipped.remove(item)
            self.inventory.append(item)


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


def is_direction(d):
    return DIRECTION.__contains__(d)


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