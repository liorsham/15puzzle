from puzzle import *

import unittest

class TestPuzzle(unittest.TestCase):

    def test_sanity(self):
        p = Puzzle()
        self.assertFalse(p.check_if_done())

    def create_solved_puzzle(self):
        p = Puzzle()
        p.create_valid_puzzle()
        return p

    def test_complete_puzzle(self):
        p = self.create_solved_puzzle()
        self.assertTrue(p.check_if_done())

    def test_illegal_moves(self):
        p = self.create_solved_puzzle()
        self.assertFalse(p.move(Action.UP))
        self.assertFalse(p.move(Action.LEFT))
        for i in range(p.row_count-1):
            self.assertTrue(p.move(Action.RIGHT))
            self.assertTrue(p.move(Action.DOWN))
        self.assertFalse(p.move(Action.RIGHT))
        self.assertFalse(p.move(Action.DOWN))


if __name__ == '__main__':
    unittest.main()