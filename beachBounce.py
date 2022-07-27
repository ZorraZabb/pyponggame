
# beachBounce.py
# Bounce a beach ball around a window

import pygame
from pygame.locals import *

BLACK = (   0,   0,   0)
WHITE = ( 255, 255, 255)


# ---------- main -------------

pygame.init()
screen = pygame.display.set_mode([640,480])
screen.fill(WHITE)
pygame.display.set_caption("Bouncing Beachball")


ballIm = pygame.image.load('ball.png').convert_alpha()

# store dimensions for later
scrWidth, scrHeight = screen.get_size()
imWidth, imHeight = ballIm.get_size()


# start position of the ball
x = 50; y = 50

# step size and direction along each axis
xStep = 10; yStep = 10

clock = pygame.time.Clock()

running = True    
while running:
    clock.tick(30)

    # handle events
    for event in pygame.event.get():
        if event.type == QUIT: 
            running = False
        
        #!KEYDOWN event to change direction.
        if event.type == KEYDOWN:
            if event.key == K_x:
                xStep = -xStep
            if event.key == K_y:
                yStep = -yStep

    # update game state
    #? change x position, if the ball moves to the right edge of windows
    if (x >= scrWidth - 1 - imWidth):      
        x = 1

    #? change x position, if the ball moves to the left edge of windows
    if (x <= 0):
        x = scrWidth - 2 - imWidth

    # change y-step direction at top and bottom sides
    if (y <= 0) or (y >= scrHeight -1 - imHeight):        
        yStep = -yStep     
                                   
    x += xStep   # move the ball horizontally
    y += yStep   # and vertically


    # redraw
    screen.fill(WHITE)                       
    screen.blit(ballIm, [x, y])
    pygame.display.update()

pygame.quit()
