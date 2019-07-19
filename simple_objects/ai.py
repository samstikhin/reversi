from random import randint


class AI:
    def __init__(self, rock, difficult):
        self.rock = rock
        self.color = rock.color
        self.diff = difficult

    def __str__(self):
        return str(self.rock)+str(self.diff)

    def get_best_move(self, field):
        pos_moves = field.get_pos_moves(self.rock)
        best_move = None
        best_move_len = 0
        for coord in pos_moves:
            if best_move_len < len(field.is_pos_move(self.rock, coord)):
                best_move = coord
                best_move_len = len(field.is_pos_move(self.rock, coord))
        if best_move is None:
            return False
        return best_move

    def get_worst_move(self, field):
        pos_moves = field.get_pos_moves(self.rock)
        worst_move = None
        worst_move_len = 100000000
        for coord in pos_moves:
            if worst_move_len > len(field.is_pos_move(self.rock, coord)):
                worst_move = coord
                worst_move_len = len(field.is_pos_move(self.rock, coord))
        if worst_move is None:
            return False
        return worst_move

    def get_random_move(self, field):
        pos_moves = field.get_pos_moves(self.rock)
        random_move = pos_moves[randint(0, len(pos_moves)-1)]
        return random_move

    def get_comp_move(self, field):
        if self.diff == 'E':
            return self.get_worst_move(field)
        elif self.diff == 'M':
            return self.get_random_move(field)
        elif self.diff == 'H':
            return self.get_best_move(field)
        else:
            raise Exception('ai diff')
