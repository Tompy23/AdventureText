import adv.response as resp


class Action:
    def __init__(self, count=-1):
        self.count = count

    def is_complete(self):
        return self.count == 0

    def complete(self):
        if self.count > 0:
            self.count = self.count - 1


class ActionResponse(Action):
    def __init__(self, source, text):
        super().__init__()
        self.source = source
        self.text = text

    def perform(self, responseList):
        responseList.append(resp.Response(self.source, self.text))
        return responseList


class ActionMakeItemVisible(Action):
    def __init__(self, item, count=1):
        super().__init__(count)
        self.item = item

    def perform(self):
        if not self.is_complete():
            self.item.visible = True
        self.complete()


class UseOnItemTrigger(Action):
    def __init__(self, action, target, count=-1):
        super().__init__(count=count)
        self.target = target
        self.action = action

    def perform(self, p):
        if p.area.items.__contains__(self.target) or p.equipped.__contains__(self.target):
            self.action.perform(self.target)


class OpenChestAction(Action):
    def __init__(self, chest):
        super().__init__()
        self.chest = chest

    def perform(self):
        if not self.is_complete():
            self.chest.open = True
        self.complete()


class CloseChestAction(Action):
    def __init__(self, chest):
        super().__init__()
        self.chest = chest

    def perform(self):
        if not self.is_complete():
            self.chest.open = False
        self.complete()


class ToggleLockChestAction(Action):
    def __init__(self, chest):
        super().__init__()
        self.chest = chest

    def perform(self):
        if not self.is_complete():
            self.chest.locked = not self.chest.locked
        self.complete()
