import adv.basic as adv
import adv.area as area


class Adventure:
    def __init__(self, p):
        self.proceed = True
        self.areas = {
            "room1": area.Area("room1", "Nice room", "Really nice room", ["Looks like a door", "wall", "void", "wall"]),
            "room2": area.Area("room2", "A bedroom", "Bed on the west wall and a desk on the north wall")
        }

        self.exits = {
                "exit12": area.Exit(adv.DIRECTION_NORTH, self.areas["room2"]),
                "exit21": area.Exit(adv.DIRECTION_SOUTH, self.areas["room1"])
            }

        self.areas["room1"].install_exit(self.exits["exit12"])
        self.areas["room2"].install_exit(self.exits["exit21"])

        p.set_area(self.areas["room1"])

    def stop(self):
        self.proceed = False


def main():
    p = adv.get_player()
    adv.start(p, Adventure(p))

if __name__ == "__main__":
    main()