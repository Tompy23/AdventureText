# name - unique identifier
# visible - Whether or not it is added to an area description
# targets - The things it can be used on
# inv - Whether or not it can be picked up True/False
# closable - Whether or not it can be opened and closed

# locked (opt) - whether it is locked or not


class Item:
    def __init__(self, name, description, searchDescription, visible, inv=True, closable=False):
        self.name = name
        self.description = description
        self.inv = inv
        self.closable = closable
        self.searchDescription = searchDescription
        self.visible = visible
        self.useActions = list([])

    def register_use_action(self, action):
        self.useActions.append(action)


class Chest(Item):
    def __init__(self, name, description, searchDescription, visible=True, locked=False, open=False):
        super().__init__(name, description, searchDescription, visible, inv=False, closable=True)
        self.locked = locked
        self.open = open
        self.items = list([])


class Weapon(Item):
    def __init__(self, name, description, searchDescription, visible=True):
        super().__init__(name, description, searchDescription, visible)


class Key(Item):
    def __init__(self, name, description, searchDescription, visible=True):
        super().__init__(name, description, searchDescription, visible)



