from locations.location import Location
from locations.actions.home import *


class Home(Location):
    def __init__(self, player):
        Location.__init__(self, player)
        self.notify.debug("[__init__] Creating Home location")

        self.actions = [
            [
                WakeUp(self)
            ],
            [
                Eat(self)
            ]
        ]
