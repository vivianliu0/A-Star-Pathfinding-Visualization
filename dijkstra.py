import GUI_updating as gui
import pygame


def dijkstra(start, end, grid):
    openSet = []
    closedSet = []
    path = []   

    openSet.append(start)


    while (len(openSet) > 0):
        gui.show_board(openSet, None, closedSet, grid, start, end)
        pygame.time.delay(10)

        lowest = 0 

        for i in range(len(openSet)):
            if (openSet[i].distance < openSet[lowest].distance):
                lowest = i

        current = openSet[lowest]
        #current.closed = True

        # If it is a wall, we skip it
        #if(current.obstacle):
        #    openSet.remove(current)
        #    continue;

        if (current == end):
            # If the end point has been reached, we will find the path
            temp = current
            path.append(temp)

            # # As long as the coordinate has a parent, add that to the path
            # # until we reach the starting point
            while temp.parent:
               path.append(temp.parent)
               temp = temp.parent

            gui.showpath(path)
            break

        openSet.remove(current)
        closedSet.append(current)

        nbrs = current.neighbours

        for i in range(len(nbrs)):
            nbr = nbrs[i]

            if ((not nbr in closedSet) and (not nbr.obstacle)):

                if (nbr in openSet):
                        if (current.distance + 1 < nbr.distance):
                            nbr.distance = current.distance + 1
                            nbr.parent = current;
                else:
                    nbr.distance = current.distance + 1
                    nbr.parent = current;
                    openSet.append(nbr)

                #nbr.opened = True
                
     
    if not current == end:
        print("No Solution")

    print("Out of loop")
    