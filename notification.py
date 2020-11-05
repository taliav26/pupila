from PySide2.QtCore import QObject, Slot, Signal, Property, QTimer


class Notification(QObject):
    def __init__(self):
        super(Notification, self).__init__()
        self._message = ""

    @Slot(str)
    def show_notification(self, message):
        self.set_message(message)
        QTimer.singleShot(2000, self.reset_message)

    @Slot()
    def reset_message(self):
        self.set_message("")

    def get_message(self):
        return self._message

    def set_message(self, message):
        self._message = message
        self.on_message.emit()

    on_message = Signal()

    message = Property(str, get_message, set_message, notify=on_message)
