import adv.adventure as adv


# perform()
# Params - See specific type of action, but any reference to Items must be an Item object
# return - list of Response objects
#
# The classes are grouped by type, all of the same type have the same perform() signature
class Action:
    def __init__(self, source, count=-1):
        self.source = "Action - " + source
        self.count = count

    def is_complete(self):
        return self.count == 0

    def complete(self):
        if self.count > 0:
            self.count = self.count - 1


class Response(Action):
    def __init__(self, source, text):
        super().__init__("Response")
        self.source = source
        self.text = text

    def perform(self, **kwargs):
        response = [(self.source, self.text)]
        return response


# Property setters
#
# These actions set a property on a defined item.

class ItemVisible(Action):
    def __init__(self, targetItem, count=1):
        super().__init__("ItemInvisible", count)
        self.targetItem = targetItem

    def perform(self, **kwargs):
        if not self.is_complete():
            if self.targetItem is not None:
                self.targetItem.visible = True
        self.complete()
        return []


# Use Actions
#
# These actions are placed on an Item (the source) and used on another item (the target)
# The target name is passed in during construction.  The item object is passed in during perform.  These are checked
# to make sure they are the same when performing the action.

class Open(Action):
    def __init__(self, targetItem):
        super().__init__("Open")
        self.targetItem = targetItem

    def perform(self, **kwargs):
        proposedTargetItem = kwargs[adv.PROPOSED_TARGET_ITEM]
        response = []
        if not self.is_complete():
            if (self.targetItem is None or self.targetItem == proposedTargetItem) and proposedTargetItem.can("open"):
                proposedTargetItem.props["open"] = True
                response.append((self.source, self.targetItem.name + " is now open."))
            else:
                response.append((self.source,
                                 "Are you sure you want to try and open " + proposedTargetItem.description + "?"))
        else:
            response.append((self.source, self.targetItem + " cannot be opened anymore."))
        self.complete()
        return response


class Close(Action):
    def __init__(self, targetItem):
        super().__init__("Close")
        self.targetItem = targetItem

    def perform(self, **kwargs):
        proposedTargetItem = kwargs[adv.PROPOSED_TARGET_ITEM]
        response = []
        if not self.is_complete():
            if (self.targetItem is None or self.targetItem == proposedTargetItem) and proposedTargetItem.can("open"):
                proposedTargetItem.props["open"] = False
                response.append((self.source, self.targetItem.name + " is now closed."))
            else:
                response.append((self.source,
                                 "Are you sure you want to try and close " + proposedTargetItem + "?"))
        else:
            response.append((self.source, proposedTargetItem + " cannot be closed anymore."))
        self.complete()
        return response


class ToggleLock(Action):
    def __init__(self, targetItem):
        super().__init__("ToggleLock")
        self.targetItem = targetItem

    def perform(self, **kwargs):
        proposedTargetItem = kwargs[adv.PROPOSED_TARGET_ITEM]
        response = []
        if not self.is_complete():
            if (self.targetItem is None or self.targetItem == proposedTargetItem) and proposedTargetItem.can("lock"):
                proposedTargetItem.props["lock"] = not proposedTargetItem.props["lock"]
                response.append((self.source,
                                 proposedTargetItem.description + " is now " + "locked." if proposedTargetItem.check(
                                     "lock") else "unlocked."))
            else:
                response.append((self.source, proposedTargetItem.description + " does not have a lock."))
        else:
            response.append((self.source, "This cannot be done to " + proposedTargetItem.description + "."))
        self.complete()
        return response


# Triggers
#
# These are actions that will contain a set of actions which will be performed based on the triggers implementation
class IfOpen(Action):
    def __init__(self, targetItem, actions):
        super().__init__("IfOpen")
        self.targetItem = targetItem
        self.actions = actions

    def perform(self, **kwargs):
        proposedTargetItem = kwargs[adv.PROPOSED_TARGET_ITEM]
        response = []
        if not self.is_complete():
            if (self.targetItem is None or self.targetItem == proposedTargetItem) and proposedTargetItem.check("open"):
                for a in self.actions:
                    response.extend(a.perform(response, proposedTargetItem))
        else:
            response.append((self.source, "This cannot be done to " + proposedTargetItem.description + "."))
        self.complete()
        return response
