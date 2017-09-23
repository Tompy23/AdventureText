import adv.basic as adv


class Area:
    def __init__(self,
            name,
            description = "",
            searchDescription = "Nothing to see",
            dirDescription = ["", "", "", "", "", ""]):
        self.name = name
        self.description = description
        self.searchDescription = searchDescription
        while len(dirDescription) < 6:
            dirDescription.append("");
        self.dirDescription = dirDescription
        self.exits = {}

    def get_dir_description(self, dir):
        return self.dirDescription[adv.DIRECTION.index(dir)]

    def get_exit(self, dir):
        if not dir.upper() in self.exits:
            return None
        else:
            return self.exits[dir.upper()]

    def install_exit(self, exit):
        self.exits[exit.direction.name.upper()] = exit

    def exit(self, a):
        return [adv.Response(self.name, "Leaving")]

    def enter(self, a):
        return [adv.Response(self.name, "Entering"), adv.Response(self.name, self.description)]


class Exit:
    def __init__(self, direction, area, description = ""):
        self.direction = direction
        self.area = area
        self.description = description
        self.opposite = None

    def match_exit(self, exit):
        self.opposite = exit;

    def pass_thru(self):
        response = [(adv.Response("Exit-" + self.area.name, self.description))]
        return response