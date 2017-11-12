

# Adventure
#
class Adventure:
    def __init__(self):
        self.proceed = True

    def stop(self):
        self.proceed = False

    def get_item_from_list(self, myList, myItemDesc):
        for i in myList:
            if i.description.upper() == myItemDesc.upper():
                return self.items[i]
        return None


# Item
#
# name - unique identifier
# visible - Whether or not it is added to an area description
# description - A word used to identify the thing in its context
# visible - Whether or not thing is available for other commands
# searchDescription - Text used when the thing is searched

# Dictionary of things (all are optional)
#  Many of these will exist if possible, and not if not possible.  For example, if "take" exists, it is something
#  that can be put into an inventory with the "take" command
#
# Boolean
# take - Whether or not the thing can be put into the players inventory (true only)
# open - Whether or not it can be opened and closed (true open, false closed)
# lock - whether it is locked or not (true locked, false unlocked)
# equip - Whether it can be moved from inventory to a usable place (hand, head, etc.) (true only)
# put - Whether or not other things can be added to the item
#
# String
#
# List
# target(s) - The thing(s) it can be used on
#
# Actions
# useActions - need "targets", thing can be used on targets
# searchActions - ???


class Item:
    def __init__(self, name, description, searchDescription, visible=True, **kwargs):
        self.name = name
        self.visible = visible
        self.description = description
        self.searchDescription = searchDescription
        self.items = []
        self.props = kwargs
        self.useActions = []
        self.searchActions = []

    # Functions that work on and return boolean
    def can(self, prop):
        return prop in self.props

    def check(self, prop):
        if self.can(prop):
            return self.props[prop]
        return False


# Player
#
# inventory and equipped will be Item Objects
# Area will be Area Object
class Player:
    def __init__(self, name):
        self.name = name
        self.area = None
        self.inventory = []
        self.equipped = []


# Equip and store needs to make sure there is "room" for all the things
    # Also, if this function is called, the item will be equipped if able, and only removed
    # from inventory if it started there.
    def equip(self, item):
        if len(self.equipped) <= 2:
            if item in self.inventory:
                self.inventory.remove(item)
            self.equipped.append(item)

# Storing requires a source for storing the target item, so this is incomplete
    # We'll probably just pretend the backpack is where things are stored for now.
    def store(self, item):
        if item in self.equipped:
            self.equipped.remove(item)
            self.inventory.append(item)


# Direction
#
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
    return d in DIRECTION


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


PROPOSED_TARGET_ITEM="ProposedTargetItem"



