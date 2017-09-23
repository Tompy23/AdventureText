import adv.basic as adv


class Command:
    def __init__(self):
        pass

    def execute(self, p, a):
        print("I do not understand.")


class CommandMove(Command):
    def __init__(self, parts):
        self.dir = parts[1].upper()
        self.source = "MOVE"
        self.participle = "Moving"

    def execute(self, p, a):
        myExit = p.area.get_exit(self.dir)
        if myExit is not None:
            response = [adv.Response(self.source, self.participle + " " + adv.DIRECTION_MAP[self.dir].name)]
            response.extend(p.area.exit(a))
            response.extend(myExit.pass_thru())
            response.extend(myExit.area.enter(a))
            p.set_area(myExit.area)
        else:
            response = [adv.Response(self.source, "Can not move " + adv.DIRECTION_MAP[self.dir].name)]
        return response


class CommandQuit(Command):
    def __init__(self, parts):
        pass

    def execute(self, p, a):
        a.stop()
        return [adv.Response("QUIT", "Quitting")]


class CommandSearch(Command):
    def __init__(self, parts):
        if len(parts) == 1:
            self.type = "AREA"
        elif len(parts) == 2:
            self.type = "DIRECTION"
            self.target = parts[1].upper()

    def execute(self, p, a):
        if self.type == "AREA":
            response = [adv.Response("SEARCH", p.area.searchDescription)]
        elif self.type == "DIRECTION":
            if not self.target in adv.DIRECTION_MAP:
                response = [adv.Response("SEARCH", "Not a direction")]
            else:
                response = [adv.Response("SEARCH", p.area.dirDescription[adv.get_dir_index(self.target)])]
        return response


class CommandFactory:
    def __init__(self):
        self.commands = dict([
            ("MOVE", CommandMove),
            ("QUIT", CommandQuit),
            ("SEARCH", CommandSearch)]);

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
