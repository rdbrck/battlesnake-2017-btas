import constants
from checks import invalidmove_wall, invalidmove

from copy import deepcopy

#floodfill is a tree which calculates possible paths.
#The order for a max depth of "1" is     1
#                                  /   |   |   \
#                               north east west south
# where each value holds the largest depth in that direction.
#If two branches are tied, should choose the safest direction.

def floodfill(depth, direction, length, pathlength, arena, localSnakeX, localSnakeY, snakeData, snakeNumber, width, height):

    localArena = deepcopy(arena)
#---------------------------------------------------------------------------------------
#Build local Arena, if not moving into food, then remove from tail.
#---------------------------------------------------------------------------------------

    #print 'floodfilling at depth ', depth, ' direction ', direction
    #print 'floodfilling at', localSnakeX, localSnakeY



    if direction == constants.NORTH:
        if invalidmove_wall(constants.NORTH, localArena, localSnakeX, localSnakeY, width, height) == constants.INVALID_MOVE:
            print 'invalid move at', localSnakeX, localSnakeY
            return constants.INVALID_MOVE
        #check if move is into food
        elif arena [localSnakeY - 1][localSnakeX] != 1:

            localArena [snakeData["coords"][length - depth - 1][1]][snakeData["coords"][length - depth - 1][0]] = 0

    elif direction == constants.EAST:
        #check if move is into food
        if invalidmove_wall(constants.EAST, localArena, localSnakeX, localSnakeY, width, height) == constants.INVALID_MOVE:
            print 'invalid move at', localSnakeX, localSnakeY
            return constants.INVALID_MOVE
        elif arena [localSnakeY][localSnakeX + 1] != 1:
            #remove the last tail
            localArena [snakeData["coords"][length - depth - 1][1]][snakeData["coords"][length - depth - 1][0]] = 0

    elif direction == constants.WEST:
        #check if move is into food
        if invalidmove_wall(constants.WEST, localArena, localSnakeX, localSnakeY, width, height) == constants.INVALID_MOVE:
            print 'invalid move at', localSnakeX, localSnakeY
            return constants.INVALID_MOVE
        elif arena [localSnakeY][localSnakeX - 1] != 1:
            #remove the last tail
            localArena [snakeData["coords"][length - depth - 1][1]][snakeData["coords"][length - depth - 1][0]] = 0

    elif direction == constants.SOUTH:
        #check if move is into food
        if invalidmove_wall(constants.SOUTH, localArena, localSnakeX, localSnakeY, width, height) == constants.INVALID_MOVE:
            print 'invalid move at', localSnakeX, localSnakeY
            return constants.INVALID_MOVE
        elif arena [localSnakeY + 1][localSnakeX] != 1:
            #remove the last tail
            localArena [snakeData["coords"][length - depth - 1][1]][snakeData["coords"][length - depth - 1][0]] = 0

#---------------------------------------------------------------------------------------
#Check if it is an invalid move
#---------------------------------------------------------------------------------------
    if invalidmove(localArena, localSnakeX, localSnakeY, direction, width, height):
        print 'invalid move at', localSnakeX, localSnakeY
        return constants.INVALID_MOVE
#---------------------------------------------------------------------------------------
#Add Move to the LocalArena
#---------------------------------------------------------------------------------------
    else:
        if direction == constants.NORTH:
            #add the move to the localArena
            localArena [localSnakeY - 1][localSnakeX] = snakeNumber

        elif direction == constants.EAST:
            #add the move to the localArena
            localArena [localSnakeY][localSnakeX + 1] = snakeNumber

        elif direction == constants.WEST:
            #add the move to the localArena
            localArena [localSnakeY][localSnakeX - 1] = snakeNumber

        elif direction == constants.SOUTH:
            #add the move to the localArena
            localArena [localSnakeY + 1][localSnakeX] = snakeNumber

#---------------------------------------------------------------------------------------
#Check if end of recursion
#---------------------------------------------------------------------------------------
        if depth == 0:
            print 'found path to', localSnakeX, localSnakeY
            print localArena
            print localArena[40]
            return pathlength + 1
        else:
#---------------------------------------------------------------------------------------
#Run Floodfill on on a move to the North
#---------------------------------------------------------------------------------------

            southval = 0
            westval = 0
            eastval = 0
            northval = 0

            if direction == constants.NORTH:
               northval = floodfill_start(depth, length, pathlength, localArena, localSnakeX, localSnakeY - 1, snakeData, snakeNumber, width, height)
#Run Floodfill on on a move to the East
#---------------------------------------------------------------------------------------
            elif direction == constants.EAST:
                eastval = floodfill_start(depth, length, pathlength, localArena, localSnakeX + 1, localSnakeY, snakeData, snakeNumber, width, height)
#---------------------------------------------------------------------------------------
#Run Floodfill on on a move to the West
#---------------------------------------------------------------------------------------
            elif direction == constants.WEST:
                westval = floodfill_start(depth, length, pathlength, localArena, localSnakeX - 1, localSnakeY, snakeData, snakeNumber, width, height)
#---------------------------------------------------------------------------------------
#Run Floodfill on on a move to the South
#---------------------------------------------------------------------------------------
            elif direction == constants.SOUTH:
                southval = floodfill_start(depth, length, pathlength, localArena, localSnakeX, localSnakeY + 1, snakeData, snakeNumber, width, height)

            return southval + westval + eastval + northval

            #find greatest length of sub trees.
#            if northVal > southVal:
#                if westVal > eastVal:
#                    if northVal > westVal:
#                        return northVal + 1
#                    else:
#                        return westVal + 1
#                else:
#                    if northVal > eastVal:
#                        return northVal + 1
#                    else:
#                        return eastVal + 1
#            else:
#                if westVal > eastVal:
#                    if southVal > westVal:
#                        return southVal + 1
#                    else:
#                        return westVal + 1
#                else:
#                    if southVal > eastVal:
#                        return southVal + 1
#                    else:
#                        return eastVal + 1


def floodfill_start (depth, length, pathlength, localArena, localSnakeX, localSnakeY, snakeData, snakeNumber, width, height):

    #print 'floodfill_start called here'
    #print 'to look at X Y'
    #print localSnakeX
    #print localSnakeY

    northVal = floodfill (depth - 1, constants.NORTH, length, pathlength, localArena, localSnakeX, localSnakeY, snakeData, snakeNumber, width, height)
    eastVal = floodfill (depth - 1, constants.EAST, length, pathlength, localArena, localSnakeX, localSnakeY, snakeData, snakeNumber, width, height)
    westVal = floodfill (depth - 1, constants.WEST, length, pathlength, localArena, localSnakeX, localSnakeY, snakeData, snakeNumber, width, height)
    southVal = floodfill (depth - 1, constants.SOUTH, length, pathlength, localArena, localSnakeX, localSnakeY, snakeData, snakeNumber, width, height)

    return northVal + eastVal + westVal + southVal

    #find greatest length of sub trees.
#    if northVal > southVal:
#        if westVal > eastVal:
#            if northVal > westVal:
#                return northVal + 1
#            else:
#                return westVal + 1
#        else:
#            if northVal > eastVal:
#                return northVal + 1
#            else:
#                return eastVal + 1
#    else:
#        if westVal > eastVal:
#            if southVal > westVal:
#                return southVal + 1
#            else:
#                return westVal + 1
#        else:
#            if southVal > eastVal:
#                return southVal + 1
#            else:
#                return eastVal + 1
