from puzzle import *

if __name__ == '__main__':
    p = Puzzle()
    while p.start_game():
        p.create_new_board()
