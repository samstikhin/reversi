#!/usr/bin/python3
import sys

from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QTextEdit
from PyQt5.QtGui import QCursor, QIcon
from PyQt5.QtGui import QColor, QPainter
from PyQt5.QtCore import Qt, QBasicTimer

from gui_objects.guiField import Board
from gui_objects.button import Button
from simple_objects.coord import Coord
from simple_objects.rock import Rock
from gui_objects.menu import Menu
from gui_objects.log import Log
from gui_objects.table import Table
from gui_objects.timer import Timer
from game import Game


class Reversi(QWidget):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.over = True
        self.menu = Menu(self)
        self.setGeometry(200, 75, 760, 560)
        self.setFixedSize(760, 560)
        self.setWindowTitle('Reversi')
        self.show()

    def begin_game(self, gameinfo, field):
        self.over = False
        self.game = Game(gameinfo, field, self)
        self.game.set_new_pos_moves()
        self.initialize_elements_of_the_game()
        self.show_all_game_interface()

        self.timer_black.start()

        self.game.add_step_to_undo_stack()
        self.check_end_game()
        self.comp_move()

    def show_all_game_interface(self):
        self.timer_black.show()
        self.timer_white.show()
        self.board.show()
        self.table.show()
        self.log.show()
        self.back_to_menu_button.show()
        self.save_button.show()
        if self.game.info.undo_stack:
            self.undo_button.show()
        else:
            self.undo_button.close()
        if self.game.info.redo_stack:
            self.redo_button.show()
        else:
            self.redo_button.close()

    def close_all(self):
        self.timer_black.close()
        self.timer_white.close()
        self.board.close()
        self.back_to_menu_button.close()
        self.game_over_button.close()
        self.undo_button.close()
        self.redo_button.close()
        self.save_button.close()
        self.log.close()
        self.table.close()

    def initialize_elements_of_the_game(self):
        self.timer_black = Timer(Rock('B'), self.game.info.time_for_player1,
                                 (600, 160), (250, 40), self)
        self.timer_white = Timer(Rock('W'), self.game.info.time_for_player1,
                                 (600, 200), (250, 40), self)
        self.board = Board(self.game.field, (0, 0), (560, 560), self)
        self.table = Table((600, 120), self.game.info.black_points,
                           self.game.info.white_points, self)
        self.log = Log((560, 240), (200, 320), self)
        self.game_over_button = Button('GAME OVER', self.game_over,
                                       (160, 160), (260, 55), self)
        self.back_to_menu_button = Button('BACK TO MENU', self.back_to_menu,
                                          (560, 0), (200, 40), self)
        self.undo_button = Button('UNDO', self.undo, (560, 80), (100, 40), self)
        self.redo_button = Button('REDO', self.redo, (660, 80), (100, 40), self)
        self.save_button = Button('SAVE', self.save, (560, 40), (200, 40), self)

    def back_to_menu(self):
        self.close_all()
        self.menu.start_menu()

    def undo(self):
        self.game.undo()
        self.redo_button.show()
        if len(self.game.info.undo_stack) == 1:
            self.undo_button.close()
        self.board.reset_board()
        self.log.reset_log()
        self.table.reset_table(self.game.info.black_points,
                               self.game.info.white_points)
        self.repaint()

    def redo(self):
        self.game.redo()
        self.undo_button.show()
        if len(self.game.info.redo_stack) == 0:
            self.redo_button.close()
        self.board.reset_board()
        self.log.reset_log()
        self.table.reset_table(self.game.info.black_points,
                               self.game.info.white_points)
        self.repaint()

    def save(self):
        self.game.save()

    def game_over(self):
        self.close_all()
        self.menu.start_menu()

    def check_end_game(self):
        if self.game.check_end_game():
            self.log.reset_log()
            self.timer_black.stop()
            self.timer_white.stop()
            self.game_over_button.setText(self.game.check_end_game())
            self.over = True
            self.game_over_button.show()
        self.repaint()

    def comp_move(self):
        if not self.over:
            self.game.comp_move()
            self.log.reset_log()
            self.table.reset_table(self.game.info.black_points,
                                   self.game.info.white_points)
            self.change_timers()
            self.repaint()
            self.check_end_game()

    def mousePressEvent(self, e):
        if not self.over and not self.menu.isVisible():
            if e.buttons() == Qt.LeftButton \
                    and QCursor.pos().x() - self.geometry().x() < 560:
                square = int((QCursor.pos().x() - self.geometry().x()) /
                             self.board.side_of_square), \
                         int((QCursor.pos().y() - self.geometry().y()) /
                             self.board.side_of_square)
                coord = Coord(square[0], square[1])
                self.game.player_move(coord)
                self.log.reset_log()
                self.table.reset_table(self.game.info.black_points,
                                       self.game.info.white_points)
            self.new_path_after_undo()
            self.change_timers()
            self.repaint()
            self.check_end_game()
            self.comp_move()

    def new_path_after_undo(self):
        self.undo_button.show()
        self.redo_button.close()

    def change_timers(self):
        if self.timer_black.is_active() \
                and self.game.info.curr_player == Rock('W'):
            self.timer_black.stop()
            self.timer_white.start()
        elif self.timer_white.is_active() \
                and self.game.info.curr_player == Rock('B'):
            self.timer_black.start()
            self.timer_white.stop()

def main():
    app = QApplication(sys.argv)
    Reversi()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
