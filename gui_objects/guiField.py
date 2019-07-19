from PyQt5.QtGui import QColor, QPainter
from PyQt5.QtWidgets import QWidget

from simple_objects.rock import Rock
from simple_objects.coord import Coord


class Board(QWidget):
    square_color = QColor(100, 155, 100)
    pos_move_color = QColor(0, 155, 0)
    black_color = QColor(0, 0, 0)
    white_color = QColor(255, 255, 255)

    def __init__(self, field, coordinates, size, parent=None):
        super(QWidget, self).__init__(parent)
        self.parent = parent
        self.field = field
        self.width = self.field.width
        self.height = self.field.height
        self.side_of_square = size[1]/self.field.width
        self.side_of_rock = self.side_of_square*0.75
        self.setGeometry(coordinates[0], coordinates[1], size[0], size[1])
        self.show()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.draw_squares(qp)
        self.draw_circles(qp)
        self.draw_pos_moves(qp)
        qp.end()

    def reset_board(self):
        self.field = self.parent.game.field

    def draw_squares(self, qp):
        qp.setBrush(self.square_color)
        for x in range(self.width):
            for y in range(self.height):
                qp.drawRect(x * self.side_of_square, y * self.side_of_square,
                            self.side_of_square, self.side_of_square)

    def draw_pos_moves(self, qp):
        qp.setBrush(self.pos_move_color)
        for coord in self.parent.game.info.pos_moves:#parent
            qp.drawRect(coord.x * self.side_of_square,
                        coord.y * self.side_of_square,
                        self.side_of_square, self.side_of_square)

    def draw_circles(self, qp):
        for x in range(self.width):
            for y in range(self.height):
                coord = Coord(x, y)
                if self.field.squares[coord] is not None:
                    if self.field.squares[coord] == Rock('W'):
                        qp.setBrush(self.white_color)
                    else:
                        qp.setBrush(self.black_color)
                    qp.drawEllipse(coord.x * self.side_of_square +
                                   (self.side_of_square - self.side_of_rock)/2,
                                   coord.y * self.side_of_square +
                                   (self.side_of_square - self.side_of_rock)/2,
                                   self.side_of_rock,
                                   self.side_of_rock)


