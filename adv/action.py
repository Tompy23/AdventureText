import adv.adventure as adv


class Action:
    """
    An Action is associated with an item, area or another action.  The normal pattern is to have
    an object passed into the constructor, then when the action is performed, only perform it on
    that object.
    
    The Action can be set to execute only a certain number of times or forever by setting the count
    parameter in the constructor.  -1 is forever, any other number will perform the action that many times.

    Interface
    ---------
    perform() - Performs the action on the given object(s)
    
    methods
    -------
    _is_complete() - Determine if the action is to be performed anymore
    _complete() - Finish an action and update_completeness

    """

    def __init__(self, source, count=-1):
        """
        Base Action constructor
        :param source: A tag to identify the source of the action
        :param count: How many times the action should be performed (-1 for infinite)
        """
        self.source = "Action - " + source
        self.count = count

    def _is_complete(self):
        """Check to determine if the action should be performed"""
        return self.count == 0

    def _complete(self):
        """Update the count which determines if the action is complete or not"""
        if self.count > 0:
            self.count = self.count - 1


# Response Actions
#
# Handle simple or conditional responses
class Response(Action):
    """Return a direct response when this action is performed"""

    def __init__(self, source, text):
        """
        Response action constructor
        :param source: A tag to identify the source of the action
        :param text: The text which should be in the response
        """
        super().__init__("Response - " + source)
        self.text = text

    def perform(self, **kwargs):
        """
        :param kwargs: None
        :return: A list of responses
        """
        response = [(self.source, self.text)] if not self._is_complete() else []
        self._complete()
        return response


class ResponseDirection(Action):
    """Return a response only for a specific direction"""

    def __init__(self, text, targetDirection):
        """
        :param text: The text for the response
        :param targetDirection: The direction which must match
        """
        super().__init__("Response - " + targetDirection.name)
        self.text = text
        self.targetDirection = targetDirection

    def perform(self, direction):
        """
        :param direction: A DIRECTION object on which to perform
        :return: A list of responses
        """
        response = [(self.source, self.text)] if self.targetDirection == direction and not self._is_complete() else []
        self._complete()
        return response


class ResponseProps(Action):
    """Response that is passed in through the perform action based on a target item and a specific property"""

    def __init__(self, targetItem):
        """
        Response properties constructor
        :param targetItem: The item which must be passed as an argument to be performed
        """
        super().__init__("ResponseProps")
        self.targetItem = targetItem

    def perform(self, prop, **kwargs):
        """
        Perform an action based on the check() of a property in the target item
        :param prop: The property name which will be checked
        :param kwargs:
        PROPOSED_TARGET_ITEM - The item which must match the specified item
        RESPONSE_TEXT - THe text put into the response
        :return: A list of responses
        """
        response = []
        if not self._is_complete() and self.targetItem == kwargs[adv.PROPOSED_TARGET_ITEM]:
            if self.targetItem.check(prop):
                response.append((self.source, kwargs[adv.RESPONSE_TEXT]))
                self._complete()
        return response


# Property setters
#
# These actions set a property on a defined item.
class ItemVisible(Action):
    """Make an item visible"""

    def __init__(self, targetItem, count=1):
        """
        Make an item visible constructor
        :param targetItem: The item to make visible
        :param count: The number of times to perform, defaults to 1
        """
        super().__init__("ItemInvisible", count)
        self.targetItem = targetItem

    def perform(self, **kwargs):
        """
        Perform the make visible action
        :param kwargs: Not used
        :return: An empty list of responses
        """
        if not self._is_complete():
            if self.targetItem is not None:
                self.targetItem.visible = True
                self._complete()
        return []


# Use Actions
#
# These actions are placed on an Item (the source) and used on another item (the target)
# The target name is passed in during construction.  The item object is passed in during perform.  These are checked
# to make sure they are the same when performing the action.
class Open(Action):
    """Cause an item to become open"""

    def __init__(self, targetItem, count=-1):
        """
        Open action constructor
        :param targetItem: The item which will become open if specified in the action
        """
        super().__init__("Open", count)
        self.targetItem = targetItem

    def perform(self, **kwargs):
        """
        Perform the open action.  The count is the number of successful opens.
        :param kwargs:
        PROPOSED_TARGET_ITEM - The item on which the action is attempted
        :return: A list of responses
        """
        proposedTargetItem = kwargs[adv.PROPOSED_TARGET_ITEM]
        response = []
        if not self._is_complete():
            if (proposedTargetItem is not None and self.targetItem == proposedTargetItem) and proposedTargetItem.can(
                    adv.ITEM_OPEN):
                proposedTargetItem.props[adv.ITEM_OPEN] = True
                response.append((self.source, self.targetItem.name + " is now open."))
                self._complete()
            else:
                response.append((self.source,
                                 "Are you sure you want to try and open " + proposedTargetItem.description + "?"))
        else:
            response.append((self.source, self.targetItem + " cannot be opened anymore."))
        return response


