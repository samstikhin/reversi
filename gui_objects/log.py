from PyQt5.QtWidgets import QTextEdit


class Log(QTextEdit):
    def __init__(self, coordinates, size, parent=None):
        super(QTextEdit, self).__init__(parent)
        self.parent = parent
        self.setReadOnly(True)
        self.setGeometry(coordinates[0], coordinates[1], size[0], size[1])
        self.setFixedSize(size[0], size[1])
        self.isUndoRedoEnabled()

    def reset_log(self):
        self.clear()
        log_list = self.parent.game.info.log
        for lg in log_list:
            self.append(lg)
