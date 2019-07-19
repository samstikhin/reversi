class Coord:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if type(other) != type(self):
            return False
        if self.x == other.x and self.y == other.y:
            return True
        else:
            return False

    def __hash__(self):
        return hash((self.x, self.y))

    def __add__(self, other):
        return Coord(self.x+other.x, self.y+other.y)

    def __sub__(self, other):
        return Coord(self.x-other.x, self.y-other.y)

    def __str__(self):
        return '('+str(self.x)+', '+str(self.y)+')'
