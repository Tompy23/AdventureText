import adv

class Adventure:
    def __init__(self, p):
        self.proceed = True
        self.rooms = {
        "room1": adv.Area("room1", "Nice room", "Really nice room"),
        "room2": adv.Area("room2", "A bedroom", "Bed on the west wall and a desk on the north wall")
        }

        self.exits = {
            "exit12": adv.Exit(adv.DIRECTION_NORTH, self.rooms["room2"])
            }

        self.rooms["room1"].install_exit(self.exits["exit12"])

        p.set_room("room1")

def main():
    adv.start(Adventure(adv.get_player()))

if __name__ == "__main__":
    main()