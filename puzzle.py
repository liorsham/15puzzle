import random
import math
import datetime
import time
import os

clear = lambda: os.system('clear')

LEFT='4'
RIGHT='6'
UP='8'
DOWN='2'

class Puzzle:

    def __init__(self, row_count=4):
        if row_count < 2:
            print("setting row_count to 2 (received {} - illegal!)".format(row_count))
            row_count = 2
        self.row_count = row_count
        self.demo_mode = False
        self.create_initial_random_state()
        self.key_to_action = {}
        for k in ['2', '4', '6', '8']:
            self.key_to_action[k] = self.move
        self.key_to_action['i'] = self.print_instructions
        self.key_to_action['n'] = self.create_new_board

    def create_initial_random_state(self):
        self.moves_counter = 0
        self.start_time = datetime.datetime.now()
        data = list(range(int(math.pow(self.row_count,2))))
        random.shuffle(data)
        self.matrix = [[data[x+y*self.row_count] for x in range(self.row_count)] for y in range(self.row_count)]
        self.board_done = False
        self.find_zero_location()

    def find_zero_location(self):
        for i in range(self.row_count):
            for j in range(self.row_count):
                if self.matrix[i][j] == 0:
                    self.zero_x = i
                    self.zero_y = j
                    return True
        print("illegal board! couldn't find zero location!")
        return False


    def print_current_state(self):
        for i in range(self.row_count):
            for j in range(self.row_count):
                print("{}\t".format(self.matrix[i][j] if self.matrix[i][j] > 0 else " "), end='')
            print('')

    def create_new_board(self, args=None):
        clear()
        self.create_initial_random_state()
        self.print_current_state()

    def start_game(self, demo_mode = False):
        self.demo_mode = demo_mode
        self.print_instructions()
        self.print_current_state()
        user_input = None
        while user_input != 'q' and not self.board_done:
            if not self.demo_mode:
                user_input = input() #getch.getch() #screen.getch()
                try:
                    user_input = user_input[-1].lower()
                except:
                    user_input = None
            else:
                user_input = random.choice(['4','8', '6', '2'])
                time.sleep(0.2)
            if user_input is not None:
                if user_input in self.key_to_action: # ['4','8', '6', '2']: # [curses.KEY_RIGHT, curses.KEY_LEFT, curses.KEY_UP, curses.KEY_DOWN]:
                    self.key_to_action[user_input](user_input)
                elif user_input != 'q':
                    print("received illegal command: {}".format(user_input))
                    self.print_instructions()
        if self.board_done:
            print("good job! you finished the game in {} and {} moves".format(datetime.datetime.now()-self.start_time, self.moves_counter))
        print("Bye bye!")

    def print_instructions(self, args=None):
        print("use the following commands: ")
        print("arrow keys: moving (use NumLock keys + Enter for now..)")
        print("n: create new random board")
        print("i: instructions")
        print("q: quit")
        print("Enjoy!")


    def move(self, direction):
        if (direction == UP and self.zero_x == self.row_count-1)\
        or (direction == DOWN and self.zero_x == 0)\
        or (direction == RIGHT and self.zero_y == 0)\
        or (direction == LEFT and self.zero_y == self.row_count-1):
            print("illegal move! you can't move there")
            return False
        self.moves_counter +=1
        new_x, new_y = self.zero_x, self.zero_y
        if direction == UP:
            new_x+=1
        elif direction == DOWN:
            new_x-=1
        elif direction == RIGHT:
            new_y-=1
        elif direction == LEFT:
            new_y+=1
        else:
            print("received illegal direction! ({})".format(direction))
            return False

        self.matrix[self.zero_x][self.zero_y] = self.matrix[new_x][new_y]
        self.matrix[new_x][new_y] = 0
        self.zero_x, self.zero_y = new_x, new_y
        clear()
        self.print_current_state()
        if self.zero_y == self.row_count-1 and self.zero_x == self.row_count-1:
            self.check_if_done()
        return True

    def check_if_done(self):
        self.board_done = False
        for i in range(self.row_count):
            for j in range(self.row_count):
                if i == self.row_count-1 and j == self.row_count-1:
                    if self.matrix[i][j] != 0:
                        return False
                elif self.matrix[i][j] != i*self.row_count+1+j:
                    return False
        self.board_done = True
        return True