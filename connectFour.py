"""If you want to play Connect-Four, try it out your self here first!

Step 1: BOARD

User input grid size, start with a 4*4.
Step 2: DROP PIECE

Place piece in board, alternating between players 1 and 2.
Pieces will stack on top of each other so make sure you build from the bottom up.
Step3: WINNING MOVE

The game should work for two players and tell you when you have won, be it horizontal vertical or diagonal (4 in a row).
Step 4: MOVE IS VALID

Check for excepts: "Illegal move", "This column is full. Try another one!", "The board is full!"
[execution time limit] 16 seconds (py3)
"""
class Board:
    def __init__(self, row = 4, col = 4):
        self.row = row
        self.col = col
        self.board = [[None for i in range(col)] for i in range(row)]
        self.colCounter = [0 for i in range(col)]
        self.numMoves = 0
    
    def isFull(self):
        return self.numMoves >= self.row * self.col

    def updateBoard(self, c, marker): # update the board with (r, c) and player marker
        self.board[self.row - self.colCounter[c] - 1][c] = marker
        self.colCounter[c] += 1
        self.numMoves += 1

    def isValidMove(self, c):  # check if give position is occupied
        return c >= 0 and c < self.col and self.colCounter[c] < self.col

    def isWin(self, marker): # check given player marker has won or not
        return self.checkRowWin(marker) or self.checkColWin(marker) or self.checkDiagWin(marker)

    def checkRowWin(self, marker):
        for r in range(self.row):
            for c in range(self.col - 3):
                if self.board[r][c : c + 4] == [marker] * 4:
                    return True
        return False

    def checkColWin(self, marker):
        for c in range(self.col):
            if self.colCounter[c] >= 4:
                for r in range(self.row - 3):

                    if self.board[r][c] == marker and self.board[r + 1][c] == marker and self.board[r + 2][c] == marker and self.board[r + 3][c] == marker:
                        return True
        return False

    def checkDiagWin(self, marker):
        r_end = self.row - 4 + 1
        c_end = self.col - 4 + 1

        # back slash direction
        for r in range(r_end):
            for c in range(c_end):
                if self.board[r][c] == marker and self.board[r + 1][c + 1] == marker and self.board[r + 2][c + 2] == marker and self.board[r + 3][c + 3] == marker:
                    return True
        # forward slash direction
        for r in range(r_end):
            for c in range(c_end):
                if self.board[self.row - r - 1][c] == marker and self.board[self.row - r - 1 - 1][c + 1] == marker  and self.board[self.row - r - 1 - 2][c + 2] == marker  and self.board[self.row - r - 1 - 3][c + 3] == marker :
                    return True
        
        return False


    def printBoard(self):
        for r in range(self.row):
            print(self.board[r])
        print('+' * 42)
        print('+' * 42)


class Player:
    def __init__(self, name:str, marker:str):
        self.name = name
        self.marker = marker

    def propose_a_move(self, board):
        import random
        col = board.row
        return random.randrange(col)

class Game:
    def __init__(self, row:int = 4, col:int = 4, AutoMode:bool = True):
        self.row = row
        self.col = col

        self.board = Board(row, col)
        self.board.printBoard()

        self.playerOne = Player(name = 'Tom', marker = 'X')
        self.playerTwo = Player('Jerry', 'O')

        self.curPlayer = self.playerOne   # Player 1: 'X' and Player 2: 'O'

        self.AutoMode = AutoMode

    def start(self):
        import time
        while not self.board.isFull() and not self.board.isWin(self.curPlayer.marker):
            # time.sleep(0.5)
            print('@' * 42)
            print(f'Hi {self.curPlayer.name}! Make your move now!')
            print('@' * 42)
            if not self.AutoMode:
                col = self.askForCol()
            else:
                col = self.curPlayer.propose_a_move(self.board)

            while not self.board.isValidMove(col):
                print('Invalid move. Out of board or Column is full!')
                if not self.AutoMode:
                    col = self.askForCol()
                else:
                    col = self.curPlayer.propose_a_move(self.board)
            self.board.updateBoard(col, self.curPlayer.marker)
            print(f'--------Move No. {self.board.numMoves}--------')
            self.board.printBoard()
            if self.board.isWin(self.curPlayer.marker):
                print('$' * 24)
                print(f'Congrats to Player: {self.curPlayer.name}!')
                print('$' * 24)
            else:
                self.switchPlayer()

        if self.board.isFull():
            print(f'Tie game, board is full!\n')
        
    def switchPlayer(self):
        if self.curPlayer == self.playerOne:
            self.curPlayer = self.playerTwo
        else:
            self.curPlayer = self.playerOne


    def askForCol(self) -> int:
        print(f'Hello Player: {self.curPlayer.name}\n')
        col = input('Please enter the col to play: ')
        while not col:
            col = input('Please enter the col to play: ')
        return int(col)
# attempt 3 classes
# class Board, board, numMoves, method(isFull, )
# class Player
# class Game

if __name__ == '__main__':
    game = Game(6,6)
    game.start()
