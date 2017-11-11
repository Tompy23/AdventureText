import adv.basic as adv


# execute()
# p - The player object
# a - The adventure object
# return - list of Response objects


class Command:
    def __init__(self, source="COMMAND", participle="Commanding"):
        self.source = "Command - " + source
        self.participle = participle

    def execute(self, p, a):
        return [adv.Response(self.source, "I do not understand")]


# Close <target>
class Close(Command):
    def __init__(self, parts):
        super().__init__("CLOSE", "Closing")
        self.target = parts[1]

    def execute(self, p, a):
        pass


# Drop <target>
class Drop(Command):
    def __init__(self, parts):
        super().__init__("DROP", "Dropping")
        self.target = parts[1]

    def execute(self, p, a):
        pass


# Equip <target> from <source>
class Equip(Command):
    def __init__(self, parts):
        super().__init__("EQUIP", "Equipping")
        self.target = parts[1]
        self.source = parts[3]

    def execute(self, p, a):
        response = [adv.Response(self.source, self.target + " not equippable")]
        targetItem = a.get_item_from_list(p.inventory, self.target)
        if targetItem is not None and targetItem.can("put"):
            p.equip(targetItem.name)
            response = [(adv.Response(self.source, self.participle + " " + self.target))]
        return response


# Inventory
class Inventory(Command):
    def __init__(self, parts):
        super().__init__("INVENTORY", "Listing inventory")

    def execute(self, p, a):
        response = []
        if len(p.inventory) > 0:
            response.append(adv.Response(self.source, self.participle))
            for i in p.inventory:
                response.append(adv.Response(self.source, a.items[i].description))
        if len(p.equipped) > 0:
            response.append(adv.Response(self.source, "Equipped"))
            for j in p.equipped:
                response.append(adv.Response(self.source, a.items[j].description))

        return response


# Move <direction>
class Move(Command):
    def __init__(self, parts):
        super().__init__("MOVE", "Moving")
        self.dir = parts[1]

    def execute(self, p, a):
        myExit = p.area.get_exit(self.dir)
        if myExit is not None:
            response = [adv.Response(self.source, self.participle + " " + adv.DIRECTION_MAP[self.dir].name)]
            response.extend(p.area.exit(p, a))
            response.extend(myExit.pass_thru(p, a))
            response.extend(myExit.area.enter(p, a))
            p.set_area(myExit.area)
        else:
            try:
                response = [adv.Response(self.source, "Can not move " + adv.DIRECTION_MAP[self.dir].name)]
            except:
                response = [adv.Response(self.source, "Unknown direction " + self.dir)]
        return response


# Open <target>
class Open(Command):
    def __init__(self, parts):
        super().__init__("OPEN", "Opening")
        self.target = parts[1]

    def execute(self, p, a):
        pass


# Quit
class Quit(Command):
    def __init__(self, parts):
        super().__init__("QUIT", "Quitting")
        pass

    def execute(self, p, a):
        a.stop()
        return [adv.Response(self.source, self.participle)]


# Search
# Search <direction>
# Search in <target>
# Search on <target>
class Search(Command):
    def __init__(self, parts):
        super().__init__("SEARCH", "Searching")
        if len(parts) == 1:
            self.type = "AREA"
        elif len(parts) == 2:
            if parts[1] in adv.DIRECTION_MAP:
                self.type = "DIRECTION"
                self.target = parts[1]
            else:
                self.type = "ON"
                self.target = parts[1]
        elif len(parts) == 3:
            if parts[1] == "IN":
                self.type = "IN"
                self.target = parts[2]
            elif parts[1] == "ON":
                self.type = "ON"
                self.target = parts[2]

    def execute(self, p, a):
        response = list([])
        if self.type == "AREA":
            for act in p.area.searchActions:
                act.perform()
            response = [adv.Response(self.source, p.area.searchDescription)]
            for i in p.area.items:
                if i.visible:
                    response.append(adv.Response(self.source, i.searchDescription))
        elif self.type == "DIRECTION":
            response = [adv.Response(self.source, p.area.dirDescription[adv.get_dir_index(self.target)])]
        elif self.type == "IN":
            pass
        elif self.type == "ON":
            t = p.area.get_item(self.target)
            if t is None:
                for a in p.equppied:
                    if a.name == self.target:
                        t = a
            if t is not None:
                response.append(adv.Response(t.name, t.searchDescription))
                for x in t.searchActions:
                    response.append(x)
        return response


# Store <target> in <source>
class Store(Command):
    def __init__(self, parts):
        super().__init__("STORE", "Storing")
        self.target = parts[1]
        self.source = parts[3]

    def execute(self, p, a):
        response = [adv.Response(self.source, self.target + " not storable")]
        targetItem = a.get_item_from_list(p.equipped, self.target)
        if targetItem is not None and targetItem.can("put"):
            p.store(targetItem.name)
            response = [(adv.Response(self.source, self.participle + " " + self.target))]
        return response


# Take <target> (it is now equipped)
class Take(Command):
    def __init__(self, parts):
        super().__init__("TAKE", "Taking")
        self.target = parts[1]

    def execute(self, p, a):
        # Validate
        targetItem = a.get_item_from_list(p.area.items, self.target)

        # Perform
        pass


# Use <source> on <target>
class Use(Command):
    def __init__(self, parts):
        super().__init__("USE", "Using")
        if len(parts) == 4 and parts[2] == "ON":
            self.source = parts[1]
            self.target = parts[3]

    def execute(self, p, a):
        # Validate
        sourceItem = a.get_item_from_list(p.equipped, self.source)
        targetItem = a.get_item_from_list(p.area.items, self.target)
        if targetItem is None:
            targetItem = a.get_item_from_list(p.inventory, self.source)
            if targetItem is None:
                targetItem = a.get_item_from_list(p.equipped, self.source)

        # Perform
        response = []
        if targetItem is None or sourceItem is None:
            response.append(adv.Response(self.source, "Cannot use " + self.source + " on " + self.target))
        else:
            if not targetItem.visible:
                response.append(adv.Response(self.source, "I do not see " + self.target))
            else:
                response.append(adv.Response(self.source, self.participle + " " + self.source))
                for action in sourceItem.useActions:
                    response.extend(action.perform(targetItem))
        return response


class Factory:
    def __init__(self):
        self.commands = {
            "CLOSE": Close,
            "DROP": Drop,
            "EQUIP": Equip,
            "INVENTORY": Inventory,
            "INV": Inventory,
            "I": Inventory,
            "MOVE": Move,
            "M": Move,
            "OPEN": Open,
            "QUIT": Quit,
            "SEARCH": Search,
            "S": Search,
            "STORE": Store,
            "TAKE": Take,
            "T": Take,
            "USE": Use
        }

    def create_command(self, parts):
        parts = [p.upper() for p in parts]
        if parts[0] in self.commands:
            return self.commands[parts[0]](parts)
        else:
            return None


class Parser:
    def __init__(self):
        self.cursor = ">>>>> "

    def get_command(self):
        text = input(self.cursor)
        return text
