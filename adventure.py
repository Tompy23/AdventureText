import adv.basic as adv
import adv.area as area
import adv.start as start
import adv.thing as thing
import adv.action as act


class Adventure:
    def __init__(self, p):
        self.proceed = True

        self.items = {
            "chest01": thing.Chest("chest01", "Chest", "A wooden chest", locked=True),
            "key01": thing.Key("key01", "Key", "A brass key", visible=False),
            "weapon01": thing.Weapon("weapon01", "Sword", "A sharp sword")
            }

        self.areas = {
            "room1": area.Area("room1", "Nice room", "Really nice room", ["Looks like a door", "wall", "void", "wall"],
                               items=[self.items["key01"]]),
            "room2": area.Area("room2", "A bedroom", "Bed on the west wall and a desk on the north wall",
                               items=[self.items["chest01"]])
            }

        self.exits = {
            "exit12": area.Exit(adv.DIRECTION_NORTH, self.areas["room2"]),
            "exit21": area.Exit(adv.DIRECTION_SOUTH, self.areas["room1"])
            }

        self.areas["room1"].install_exit(self.exits["exit12"])
        self.areas["room2"].install_exit(self.exits["exit21"])

        p.set_area(self.areas["room1"])

        self.areas["room1"].searchActions.append(act.ActionMakeItemVisible(self.items["key01"]))

        self.items["chest01"].items.append(self.items["weapon01"])

        self.items["key01"].useActions.append(act.UseOnItemTrigger(act.ToggleLockChestAction(self.items["chest01"]), self.items["chest01"]))

    def stop(self):
        self.proceed = False


def main():
    p = start.get_player()
    start.start(p, Adventure(p))


if __name__ == "__main__":
    main()