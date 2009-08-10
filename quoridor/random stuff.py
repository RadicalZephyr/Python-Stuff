import pygame
from pygame.locals import *
from sys import exit

white = (255,255,255)
pOne = (255,0,255)
pTwo = (0,255,0)
pThree = (0,255,255)
pFour = (255, 0, 0)

class quoriBoard():
    def __init__(self, surface):
        self.parent = surface   # Store what is being made a board.
        self.turn = 0           # Store whose turn it is

    def click(self, event):
        pass

    def drawBoard(self):
        self.parent.fill((0,0,0))   # Fill screen black
        for x in range(99, 499, 45):
            pygame.draw.line(self.parent, white, (x, 0), (x, 299), 2)
        for y in range(44, 299, 45):
            pygame.draw.line(self.parent, white, (99, y), (499, y), 2)

    def endGame(self):
        pass

if __name__ == "__main__":
    SCREEN_SIZE = (500,300)
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)
    pygame.display.set_caption("Quoridor")
    board = quoriBoard(screen)
    board.drawBoard()
    pygame.display.update()

    while True:
        board.endGame()
        event = pygame.event.wait()

        if event.type == QUIT:
            exit()

        if event.type == MOUSEBUTTONDOWN:
            board.click(event)

        board.drawBoard()
        pygame.display.update()