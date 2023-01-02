# -*- coding: utf-8 -*-
'''
Project name:Dots and Boxes
Author: PengFei Li,ig22317
Course Name: SDPA
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
        for i in range(self,row - 1):#Iterate, create row
            row_t = []
            for j in range(self,col - 1): #Iterate, create column
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