class Close(Action):
    """Cause an item to become not open"""

    def __init__(self, targetItem, count=-1):
        """
        Close action constructor
        :param targetItem: THe item which will become not open if specified when perform is called
        """
        super().__init__("Close", count)
        self.targetItem = targetItem

    def perform(self, **kwargs):
        """
        Perform an action which will cause an item to be not open
        :param kwargs:
        PROPOSED_TARGET_ITEM - The item on which the action is attempted
        :return: A list of responses
        """
        proposedTargetItem = kwargs[adv.PROPOSED_TARGET_ITEM]
        response = []
        if not self._is_complete():
            if (proposedTargetItem is not None and self.targetItem == proposedTargetItem) and proposedTargetItem.can(
                    adv.ITEM_OPEN):
                proposedTargetItem.props[adv.ITEM_OPEN] = False
                response.append((self.source, self.targetItem.name + " is now closed."))
                self._complete()
            else:
                response.append((self.source,
                                 "Are you sure you want to try and close " + proposedTargetItem + "?"))
        else:
            response.append((self.source, proposedTargetItem + " cannot be closed anymore."))
        return response


class ToggleLock(Action):
    """Toggle the Lock property which is boolean True or False"""

    def __init__(self, targetItem, count=-1):
        """
        Toggle lock action constructory
        :param targetItem: The item which which will be toggled
        """
        super().__init__("ToggleLock", count)
        self.targetItem = targetItem

    def perform(self, **kwargs):
        """
        Perform the toggle of the Lock property which must be not open
        :param kwargs:
        PROPOSED_TARGET_ITEM - The item on which the action is attempted
        :return: A list of responses
        """
        proposedTargetItem = kwargs[adv.PROPOSED_TARGET_ITEM]
        response = []
        if not self.targetItem.check(adv.ITEM_OPEN):
            if not self._is_complete():
                if (self.targetItem is None or self.targetItem == proposedTargetItem) and proposedTargetItem.can(
                        adv.ITEM_LOCK):
                    proposedTargetItem.props[adv.ITEM_LOCK] = not proposedTargetItem.props[adv.ITEM_LOCK]
                    response.append((self.source,
                                     proposedTargetItem.description + " is now " + (
                                         "locked." if proposedTargetItem.check(
                                             adv.ITEM_LOCK) else "unlocked.")))
                    self._complete()
                else:
                    response.append((self.source, proposedTargetItem.description + " does not have a lock."))
            else:
                response.append((self.source, "This cannot be done to " + proposedTargetItem.description + "."))
        else:
            response.append((self.source, self.targetItem + " is open and cannot be locked."))
        return response


class Drop(Action):
    """Drop an item"""

    def __init__(self, targetItem):
        """
        Toggle lock action constructory
        :param targetItem: The item which which will be toggled
        """
        super().__init__("Drop")
        self.targetItem = targetItem

    def perform(self, **kwargs):
        """
        Perform the toggle of the Lock property which must be not open
        :param kwargs:
        PROPOSED_TARGET_ITEM - The item on which the action is attempted
        CURRENT_AREA - The place where the item will be dropped
        :return: A list of responses
        """
        player = kwargs[adv.PLAYER]
        proposedTargetItem = kwargs[adv.PROPOSED_TARGET_ITEM]
        response = []
        if not self._is_complete():
            if proposedTargetItem is not None and self.targetItem == proposedTargetItem \
                    and player is not None and adv.get_item_from_list(player.equipped, proposedTargetItem) is not None:
                player.equipped.remove(proposedTargetItem)
                player.area.items.append(proposedTargetItem)
                response.append((self.source, proposedTargetItem.description + " has been dropped in the current room."))
                self._complete()

        return response


# Triggers
#
# These are actions that will contain a set of actions which will be performed based on the triggers implementation
class IfOpen(Action):
    """Actions to be performed if target item is open"""

    def __init__(self, targetItem, actions, count=-1):
        """
        If open action trigger constructor
        :param targetItem: The item which which must be designated to perform the actions
        :param actions: A list of actions which will be sent the target item to perform
        """
        super().__init__("IfOpen", count)
        self.targetItem = targetItem
        self.actions = actions

    def perform(self, **kwargs):
        """
        Perform a list of actions if the target item is open
        :param kwargs:
        PROPOSED_TARGET_ITEM - The item on which the action is attempted
        :return: A list of responses
        """
        proposedTargetItem = kwargs[adv.PROPOSED_TARGET_ITEM]
        response = []
        if not self._is_complete():
            if (self.targetItem is None or self.targetItem == proposedTargetItem) and proposedTargetItem.check(
                    adv.ITEM_OPEN):
                for a in self.actions:
                    response.extend(a.perform(proposedTargetItem=proposedTargetItem))
                self._complete()
        else:
            response.append((self.source, "This cannot be done to " + proposedTargetItem.description + "."))
        return response


class CountDown(Action):
    """
    Action performs something when complete
            When the action is complete, it performs the list of actions, this allows something
        to happen a number of times triggering this action BEFORE any real actions are perfomed.
    """

    def __init__(self, actions, count=0):
        """
        Countdown Action Constructor
        :param actions: A list of actions to activate when the action is completed
        """
        super().__init__("CountDown", count)
        self.actions = actions

    def perform(self, **kwargs):
        """
          Perform a list of actions if the target item is open
          :param kwargs: Passed along to the actions performed
          :return: A list of responses
          """
        response = []
        if self._is_complete():
            response.extend((x.perform(kwargs) for x in self.actions))
            self.count = -1
        else:
            self.complete()

        return response


#Default actions
EXIT_PASS_THRU = Response("EXIT_PASS_THRU", "Passing through")
AREA_ENTER = Response("AREA_ENTER", "Entering")
AREA_EXIT = Response("AREA_EXIT)", "Exiting")
