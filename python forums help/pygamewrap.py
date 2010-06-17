import pygame
from pygame.locals import *

pygame.init()

size = width, height = 800, 600
black = (0,0,0)
white = (255,255,255)

events = {"mouse_clicked" : "MouseButtonDown",
          "next_tick" : "NextFrame",
          "key_pressed" : "KeyDown"}

def begin_graphics():
    global __screen
    __screen = pygame.display.set_mode(size)
    __screen.fill(white)
    pygame.display.flip()

def wait_for_key_press():
    pass

def end_graphics():
    pygame.display.quit()

def invertAxis(coord):
    return coord[0], height - coord[1]

def flipRect(coord, dimen):
    coord = invertAxis(coord)
    coord = coord[0], coord[1] - dimen[1]
    return coord, dimen

def myRect(*args):
    if len(args) == 2:
        coord, dimen = flipRect(args[0], args[1])
    elif len(args) == 4:
        coord, dimen = flipRect((args[0], args[1]), (args[2], args[3]))
    else:
        raise AttributeError
    return Rect(coord, dimen)

def Box(coord, width, height):
    r = myRect(coord, (width, height))
    pygame.draw.rect(__screen, black, r, 2)
    pygame.display.flip()

def Line(start, end):
    start = invertAxis(start)
    end = invertAxis(end)
    pygame.draw.line(__screen, black, start, end, 2)
    pygame.display.flip()

def Circle

def update_when(event):
    go = True
    newevent = pygame.event.wait()
    while go:
        newevent = pygame.event.wait()
        print pygame.event.event_name(newevent.type)
        if pygame.event.event_name(newevent.type) == events[event]:
            go = False

        

if __name__ == "__main__":
    begin_graphics()            # open the graphics canvas

    Box((20, 20), 100, 100)     # the house
    Box((55, 20), 30, 50)       # the door
    Box((40, 80), 20, 20)       # the left window
    Box((80, 80), 20, 20)       # the right window
    Line((20, 120), (70, 160))  # the left roof
    Line((70, 160), (120, 120)) # the right roof

    update_when("key_pressed")
    end_graphics()              # c