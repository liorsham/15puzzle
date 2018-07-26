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

    def create_new_board_get_steps(self, p):
        p.last_shuffle_move = None
        p.board_done = True
        moves = []
        while p.board_done:
            p.create_valid_puzzle()
            for i in range(int(pow(2,p.row_count*2))):
                p.last_shuffle_move = random.choice(p.get_valid_moves())
                p.move(p.last_shuffle_move)
                moves.append(p.last_shuffle_move)
            p.check_if_done()
        p.moves_counter = 0
        return moves

    def test_solving_puzzle(self):
        p = Puzzle()
        moves = self.create_new_board_get_steps(p)
        moves.reverse()
        solving_moves = [p.get_opposite_action(a) for a in moves]
        for move in solving_moves:
            self.assertFalse(p.check_if_done())
            p.move(move)
        self.assertTrue(p.check_if_done())



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