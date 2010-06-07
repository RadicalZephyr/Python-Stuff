
import os, sys, random, pygame
from pygame.locals import *

screen = pygame.display.set_mode((100,100))
screen.fill((255,255,255))
preScreen = pygame.Surface((140,140))
preScreen.set_colorkey((0,0,1))
preScreen.fill((0,0,1))
squareSurfs = []
points = [[0,0],[9,0],[9,9],[0,9]]

for i in range(10):
    square = pygame.Surface((10,10))
    square.set_colorkey((0,0,1))
    square.fill((0,0,1))
    pygame.draw.lines(square, (0,0,0), True, points, 1)
    squareSurfs.append(square)
    points[0][1] += 1
    points[1][0] -= 1
    points[2][1] -= 1
    points[3][0] += 1

#makes variables square0 through square24 (each square is dictionary below) all in squareData list
squareData = []
cc = 0
for y in range(0,100,20):
    for x in range(0,100,20):
        vars()['square' + str(cc)] = {'xy':[x,y], 'xyGrid':[x,y], 'action':'none'}
        squareData.append(vars()['square' + str(cc)])
        cc+=1

myClock = pygame.time.Clock()
running = True
count = 0
while running:
    for event in pygame.event.get():
        if (event.type == pygame.QUIT or event.type == pygame.KEYDOWN and
            event.key == pygame.K_ESCAPE):
            running = False
    
    #plus stuff. note: still need to ONLY select from available
    if count % 10 == 0:
        for i in range(random.randint(0,4)): #setting 0 to 3 plus signs
            rr = random.randint(0,24)
            isPlusNone = True
            if squareData[rr]['action'] != 'none':
                isPlusNone = False
            if squareData[rr]['action'] == 'none':
                u = [ squareData[rr]['xyGrid'][0], squareData[rr]['xyGrid'][1] - 20]
                if u[1] == -20: # < instead of ==?
                    u[1] = 80
                d = [squareData[rr]['xyGrid'][0], squareData[rr]['xyGrid'][1] + 20]
                if d[1] == 100:
                    d[1] = 0
                l = [squareData[rr]['xyGrid'][0] - 20, squareData[rr]['xyGrid'][1]]
                if l[0] == -20:
                    l[0] = 80
                r = [squareData[rr]['xyGrid'][0] + 20, squareData[rr]['xyGrid'][1]]
                if r[0] == 100:
                    r[0] = 0
                
                for i in squareData:
                    if i['xyGrid'] == u or i['xyGrid'] == d or i['xyGrid'] == l or i['xyGrid'] == r:
                        if i['action'] != 'none':
                            isPlusNone = False
                if isPlusNone == True:
                    for i in squareData:
                        if i['xyGrid'] == u:
                            i['action'] = 'plusDown'
                        if i['xyGrid'] == d:
                            i['action'] = 'plusUp'
                        if i['xyGrid'] == l:
                            i['action'] = 'plusRight'
                        if i['xyGrid'] == r:
                            i['action'] = 'plusLeft'
    for i in squareData:
        preScreen.blit( squareSurfs[0], (i['xy'][0] +20,i['xy'][1] +20) )
    screen.blit( preScreen, (0,0), (20,20,100,100) )
    #need pacman sides too
    pygame.display.flip()
    myClock.tick(20)
    screen.fill((255,255,255))
    preScreen.fill((0,0,1))
    
    #crap, plus has to reverse out of plus too. no, gonna move +2 instead.
    for i in squareData:
        if i['action'] == 'plusDown':
            if count%10 in range(0,5):
                i['xy'][1] += 2
                i['xyGrid'][1] += 2
                
            else:
                i['xy'][1] -= 2
                i['xyGrid'][1] -= 2
                if count%10 == 9: #or 0???
                    i['action'] = 'none'
        if i['action'] == 'plusUp':
            if count%10 in range(0,5):
                i['xy'][1] -= 2
                i['xyGrid'][1] -= 2
                
            else:
                i['xy'][1] += 2
                i['xyGrid'][1] += 2
                if count%10 == 9: #or 0???
                    i['action'] = 'none'
        if i['action'] == 'plusRight':
            if count%10 in range(0,5):
                i['xy'][0] += 2
                i['xyGrid'][0] += 2
                
            else:
                i['xy'][0] -= 2
                i['xyGrid'][0] -= 2
                if count%10 == 9: #or 0???
                    i['action'] = 'none'
        if i['action'] == 'plusLeft':
            if count%10 in range(0,5):
                i['xy'][0] -= 2
                i['xyGrid'][0] -= 2
                
            else:
                i['xy'][0] += 2
                i['xyGrid'][0] += 2
                if count%10 == 9: #or 0???
                    i['action'] = 'none'
    
    count+=1
