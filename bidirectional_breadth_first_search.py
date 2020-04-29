import GUI_updating as gui
import pygame

def bi_breadth_first_search(start, end, grid):
    openSetA = []
    openSetB = []
    closed = []
    path = []

    # Implemented using openSet as a queue1
    openSetA.append(start)
    openSetB.append(end)

    start.opened = True
    end.opened = True

    start.direction = 's'
    end.direction = 'e'

    found_path = False


    while (len(openSetA) > 0 and len(openSetB) > 0):
        gui.show_board(openSetA, openSetB, closed, grid, start, end)
        pygame.time.delay(10)

        print(len(openSetA))
        print(len(openSetB))

        currentA = openSetA.pop(0)
        currentA.closed = True
        closed.append(currentA)


        currentB = openSetB.pop(0)
        currentB.closed = True
        closed.append(currentB)

        nbrs = currentA.neighbours

        for i in range(len(nbrs)):
            nbr = nbrs[i]

            if (nbr.closed or nbr.obstacle):
                continue

            if (nbr.opened): 

                # If this position has been searched in the other direction, 
                # path has been found
                if(nbr.direction == 'e'):                    
                    path = bi_backtrace(currentA, nbr)
                    gui.showpath(path)
                    found_path = True
                    break 

                continue

            openSetA.append(nbr)
            nbr.parent = currentA
            nbr.opened = True
            nbr.direction = 's'


        if (found_path):
            break

        nbrs = currentB.neighbours

        for i in range(len(nbrs)):
            nbr = nbrs[i]

            if (nbr.closed or nbr.obstacle):
                continue

            if (nbr.opened): 

                # If this position has been searched in the other direction, 
                # path has been found
                if(nbr.direction == 's'):                    
                    path = bi_backtrace(currentB, nbr)
                    gui.showpath(path)
                    found_path = True
                    break

                continue

            openSetB.append(nbr)
            nbr.parent = currentB
            nbr.opened = True
            nbr.direction = 'e'

        if (found_path):
            break

    print("Out of loop")


def backtrace(node):
    pathA = []
    temp = node
    pathA.append(temp)

    while (temp.parent):
        pathA.append(temp.parent)
        temp = temp.parent

    return pathA

def bi_backtrace(nodeA, nodeB):
    pathA = backtrace(nodeA)
    pathB = backtrace(nodeB)

    pathB.reverse()

    return pathA + pathB
