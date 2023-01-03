'''
Project name:Dots and Boxes
Author: PengFei Li,ig22317
Course Name: SDPA
Description: all code needed to run the game
'''
from classes import Board,ComputerPlayer,HumanPlayer,SmartComputerPlayer
import random

if __name__ == '__main__':
    #palyers can input their symbol
    id1 =input("ID of player1(1 character): ")
    palyer1 = HumanPlayer(id1)
    id2 = input("ID of player2(1 character): ")
    while id2 == id1: #prevent duplication
        id2 = input("ID exists, please input a different id:")
    opponent = input("Computer (c) or SmartComputer(sc) or Human (h)?(default:H) ").lower() #select the type of player
    if opponent =='computer' or opponent == "c":

        palyer2 = ComputerPlayer(id2)
    elif opponent == 'smartcomputer' or opponent =="sc":
        palyer2 =SmartComputerPlayer(id2)

    else:
        print('The game will start with the default player (H)')
        player2 = HumanPlayer(id2)