from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import QBasicTimer


class Timer(QLabel):
    def __init__(self, rock, time, coordinates, size, parent=None):
        super(QLabel, self).__init__(parent)
        self.parent = parent
        self.rock = rock
        self.time = time
        self.timer = QBasicTimer()
        self.setGeometry(coordinates[0], coordinates[1], size[0], size[1])
        self.setText('Left Time for {}:{}'.format(str(self.rock), self.time))

    def is_active(self):
        return self.timer.isActive()

    def stop(self):
        if self.timer.isActive():
            self.timer.stop()

    def start(self):
        self.timer.start(self.time, self)

    def timerEvent(self, e):
        if 0 >= self.time:
            self.stop()
            self.parent.game.end_game(self.rock)
        self.time -= 1
        self.setText('Left Time for {}:{}'.format(str(self.rock), self.time))
        self.repaint()
