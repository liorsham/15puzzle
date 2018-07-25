from puzzle import *

import unittest

class TestPuzzle(unittest.TestCase):

    def test_sanity(self):
        p = Puzzle()
        self.assertTrue(p.find_zero_location())
        self.assertFalse(p.check_if_done())

    def create_solved_puzzle(self):
        p = Puzzle()
        data = list(range(int(math.pow(p.row_count, 2))))
        data.append(data.pop(0))
        p.matrix = [[data[x + y * p.row_count] for x in range(p.row_count)] for y in range(p.row_count)]
        p.find_zero_location()
        return p

    def test_complete_puzzle(self):
        p = self.create_solved_puzzle()
        self.assertTrue(p.check_if_done())

    def test_illegal_moves(self):
        p = self.create_solved_puzzle()
        self.assertFalse(p.move(UP))
        self.assertFalse(p.move(LEFT))
        for i in range(p.row_count-1):
            self.assertTrue(p.move(RIGHT))
            self.assertTrue(p.move(DOWN))
        self.assertFalse(p.move(RIGHT))
        self.assertFalse(p.move(DOWN))


if __name__ == '__main__':
    unittest.main()