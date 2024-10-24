from direct.gui.DirectButton import DirectButton
from direct.showbase.ShowBaseGlobal import aspect2d
from panda3d.core import TextNode
from objects.ui.detailrectangle import LogEntry

text_scale = 0.1


class Action:
    def __init__(self, text, player):
        """
        An action doable in a location
        @param text: Text to display on button
        @param player: player object
        """
        self.text_node_path = None
        self.button = None
        self.player = player
        self.text_node = TextNode(text)
        self.text_node.setText(text)
        self.text_node.setFont(self.player.font)
        self.text_node.setAlign(TextNode.ACenter)

    def create_button(self):
        """
        Creates a DirectButton
        """
        self.button = DirectButton(scale=((self.text_node.getWidth() * text_scale) + 0.2, 1, 0.3), relief=None,
                                   command=self.command,
                                   geom=self.player.drawn_square)
        self.text_node_path = aspect2d.attachNewNode(self.text_node.generate())
        self.text_node_path.setScale(text_scale)

    def destroy_button(self):
        """
        Destroys the DirectButton self.button
        """
        self.button.destroy()
        self.text_node_path.removeNode()

    def command(self):
        """
        OVERWRITE! Function ran when DirectButton pressed
        """
        pass

    def set_pos(self, pos):
        self.button.setPos(pos)
        self.text_node_path.setPos(pos[0], pos[1], pos[2] - (self.text_node.getHeight() * text_scale / 2) + 0.01)

    def add_log(self, text):
        log = self.player.detail_rectangle.log
        log.add(LogEntry(log, text))


class DelayedAction(Action):
    def __init__(self, text, player):
        super().__init__(text, player)

    def post(self, e):
        pass
