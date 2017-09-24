import adv.basic as adv


class Command:
    def __init__(self):
        self.source = "COMMAND"

    def execute(self, p, a):
        return [adv.Response(self.source, "I do not understand")]


class CommandMove(Command):
    def __init__(self, parts):
        super().__init__()
        self.dir = parts[1].upper()
        self.source = "MOVE"
        self.participle = "Moving"

    def execute(self, p, a):
        myExit = p.area.get_exit(self.dir)
        if myExit is not None:
            response = [adv.Response(self.source, self.participle + " " + adv.DIRECTION_MAP[self.dir].name)]
            response.extend(p.area.exit(p, a))
            response.extend(myExit.pass_thru(p, a))
            response.extend(myExit.area.enter(p, a))
            p.set_area(myExit.area)
        else:
            response = [adv.Response(self.source, "Can not move " + adv.DIRECTION_MAP[self.dir].name)]
        return response


class CommandQuit(Command):
    def __init__(self, parts):
        super().__init__()
        pass

    def execute(self, p, a):
        a.stop()
        return [adv.Response("QUIT", "Quitting")]


class CommandSearch(Command):
    def __init__(self, parts):
        super().__init__()
        if len(parts) == 1:
            self.type = "AREA"
        elif len(parts) == 2:
            self.type = "DIRECTION"
            self.target = parts[1].upper()
        elif len(parts) == 3:
            if parts[1].upper() == "IN":
                self.type = "IN"
                self.target = parts[2].upper()
            elif parts[1].upper() == "ON":
                self.type = "ON"
                self.target = parts[2].upper()

    def execute(self, p, a):
        response = []
        if self.type == "AREA":
            response = [adv.Response("SEARCH", p.area.searchDescription)]
        elif self.type == "DIRECTION":
            if self.target not in adv.DIRECTION_MAP:
                response = [adv.Response("SEARCH", "Not a direction")]
            else:
                response = [adv.Response("SEARCH", p.area.dirDescription[adv.get_dir_index(self.target)])]
        elif self.type == "IN":
            pass
        elif self.type == "ON":
            pass
        return response


class CommandTake(Command):
    def __init__(self):
        super().__init__()


class CommandUse(Command):
    def __init__(self):
        super().__init__()


class CommandFactory:
    def __init__(self):
        self.commands = {
            "MOVE": CommandMove,
            "QUIT": CommandQuit,
            "SEARCH": CommandSearch,
            "TAKE": CommandTake,
            "USE": CommandUse}

    def create_command(self, parts):
        if parts[0].upper() in self.commands:
            return self.commands[parts[0].upper()](parts)
        else:
            return None


class CommandParser:
    def __init__(self):
        self.cursor = ">>>>> "

    def get_command(self):
        text = input(self.cursor)
        return text

