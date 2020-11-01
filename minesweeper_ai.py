import random
import string
import string
import re
import numpy as np
import time
words = string.ascii_lowercase


class board:
    def __init__(self, n_grid=None):
        if n_grid == None:
            n_grid = 9
        self.n_grid = n_grid
        self.cur = [[' ' for _ in range(self.n_grid)] for _ in range(self.n_grid)]
        # self.generate_alphabetanumbers(n_grid)
        # print(words)



    def __repr__(self):
        # structured print for the board
        res = ''
        for i in range(2*(self.n_grid+1)):
            if i == 0:
                res += ' ' * 6
                res += '   '.join(words[:self.n_grid])
                # res += '   '.join(self.letter_labels)
                res += ' ' * 2
                res += '\n'
                continue
            if i % 2 == 1:
                res += ' ' * 4  + '-'* (4*self.n_grid+1) + '\n'
                continue
            res += str(i//2) + ' '*(4-len(str(i//2))) + '| ' + ' | '.join(self.cur[(i-1)//2]) + ' |\n'
        return res



    def generate_alphabetanumbers(self, n):
        '''
        0 -> a, 1->b, 26->aa
        '''
        output = ''
        while n != 0:
            if len(output) == 0:
                output = string.ascii_lowercase[n%26] + output
            else:
                output = string.ascii_lowercase[n%26 - 1] + output
            n = n // 26
        
        return output


class Player:

    # def __init__(self):

    def get_board(self, board):
        self.board = board
        self.num_grid = len(board.cur)

        return 42

    def make_move(self):
        row = random.randint(0, self.num_grid - 1)
        col = random.randint(0, self.num_grid - 1)

        while self.board.cur[row][col] != ' ':
            row = random.randint(0, self.num_grid - 1)
            col = random.randint(0, self.num_grid - 1)
        
        return (row, col)

        # propose click

        # propose flag


    
class game(board):
    def __init__(self, n_mines=None, n_grid=None, auto_mode = True):
        if n_mines is None:
            n_mines = 10
        if n_grid is None:
            n_grid = 9
        self.mine_map = board(n_grid) # mine board
        self.dis_map = board(n_grid) # display board
        self.n_mines = n_mines
        self.n_grid = n_grid
        # randomly initialize the mine positions
        self.pos_mines = list(map(lambda x: divmod(x, self.n_grid), np.random.choice(self.n_grid**2, self.n_mines, replace=False)))

        # additional store the flagged positions
        self.flags = []
        self.num_revealed = 0 # checking how many flipped
        self.gameover = False
        self.win_game = False
        self.time_over = False

        self.auto_mode = auto_mode
        self.player = Player() # the agent that propose moves


    def play(self):
        """
        Play the game
        """
        print('='*70)
        print("Starting Minesweeper (with {} mines on {}x{} grid.)".format(self.n_mines, self.n_grid, self.n_grid) + '\n')
        print(self.dis_map)
        # print(self.pos_mines)
        print('='*70)
        # print(self.dis_map.cur)
        self.initialize_mine_board()
        # print(self.dis_map)
        # print(self.mine_map)

        self.tic = time.time()
        while not self.win_game and not self.gameover:
            self.print_time_played()

            # Getting Inputs from auto / manual input
            if self.auto_mode:
                self.player.get_board(self.dis_map)
                row, col = self.player.make_move()
                self.click_on_board(row, col)
            else:
                col_row = input('Input the position you want to click:')
                if col_row[-1] == 'f':
                    row, col = self.get_r_c(col_row[:-1])
                    # flag place
                    if (row, col) not in self.flags:
                        self.flag_on_board(row, col)
                    else:
                        print('Already Flagged Here!')
                else:
                    row, col = self.get_r_c(col_row)
                    # click place
                    self.click_on_board(row, col)


            if self.num_revealed == (self.n_grid ** 2 - self.n_mines):
                self.win_game = True

            print(self.dis_map)
            # print(self.mine_map)

        if self.gameover:
            print("You clicked on the mine. You lose! :-(")
            
        if self.win_game:
            print('You win the game')
        want_replay = input("Want a rematch? [y/n]")
        if want_replay == 'y':
            self.__init__(self.n_mines, self.n_grid)
            self.play()
        else:
            print('Good Bye!')



    def flag_on_board(self, r, c):
        if (r, c) not in self.flags:
            self.flags.append((r,c))
            self.dis_map.cur[r][c] = 'F' # Temp mark for flag
        else:
            self.flags.remove((r,c))
            self.dis_map.cur[r][c] = ' '

        return 42


    def click_on_board(self, r, c):
        # click on flags
        if (r,c) in self.flags:
            print('Cannot click on flags! Unflag them first!')
        # click on minei
        elif (r,c) in self.pos_mines:
            self.gameover = True
            self.dis_map.cur[r][c] = '*' # need to do more
        # click on non-zeros
        elif int(self.mine_map.cur[r][c]) > 0:
            self.num_revealed += 1
            self.dis_map.cur[r][c] = self.mine_map.cur[r][c]
        # click on zeros
        elif self.mine_map.cur[r][c] == '0':
            self.reveal_nearby_zeros(r,c)
        return 42

    def reveal_nearby_zeros(self, r, c):
        if self.mine_map.cur[r][c] == '0':
            self.dis_map.cur[r][c] = '0'
            self.num_revealed += 1
        if self.mine_map.cur[r][c] != '0':
            return
        # neib r,c
        r_0 = max(0, r - 1)
        r_1 = min(self.n_grid - 1, r + 1)
        c_0 = max(0, c - 1)
        c_1 = min(self.n_grid - 1, c + 1)

        for ii in range(r_0, r_1 + 1):
            for jj in range(c_0, c_1 + 1):
                if self.dis_map.cur[ii][jj] == ' ' and self.mine_map.cur[ii][jj] == '0':
                    self.reveal_nearby_zeros(ii, jj)
                elif self.dis_map.cur[ii][jj] == ' ' and self.mine_map.cur[ii][jj] != '0':
                    self.dis_map.cur[ii][jj] = self.mine_map.cur[ii][jj]
                    self.num_revealed += 1
        

    def get_r_c(self, rcString): # letter for col and number for row
        letters = 0
        nums = 0
        for ii in range(len(rcString)):
            if rcString[ii] in string.ascii_lowercase:
                letters += letters * 26 + ord(rcString[ii]) - ord('a')
            elif rcString[ii] in string.digits:
                nums += nums * 10 + int(rcString[ii])
            else:
                print('Input only letters and numbers')
        
        row = nums - 1
        col = letters

        return (row, col)


        # Given the locations of the mines, generate the number + mine map
    
    
    
    def initialize_mine_board(self): # get the number of mine map on the mine_map.cur
        self.mine_map
        self.pos_mines

        map_row = len(self.mine_map.cur)
        map_col = len(self.mine_map.cur[0])

        for ii in range(map_row):
            for jj in range(map_col):
                if (ii, jj) not in self.pos_mines:
                    self.mine_map.cur[ii][jj] = self.num_of_neib_mines(ii, jj)

        # Board().cur
        return 42


    def num_of_neib_mines(self, r, c):
        r_0 = max(0, r - 1)
        r_1 = min(self.n_grid - 1, r + 1)
        c_0 = max(0, c - 1)
        c_1 = min(self.n_grid - 1, c + 1)

        counter = 0
        for ii in range(r_0, r_1 + 1):
            for jj in range(c_0, c_1 + 1):
                if ii!=r or jj!=c:
                    if (ii, jj) in self.pos_mines:
                        counter += 1
        return str(counter)

    
    def print_time_played(self):
        mins, secs = divmod(int(time.time() - self.tic), 60)
        print('=' * 42)
        print(f'Time Played: {mins} minutes, {secs} seconds.')
        print('=' * 42)


        

    
    # check on the mine?
    # check on the zeros?
    # if on the number > 0, just display the number




if __name__ == '__main__':
    g = game(10, 10) # Note, so fart the printing cant handle over 26 gird, # n_mines=15, n_grid=12 
    g.play()
 




"""
Step 0: Play a Minesweeper game and/or check out the example below.

Step 1: Take any board length (the board is square) and number of mines

Default is 9x9 board with 10 mines
Now silently thank Amber for gifting you this beautiful board
Step 2: Take user input as x, y coordinates

Easiest to make the rows numbers and columns letters (eg. a5).
Step 3: End the game if they click a mine

Step 4: Reveal the numbers if they click somewhere else.

Step 5: If they click on a square with “zero”, the board propagates the reveal all consecutive 0's (and surrounding numbers) as a convenience method. This is the hardest part!

Step 6: Check edge cases

Tips:
import re
from string import ascii_lowercase
Step 7: Have the player be able to mark the mines

To place or remove a flag, add 'f' to the cell (eg. a5f).
You can also toggle flag (flag: a5)
Step 8: Bonus
Add time played

import time
Minutes, seconds = divmod(int(time.time() - starttime), 60)
Or use a @decorator
Or timeit
time.time or time.clock, see timeit.default_timer
Add animate to the propagation
"""