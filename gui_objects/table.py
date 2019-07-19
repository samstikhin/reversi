from PyQt5.QtWidgets import QLabel


class Table(QLabel):
    def __init__(self, coordinates, black_points, white_points, parent=None):
        super(QLabel, self).__init__(parent)
        self.parent = parent
        self.setGeometry(coordinates[0], coordinates[1], 200, 40)
        self.str = 'BLACK {}:{} WHITE'.format(str(black_points),
                                              str(white_points))
        self.setText(self.str)

    def reset_table(self, black_points, white_points):
        self.str = 'BLACK {}:{} WHITE'.format(str(black_points),
                                              str(white_points))
        self.setText(self.str)
        self.repaint()
