import adv.adventure as adv
import adv.action as action


class Command:
    """
    Base command class
    All commands are created in their constructor, assigning descriptions from the parts of the command.
    Commands are then executed, usually firing off actions at certain times which are either attached to
    the command itself or other items or other entities

    Interface
    ---------
    Constructor() - Puts the parts of the command into variables
    validate() - Validates the command by acquiring the Object Items from the descriptions
    execute() - Executes the command and all its parts from legally constructed command
    """

    def __init__(self, source="COMMAND", participle="Commanding"):
        """
        Base command constructor
        :param source: Command name
        :param participle: Word used when describing command response
        """
        self.source = "Command - " + source
        self.participle = participle

    def validate(self, p, a):
        """
        Default implementation
        :param p: Player object
        :param a: Adventure object
        :return: Boolean, List of Responses
        """
        return True, []

    def execute(self, p, a):
        """
        Default Implementation
        :param p: Player object
        :param a: Adventure object
        :return: A list of responses
        """
        return [(self.source, "I do not understand")]


class Close(Command):
    """Close <target>"""

    def __init__(self, parts):
        """
        Constructor
        :param parts:
        """
        super().__init__("CLOSE", "Closing")
        self.target = parts[1]

    def execute(self, p, a):
        """
        ITEM_PRE_CLOSE_ACTIONS
        Close an item
        ITEM_POST_CLOSE_ACTIONS
        :param p: Player object
        :param a: Adventure object
        :return: A list of responses
        """
        response = []
        targetItem = adv.get_item_from_lists((p.area.items, p.equipped), self.target)

        if targetItem is not None and targetItem.can(adv.ITEM_OPEN):
            response.extend(
                (x.perform(proposedTargetItem=targetItem) for x in targetItem.props(adv.ITEM_PRE_CLOSE_ACTIONS)) if
                targetItem.can(adv.ITEM_PRE_CLOSE_ACTIONS) else [])
            response.extend(action.Close(targetItem).perform(proposedTargetItem=targetItem))
            response.extend(
                (x.perform(proposedTargetItem=targetItem) for x in targetItem.props(adv.ITEM_POST_CLOSE_ACTIONS)) if
                targetItem.can(adv.ITEM_POST_CLOSE_ACTIONS) else [])

        return response


class Drop(Command):
    """Drop <target>"""

    def __init__(self, parts):
        """
        Constructor
        :param parts:
        """
        super().__init__("DROP", "Dropping")
        self.target = parts[1]

    def execute(self, p, a):
        """

        :param p: Player object
        :param a: Adventure object
        :return: A list of responses
        """
        response = []
        targetItem = adv.get_item_from_list(p.equipped, self.target)

        if targetItem is not None:
            response.extend(x.perform(proposedTargetItem=targetItem) for x in p.area.props(adv.AREA_PRE_DROP_ACTIONS))
            response.extend(
                (x.perform(proposedTargetItem=targetItem) for x in targetItem.props(adv.ITEM_PRE_DROP_ACTIONS)))
            response.extend(action.Drop(targetItem).perform(proposedTargetItem=targetItem, player=p))
            response.extend(
                (x.perform(proposedTargetItem=targetItem) for x in targetItem.props(adv.ITEM_PRE_DROP_ACTIONS)))
            response.extend(x.perform(proposedTargetItem=targetItem) for x in p.area.props(adv.AREA_PRE_DROP_ACTIONS))

        return response


# Equip <target> from <source>
class Equip(Command):
    def __init__(self, parts):
        """
        Constructor
        :param parts:
        """
        super().__init__("EQUIP", "Equipping")
        self.target = parts[1]

    def execute(self, p, a):
        """

        :param p: Player object
        :param a: Adventure object
        :return: A list of responses
        """
        response = [(self.source, "Not able to equip " + self.target + ".")]
        targetItem = adv.get_item_from_list(p.inventory, self.target)
        if targetItem is not None:
            p.equip(targetItem.name)
            response = [(self.source, self.participle + " " + self.target)]
        return response


# Inventory
class Inventory(Command):
    def __init__(self, parts):
        """
        Constructor
        :param parts:
        """
        super().__init__("INVENTORY", "Listing inventory")

    def execute(self, p, a):
        """

        :param p: Player object
        :param a: Adventure object
        :return: A list of responses
        """
        response = []
        if len(p.inventory) > 0:
            response.append((self.source, self.participle))
            for i in p.inventory:
                response.append((self.source, i.description))
        if len(p.equipped) > 0:
            response.append((self.source, "Equipped"))
            for j in p.equipped:
                response.append((self.source, j.description))

        return response


