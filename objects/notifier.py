from direct.directnotify.DirectNotifyGlobal import directNotify


class Notifier(directNotify):
    def __init__(self, name):
        self.notify = directNotify.newCategory(name)
