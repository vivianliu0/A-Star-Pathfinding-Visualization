import pygame, sys, math, random
from pygame.locals import *
from tkinter import messagebox


# Colours
LIGHTGRAY = (200,200,200)
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,51,51)
GREEN = (128, 255,0)
PINK = (255, 8, 127)
BLUE = (102, 178,255)

BOARDWIDTH = 600
BOARDHEIGHT = 600
WINDOWWIDTH = BOARDWIDTH
WINDOWHEIGHT = BOARDHEIGHT + 100
BUTTONWIDTH = 100
BUTTONHEIGHT = 30

COLS = 25
ROWS = 25
SPOTWIDTH = BOARDWIDTH // COLS
SPOTHEIGHT = BOARDHEIGHT // ROWS


class Coordinate():
    def __init__(self,x,y):
        self.f = 0
        self.g = 0
        self.h = 0
        self.x = x
        self.y = y
        self.neighbours = []
        self.parent = None
        # Each point on the grid can potentially be a obstacle
        # We will assume that each coordinate initially is not
        self.obstacle = False

        # Randomizer with a probability of 1/10. Used to decide if
        # the coordinates is a wall
        if (random.randint(0,10) < 2):
            self.obstacle = True

    def show(self, colour, thickness):
    # Draws an empty rectangle
        if self.obstacle:
            pygame.draw.rect(win, BLACK, (self.x * SPOTWIDTH, self.y* SPOTHEIGHT, SPOTWIDTH, SPOTHEIGHT), 0)
        else:
            pygame.draw.rect(win, colour, (self.x * SPOTWIDTH, self.y* SPOTHEIGHT, SPOTWIDTH, SPOTHEIGHT), thickness)

    def add_neighbours(self, grid):
        if(self.x < (COLS-1)):
            self.neighbours.append(grid[self.x+1][self.y])
        if(self.x > 0):
            self.neighbours.append(grid[self.x-1][self.y])
        if(self.y < (ROWS-1)):
            self.neighbours.append(grid[self.x][self.y+1])
        if(self.y > 0):
            self.neighbours.append(grid[self.x][self.y-1])

        # Allowing Diagonal Movement
        if(self.x > 0 and self.y > 0):
            self.neighbours.append(grid[self.x-1][self.y-1])
        if(self.x < (COLS-1) and self.y > 0):
            self.neighbours.append(grid[self.x+1][self.y-1])
        if(self.x > 0 and self.y < (ROWS-1)):
            self.neighbours.append(grid[self.x-1][self.y+1])
        if(self.x < (COLS-1) and self.y < (ROWS-1)):
            self.neighbours.append(grid[self.x+1][self.y+1])

class Button():

    def __init__(self, colour, x, y, width, height, text = ''):
        self.colour = colour
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win, outline = None):
        if outline:
            pygame.draw.rect(win, self.colour, (self.x-2, self.y-2, self.width+4, self.height+4), 0)

        pygame.draw.rect(win, self.colour, (self.x,self.y,self.width,self.height),0)

        if self.text != '':
            font = pygame.font.SysFont('freesansbold.ttf', 18)
            text = font.render(self.text, 1, BLACK)
            # Centers text in the middle of the button
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def is_over(self, pos):
        #pos represents the position of the mouse as a tuple (x,y)
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False

    def change_text(self, text):
        self.text = text

def board_hover(pos):
    if pos[0] < BOARDWIDTH and pos[0] > 0 and pos[1] < BOARDHEIGHT and pos[1] > 0:
        return True
    else:
        return False

def setup():
    global openSet,closedSet,grid,start,end,path
    openSet = []
    closedSet = []
    path = []

    # Making a 2D list to represent a grid
    grid = [[Coordinate(x,y) for x in range(ROWS)] for y in range(COLS)]

    # Making all the possible coordinates on the grid
    for i in range(len(grid[0])):
        for j in range(len(grid)):
            grid[i][j] = Coordinate(i,j)

    # Adding all the neighbours to each spot on the grid
    for i in range(len(grid[0])):
        for j in range(len(grid)):
            grid[i][j].add_neighbours(grid)

    start = grid[0][0]
    end = grid[COLS - 1][ROWS - 1]
    start.obstacle = False
    end.obstacle = False

    openSet.append(start)
    print("Setup start parent: ")
    print(start.parent)

# For testing purposes
def lstfgh(lst):
    fghlst = []
    for elem in lst:
        fghlst.append((elem.f, elem.g, elem.h))
    return fghlst

