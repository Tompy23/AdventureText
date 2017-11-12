import adv.action as act
import adv.area as area
import adv.adventure as adv
import adv.main as main


# There are really only 3 things, areas, items and the player.  Exits are used to connect rooms and create
#   space in between rooms for transitions, traps, tricks, etc.
class AdventureTest(adv.Adventure):
    def __init__(self, p):
        super().__init__()

        self.items = {
            "chest01": adv.Item("chest01", "Chest", "A wooden chest", lock=True, open=False, put=True),
            "key01": adv.Item("key01", "Key", "A brass key", visible=False, take=True, targets=["chest01"], equip=True),
            "weapon01": adv.Item("weapon01", "Sword", "A sharp sword", take=True, equip=True),
            "bp01": adv.Item("bp01", "Backpack", "A small backpack", open=False, take=True, put=True)
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

        p.area = self.areas["room1"]
        p.inventory.append(self.items["bp01"])

        self.areas["room1"].searchActions.append(act.ItemVisible(self.items["key01"]))

        self.items["chest01"].items.append(self.items["weapon01"])

        self.items["key01"].useActions.append(act.ToggleLock(self.items["chest01"]))


if __name__ == "__main__":
    main.main(AdventureTest)
