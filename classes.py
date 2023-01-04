# -*- coding: utf-8 -*-
'''
Project name:Dots and Boxes
Author: PengFei Li,ig22317
Course Name: SDPA
Description: all classes need to finish the game
'''
import random


class Board(): #Create the class of Board
    def __int__(self,row,col):
        self.row = row
        self.col = col
        self.moves = []
        self.board = self.createBoard()

    def createBoard(self):
        board = []
        for i in range(self.row - 1):#Iterate, create row
            row_t = []
            for j in range(self.col - 1): #Iterate, create column
                col_t = [0,0,0,0,'']   #Left, top, right, bottom
                row_t.append(col_t) #concat the row_t and col_t
            board.append(row_t)
        return board

    def getBoard(self): #easy to get board
        return self.board

    def checkMoves(self,px1,py1,px2,py2): #Check if the movement makes sense
        if [px1,py1,px2,py2] in self.moves or [px2, py2, px1, py1] in self.moves:
            return  False
        return True

    def addMove(self,px1,py1,px2,py2):  #class of adding movement
        self.moves.append([px1,py1,px2,py2])

    def change_Board(self,x,y,pos):  #Draw the edges and modify the attribution of the grid
        self.board[x][y][pos] = 1

    def check_Board(self):#Check if there are new scores, and if the name should be filled into the board
        new_score = 0
        for i in range(self.row -1):
            for j in range(self.col -1):
                flag = 0
                for k in range(4):
                    flag += self.board[i][j][k]
                if flag == 4 and self.board[i][j][4] == '':
                    self.board[i][j][4] = self.id
                    new_score += 1

        if new_score == 0:
            self.switchPlayer() #class of changing the player
        return new_score

    def setPlayer(self,id1,id2,order):  #class of selecting the palyer and setting
        self.id1 = id1
        self.id2 = id2
        if order == 0: #Randomly determine the order of players
            self.id = self.id1
            print('Player 1 moves firstly:')
        else:
            self.id =self.id2
            print('Player 2 moves firstly:')

    def switchPlayer(self):
        if self.id ==self.id1: #Determine if the id is the same, otherwise it will automatically change to id1 player
            self.id = self.id2
        else:
            self.id = self.id1

    def print_Board(self):
        for i in range(1,self.row +1):
            if i < self.row:
                for j in range(1,self.col +1): #Print the horizontal of the chessboard
                    if j < self.col:
                        if self.board[i - 1][j - 1][1] ==1:
                            print(f"({i}, {j})--", end='')
                        else:
                            print(f"({i}, {j})  ", end='')
                    else:
                        print(f"({i}, {j})")

                for j in range(1,self.col +1): #Print the vertical of the chessboard
                    if j < self.col:
                        if self.board[i - 1][j - 1][0] ==1:
                            print("   | ", end='')
                        else:
                            print(f"    ", end='')

                        if self.board[i - 1][j - 1][4] != "":
                            print(f" {self.board[i - 1][j - 1][4]}", end='')
                        else:
                            print("   ", end='')

                    else:
                        if self.board[i - 1][j - 2][2] == 1:
                            print("   | ")
                        else:
                            print("    ")
            else:
                for j in range(1, self.col + 1):  # 横
                    if j < self.col:
                        if self.board[i - 2][j - 1][3] == 1:
                            print(f"({i}, {j})--", end='')
                        else:
                            print(f"({i}, {j})  ", end='')
                    else:
                        print(f"({i}, {j})")


class Player(): #class of player
    def __int__(self,id):
        self.id = id
        self.score = 0

