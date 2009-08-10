import pygame
from pygame.locals import *
from sys import exit

class quoriBoard():
    def __init__(self, surface):
        self.parent = surface   # Store what is being made a board.
        self.turn = 1           # Store whose turn it is

    def click(self, event):
        pass

    def drawBoard(self):
        pass

    def endGame(self):
        pass

        