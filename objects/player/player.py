from objects.player.locations.home import Home
from objects.player.ui.action_bar import ActionBar
from objects.notifier import Notifier
from objects.player.clock import Clock
from objects.player.ui.inventory import Inventory
from objects.player.ui.selfportrait import SelfPortrait, EATING, PERSON, BATHING
from objects.player.ui.stats.statswidget import StatsWidget
from objects.player.ui.stats.stat import Stat
from objects.player.locations.location import HOME


class Player(Notifier):
    def __init__(self):
        """
        Player object
        @param clock: Clock object
        """
        Notifier.__init__(self, "player")

        self.font = loader.loadFont("Monotony1-Regular.ttf")
        self.font.setPixelsPerUnit(60)

        # Widgets
        self.self_portrait = SelfPortrait()
        self.action_bar = ActionBar()
        self.inventory = Inventory()
        self.clock = Clock(self)

        # Location
        self.location_dict = {
            HOME: Home
        }
        self.location = None
        self.head_to_location(HOME)

        # Stats
        self.hygiene = Stat(20)
        self.cleaning_amount = 0 # adds hygiene after bathing
        self.hunger = Stat(20)
        self.consuming_calories = 0 # adds calories when done eating
        self.sleep = Stat(100)
        self.in_bed = True
        self.money = 0

        self.stats_widget = StatsWidget(self)

    def head_to_location(self, destination, stage=0):
        if destination in self.location_dict:
            self.location = self.location_dict[destination](self)
        else:
            return False

        self.location.set_stage(stage)

        return True

    def deteriorate(self):
        self.starve()
        self.stink()
        if self.in_bed:
            self.rest()
        else:
            self.tire()
        self.stats_widget.update_stats()

    def stink(self):
        """
        Pee-ew!
        """
        self.hygiene -= 5

    def bathe(self, duration=2, effect=80):
        """
        The player takes a bath
        @param duration: How long it takes to wash
        @param effect: How much hygiene restored
        """
        self.notify.debug(f"[bathe] Start bathing for {duration} seconds for {effect} hygiene.")
        self.self_portrait.update_state(BATHING)
        self.cleaning_amount = effect
        taskMgr.doMethodLater(duration, self.finish_bathing, "Bathing")
        self.daze(duration)

    def finish_bathing(self, task):
        self.notify.debug(f"[finish_bathing] Finished bathing; restoring {self.cleaning_amount} to {self.hygiene}.")
        self.self_portrait.update_state(PERSON)
        self.hygiene += self.cleaning_amount
        self.cleaning_amount = 0
        self.stats_widget.update_stats()

    def starve(self):
        """
        No cheezburger
        """
        self.hunger -= 10

    def feed(self, calories=20, daze_time=2):
        """
        Cheezburger
        @param calories: Amount of hunger to restore
        @param daze_time: How long to eat
        """
        self.notify.debug(f"[feed] Start feeding: {daze_time}s for +{calories}.")
        self.self_portrait.update_state(EATING)
        self.consuming_calories += calories
        taskMgr.doMethodLater(daze_time, self.finish_eating, "Eating")
        self.daze(daze_time)

    def finish_eating(self, task):
        self.notify.debug(f"[finish_eating] Finished eating; restoring {self.consuming_calories} to {self.hunger}.")
        self.hunger += self.consuming_calories
        self.consuming_calories = 0
        self.self_portrait.update_state(PERSON)

        self.stats_widget.update_stats()

    def tire(self):
        """
        Another hour awake
        """
        self.sleep -= 5

    def rest(self, power_boost=10):
        """
        Zzz...
        @param power_boost: Amount of sleep to restore
        """
        self.sleep += power_boost

    def daze(self, duration=5):
        self.action_bar.hide()
        taskMgr.doMethodLater(duration, self.undaze, 'DazePlayer')

    def undaze(self, task):
        self.action_bar.show()
