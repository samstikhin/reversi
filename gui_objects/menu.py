from PyQt5.QtWidgets import QWidget

from PyQt5.QtGui import QPainter

from simple_objects.rock import Rock
from gui_objects.button import Button
from simple_objects.field import Field
from simple_objects.gameinfo import GameInformation
from simple_objects.ai import AI
from game import load


class Menu(QWidget):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        self.parent = parent
        self.init_ui()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        qp.end()

    def init_ui(self):
        self.board_size = 8
        self.ai = None
        self.setGeometry(0, 0, 560, 560)
        self.initialize_buttons()
        self.start_menu()

    def initialize_buttons(self):
        self.new_game_button = Button('NEW GAME',
                                      self.new_game_menu,
                                      (260, 160), (260, 40), self)
        self.load_button = Button('LOAD', self.load,
                                  (260, 240), (260, 40), self)
        self.quit_button = Button('QUIT', self.quit_game,
                                  (260, 320), (260, 40), self)
        self.one_player_button = Button('ONE PLAYER',
                                        self.one_player,
                                        (260, 160), (260, 40), self)
        self.two_players_button = Button('TWO PLAYER',
                                         self.two_players,
                                         (260, 240), (260, 40), self)
        self.back_button = Button('BACK', self.back,
                                  (260, 320), (260, 40), self)
        self.white_button = Button('WHITE', self.white_color,
                                   (260, 160), (260, 40), self)
        self.black_button = Button('BLACK', self.black_color,
                                   (260, 240), (260, 40), self)
        self.continue_button = Button('CONTINUE', self.continue_play,
                                      (260, 80), (260, 40), self)
        self.no_load_game_button = Button('NO LOAD GAME', self.no_load_game,
                                          (200, 100), (380, 100), self)
        self.easy_button = Button('EASY', self.easy,
                                  (260, 80), (260, 40), self)
        self.medium_button = Button('MEDIUM', self.medium,
                                    (260, 160), (260, 40), self)
        self.hard_button = Button('HARD', self.hard,
                                  (260, 240), (260, 40), self)

    def close_buttons(self):
        self.one_player_button.close()
        self.two_players_button.close()
        self.back_button.close()
        self.white_button.close()
        self.black_button.close()
        self.new_game_button.close()
        self.continue_button.close()
        self.quit_button.close()
        self.load_button.close()
        self.no_load_game_button.close()
        self.easy_button.close()
        self.medium_button.close()
        self.hard_button.close()

    def start_menu(self):
        self.show()
        self.close_buttons()
        self.new_game_button.show()
        self.load_button.show()
        self.quit_button.show()
        if not self.parent.over:
            self.continue_button.show()

    def continue_play(self): #parent
        self.close_buttons()
        self.close()
        self.parent.show_all_game_interface()

    def no_load_game(self):
        self.no_load_game_button.close()
        self.start_menu()

    def quit_game(self):
        quit()

    def new_game_menu(self):
        self.close_buttons()
        self.one_player_button.show()
        self.two_players_button.show()
        self.back_button.show()

    def one_player(self):
        self.close_buttons()
        self.white_button.show()
        self.black_button.show()
        self.back_button.show()
        self.count_of_players = 1

    def two_players(self):
        self.count_of_players = 2
        self.start_new_game()

    def white_color(self):
        self.player_color = 'W'
        self.ai_menu()

    def black_color(self):
        self.player_color = 'B'
        self.ai_menu()

    def back(self):
        if self.one_player_button.isVisible():
            self.start_menu()
        elif self.white_button.isVisible():
            self.new_game_menu()
        else:
            self.one_player()

    def ai_menu(self):
        self.close_buttons()
        self.easy_button.show()
        self.medium_button.show()
        self.hard_button.show()
        self.back_button.show()

    def easy(self):
        self.close_buttons()
        self.ai = AI(Rock(self.player_color).invert(), 'E')
        self.start_new_game()

    def medium(self):
        self.close_buttons()
        self.ai = AI(Rock(self.player_color).invert(), 'M')
        self.start_new_game()

    def hard(self):
        self.close_buttons()
        self.ai = AI(Rock(self.player_color).invert(), 'H')
        self.start_new_game()

    def start_new_game(self):
        self.close()
        field = Field(self.board_size, self.board_size)
        field.arrange_rocks()
        gameinfo = GameInformation(self.count_of_players,
                                   Rock('B'), self.ai)
        self.parent.begin_game(gameinfo, field)

    def load(self): #TODO
        load_game = load('load_game.txt')
        if load_game:
            gameinfo = load_game[0]
            field = load_game[1]
            self.parent.begin_game(gameinfo, field)
            self.close()
        else:
            self.close_buttons()
            self.no_load_game_button.show()

