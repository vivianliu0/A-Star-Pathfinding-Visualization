import pygame, sys, math, random
from pygame.locals import *
from tkinter import *

import a_star, dijkstra, bidirectional_breadth_first_search as bfs, GUI_updating as gui

# Colours

WHITE = (255,255,255)
BLACK = (0,0,0)
LIGHTGRAY = (200,200,200)
LIGHTBLUE = (191, 227, 235)
BLUE = (114, 193, 213)

BOARDWIDTH = 600
BOARDHEIGHT = 600
WINDOWWIDTH = BOARDWIDTH
WINDOWHEIGHT = BOARDHEIGHT + 170
BUTTONWIDTH = 100
BUTTONHEIGHT = 30


COLS = 30
ROWS = 30
SPOTWIDTH = BOARDWIDTH // COLS
SPOTHEIGHT = BOARDHEIGHT // ROWS


grid = []
start = None
end = None

algorithms = ["A*", "Dijkstra", "Bidirectional BFS"]


class Coordinate():
    def __init__(self,x,y,rand):
        self.f = 0
        self.g = 0
        self.h = 0
        self.x = x
        self.y = y
        self.neighbours = []
        self.parent = None

        #implemented for bfs
        self.opened = False
        self.closed = False
        self.direction = None

        #implemented for dijkstra
        self.distance = 0

        # Each point on the grid can potentially be a obstacle
        # We will assume that each coordinate initially is not
        self.obstacle = False

        # Randomizer with a probability of 1/10. Used to decide if
        # the coordinates is a wall
        if (rand and random.randint(0,10) < 3):
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

    def change_colour(self, colour):
        self.colour = colour

def board_hover(pos):
    if pos[0] < BOARDWIDTH and pos[0] > 0 and pos[1] < BOARDHEIGHT and pos[1] > 0:
        return True
    else:
        return False

def setup(rand):
    
    global grid, start, end

    # Making a 2D list to represent a grid
    grid = [[Coordinate(x,y, rand) for x in range(ROWS)] for y in range(COLS)]

    # Making all the possible coordinates on the grid
    for i in range(len(grid[0])):
        for j in range(len(grid)):
            grid[i][j] = Coordinate(i,j, rand)

    # Adding all the neighbours to each spot on the grid
    for i in range(len(grid[0])):
        for j in range(len(grid)):
            grid[i][j].add_neighbours(grid)


    start = grid[0][0]
    end = grid[COLS - 1][ROWS - 1]
    start.obstacle = False
    end.obstacle = False



def main():
    global win, startButton
    pygame.init()
    win = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
    pygame.display.set_caption("Pathfinding Visualization")

    solveButton = Button(LIGHTGRAY, BOARDWIDTH / 2 - BUTTONWIDTH / 2, 
        BOARDHEIGHT + 30, BUTTONWIDTH, BUTTONHEIGHT, "Find Path!")

    clearButton = Button(LIGHTGRAY, BOARDWIDTH / 2 - BUTTONWIDTH * 2,
        BOARDHEIGHT + 30, BUTTONWIDTH, BUTTONHEIGHT, "Clear Board")

    randomBoardButton = Button(LIGHTGRAY, BOARDWIDTH / 2 + BUTTONWIDTH, 
        BOARDHEIGHT + 30, BUTTONWIDTH, BUTTONHEIGHT, "Random Board")

    selectButton = Button(WHITE, BOARDWIDTH / 2 - BUTTONWIDTH / 2, 
        BOARDHEIGHT + BUTTONHEIGHT + 45, BUTTONWIDTH, BUTTONHEIGHT, "Select An Algorithm:")
    
    aStarButton = Button(BLUE, BOARDWIDTH / 2 - BUTTONWIDTH / 2, 
        BOARDHEIGHT + 105, BUTTONWIDTH, BUTTONHEIGHT, "A Star")

    dijkstraButton = Button(LIGHTBLUE, BOARDWIDTH / 2 - BUTTONWIDTH * 7 / 4, 
        BOARDHEIGHT + 105, BUTTONWIDTH, BUTTONHEIGHT, "Dijkstra")

    bfsButton = Button(LIGHTBLUE, BOARDWIDTH / 2 + BUTTONWIDTH * 3 / 4, 
        BOARDHEIGHT + 105, BUTTONWIDTH, BUTTONHEIGHT, "Bidirectional BFS")

    win.fill(WHITE)
    setup(True)
    print(start)
    gui.show_board(None, None, None, grid, start, end)
    solveButton.draw(win,BLACK)
    clearButton.draw(win,BLACK)
    randomBoardButton.draw(win, BLACK)
    selectButton.draw(win, BLACK)
    aStarButton.draw(win,BLACK)
    dijkstraButton.draw(win,BLACK)
    bfsButton.draw(win, BLACK)

    algorithm = 2
    relocating_start = False
    relocating_end = False

    while True:
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:

                if solveButton.is_over(pos) and not relocating_start and not relocating_end:
                    # Find Path Button to start solving
                    print(algorithm)

                    if algorithm == 1:
                        dijkstra.dijkstra(start, end, grid)
                    elif algorithm == 2:
                        a_star.a_star(start, end, grid)
                    elif algorithm == 3:
                        bfs.bi_breadth_first_search(start, end, grid)

                elif clearButton.is_over(pos) and not relocating_start and not relocating_end:
                    # Clears the board of all obstacles
                    setup(False)
                    gui.show_board(None, None, None, grid, start, end)


                elif randomBoardButton.is_over(pos) and not relocating_start and not relocating_end:
                    # Resets the board with randomized obstacles
                    setup(True)
                    gui.show_board(None, None, None, grid, start, end)


                elif board_hover(pos):
                    # Creating obstacles when user clicks on board
                    xCoord = pos[0] // SPOTWIDTH
                    yCoord = pos[1] // SPOTHEIGHT

                    if (xCoord == 0 and yCoord == 0) or (xCoord == COLS-1 and yCoord == ROWS-1):
                        continue
                    elif grid[xCoord][yCoord].obstacle == True:
                        grid[xCoord][yCoord].obstacle = False
                        gui.show_board(None, None, None, grid, start, end)
                    else:
                        grid[xCoord][yCoord].obstacle = True
                        gui.show_board(None, None, None, grid, start, end)
                
                elif dijkstraButton.is_over(pos):
                    algorithm = 1
                    gui.redraw_buttons(dijkstraButton, aStarButton, bfsButton, algorithm, win)

                elif aStarButton.is_over(pos):
                    algorithm = 2
                    gui.redraw_buttons(dijkstraButton, aStarButton, bfsButton, algorithm, win)

                elif bfsButton.is_over(pos):
                    algorithm = 3
                    gui.redraw_buttons(dijkstraButton, aStarButton, bfsButton, algorithm, win)
                else:
                    continue


main()
