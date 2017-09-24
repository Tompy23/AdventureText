class Thing:
    def __init__(self):
        pass


class Feature(Thing):
    def __init__(self):
        super().__init__()


class Item(Thing):
    def __init__(self):
        super().__init__()


class Chest(Feature):
    def __init__(self):
        super().__init__()


class Weapon(Item):
    def __init__(self):
        super().__init__()
