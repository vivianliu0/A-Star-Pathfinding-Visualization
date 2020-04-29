
import GUI_updating as gui
import pygame

def a_star(start, end, grid):
    # Index with the lowest f value
    openSet = []
    closedSet = []
    path = []
    
    openSet.append(start)

    while (len(openSet) > 0):
        # If there exists elements in the open set, we can continue
        # the algorithm

        gui.show_board(openSet, None, closedSet, grid, start, end)
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
            gui.showpath(path)
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
                        nbr.parent = current

                else:
                # If the neighbour does not exist in the open set, add it
                    nbr.g = temporaryg
                    nbr.parent = current
                    openSet.append(nbr)

                #if (not nbr.parent):
                #    nbr.parent = current

            nbr.h = heuristic(nbr, end)
            nbr.f = nbr.g + nbr.h
            # Stores the parent which is used when drawing the final path
            
    if not current == end:
        print("No Solution")

    print("Out of loop")
    # Pathfinding_visualization.draw(openSet, None, closedSet)
        

def heuristic(a,b):
    #Euclidean calculation
    #distance = math.sqrt((b.x - a.x)**2 + (b.y - a.y)**2)
    
    # Manhattan distance
    distance = abs(a.x-b.x) + abs(a.y-b.y)
    return distance