def A_Star():
    # Index with the lowest f value
    
    while (len(openSet) > 0):
        # If there exists elements in the open set, we can continue
        # the algorithm

        draw()
        pygame.time.delay(10)
        # Testing: print(lstfgh(openSet))

        lowest = 0 

        for i in range(len(openSet)):
            if (openSet[i].f < openSet[lowest].f):
                lowest = i

        current = openSet[lowest]

        if (current == end):
            # If the end point has been reached, we will find the path
            print("Path found! Done!")
            temp = current
            path.append(temp)

            # # As long as the coordinate has a parent, add that to the path
            # # until we reach the starting point
            while temp.parent:
               path.append(temp.parent)
               temp = temp.parent

            print(len(path))
            showpath()
            break

        openSet.remove(current)
        closedSet.append(current)

        nbrs = current.neighbours

        for i in range(len(nbrs)):
            nbr = nbrs[i]

            if ((not nbr in closedSet) and (not nbr.obstacle)):

                # we store the g value in another variable called 
                # temporary because it is possible that there exists
                # another lower g value for that spot
                temporaryg = current.g + 1

                if (nbr in openSet):

                # Checks if the neighbour is in the openSet (i.e. g value
                # has already been evaluated. If it has, we compare the
                # temporary g value to the current g value and take the smaller 
                # value)
                    if (temporaryg < nbr.g):
                        nbr.g = temporaryg

                else:
                # If the neighbour does not exist in the open set, add it
                    nbr.g = temporaryg
                    openSet.append(nbr)

                if (not nbr.parent):
                    nbr.parent = current

            nbr.h = heuristic(nbr, end)
            nbr.f = nbr.g + nbr.h
            # Stores the parent which is used when drawing the final path
            
    if not current == end:
        print("No Solution")

    print("Out of loop")
    draw()
        

def heuristic(a,b):
    distance = math.sqrt((b.x - a.x)**2 + (b.y - a.y)**2)
    # distance = abs(a.x-b.x) + abs(a.y-b.y)
    return distance


def draw():
    # Drawing the empty grid on the screen
    for i in range(len(grid[0])):
        for j in range(len(grid)):
            grid[i][j].show(LIGHTGRAY,1)

    # All coordinates in the closed set appear red on the screen
    for i in range(len(closedSet)):
        closedSet[i].show(RED,0)

    # All coordinates in the open set appear red on the screen
    for i in range(len(openSet)):
        openSet[i].show(GREEN,0)

    start.show(PINK, 0)
    end.show(PINK, 0)

    pygame.display.update()

def showpath():
    for i in range(len(path)):
        path[i].show(BLUE, 0)
    pygame.display.update()

def main():
    global win, startButton
    pygame.init()
    win = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
    pygame.display.set_caption("A* Pathfinding")

    solveButton = Button(LIGHTGRAY, BOARDWIDTH / 2 - BUTTONWIDTH / 2, 
        BOARDHEIGHT + 30, BUTTONWIDTH, BUTTONHEIGHT, "Find Path!")

    win.fill(WHITE)
    setup()
    draw()
    solveButton.draw(win,BLACK)

    buttonClicked = False

    while True:
       for event in pygame.event.get():
           pos = pygame.mouse.get_pos()

           if event.type == pygame.QUIT:
              pygame.quit()
              sys.exit()
           pygame.display.update()

           if event.type == pygame.MOUSEBUTTONDOWN:
                if solveButton.is_over(pos) and not buttonClicked:
                    # START SOLVING
                    print('Start Algorithm')
                    A_Star()
                    showpath()
                    buttonClicked = True
                    solveButton.change_text("Restart")
                    solveButton.draw(win,BLACK)
                elif board_hover(pos) and not buttonClicked:
                    xCoord = pos[0] // SPOTWIDTH
                    yCoord = pos[1] // SPOTHEIGHT
                    if (xCoord == 0 and yCoord == 0) or (xCoord == COLS-1 and yCoord == ROWS-1):
                        continue
                    else:
                        grid[xCoord][yCoord].obstacle = True
                        draw()
                elif solveButton.is_over(pos) and buttonClicked:
                    win.fill(WHITE)
                    setup()
                    draw()
                    solveButton.change_text("Find Path!")
                    solveButton.draw(win,BLACK)
                    buttonClicked = False


# A* algorithm ends when it finds the end node, or when there are no more spots 
# to evaluate, algorithm also ends



main()

# test = Coordinate()
# test.parent

#python A_Star_Algorithm.py