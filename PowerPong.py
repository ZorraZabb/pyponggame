
# pong.py


import pygame, random
from pygame.locals import *
from pygame.font import *
import time

# some colors
BLACK = (   0,   0,   0)
WHITE = ( 255, 255, 255)
RED   = ( 255,   0,   0)
GREEN = (   0, 255,   0)
BLUE  = ( 0,   0,   255)

WALL_SIZE = 10
STEP = 8

PADDLE_STEP = 10
LEFT  = 0
RIGHT = 1

WINNING_SCORE = 10 #* (1.2) Increased score higher
TIME_END = 45 #*(3) set the end time if the time has reached


class BlockSprite(pygame.sprite.Sprite):
    
    def __init__(self, x, y, width, height, color=BLACK):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


# ---------------------------------------------------------

class TopPaddle(BlockSprite):
    
    def __init__(self, x, y,width,height,color):
        super().__init__(x, y - 75, width, height, color)  # paddle width & height


    def move(self, step):
        if pygame.sprite.collide_rect(self, top) and (step < 0):  # at top & going up
            step = 0
        elif pygame.sprite.collide_rect(self, bottom) and (step > 0):  
            # at bottom and going down
            step = 0
        self.rect.y += step

class BottomPaddle(BlockSprite):
    def __init__(self, x, y,width,height,color):
        super().__init__(x, y - 75, width, height, color)  # paddle width & height


    def move(self, step):
        #! (4) condition if the bottom paddle collides with the top paddle
        if pygame.sprite.collide_rect(self, leftTopPaddle) and (step < 0):  # at top & going up
            step = 0
        elif pygame.sprite.collide_rect(self, rightTopPaddle) and (step < 0):  
            step = 0

        if pygame.sprite.collide_rect(self, top) and (step < 0):  # at top & going up
            step = 0
        if pygame.sprite.collide_rect(self, bottom) and (step > 0):  
            # at bottom and going down
            step = 0
        
        self.rect.y += step


# ---------------------------------------------------------

class BallSprite(pygame.sprite.Sprite):

    def __init__(self, fnm):
        super().__init__()
        self.image = pygame.image.load(fnm).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = [scrWidth/2, scrHeight/2]
                       # start position of the ball in center of window
        self.xStep, self.yStep = self.randomSteps()
                       # step size and direction along each axis


    def update(self):
        global scoreLeft, scoreRight
        if pygame.sprite.collide_rect(self, leftTopPaddle) and (self.xStep < 0):  
            # hit left paddle and going left
            self.xStep, self.yStep = self.randomSteps()
            self.xStep = -self.xStep    # change direction

        elif pygame.sprite.collide_rect(self, rightTopPaddle) and (self.xStep > 0):  
            # hit right paddle and going right
            self.xStep, self.yStep = self.randomSteps()
            self.xStep = -self.xStep    # change direction


        #! (4) check if ball hits bottom paddle
        if pygame.sprite.collide_rect(self, leftBottomPaddle) and (self.xStep < 0):  
            # hit left paddle and going left
            self.xStep = -self.xStep    # change direction
            self.yStep = 0


        elif pygame.sprite.collide_rect(self, rightBottomPaddle) and (self.xStep > 0):  
            # hit right paddle and going right
            self.xStep = -self.xStep
            self.yStep = 0

        if pygame.sprite.spritecollideany(self, horizWalls):
            # change y-step direction at top and bottom sides
            self.yStep = -self.yStep

        if pygame.sprite.spritecollideany(self, vertWalls):
            # ball has reached left or right sides
            if pygame.sprite.collide_rect(self, right):
                scoreLeft += 1
            elif pygame.sprite.collide_rect(self, left):   # left side
                scoreRight += 1
            #! (5) the better score if the ball has collided
            if pygame.sprite.collide_rect(self, center_right):
                scoreLeft += 3
            elif pygame.sprite.collide_rect(self, center_left):   # left side
                scoreRight += 3

            # reset the ball
            self.rect.center = (scrWidth/2, scrHeight/2)
            self.xStep, self.yStep = self.randomSteps()

        self.rect.x += self.xStep   # move the ball horizontally
        self.rect.y += self.yStep   # and vertically



    def randomSteps(self):
        # create a random +/- STEP pair
        x = STEP
        if random.random() > 0.5:
            x = -x
        y = STEP
        if random.random() > 0.5:
            y = -y
        return [x,y]



# -----------------------------------

def centerImage(screen, im):
    x = (scrWidth - im.get_width())/2
    y = (scrHeight - im.get_height())/2
    screen.blit(im, (x,y))


# ---------- main -------------

