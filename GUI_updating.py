import pygame

LIGHTGRAY = (200,200,200)
RED = (255,51,51)
GREEN = (128, 255,0)
PINK = (255, 8, 127)
BLUE = (102, 178,255)
WHITE = (255, 255, 255)
BLACK = (0,0,0)
LIGHTBLUE = (191, 227, 235)
BLUE = (114, 193, 213)

def show_board(openA, openB, closed, grid, start, end):
    # # Drawing the empty grid on the screen
    for i in range(len(grid[0])):
        for j in range(len(grid)):
            grid[i][j].show(WHITE,0)
            grid[i][j].show(LIGHTGRAY,1)

    # # All coordinates in the closed set appear red on the screen
    if (closed):
        for i in range(len(closed)):
           closed[i].show(RED,0)

    # # All coordinates in the open set appear red on the screen
    if (openA):
        for i in range(len(openA)):
            openA[i].show(GREEN,0)

    # # If the function is bidirectional, print the second open set
    if (openB):
        for i in range(len(openB)):
            openB[i].show(GREEN,0)

    if start:
        start.show(PINK, 0)
    
    if end:
        end.show(PINK, 0)

    pygame.display.update()


def showpath(path):
    print("printing path")
    length = len(path)
    print(path)
    print(f"path length: {length}")
    for i in range(len(path)):
        print("in loop")
        path[i].show(BLUE, 0)
    pygame.display.update()

def redraw_buttons(bt1, bt2, bt3, selected, win):
    if selected == 1:
        bt1.change_colour(BLUE)
        bt2.change_colour(LIGHTBLUE)
        bt3.change_colour(LIGHTBLUE)
        bt1.draw(win, BLACK)
        bt2.draw(win, BLACK)
        bt3.draw(win, BLACK)
    elif selected == 2:
        bt1.change_colour(LIGHTBLUE)
        bt2.change_colour(BLUE)
        bt3.change_colour(LIGHTBLUE)
        bt1.draw(win, BLACK)
        bt2.draw(win, BLACK)
        bt3.draw(win, BLACK)
    else:
        bt1.change_colour(LIGHTBLUE)
        bt2.change_colour(LIGHTBLUE)
        bt3.change_colour(BLUE)
        bt1.draw(win, BLACK)
        bt2.draw(win, BLACK)
        bt3.draw(win, BLACK)