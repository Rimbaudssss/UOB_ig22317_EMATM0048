# -*- coding: utf-8 -*-
# @FileName: main.py
# @Software: PyCharm
# @Notes:
'''
Project name:Dots and Boxes
Author: PengFei Li,ig22317
Course Name: SDPA
Description: all code needed to run the game
'''
from classes import Board, ComputerPlayer, HumanPlayer, SmartComputerPlayer
import random

if __name__ == '__main__':
    id1 = input("ID of player1(1 character): ")
    player1 = HumanPlayer(id1)
    id2 = input("ID of player2(1 character): ")
    while id2 == id1:
        id2 = input("ID exists, please input a different id: ")
    opponent = input("Computer (c) or SmartComputer(sc) or Human (H)?(default:H) ").lower()#select the type of player
    if opponent == 'computer' or opponent == "c":

        player2 = ComputerPlayer(id2)
    elif opponent == 'smartcomputer' or opponent == "sc":
        player2 = SmartComputerPlayer(id2)

    else:
        print('The game will start with the default player (H)')
        player2 = HumanPlayer(id2)

    sizes = input("Input the size of board: (Please be like *,*)").split(',')
    row = int(sizes[0])
    col = int(sizes[1])

    sum = (row - 1) * (col - 1)
    board_c = Board(row, col)
    board_c.print_Board()
    board_c.setPlayer(player1.id, player2.id, random.randint(0, 1))
    while True:
        board = board_c.getBoard()
        if board_c.id == player1.id:
            print('Player 1 Inputs move:(Please be like (*,*)-(*,*))')
            px1, py1, px2, py2 = player1.generateMove(board)
        else:
            print('Player 2 Inputs move:(Please be like (*,*)-(*,*))')
            px1, py1, px2, py2 = player2.generateMove(board)
            # print(px1, py1, px2, py2)

        if px1 < 1 or px1 > row or px2 < 1 or px2 > row or py1 < 1 or py1 > col or py2 < 1 or py2 > col:
            print("Input move is not valid.")
            continue

        if board_c.checkMoves(px1, py1, px2, py2):  #Check if move already exists
            board_c.addMove(px1, py1, px2, py2)
        else:
            print("Input move exists.")
            continue

        if px1 == px2 and abs(py1 - py2) == 1:  #Judging the horizontal lines of a chessboard
            if px1 == 1:  # first line
                px, py = 0, min(py1, py2) - 1
                board_c.change_Board(px, py, 1)
            elif px1 == row:  # last line
                px, py = row - 2, min(py1, py2) - 1
                board_c.change_Board(px, py, 3)
            else:
                px, py = px1 - 2, min(py1, py2) - 1
                board_c.change_Board(px, py, 3)  # Bottom edge of the upper grid
                px, py = px1 - 1, min(py1, py2) - 1
                board_c.change_Board(px, py, 1)  # Top edge of the grid below
        elif py1 == py2 and abs(px1 - px2) == 1:  # vertical line
            if py1 == 1:  # first column
                px, py = min(px1, px2) - 1, 0
                board_c.change_Board(px, py, 0)
            elif py1 == col:  # last column
                px, py = min(px1, px2) - 1, col - 2
                board_c.change_Board(px, py, 2)
            else:
                px, py = min(px1, px2) - 1, py1 - 2
                board_c.change_Board(px, py, 2)  # The right side of the left grid
                px, py = min(px1, px2) - 1, py1 - 1
                board_c.change_Board(px, py, 0)  # The left side of the right grid
        else:
            print("Input move is not valid.")
            continue

        score = board_c.check_Board()   #check and print the score
        if score != 0:
            if board_c.id == player1.id:
                player1.score += score
            else:
                player2.score += score

        board_c.print_Board()
        print(f"Scores: {player1.id}:{player1.score}, {player2.id}:{player2.score}")

        if player1.score + player2.score == sum:
            break
