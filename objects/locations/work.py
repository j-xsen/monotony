import random

from direct.gui.DirectGui import DGG
from direct.interval.LerpInterval import LerpColorInterval
from direct.showbase.DirectObject import DirectObject

from objects.locations.location import Location
from objects.ui.action import Action
from objects.ui.selfportrait import DRIVING, PERSON


class WorkAction(Action, DirectObject):
    def __init__(self, index):
        """
        A special action for the Work scene's minigame.
        :param index: The index of the action (0-4)
        :type index: int
        """
        Action.__init__(self, str(index))
        self.number = 0
        self.text_scale = 0.08
        self.index = index

        self.accept("randomize", self.randomize)

    def randomize(self):
        self.number = random.randrange(10, 100)
        self.text_node.setText(str(self.number))

    def command(self):
        messenger.send("pressed_card", [self.index, self.number])


class Work(Location):
    def __init__(self, action_bar):
        Location.__init__(self, action_bar)
        self.notify.debug("[__init__] Creating Work location")
        messenger.send("update_state", [DRIVING])
        self.actions = [
            [

            ],
            [
                WorkAction(0),
                WorkAction(1),
                WorkAction(2),
                WorkAction(3),
                WorkAction(4),
            ]
        ]

        self.randomize_cards()

        self.click_order = []

        self.accept("pressed_card", self.pressed_card)

    def set_stage(self, stage):
        super().set_stage(stage)
        if stage == 0:
            taskMgr.doMethodLater(0.5, self.show_cards, "Driving")

    def pressed_card(self, index, number):
        """
        Ran when a card is pressed. Disables card and adds to the click order.
        :param index: The index of the card.
        :type index: int
        :param number: Number of the card.
        :type number: int
        """
        self.actions[1][index].disable_button()
        self.click_order.append(number)

        if self.check_if_all_clicked():
            self.check_cards()

    def check_if_all_clicked(self):
        for action in self.actions[1]:
            if action.button['state'] == DGG.NORMAL:
                return False
        return True

    def check_cards(self):
        min = 0
        for number in self.click_order:
            if number < min:
                self.reset_cards()
                self.flash_action_bar(True)
                return False
            min = number
        messenger.send("profit")
        self.reset_cards()
        self.flash_action_bar(False)
        return True

    def flash_action_bar(self, is_red):
        color = (1, 0, 0, 1) if is_red else (0, 1, 0, 1)
        lerpcolor = LerpColorInterval(self.action_bar.background, 1, (1, 1, 1, 1), color)
        lerpcolor.start()
        for action in self.actions[self.stage]:
            new_color = LerpColorInterval(action.button, 1, (1, 1, 1, 1), color)
            new_color.start()

    def reset_cards(self):
        self.delete_all_card_buttons()
        self.randomize_cards()
        self.enable_all_cards()

    def randomize_cards(self):
        self.click_order = []
        for i in range(0, 5):
            self.actions[1][i].randomize()

    def enable_all_cards(self):
        counter = 0
        for card in self.actions[1]:
            card.create_button()
            self.actions[1][counter].set_pos(self.action_bar.pos[5][counter])
            counter += 1

    def delete_all_card_buttons(self):
        for card in self.actions[1]:
            card.destroy_button()

    def show_cards(self, e):
        self.set_stage(1)
        messenger.send("update_state", [PERSON])
