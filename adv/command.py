import adv.basic as adv
import adv.response as resp


class Command:
    def __init__(self, source="COMMAND", participle="Commanding"):
        self.source = source
        self.participle = participle

    def execute(self, p, a):
        return [resp.Response(self.source, "I do not understand")]


class CommandClose(Command):
    def __init__(self, parts):
        super().__init__("CLOSE", "Closing")
        self.target = parts[1]

    def execute(self, p, a):
        response = [resp.Response(self.source, "Not closable")]
        for i in p.area.items:
            if i.description == self.target and self.taget.closable:
                i.open = False
                for j in i.items:
                    j.visible = False
                    response = [resp.Response(self.source, self.participle + " " + j.description)]
        return response

class CommandEquip(Command):
    def __init__(self, parts):
        super().__init__("EQUIP", "Equipping")
        self.target = parts[1]

    def execute(self, p, a):
        response = [resp.Response(self.source, self.target + " not equippable")]
        for i in p.inventory:
            if i.description == self.target:
                p.equip(i)
                response = [(resp.Response(self.source, self.participle + " " + i.description))]
        return response


class CommandInventory(Command):
    def __init__(self, parts):
        super().__init__("INVENTORY", "Listing inventory")

    def execute(self, p, a):
        response = list([])
        if len(p.inventory) > 0:
            response.append(resp.Response(self.source, self.participle))
            for i in p.inventory:
                response.append(resp.Response(self.source, i.description))
        if len(p.equipped) > 0:
            response.append(resp.Response(self.source), "Equipped")
            for j in p.equipped:
                response.append(resp.Response(self.source, j.description))

        return response


class CommandMove(Command):
    def __init__(self, parts):
        super().__init__("MOVE", "Moving")
        self.dir = parts[1]

    def execute(self, p, a):
        myExit = p.area.get_exit(self.dir)
        if myExit is not None:
            response = [resp.Response(self.source, self.participle + " " + adv.DIRECTION_MAP[self.dir].name)]
            response.extend(p.area.exit(p, a))
            response.extend(myExit.pass_thru(p, a))
            response.extend(myExit.area.enter(p, a))
            p.set_area(myExit.area)
        else:
            try:
                response = [resp.Response(self.source, "Can not move " + adv.DIRECTION_MAP[self.dir].name)]
            except:
                response = [resp.Response(self.source, "Unknown direction " + self.dir)]
        return response


class CommandOpen(Command):
    def __init__(self, parts):
        super().__init__("OPEN", "Opening")
        self.target = parts[1]

    def execute(self, p, a):
        for i in p.area.items:
            if i.description == self.target and self.taget.closable:
                i.open = True
                for j in i.items:
                    j.visible = True


class CommandQuit(Command):
    def __init__(self, parts):
        super().__init__("QUIT", "Quitting")
        pass

    def execute(self, p, a):
        a.stop()
        return [resp.Response(self.source, self.participle)]


class CommandSearch(Command):
    def __init__(self, parts):
        super().__init__("SEARCH", "Searching")
        if len(parts) == 1:
            self.type = "AREA"
        elif len(parts) == 2:
            if adv.DIRECTION_MAP.__contains__(parts[1]):
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
            response = [resp.Response(self.source, p.area.searchDescription)]
            for i in p.area.items:
                if i.visible:
                    response.append(resp.Response(self.source, i.searchDescription))
        elif self.type == "DIRECTION":
            response = [resp.Response(self.source, p.area.dirDescription[adv.get_dir_index(self.target)])]
        elif self.type == "IN":
            pass
        elif self.type == "ON":
            pass
        return response


class CommandTake(Command):
    def __init__(self, parts):
        super().__init__("TAKE", "Taking")
        self.target = parts[1]

    def execute(self, p, a):
        item = p.area.get_item(self.target)
        if item is None:
            for i in p.area.items:
                if i.description == self.target:
                    item = i
        if item is not None and item.visible and item.inv:
            p.add_inventory(item)

        return [resp.Response(self.source, self.participle + " " + item.description)]


class CommandUse(Command):
    def __init__(self, parts):
        super().__init__("USE", "Using")
        if len(parts) == 4 and parts[2] == "ON":
            self.source = parts[1]
            self.target = parts[3]

    def execute(self, p, a):
        for i in p.equipped:
            for j in i.useActions:
                j.perform(p)


class CommandFactory:
    def __init__(self):
        self.commands = {
            "CLOSE": CommandClose,
            "EQUIP": CommandEquip,
            "INV": CommandInventory,
            "I": CommandInventory,
            "MOVE": CommandMove,
            "M": CommandMove,
            "OPEN": CommandOpen,
            "QUIT": CommandQuit,
            "SEARCH": CommandSearch,
            "S": CommandSearch,
            "TAKE": CommandTake,
            "T": CommandTake,
            "USE": CommandUse
            }

    def create_command(self, parts):
        parts = [p.upper() for p in parts]
        if parts[0] in self.commands:
            return self.commands[parts[0]](parts)
        else:
            return None


class CommandParser:
    def __init__(self):
        self.cursor = ">>>>> "

    def get_command(self):
        text = input(self.cursor)
        return text