pygame.init()
# screen = pygame.display.set_mode([640,480])

screen = pygame.display.set_mode([1280,720]) #* (1.1) Increased area size
screen.fill(WHITE)
pygame.display.set_caption("Pong")

scrWidth, scrHeight = screen.get_size()

# create wall sprites
top    = BlockSprite(0, 0, scrWidth, WALL_SIZE)
bottom = BlockSprite(0, scrHeight-WALL_SIZE, scrWidth, WALL_SIZE)
left   = BlockSprite(0, 0, WALL_SIZE, scrHeight)
right  = BlockSprite(scrWidth-WALL_SIZE, 0, WALL_SIZE, scrHeight)

#?(5) make a new wall to set the score
center_left = BlockSprite(0, scrHeight / 2.75, WALL_SIZE, scrHeight / 4, RED)
center_right = BlockSprite(scrWidth-WALL_SIZE, scrHeight / 2.75, WALL_SIZE, scrHeight / 4, RED)

#?(4) separate the paddle to top and bottom
#? 285 comes from (scrHeight - leftTopPaddle's Position - leftTopPaddle's Height)
leftTopPaddle = TopPaddle(50, (scrHeight/2),10,75,BLUE)
leftBottomPaddle = BottomPaddle(50, (scrHeight-285),10,75,RED)
rightTopPaddle = TopPaddle(scrWidth-50, (scrHeight/2),10,75,BLUE)
rightBottomPaddle = BottomPaddle(scrWidth-50, (scrHeight-285),10,75,RED)


horizWalls = pygame.sprite.Group(top, bottom)
vertWalls = pygame.sprite.Group(left, right)


ball = BallSprite('smallBall.png')

sprites = pygame.sprite.OrderedUpdates(top, bottom, left, right, 
                               leftTopPaddle, leftBottomPaddle,
                               rightTopPaddle, rightBottomPaddle,
                               ball,center_right,center_left)

# game vars
leftStep = 0; rightStep = 0
  # move step in pixels for paddles
scoreLeft = 0; scoreRight = 0
winMsg = ""
gameOver = False

# font = pygame.font.Font(None, 30)
font = pygame.font.Font(None, 72)



clock = pygame.time.Clock()

running = True

start_time = time.time() #* values from (2) for count start time
while running:
    sec_time = int(time.time() - start_time) #* (2) declare sec_time for count second that have passed
    clock.tick(30 + (scoreLeft + scoreRight) * 4 + sec_time) #!(6) the speed of ball depends on player's score and the game time


    # print(f"start_time : {start_time}, a time : {time.time()}, sec_time : {sec_time}")

    # handle events
    for event in pygame.event.get():
        if event.type == QUIT: 
            running = False
    
        if event.type == KEYDOWN:
            if event.key == K_w:   # left paddle
                leftStep = -PADDLE_STEP    # up
            elif event.key == K_s:
                leftStep = PADDLE_STEP     # down

            if event.key == K_p:   # right paddle
                rightStep = -PADDLE_STEP   # up
            elif event.key == K_l:
                rightStep = PADDLE_STEP    # down

        elif event.type == KEYUP: 
            if event.key == K_w or event.key == K_s:   # left paddle
                leftStep = 0
            if event.key == K_p or event.key == K_l:   # right paddle
                rightStep = 0


    # update game
    #! (4) both paddles move together
    if not gameOver:
        leftTopPaddle.move(leftStep)
        leftBottomPaddle.move(leftStep)
        rightTopPaddle.move(rightStep)
        rightBottomPaddle.move(rightStep)
        ball.update()

        if scoreLeft >= WINNING_SCORE:
            winMsg = "Left Wins!"
            gameOver = True
        elif scoreRight >= WINNING_SCORE:
            winMsg = "Right Wins!"
            gameOver = True


    # redraw
    screen.fill(WHITE)                       
    sprites.draw(screen);

    screen.blit( font.render(str(scoreLeft) + ":" + 
                             str(scoreRight), True, RED), [20, 20])
    
    #* (2) Show play time in second
    screen.blit( font.render( "Time : " + str(sec_time),True, RED),[1000,20])

    #* (3) Check game end if time has passed for TIME_END seconds
    if sec_time >= TIME_END:
        gameOver = True
        if scoreLeft > scoreRight:
            winMsg = "Left Wins! By time end"
        elif scoreLeft < scoreRight:
            winMsg = "Right Wins! By time end"
        else:
            winMsg = "Both Wins! By time end"

    if gameOver:
        centerImage(screen, font.render(winMsg, True, RED))

    pygame.display.update()

pygame.quit()
