class Rock:
    def __init__(self, color):
        self.x = None
        self.y = None
        self.color = color
        if self.color == 'W':
            self.vs_color = 'B'
        else:
            self.vs_color = 'W'

    def __str__(self):
        return self.color

    def __eq__(self, other):
        if type(other) != type(self):
            return False
        if other.color == self.color:
            return True
        else:
            return False

    def set_coord(self, coord):
        self.x = coord.x
        self.y = coord.y

    def invert(self):
        if self.color == 'W':
            return Rock('B')
        else:
            return Rock('W')

