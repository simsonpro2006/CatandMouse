import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
import pygame, sys, random
from pygame.locals import *

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PURPLE= (166,0,255)

FRAMERATE = 200
UPDATEFRAME = 1
#ID of cat, mouse and cheese
NONEID = 0
MOUSEID = 1
CATID = 2
CHEESEID = 3

# Row/col
GRIDSIZE= (4,4)
WINDOWSIZE=(610,610)
# This sets the margin between each cell
MARGIN = 2

CELLX = (WINDOWSIZE[0] - (MARGIN * (GRIDSIZE[0] + 1))) / GRIDSIZE[0]
CELLY = (WINDOWSIZE[1] - (MARGIN * (GRIDSIZE[1] + 1))) / GRIDSIZE[1]
CELLSIZE = (int(CELLY), int(CELLX))

def Grid_to_Pixel(gridPos):
    return ((MARGIN + CELLSIZE[0]) * gridPos[0] + MARGIN, (MARGIN + CELLSIZE[1]) * gridPos[1] + MARGIN)

# Create a 2 dimensional array. A two dimensional
# array is simply a list of lists.
class CatandMousegame:
    def __init__(self):
        self.grid = []
        self.catwin = False
        self.mousewin = False

        for row in range(GRIDSIZE[0]):
            # Add an empty array that will hold each cell
            # in this row
            self.grid.append([])
            for column in range(GRIDSIZE[1]):
                self.grid[row].append(NONEID)  # Append a cell
        #number of cheese is being display on the board
        counter = 0
        while counter < 2:
            rX = random.randint(0, GRIDSIZE[1] - 1)
            rY = random.randint(0, GRIDSIZE[0] - 1)
            if self.grid[rY][rX] == NONEID:
                self.grid[rY][rX] = CHEESEID
                counter += 1
        #Mouse placement
        while True:
            rX = random.randint(0, GRIDSIZE[1] - 1)
            rY = random.randint(0, GRIDSIZE[0] - 1)
            if self.grid[rY][rX] == NONEID:
                self.grid[rY][rX] = MOUSEID
                break

        #Cat placement
        while True:
            rX = random.randint(0, GRIDSIZE[1] - 1)
            rY = random.randint(0, GRIDSIZE[0] - 1)
            if self.grid[rY][rX] == NONEID:
                self.grid[rY][rX] = CATID
                break

        # Initialize pygame
        pygame.init()

        # Set the HEIGHT and WIDTH of the screen
        self.screen = pygame.display.set_mode(WINDOWSIZE)

        # Set title of screen
        pygame.display.set_caption("Array Backed Grid")

        self.catImg = pygame.image.load("ImProject2\\cat.png")
        self.catImg = pygame.transform.scale(self.catImg, CELLSIZE)

        self.mouseImg = pygame.image.load("ImProject2\\mouse.png")
        self.mouseImg = pygame.transform.scale(self.mouseImg, CELLSIZE)

        self.cheeseImg = pygame.image.load("ImProject2\\Chesse.png")
        self.cheeseImg = pygame.transform.scale(self.cheeseImg, CELLSIZE)
        self.font = pygame.font.SysFont('Calibri', 25, True, False)

    def walk(self,board, pos):
        move = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        movefrom = board[pos[0]][pos[1]]

        while len(move) > 0:
            newposition = [pos[0], pos[1]]
            nextmove = move.pop(random.randint(0, len(move) - 1))
            newposition[0] += nextmove[0]
            newposition[1] += nextmove[1]
            if newposition[0] < 0 or newposition[0] >= GRIDSIZE[0] or newposition[1] < 0 or newposition[1] >= \
                    GRIDSIZE[1]:
                continue
            else:
                moveto = board[newposition[0]][newposition[1]]
                if moveto == CATID and movefrom == MOUSEID:
                    continue
                elif moveto == CHEESEID and movefrom == CATID:
                    continue
                else:
                    board[pos[0]][pos[1]] = NONEID
                    board[newposition[0]][newposition[1]] = movefrom
                    break
    def rungame(self):
# Loop until the user clicks the close button.
        done = False
        doupdate = True
        # Used to manage how fast the screen updates
        clock = pygame.time.Clock()

        frameCounter = FRAMERATE

        mouseMoved = False
        catMoved = False
        catMovedcounter = 0
        # -------- Main Program Loop -----------
        while not done:
            for event in pygame.event.get():  # User did something
                if event.type == pygame.QUIT:  # If user clicked close
                    done = True  # Flag that we are done so we exit this loop

            # Set the screen background
            self.screen.fill(PURPLE)

            frameCounter += 1

            mouseMoved = False
            catMoved = False

            if doupdate and frameCounter % UPDATEFRAME == 0:
                # Update cat and mouse pos
                for row in range(GRIDSIZE[0]):
                    for column in range(GRIDSIZE[1]):
                        entityId = self.grid[row][column]
                        if entityId == NONEID or entityId ==CHEESEID:
                            continue
                        elif entityId == MOUSEID and mouseMoved ==False:
                            self.walk(self.grid,[row,column])
                            mouseMoved= True
                        elif entityId == CATID and catMoved ==False:
                            if catMovedcounter % 2== 0:
                                self.walk(self.grid,[row,column])
                            catMoved= True
                            catMovedcounter += 1
            Mousecounter= 0
            Cheesecounter= 0
            # Draw the grid and entities
            for row in range(GRIDSIZE[0]):
                for column in range(GRIDSIZE[1]):
                    color = WHITE
                    pxPos = Grid_to_Pixel([column, row])
                    pygame.draw.rect(self.screen,
                                     color,
                                     [pxPos[0],
                                      pxPos[1],
                                      CELLSIZE[0],
                                      CELLSIZE[1]])
                    entityId = self.grid[row][column]
                    if entityId == 0:
                        continue
                    elif entityId == MOUSEID: # Mouse
                        self.screen.blit(self.mouseImg, pxPos)
                        Mousecounter += 1
                    elif entityId == CATID: # Mouse
                        self.screen.blit(self.catImg, pxPos)
                    elif entityId == CHEESEID:  # Mouse
                        self.screen.blit(self.cheeseImg, pxPos)
                        Cheesecounter += 1
            if Mousecounter ==0:
                doupdate =False
                done = True
                self.catwin = True
                print('cat win')
            elif Cheesecounter ==0:
                doupdate = False
                done = True
                self.mousewin = True
                print ('mouse win')

            clock.tick(1)

            #Go ahead and update the screen with what we've drawn.
            pygame.display.flip()

# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
countermouse= 0
countercat = 0
for i in range(10):
    Game = CatandMousegame()
    Game.rungame()
    if Game.mousewin:
        countermouse += 1
    elif Game.catwin:
        countercat += 1
print ('mouse win number of times = ',countermouse/(countermouse+countercat))
print ('cat win number of times = ',countercat/(countermouse+countercat))
objects = ('Mousewin', 'cat win')
y_pos = np.arange(len(objects))
performance = [countermouse/(countermouse+countercat), countercat/(countermouse+countercat)]

plt.bar(y_pos, performance, align='center', alpha=0.5)
plt.xticks(y_pos, objects)
plt.ylabel('percentage')
plt.title('cat and mouse with cheese')

plt.show()