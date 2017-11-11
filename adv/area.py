import adv.basic as adv
import adv.response as resp


class Area:
    def __init__(self,
                 name,
                 description="",
                 searchDescription="Nothing to see",
                 dirDescription=("", "", "", "", "", ""),
                 enterDescription="Entering",
                 exitDescription="Leaving",
                 items=[]):
        self.name = name
        self.description = description
        self.searchDescription = searchDescription
        while len(dirDescription) < 6:
            dirDescription.append("")
        self.dirDescription = dirDescription
        self.enterDescription = enterDescription
        self.exitDescription = exitDescription
        self.items = items
        self.exits = {}
        self.searchActions = []

    def get_dir_description(self, d):
        return self.dirDescription[adv.DIRECTION.index(d)]

    def get_exit(self, d):
        if not d.upper() in self.exits:
            return None
        else:
            return self.exits[d.upper()]

    def install_exit(self, e):
        self.exits[e.direction.name.upper()] = e

    def exit(self, p, a):
        return [resp.Response(self.name, self.exitDescription)]

    def enter(self, p, a):
        return [resp.Response(self.name, self.enterDescription), resp.Response(self.name, self.description)]

    def add_item(self, item):
        self.items.append(item)

    def get_item(self, itemDesc):
        for i in self.items:
            if i.description.upper() == itemDesc:
                return i
        return None


class Exit:
    def __init__(self, direction, area, description=""):
        self.direction = direction
        self.area = area
        self.description = description
        self.opposite = None

    def match_exit(self, e):
        self.opposite = e

    def pass_thru(self, p, a):
        response = [(resp.Response("Exit-" + self.area.name, self.description))]
        return response
