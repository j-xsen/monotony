from direct.showbase.DirectObject import DirectObject

from objects.locations.location import Location, WORK
from objects.ui.action import Action, DelayedAction
from objects.ui.message import Message
from objects.ui.selfportrait import PERSON


class WakeUp(Action):
    def __init__(self):
        Action.__init__(self, "Wake Up")

    def command(self):
        # change stage
        messenger.send("set_stage", [1])
        # update portrait
        messenger.send("update_state", [PERSON])
        # change player variable for deteriorate
        messenger.send("wake_up")
        self.add_log("Good morning Me!")


class GoToWork(Action):
    def __init__(self):
        Action.__init__(self, "Go to Work")

    def command(self):
        messenger.send("head_to_location", [WORK])


class Eat(DelayedAction):
    def __init__(self):
        Action.__init__(self, "Eat")

    def command(self):
        messenger.send("feed", [60, 1, self.post])

    def post(self, e):
        self.add_log("Delicious!")


class Bathe(DelayedAction):
    def __init__(self, ):
        Action.__init__(self, "Bathe")

    def command(self):
        messenger.send("bathe", [2, 80, self.post])

    def post(self, e):
        self.add_log("All clean.")


class Home(Location, DirectObject):
    def __init__(self):
        """
        Home Location object
        @param player: Player object
        """
        Location.__init__(self)
        self.notify.debug("[__init__] Creating Home location")
        self.actions = [
            [
                WakeUp()
            ],
            [
                Eat(),
                Bathe(),
                GoToWork()
            ]
        ]

    def set_stage(self, stage=0):
        Location.set_stage(self, stage)
        if stage == 0:
            welcome_note = Message("Welcome to Monotony!",
                                   "In this game, you live the life of someone with a 9-5 job, "
                                   "with every day being the same.\n\n"
                                   "The most important boxes that you need to keep an eye on are"
                                   " the lower-left and upper-right boxes.\n\n"
                                   "The lower-left box will hold both your characters' thoughts "
                                   "in the Log and any messages that you may want to refer back "
                                   "to, such as this one, in the Inventory.\n\n"
                                   "The upper-right box is where you will see the actions "
                                   "available to you.")
            messenger.send("add_note", [welcome_note])
