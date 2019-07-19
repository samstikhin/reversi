from simple_objects.exceptions import ImpossibleAction


class GameInformation:
    def __init__(self, count_of_players, curr_player, ai=None):
        self.time_for_player1 = 1000
        self.time_for_player2 = 100
        self.count_of_players = count_of_players
        self.game_over = True
        self.white_points = 0
        self.black_points = 0
        self.curr_player = curr_player
        self.pos_moves = []
        self.log = ['Begining of the game']
        self.anti_log = []
        self.undo_stack = []
        self.redo_stack = []

        if count_of_players == 2:
            self.vs_player = True
        elif count_of_players == 1:
            self.vs_player = False
            self.comp = ai
            self.player = self.comp.rock.invert()
        else:
            raise ImpossibleAction('Impossible count of players')

    def log_add_move(self, coord, rocks_to_invert):
        clr = str(self.curr_player)
        log = clr + ':' + str(coord) + '-> invert to ' + clr
        for rock_coord in rocks_to_invert:
            log += ' ' + str(rock_coord)
        log += '\n'
        self.log.append(log)

    def log_add_no_pos_moves(self):
        clr = str(self.curr_player)
        self.log.append('No pos. moves for '+clr+'player, change player' + '\n')

    def log_add_incorrect_move(self, coord):
        clr = str(self.curr_player)
        self.log.append(clr+'-'+str(coord)+': Incorrect move'+'\n')

    def log_add_game_over(self):
        self.log.append('GAME OVER'+'\n')

    def log_undo(self): #refactor
        if self.log:
            self.anti_log.append(self.log.pop())
        else:
            raise ImpossibleAction('log')

    def log_redo(self):
        if self.anti_log:
            self.log.append(self.anti_log.pop())
        else:
            raise ImpossibleAction('anti_log')