class ComputerPlayer(Player): #Create the computer player
    def __init__(self, id):
        super().__init__(id)

    def generateMove(self, board): #The computer can automatically move
        row = len(board)
        col = len(board[0])
        # print("row, col", row, col)

        # Find the side where you can score one point at a time
        for i in range(row):
            for j in range(col):
                sum_t = board[i][j][0] + board[i][j][1] + board[i][j][2] + board[i][j][3]
                if sum_t == 3:
                    if board[i][j][0] == 0:
                        return i + 1, j + 1, i + 2, j + 1
                    elif board[i][j][1] == 0:
                        return i + 1, j + 1, i + 1, j + 2
                    elif board[i][j][2] == 0:
                        return i + 1, j + 2, i + 2, j + 2
                    else:
                        return i + 2, j + 1, i + 2, j + 2

        # If there is no position where can score, just randomize a position.
        i = random.randint(0, row - 1)
        j = random.randint(0, col - 1)
        k = random.randint(0, 3)
        while board[i][j][4] != "":
            i = random.randint(0, row - 1)
            j = random.randint(0, col - 1)

        while board[i][j][k] == 1:
            k = random.randint(0, 3)

        # print(i, j, k)
        if k == 0:
            return i + 1, j + 1, i + 2, j + 1
        elif k == 1:
            return i + 1, j + 1, i + 1, j + 2
        elif k == 2:
            return i + 1, j + 2, i + 2, j + 2
        else:  # k==3
            return i + 2, j + 1, i + 2, j + 2

class HumanPlayer(Player):
    def __int__(self,id):
        super().__init__(id) #Call the id of the parent class Player

    def generateMove(self,board): #
        move = input("Input move:(Please be like the form of (x1,y1)-(x2,y2)").split('-')
        px1 = int(move[0][1])
        py1 = int(move[0][3])
        px2 = int(move[1][1])
        py2 = int(move[1][3])
        return px1,py1,px2,py2


#Add intelligent computer players, equivalent to computer players with optimized algorithms
class SmartComputerPlayer(Player):
    def __int__(self,id):
        super().__init__(id)

    def generateMove(self, board):
        row = len(board)
        col = len(board[0])
        # print("row, col", row, col)

        # Here's a computer strategy to add. The priority is to find the one that adds two points at a time, then the one point
        # Two points at a time, only down or right
        for i in range(row):
            # Deal with the lower side first
            if i < row - 1:  # The last line is not processed
                for j in range(col):
                    if board[i][j][3] == 0 and board[i][j][0] == 1 and board[i][j][1] == 1 and board[i][j][2] == 1:
                        if board[i + 1][j][0] == 1 and board[i + 1][j][2] == 1 and board[i + 1][j][3] == 1 and \
                                board[i + 1][j][1] == 0:
                            return i + 2, j + 1, i + 2, j + 2

            # deal with right
            for j in range(col - 1):
                if board[i][j][0] == 1 and board[i][j][1] == 1 and board[i][j][3] == 1 and board[i][j][2] == 0:
                    if board[i][j + 1][0] == 0 and board[i][j + 1][1] == 1 and board[i][j + 1][2] == 1 and \
                            board[i][j + 1][3] == 1:
                        return i + 1, j + 2, i + 2, j + 2

        # Find a position where you can add one point at a time
        for i in range(row):
            for j in range(col):
                sum_t = board[i][j][0] + board[i][j][1] + board[i][j][2] + board[i][j][3]
                if sum_t == 3:
                    if board[i][j][0] == 0:
                        return i + 1, j + 1, i + 2, j + 1
                    elif board[i][j][1] == 0:
                        return i + 1, j + 1, i + 1, j + 2
                    elif board[i][j][2] == 0:
                        return i + 1, j + 2, i + 2, j + 2
                    else:
                        return i + 2, j + 1, i + 2, j + 2

        # If there is no position that can score, just randomize a position.
        i = random.randint(0, row - 1)
        j = random.randint(0, col - 1)
        k = random.randint(0, 3)
        while board[i][j][4] != "":
            i = random.randint(0, row - 1)
            j = random.randint(0, col - 1)

        while board[i][j][k] == 1:
            k = random.randint(0, 3)

        # print(i, j, k)
        if k == 0:
            return i + 1, j + 1, i + 2, j + 1
        elif k == 1:
            return i + 1, j + 1, i + 1, j + 2
        elif k == 2:
            return i + 1, j + 2, i + 2, j + 2
        else:  # k==3
            return i + 2, j + 1, i + 2, j + 2















