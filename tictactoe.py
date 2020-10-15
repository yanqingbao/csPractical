#Objective: Coding Tic Tac Toe from scratch
'''
Step 0: Create a game class

Input a move through the command line (have clear instructions for them)
Write make_move function that will take in a location [r,c] and a mark type ('X' or 'O')
Validate it (and give clarification if the user input is wrong)
Keep going until the board is full!
Detect if a player has won!
Provide the option for the players to play again after the game has ended.
Step 1: Create board class

Display current board status in the terminal and ask for the next move
Step 2: Create human player class

Write a second player or agent that takes the board and plays a random move
Use input() from a command line
Step 2: Create an agent class

Use either input() from a command line or a random number generated directly from your script
Step 3: Add in conditional breaks

Spot is taken
Board is full
Valid inputs

'''
import sys

class TicTacToe:
    def __init__(self, size = 3): # assume only 3 by 3
        self.size = size
        # self.board = [[None] * size] * size # this creats alias 
        self.board = [[None for i in range(size)] for i in range(size)]
        self.curPlayer = 'X' # swtich from 'X' and 'O'
        self.moveCount = 0

    def ask_input(self):
        rc = input(f'Player: {self.curPlayer} Please give row and col as r,c : \n')
        rc = rc.split(',')
        rc[0], rc[1] = int(rc[0]), int(rc[1])
        return rc    


    def make_move(self, rc):
        self.isValidMove(rc)
        row = rc[0]
        col = rc[1]
        self.board[row][col] = self.curPlayer

        self.moveCount += 1



    def isBoardFull(self):
        return self.moveCount >= self.size ** 2
 

    def isWin(self): # only for 3 by 3 
        player = self.curPlayer
        if self.check_row(player) or self.check_col(player) or self.check_diag(player):
            return True
        else:
            return False


    def check_row(self, player):
        for ii in range(self.size):
            if self.board[ii] == [player] * self.size and self.board[ii][0]:
                return True
        else:
            return False

    def check_col(self, player):
        for ii in range(self.size):
            if self.board[0][ii] == player and self.board[1][ii] == player and self.board[2][ii] == player and self.board[0][ii]:
                return True
        else:
            return False


    def check_diag(self, player):
        if (self.board[0][0] == player and self.board[1][1] == player and self.board[2][2] == player and self.board[0][0]) or (self.board[0][2] == player and self.board[1][1] == player and self.board[2][0] == player and self.board[0][2]):
            return True
        else:
            return False
                


    def isValidMove(self, rc): # check if is occupied
        if rc[0] >= 0 and rc[0] < self.size and rc[1] >= 0 and rc[1] < self.size:
            if not self.board[rc[0]][rc[1]]:
                return True
        else:
            return False

    def switchPlayer(self):
        if self.curPlayer == 'X':
            self.curPlayer = 'O'
        else:
            self.curPlayer = 'X'



    def refreshGame(self):
        self.board = [[None for i in range(self.size)] for i in range(self.size)]
        self.moveCount = 0
        self.curPlayer = 'X'
    
    def print_board(self):
        print('Current board:\n')
        line_0 = self.board[0]
        line_1 = self.board[1]
        line_2 = self.board[2]
        print(f'{line_0}\n')
        print(f'{line_1}\n')
        print(f'{line_2}\n')
        print('\n')


    def play_game(self):
        while not self.isBoardFull() and (not self.isWin()):
            rc = self.ask_input()
            while not self.isValidMove(rc):
                print('Invalid Move!\n')
                rc = self.ask_input()
            
            self.make_move(rc)
            self.print_board()

            if self.isWin():
                print(f'Congrats: {self.curPlayer} wins the game!!\n')
                self.check_refresh()

            self.switchPlayer()            

        print(f'Game is a tie!')
        self.check_refresh()
        # sys.exit()
        




    def check_refresh(self):
        want_to_refresh = input(f'Game is over! Type in \'True\', if you want to restart. Type in others to end the game.\n')
        if want_to_refresh == 'True':
            self.refreshGame()
            star_line = '*' * 42
            print(f'{star_line}')
            print(f'{star_line}')
            print('Lets play again')
            print(f'{star_line}')
            print(f'{star_line}')
            self.print_board()
            self.play_game()
        else:
            
            print('@' * 42)
            print('@' * 42)
            print('Good Bye!')
            print('@' * 42)
            print('@' * 42)
            print('\n')
            sys.exit()
        
# class board(self)

if __name__ == "__main__":
    game = TicTacToe()
    game.print_board()
    game.play_game()


'''
if __name__ == "__main__":

        game = TicTacToe()
        game.print_board()
        game.play_game()
'''        
