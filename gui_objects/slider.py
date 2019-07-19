from PyQt5.QtWidgets import QLabel, QSlider
from PyQt5.QtCore import Qt
#TODO
class Slider(QSlider):
    def __init__(self, coordinates, size, parent=None):
        super(QSlider(Qt.Horizontal), self).__init__(parent)
        self.parent = parent
        self.setFocusPolicy(Qt.NoFocus)
        self.setGeometry(coordinates[0], coordinates[1], size[0], size[1])
        self.valueChanged[int].connect(self.changeValue)



    def initUI(self):

        sld = QSlider(Qt.Horizontal, self)
        sld.setFocusPolicy(Qt.NoFocus)
        sld.setGeometry(30, 40, 100, 30)
        sld.valueChanged[int].connect(self.changeValue)


        self.label = QLabel(self)
        self.label.setPixmap(QPixmap('mute.png'))
        self.label.setGeometry(160, 40, 80, 30)

        self.setGeometry(300, 300, 280, 170)
        self.setWindowTitle('QSlider')
        self.show()

    def changeValue(self, value):
        if value == 0:
            self.label.setPixmap(QPixmap('mute.png'))
        elif value > 0 and value <= 30:
            self.label.setPixmap(QPixmap('min.png'))
        elif value > 30 and value < 80:
            self.label.setPixmap(QPixmap('med.png'))
        else:
            self.label.setPixmap(QPixmap('max.png'))