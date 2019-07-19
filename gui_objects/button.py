from PyQt5.QtWidgets import QPushButton


class Button(QPushButton):
    def __init__(self, name, function, coordinates, size, parent=None):
        super(QPushButton, self).__init__(parent)
        self.function = function
        self.setGeometry(coordinates[0], coordinates[1], size[0], size[1])
        self.setText(name)
        self.clicked.connect(self._on_click)

    def _on_click(self):
        self.function()