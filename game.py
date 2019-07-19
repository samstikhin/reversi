from simple_objects.rock import Rock
from simple_objects.field import create_field_from_str
from simple_objects.ai import AI
from simple_objects.gameinfo import GameInformation


class Game:
    def __init__(self, info, field, parent=None):
        self.parent = parent
        self.field = field
        self.info = info
        self.info.game_over = False
        self.set_new_pos_moves()

    def end_game(self, rock):
        self.info.game_over = True
        if str(rock) == 'W':
            self.info.white_points = -1
        else:
            self.info.black_points = -1
        self.parent.check_end_game()

    def change_player(self):
        self.info.curr_player = self.info.curr_player.invert()

    def set_new_pos_moves(self):
        self.info.pos_moves = self.field.get_pos_moves(self.info.curr_player)

    def reset_points(self):
        self.info.white_points = self.field.count_rocks(Rock('W'))
        self.info.black_points = self.field.count_rocks(Rock('B'))

    def add_step_to_undo_stack(self):
        self.info.undo_stack.append(str(self.field))

    def create_field_from_undo_stack(self):
        self.field = create_field_from_str(
            self.info.undo_stack[len(self.info.undo_stack)-1])

    def new_path_after_undo(self):
        self.add_step_to_undo_stack()
        self.info.redo_stack = []

    def player_move(self, coord):
        pos = self.info.pos_moves
        if not pos:
            self.info.log_add_no_pos_moves()
            self.change_player()
        elif coord in pos:
            rock_to_invert = self.field.move(self.info.curr_player, coord)
            self.info.log_add_move(coord, rock_to_invert)
            self.change_player()
        else:
            self.info.log_add_incorrect_move(coord)
        self.set_new_pos_moves()
        self.reset_points()
        self.new_path_after_undo()

    def comp_move(self):
        if not self.info.vs_player and not self.info.game_over \
                and self.info.curr_player == self.info.comp.rock:
            move = self.info.comp.get_comp_move(self.field)
            if move:
                rocks_to_invert = \
                    self.field.move(self.info.comp.rock, move)
                self.info.log_add_move(move, rocks_to_invert)
                self.change_player()
            else:
                self.info.log_add_no_pos_moves()
                self.change_player()
            self.set_new_pos_moves()
            self.reset_points()
        self.check_end_game()
        self.miss_move()

    def miss_move(self):
        if not self.info.pos_moves and not self.info.game_over:
            self.info.log_add_no_pos_moves()
            self.add_step_to_undo_stack()
            self.change_player()
            self.set_new_pos_moves()

    def check_end_game(self):
        if (not self.field.get_pos_moves(Rock('B')) and
                not self.field.get_pos_moves(Rock('W'))) \
                or self.info.game_over:
            self.info.log_add_game_over()
            if self.info.white_points > self.info.black_points:
                result = 'GAME OVER: WHITE WON'
            elif self.info.white_points < self.info.black_points:
                result = 'GAME OVER: BLACK WON'
            else:
                result = 'GAME OVER: DRAW'
            self.info.game_over = True
            return result
        else:
            return None

    def undo(self):
        self.info.redo_stack.append(self.info.undo_stack.pop())
        self.create_field_from_undo_stack()
        if self.info.vs_player:
            self.change_player()
            self.info.log_undo()
        else:
            self.info.log_undo()
            self.info.log_undo()
        self.set_new_pos_moves()
        self.reset_points()

    def redo(self):
        self.info.undo_stack.append(self.info.redo_stack.pop())
        self.create_field_from_undo_stack()
        if self.info.vs_player:
            self.change_player()
            self.info.log_redo()
        else:
            self.info.log_redo()
            self.info.log_redo()
        self.set_new_pos_moves()
        self.reset_points()

    def save(self):
        new_file = open('load_game.txt', "w+")
        new_file.write(str(self.field)+'&&&')
        new_file.write(str(self.info.count_of_players))
        new_file.write(str(self.info.curr_player))
        if not self.info.vs_player:
            new_file.write('&&&'+str(self.info.comp))
        new_file.close()


def load(filename):
    try:
        with open(filename, encoding='utf-8') as f:
             load_game = f.read().split('&&&')
    except FileNotFoundError:
        return False
    if load_game != ['']:
        count_of_players = int(load_game[1][0])
        curr_player = Rock(load_game[1][1])
        if count_of_players == 2:
            ai = None
        else:
            ai = AI(Rock(load_game[2][0]), load_game[2][1])
        field = create_field_from_str(load_game[0])
        gameinfo = GameInformation(count_of_players, curr_player, ai)
        return (gameinfo, field)
    else:
        return False


