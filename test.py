#!/usr/bin/python3
import unittest

from simple_objects.field import Field
from simple_objects.coord import Coord
from simple_objects.rock import Rock


class TestChecks(unittest.TestCase):

    def test_in_borders(self):
        f = Field(8, 8)
        self.assertEqual(True, f.in_borders(Coord(2, 4)))
        self.assertEqual(False, f.in_borders(Coord(2, 8)))
        self.assertEqual(False, f.in_borders(Coord(2, -1)))
        self.assertEqual(False, f.in_borders(Coord(2, 80)))
        self.assertEqual(False, f.in_borders(Coord(8, 2)))
        self.assertEqual(False, f.in_borders(Coord(-2, 2)))
        self.assertEqual(False, f.in_borders(Coord(20, 2)))

    def test_get_points_by_one_dir(self):
        f = Field(8, 8)
        f.add_rock(Rock('W'), Coord(2, 4))
        f.add_rock(Rock('W'), Coord(2, 5))
        f.add_rock(Rock('B'), Coord(2, 6))

        f.add_rock(Rock('W'), Coord(1, 3))
        f.add_rock(Rock('W'), Coord(0, 3))

        f.add_rock(Rock('W'), Coord(3, 1))

        f.add_rock(Rock('W'), Coord(3, 3))
        f.add_rock(Rock('W'), Coord(4, 3))
        f.add_rock(Rock('W'), Coord(5, 3))
        f.add_rock(Rock('W'), Coord(6, 3))
        f.add_rock(Rock('B'), Coord(7, 3))

        f.add_rock(Rock('W'), Coord(1, 2))
        f.add_rock(Rock('B'), Coord(0, 1))

        self.assertSetEqual({Coord(2, 5), Coord(2, 4)},
                            set(f.get_points_by_one_dir(Rock('B'),
                                                        Coord(2, 3),
                                                        Coord(0, 1))))
        self.assertSetEqual({Coord(6, 3), Coord(5, 3),
                             Coord(4, 3), Coord(3, 3)},
                            set(f.get_points_by_one_dir(Rock('B'),
                                                        Coord(2, 3),
                                                        Coord(1, 0))))
        self.assertEqual([],
                         f.get_points_by_one_dir(Rock('B'),
                                                 Coord(2, 3), Coord(-1, 0)))
        self.assertSetEqual({Coord(1, 2)},
                            set(f.get_points_by_one_dir(Rock('B'),
                                                        Coord(2, 3),
                                                        Coord(-1, -1))))
        self.assertEqual([],
                         f.get_points_by_one_dir(Rock('B'),
                                                 Coord(2, 3), Coord(0, -1)))

    def test_is_pos_move(self):
        f = Field(8, 8)
        f.add_rock(Rock('W'), Coord(2, 4))
        f.add_rock(Rock('W'), Coord(2, 5))
        f.add_rock(Rock('B'), Coord(2, 6))

        f.add_rock(Rock('W'), Coord(1, 3))
        f.add_rock(Rock('W'), Coord(0, 3))

        f.add_rock(Rock('W'), Coord(3, 1))

        f.add_rock(Rock('W'), Coord(3, 3))
        f.add_rock(Rock('W'), Coord(4, 3))
        f.add_rock(Rock('W'), Coord(5, 3))
        f.add_rock(Rock('W'), Coord(6, 3))
        f.add_rock(Rock('B'), Coord(7, 3))

        f.add_rock(Rock('W'), Coord(1, 2))
        f.add_rock(Rock('B'), Coord(0, 1))

        self.assertSetEqual({Coord(2, 4), Coord(2, 5), Coord(6, 3),
                             Coord(5, 3), Coord(4, 3), Coord(3, 3),
                             Coord(1, 2)},
                            set(f.is_pos_move(Rock('B'), Coord(2, 3))))
        self.assertEqual(False, f.is_pos_move(Rock('B'), Coord(3, 3)))

    def test_get_pos_move(self):
        f = Field(8, 8)
        f.arrange_rocks()

        self.assertSetEqual({Coord(4, 2), Coord(2, 4),
                             Coord(3, 5), Coord(5, 3)},
                            set(f.get_pos_moves(Rock('B'))))
        self.assertEqual(False, f.is_pos_move(Rock('B'), Coord(3, 3)))

if __name__ == "__main__":
    unittest.main()
