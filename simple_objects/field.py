from simple_objects.rock import Rock
from simple_objects.coord import Coord
from simple_objects.exceptions import ImpossibleAction


class Field:
    directions = [Coord(-1, 0), Coord(-1, -1), Coord(-1, 1),
                  Coord(0, -1), Coord(0, 1),
                  Coord(1, -1), Coord(1, 0), Coord(1, 1)]

    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.squares = {}
        self.coords = []
        for x in range(self.width):
            for y in range(self.height):
                self.coords.append(Coord(x, y))
        for coord in self.coords:
                self.squares[coord] = None

    def add_rock(self, rock, coord):
        self.squares[coord] = rock

    def clear(self):
        for coord in self.coords:
            self.squares[coord] = None

    def arrange_rocks(self):
        self.add_rock(Rock('B'),
                      Coord(self.width/2 - 1, self.height/2 - 1))
        self.add_rock(Rock('W'), Coord(self.width/2 - 1, self.height/2))
        self.add_rock(Rock('W'), Coord(self.width/2, self.height/2 - 1))
        self.add_rock(Rock('B'), Coord(self.width/2, self.height/2))

    def is_pos_move(self, rock, coord):
        points = []
        if not self.in_borders(coord):
            raise ImpossibleAction('coords out of field')
        if self.squares[coord] is not None:
            return False
        for direction in self.directions:
            points.extend(self.get_points_by_one_dir(rock, coord, direction))
        if not points:
            return False
        return points

    def get_points_by_one_dir(self, rock, coord, dir):
        points = []
        new_coord = coord + dir
        if not self.in_borders(new_coord):
            return []
        while self.in_borders(new_coord) \
                and self.squares[new_coord] == rock.invert():
            new_coord = new_coord + dir
        if not self.in_borders(new_coord):
            return []
        if self.squares[new_coord] == rock:
            new_coord = new_coord - dir
            while new_coord != coord:
                points.append(new_coord)
                new_coord = new_coord - dir
        return points

    def in_borders(self, coord):
        return (coord.x < self.width) and (coord.x >= 0) and\
               (coord.y >= 0) and (coord.y < self.height)

    def get_pos_moves(self, rock):
        pos_moves = []
        for coord in self.coords:
            pos = self.is_pos_move(rock, coord)
            if pos:
                if len(pos) > 0:
                    pos_moves.append(coord)
        return pos_moves

    def move(self, rock, coord):
        rocks_for_invert = self.is_pos_move(rock, coord)
        if not rocks_for_invert:
            return False
        self.add_rock(rock, coord)
        for coord in rocks_for_invert:
            self.add_rock(rock, coord)
        return rocks_for_invert

    def count_rocks(self, rock):
        count = 0
        for coord in self.coords:
            if self.squares[coord] == rock:
                count += 1
        return count

    def print_field(self):
        for y in range(self.height):
            print(y, end=' ')
            for x in range(self.width):
                print(self.squares[Coord(x, y)] or '_', end=' ')
            print()
        print(' ', end='')
        for i in range(self.width):
            print(' '+str(i), end='')
        print()

    def __str__(self):
        str_field = ''
        for y in range(self.height):
            for x in range(self.width):
                str_field += str(self.squares[Coord(x, y)] or '_')
            if y != self.height - 1:
                str_field += '\n'
        return str_field


def create_field_from_str(str_field):
    lines = str_field.split('\n')
    height = len(lines)
    width = len(lines[0])
    f = Field(height, width)
    for y in range(height):
        for x in range(width):
            rock = None
            if lines[y][x] == 'B' or lines[y][x] == 'W':
                rock = Rock(lines[y][x])
            f.squares[Coord(x, y)] = rock
    return f
