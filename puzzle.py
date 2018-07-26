import random
import math
import datetime
import os
from enum import Enum

clear = lambda: os.system('clear')

LEFT_KEY='4'
RIGHT_KEY='6'
UP_KEY='8'
DOWN_KEY='2'

class Action(Enum):
    RIGHT = 0
    LEFT = 1
    UP = 2
    DOWN = 3
    INSTRUCTIONS = 4
    QUIT = 5
    NEW_BOARD = 6
    ILLEGAL = 7

key_to_action = {LEFT_KEY: Action.LEFT, RIGHT_KEY: Action.RIGHT, UP_KEY: Action.UP, DOWN_KEY: Action.DOWN, 'i': Action.INSTRUCTIONS, 'q': Action.QUIT, 'n': Action.NEW_BOARD}
opposite_actions = {Action.DOWN: Action.UP, Action.LEFT: Action.RIGHT, Action.UP: Action.DOWN, Action.RIGHT: Action.LEFT}

class Puzzle:

    def __init__(self, row_count=4):
        if row_count < 2:
            print("setting row_count to 2 (received {} - illegal!)".format(row_count))
            row_count = 2
        self.row_count = row_count
        self.moves_counter = 0
        self.create_new_board()

    def create_new_board(self):
        self.last_shuffle_move = None
        self.start_time = datetime.datetime.now()
        self.board_done = True
        while self.board_done:
            self.create_valid_puzzle()
            for i in range(int(pow(2,self.row_count*2))):
                self.last_shuffle_move = random.choice(self.get_valid_moves())
                self.move(self.last_shuffle_move)
            self.check_if_done()
        self.moves_counter = 0

    def get_opposite_action(self, action):
        return opposite_actions[action]

    def get_valid_moves(self):
        legal_moves = [Action.UP, Action.DOWN, Action.RIGHT, Action.LEFT]
        if self.last_shuffle_move is not None:
            legal_moves.remove(self.get_opposite_action(self.last_shuffle_move))
        if self.zero_x <= 0:
            legal_moves.remove(Action.DOWN)
        elif self.zero_x >= self.row_count-1:
            legal_moves.remove(Action.UP)
        if self.zero_y <= 0:
            legal_moves.remove(Action.RIGHT)
        elif self.zero_y >= self.row_count-1:
            legal_moves.remove(Action.LEFT)

        return legal_moves

    def print_puzzle(self):
        for i in range(self.row_count):
            for j in range(self.row_count):
                print("{}\t".format(self.matrix[i][j] if self.matrix[i][j] > 0 else " "), end='')
            print('')


    def get_user_input(self):
        try:
            user_input = input()[-1].lower()
            return key_to_action[user_input]
        except:
           pass
        return Action.ILLEGAL

    def handle_user_action(self, action):
        if action == Action.ILLEGAL:
            print("received illegal action!")
            self.print_instructions()
        elif action == Action.NEW_BOARD:
            clear()
            print("creating new board")
            self.create_new_board()
            self.print_puzzle()
        elif action == Action.QUIT:
            print("Bye bye!")
        elif action == Action.INSTRUCTIONS:
            self.print_instructions()
        else:
            if self.move(action):
                self.check_if_done()
                clear()
                self.print_puzzle()

    def start_game(self):
        self.print_instructions()
        self.print_puzzle()
        action = Action.ILLEGAL
        while not action == Action.QUIT:
            action = self.get_user_input()
            self.handle_user_action(action)

            if self.board_done:
                print("good job! you finished the game in {} and {} moves".format(datetime.datetime.now()-self.start_time, self.moves_counter))
                print("do you want to start a new game? (N/Y)")
                answer = input().lower()
                if answer != 'y':
                    return
                self.handle_user_action(Action.NEW_BOARD)


    def create_valid_puzzle(self):
        data = list(range(int(math.pow(self.row_count, 2))))
        data.append(data.pop(0))
        self.matrix = [[data[x + y * self.row_count] for x in range(self.row_count)] for y in range(self.row_count)]
        self.zero_x = self.row_count-1
        self.zero_y = self.row_count-1

    def print_instructions(self):
        print("use the following commands: ")
        print("arrow keys: moving (use NumLock keys + Enter for now..)")
        print("n: create new random board")
        print("i: instructions")
        print("q: quit")
        print("Enjoy!")

    def get_new_zero_location(self, direction):
        if direction == Action.UP:
            return self.zero_x+1, self.zero_y
        elif direction == Action.DOWN:
            return self.zero_x - 1, self.zero_y
        elif direction == Action.RIGHT:
            return self.zero_x, self.zero_y - 1
        elif direction == Action.LEFT:
            return self.zero_x, self.zero_y + 1
        raise Exception("received illegal direction {}".format(direction))

    def move_empty_to_new_location(self, new_x, new_y):
        self.matrix[self.zero_x][self.zero_y] = self.matrix[new_x][new_y]
        self.matrix[new_x][new_y] = 0
        self.zero_x, self.zero_y = new_x, new_y

    def move(self, direction):
        try:
            new_x, new_y = self.get_new_zero_location(direction)
            for coordinate in [new_x, new_y]:
                if coordinate < 0 or coordinate >= self.row_count:
                    raise Exception("can't move {} in current state".format(direction.name))
        except Exception as ex:
            print(ex)
            return False
        self.moves_counter += 1
        self.move_empty_to_new_location(new_x, new_y)
        return True

    def check_if_done(self):
        self.board_done = False
        if not (self.zero_y == self.row_count - 1 and self.zero_x == self.row_count - 1):
            return False
        for i in range(self.row_count):
            for j in range(self.row_count):
                if i == self.row_count-1 and j == self.row_count-1:
                    if self.matrix[i][j] != 0:
                        return False
                elif self.matrix[i][j] != i*self.row_count+1+j:
                    return False
        self.board_done = True
        return True