# Move <direction>
class Move(Command):
    def __init__(self, parts):
        """
        Constructor
        :param parts:
        """
        super().__init__("MOVE", "Moving")
        self.myDir = parts[1]
        self.myExit = None

    def validate(self, p, a):
        """
        Determine the direction of the move
        :param p: Player object
        :param a: Adventure object
        :return: Boolean, List of Responses
        """
        response = []
        self.myExit = p.area.get_exit(self.myDir)
        if self.myExit is not None:
            valid = True
        else:
            valid = False
            try:
                response.append((self.source, "Can not move " + adv.DIRECTION_MAP[self.myDir].name))
            except:
                response.append((self.source, "Unknown direction " + self.myDir))
        return valid, response

    def execute(self, p, a):
        """
        Move through an exit to another area for a certain direction
        :param p: Player object
        :param a: Adventure object
        :return: A list of responses
        """

        response = [(self.source, self.participle + " " + adv.DIRECTION_MAP[self.dir].name)]
        #response.extend(p.area.exit(p, a))
        response.extend((x.perform() for x in p.area.enterActions))
        #response.extend(self.myExit.pass_thru(p, a))
        response.extend((x.perform() for x in self.myExit.exitActions))
        #response.extend(self.myExit.area.enter(p, a))
        response.extend((x.perform() for x in p.area.exitActions))
        p.area = self.myExit.area
        return response


# Open <target>
class Open(Command):
    def __init__(self, parts):
        """
        Constructor
        :param parts:
        """
        super().__init__("OPEN", "Opening")
        self.target = parts[1]

    def execute(self, p, a):
        """

        :param p: Player object
        :param a: Adventure object
        :return: A list of responses
        """
        response = []
        targetItem = adv.get_item_from_list(p.area.items, self.target)
        if targetItem is not None and targetItem.can(adv.ITEM_OPEN) and not targetItem.check(adv.ITEM_OPEN):
            if targetItem.can(adv.ITEM_LOCK):
                if not targetItem.check(adv.ITEM_LOCK):
                    targetItem.props[adv.ITEM_OPEN] = True
                    response.append((self.source, self.target + " is now open"))
                else:
                    response.append((self.source, self.target + " is locked and cannot be opened"))
            else:
                targetItem.props[adv.ITEM_OPEN] = True
                response.append((self.source, self.target + " is now open"))
        else:
            response.append((self.source, "Cannot open " + self.target))
        return response


# Quit
class Quit(Command):
    def __init__(self, parts):
        """
        Constructor
        :param parts:
        """
        super().__init__("QUIT", "Quitting")
        pass

    def execute(self, p, a):
        """

        :param p: Player object
        :param a: Adventure object
        :return: A list of responses
        """
        a.stop()
        return [(self.source, self.participle)]


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
        """

        :param p: Player object
        :param a: Adventure object
        :return: A list of responses
        """
        response = list([])
        if self.type == "AREA":
            for act in p.area.searchActions:
                act.perform()
            response = [(self.source, p.area.searchDescription)]
            for i in p.area.items:
                if i.visible:
                    response.append((self.source, i.searchDescription))
        elif self.type == "DIRECTION":
            response = [(self.source, p.area.dirDescription[adv.get_dir_index(self.target)])]
        elif self.type == "IN":
            pass
        elif self.type == "ON":
            t = p.area.get_item(self.target)
            if t is None:
                for a in p.equipped:
                    if a.name == self.target:
                        t = a
            if t is not None:
                response.append((t.name, t.searchDescription))
                for x in t.searchActions:
                    response.append(x)
        return response


# Store <target> in <source>
class Store(Command):
    def __init__(self, parts):
        super().__init__("STORE", "Storing")
        self.target = parts[1]
        if len(parts) == 4 and parts[2].upper() == "IN":
            self.source = parts[3]

    def execute(self, p, a):
        """

        :param p: Player object
        :param a: Adventure object
        :return: A list of responses
        """
        response = [(self.source, self.target + " not storable")]
        targetItem = adv.get_item_from_list(p.equipped, self.target)
        if targetItem is not None:
            response = p.store(targetItem)
            response.append((self.source, self.participle + " " + self.target))
        return response


# Take <target> (it is now equipped)
class Take(Command):
    def __init__(self, parts):
        super().__init__("TAKE", "Taking")
        self.target = parts[1]

    def execute(self, p, a):
        """

        :param p: Player object
        :param a: Adventure object
        :return: A list of responses
        """
        # Validate
        targetItem = adv.get_item_from_list(p.area.items, self.target)

        # Perform
        if targetItem is not None and targetItem.description.upper() == self.target.upper() and targetItem.visible:
            response = p.equip(targetItem)
        else:
            response = [(self.source, "Unable to take " + self.target)]
        return response


# Use <source> on <target>
class Use(Command):
    def __init__(self, parts):
        super().__init__("USE", "Using")
        if len(parts) == 4 and parts[2] == "ON":
            self.source = parts[1]
            self.target = parts[3]

    def execute(self, p, a):
        """

        :param p: Player object
        :param a: Adventure object
        :return: A list of responses
        """
        # Validate
        sourceItem = adv.get_item_from_list(p.equipped, self.source)
        targetItem = adv.get_item_from_list(p.area.items, self.target)
        if targetItem is None:
            targetItem = adv.get_item_from_list(p.inventory, self.source)
            if targetItem is None:
                targetItem = adv.get_item_from_list(p.equipped, self.source)

        # Perform
        response = []
        if targetItem is None or sourceItem is None:
            response.append((self.source, "Cannot use " + self.source + " on " + self.target))
        else:
            if not targetItem.visible:
                response.append((self.source, "I do not see " + self.target))
            else:
                response.append((self.source, self.participle + " " + self.source))
                for action in sourceItem.useActions:
                    response.extend(action.perform(proposedTargetItem=targetItem))
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
