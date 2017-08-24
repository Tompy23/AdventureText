class Command:
    def __init__(self):
        pass

    def execute(self, p, a):
        print("I do not understand.")


class CommandMove(Command):
    def __init__(self, parts):
        self.dir = parts[1].upper()

    def execute(self, p, a):
        myExit = p.area.get_exit(self.dir)
        response = [Response("MOVE", "Moving " + DIRECTION_MAP[self.dir].name)]
        response.extend(myExit.pass_thru())
        p.set_area(myExit.area)
        return response


class CommandSearch(Command):
    def __init__(self):
        pass

    def execute(self, p, a):
        print("Searching")


class CommandFactory:
    def __init__(self):
        self.commands = dict([("MOVE", CommandMove), ("SEARCH", CommandSearch)]);

    def create_command(self, parts):
        return self.commands[parts[0].upper()](parts)


class Area:
    def __init__(self,
            id,
            description = "",
            searchDescription = "Nothing to see",
            dirDescription=["", "", "", "", "", ""]):
        self.id = id
        self.description = description
        while (len(dirDescription) < 6):
            dirDescription.append("");
        self.dirDescription = dirDescription
        self.exits = {}

    def get_dir_description(self, dir):
        return self.dirDescription[DIRECTION.index(dir)]

    def get_exit(self, dir):
        return self.exits[dir.upper()]

    def install_exit(self, exit):
        self.exits[exit.direction.name.upper()] = exit


class Exit:
    def __init__(self, direction, area, description = ""):
        self.direction = direction
        self.area = area
        self.description = description

    def match_exit(self, exit):
        self.opposite = exit;

    def pass_thru(self):
        response = [(Response("[Exit|" + self.area.id + "]", self.description))]
        return response


class Response:
    def __init__(self, source, text):
        self.source = source
        self.text = text


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

def get_opposite_direction(dir):
    index = DIRECTION.index(dir)
    if (index < 4):
        index += 2
        if (index > 3):
            index -=4
    else:
        index = 4 if (index == 5) else 5
    return DIRECTION[index]


class Player:
    def __init__(self, name):
        self.name = name

    def set_area(self, area):
        self.area = area


class CommandParser:
    def __init__(self):
        self.cursor = ">>>>> "

    def get_command(self):
        text = input(self.cursor)
        return text


# Startup functions

def get_player():
    name = input("What is your name? ")
    return Player(name)

def start(player, adventure):
    parser = CommandParser()
    factory = CommandFactory()
    while (adventure.proceed):
        input = parser.get_command()
        myCommand = factory.create_command(input.split())
        responses = myCommand.execute(player, adventure)
        for r in responses:
            print("[" + r.source + "] " + r.text)


# Below here is what goes into the unique adventure file
# Remember to add "adv" package identifier to Room, Exit, Area, Direction
# and get_player

class Adventure:
    def __init__(self, p):
        self.proceed = True
        self.areas = {
        "room1": Area("room1", "Nice room", "Really nice room"),
        "room2": Area("room2", "A bedroom", "Bed on the west wall and a desk on the north wall")
        }

        self.exits = {
            "exit12": Exit(DIRECTION_NORTH, self.areas["room2"])
            }

        self.areas["room1"].install_exit(self.exits["exit12"])

        p.set_area(self.areas["room1"])

def main():
    p = get_player()
    start(p, Adventure(p))

if __name__ == "__main__":
    main()