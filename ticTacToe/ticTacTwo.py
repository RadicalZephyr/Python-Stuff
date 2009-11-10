import pygame
from pygame.locals import *
from sys import exit

class ticBoard():
    def __init__(self, surface):
        self.parent = surface           #Store what is being made a board.
        self.turn = 1                   # Store whose turn it is
        self.boxes = [0,0,0,0,0,0,0,0,0]# Variable storing box image state, 0:unfilled# 1:X'ed 2:O'd  Also used by endGame to check
        self.winList = [(0,1,2),(3,4,5),
                        (6,7,8),(0,3,6),
                        (1,4,7),(2,5,8),
                        (0,4,8),(2,4,6)]
        
    def click(self, event):
        point = event.pos
        box = self.clickTest(point)
        if not self.boxes[box]:
            if self.turn % 2:
                self.boxes[box] = 1
                self.turn += 1
            else:
                self.boxes[box] = 2
                self.turn += 1

    def clickTest(self, point):
        for x in xrange(9):
            if self.rectList[x].collidepoint(point):
                return x    # Test all rect's for having been clicked
            

    def drawBoard(self, size):
        # Should I make internal variables for each box that are rect objects everytime
        # drawBoard gets called?  What purpose would this serve?  rect.collidepoint is
        # an easy way to check if the point is inside the box, call collidepoint in a loop
        # for each box and return which box was clicked.
        def drawXO(box):
            # This function should also retrieve the corner coordinates for the box it
            # represents.  These are then fed to the draw functions as local var's
            # tl,tr,bl,br and cent and rad
            tl,tr,bl,br = boxCoords(box)
            cent = getC(tl,tr,bl,br)
            rad = min((tr[0] - tl[0])/3,(br[1] - tr[1])/3)
            
            if self.boxes[box] == 2:    # Check if it should be an O
                pygame.draw.circle(self.parent, (0,0,0), cent, rad, 3)
            elif self.boxes[box] == 1:  # Check if it should be an X
                pygame.draw.aaline(self.parent, (0,0,0), (tl), (br), 2)
                pygame.draw.aaline(self.parent, (0,0,0), (tr), (bl), 5)
        def boxCoords(box): #Retrieves the stored variables in a coherent form for each box
            if box == 0: 
                return [(0,0),(self.wa,0),(0,self.ha),(self.wa,self.ha)]
            elif box == 1:
                return [(self.wa,0),(self.wb,0),(self.wa,self.ha),(self.wb,self.ha)]
            elif box == 2:
                return [(self.wb,0),(self.wf,0),(self.wb,self.ha),(self.wf,self.ha)]
            elif box == 3:
                return [(0,self.ha),(self.wa,self.ha),(0,self.hb),(self.wa,self.hb)]
            elif box == 4:
                return [(self.wa,self.ha),(self.wb,self.ha),(self.wa,self.hb),(self.wb,
                                                                               self.hb)]
            elif box == 5:
                return [(self.wb,self.ha),(self.wf,self.ha),(self.wb,self.hb),(self.wf,
                                                                               self.hb)]
            elif box == 6:
                return [(0,self.hb),(self.wa,self.hb),(0,self.hf),(self.wa,self.hf)]
            elif box == 7:
                return [(self.wa,self.hb),(self.wb,self.hb),(self.wa,self.hf),(self.wb,
                                                                               self.hf)]
            elif box == 8:
                return [(self.wb,self.hb),(self.wf,self.hb),(self.wb,self.hf),(self.wf,
                                                                               self.hf)]

        def getC(tl,tr,bl,br):
            xcomp = tl[0] + (tr[0] - tl[0])/2
            ycomp = tr[1] + (br[1] - tr[1])/2
            return (xcomp,ycomp)

        def makeRect(boxCoords):    # Given the x,y coord's for all 4 corners of a rect,
                                    # return a Rect object for that area
            width = boxCoords[1][0] - boxCoords[0][0]
            height = boxCoords[3][1] - boxCoords[1][1]
            return pygame.Rect(boxCoords[0],(width,height))
            
        self.wa = size[0]/3 - 1     # Assign the useful grid points to variables
        self.wb = 2*size[0]/3 - 1
        self.wf = size[0] - 1
        self.ha = size[1]/3 - 1
        self.hb = 2*size[1]/3 - 1
        self.hf = size[1] - 1
        
        self.parent.fill((255,255,255)) # Fill screen white

        pygame.draw.line(self.parent, (0,0,0), (self.wa,0), (self.wa,self.hf),5) 
        pygame.draw.line(self.parent, (0,0,0), (self.wb,0), (self.wb,self.hf),5) 
        pygame.draw.line(self.parent, (0,0,0), (0,self.ha), (self.wf,self.ha),5) 
        pygame.draw.line(self.parent, (0,0,0), (0,self.hb), (self.wf,self.hb),5) 
        # Previous four lines draw the lines on the board.
        self.rectList = []
        for a in xrange(9):     # Draw the marked X's and O's
            drawXO(a)
            self.rectList.append(makeRect(boxCoords(a)))

    def endGame(self):
        if all(self.boxes):
            print "Cat's Game!"
            exit()

        for a,b,c in self.winList:
            if self.boxes[a] == self.boxes[b] == self.boxes[c] and self.boxes[a] != 0:
                print "Player" + str(self.boxes[a]) + "wins!"
                exit()
if __name__ == "__main__":
    # ACTUAL GAME CODE STARTS HERE
    SCREEN_SIZE = (150,150)
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE,RESIZABLE,32)  # Start the game with a reasonable
    pygame.display.set_caption("Tic-Tac-Toe")                   # size frame, but let it change
    board = ticBoard(screen)
    board.drawBoard(SCREEN_SIZE)
    pygame.display.update()

    while True:
        board.endGame()
        event = pygame.event.wait()

        if event.type == QUIT:
            exit()

        if event.type == VIDEORESIZE:
            SCREEN_SIZE = event.size
            screen = pygame.display.set_mode(SCREEN_SIZE, RESIZABLE, 32)

        if event.type == MOUSEBUTTONDOWN:
            board.click(event)
            
        board.drawBoard(SCREEN_SIZE)
        pygame.display.update()