import bottle
import constants
import os
from copy import deepcopy

#global variables
global RedSnakeData

@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')


@bottle.get('/')
def index():
    head_url = '%s://%s/static/head.png' % (
        bottle.request.urlparts.scheme,
        bottle.request.urlparts.netloc
    )

    return {
        'color': '#BADA55',
        #'head': head_url
    }


@bottle.post('/start')
def start():
    data = bottle.request.json

    # TODO: Do things with data

    return {
        'taunt': 'battlesnake-python!'
    }


@bottle.post('/move')
def move():
    data = bottle.request.json

    #print 'you are the new day ---------------------- '

    # TODO: Do things with data

    #populate a local gameboard
    arenaarray = [[0 for x in range(data["width"])] for y in range(data["height"])]
    for iterator in data["food"]:
        arenaarray [iterator[1]][iterator[0]] = 1

    SnakeList = data["snakes"]
    for iterator2 in SnakeList:
        if iterator2["name"] == "basesnake":
            RedSnakeData = iterator2
            for square in iterator2["coords"]:
                arenaarray[square[1]][square[0]] = 2
        else:
            for square in iterator2["coords"]:
                arenaarray[square[1]][square[0]] = 3


    RedSnakeX = RedSnakeData["coords"][0][0]
    RedSnakeY = RedSnakeData["coords"][0][1]
    arenaWidth = data["width"]
    arenaHeight = data["height"]

    """
    #---------------------------------------------------------------------------------------
    #Run Floodfill on on a move to the North
    #---------------------------------------------------------------------------------------

    #print arenaarray
    #print "\n\n"

    #northVal = floodfill_start(3, len(RedSnakeData["coords"]), 0, arenaarray, RedSnakeX, RedSnakeY - 1, RedSnakeData, constants.REDSNAKE, arenaWidth, arenaHeight)
    #print 'paths north'
    #print northVal
    #Run Floodfill on on a move to the East
    #---------------------------------------------------------------------------------------

    #eastVal = floodfill_start(3, len(RedSnakeData["coords"]), 0, arenaarray, RedSnakeX + 1, RedSnakeY, RedSnakeData, constants.REDSNAKE, arenaWidth, arenaHeight)
    #print 'paths east'
    #print eastVal
    #---------------------------------------------------------------------------------------
    #Run Floodfill on on a move to the West
    #---------------------------------------------------------------------------------------

    #westVal = floodfill_start(3, len(RedSnakeData["coords"]), 0, arenaarray, RedSnakeX - 1, RedSnakeY, RedSnakeData, constants.REDSNAKE, arenaWidth, arenaHeight)
    #print 'paths west'
    #print westVal
    #---------------------------------------------------------------------------------------
    #Run Floodfill on on a move to the South
    #---------------------------------------------------------------------------------------

    southVal = floodfill_start(3, len(RedSnakeData["coords"]), 0, arenaarray, RedSnakeX, RedSnakeY + 1, RedSnakeData, constants.REDSNAKE, arenaWidth, arenaHeight)
    print 'paths south'
    print southVal

    #find greatest length of sub trees.
    if northVal > southVal:
        if westVal > eastVal:
            if northVal > westVal:
                print 'north tree'
                print northVal + 1
            else:
                print 'west tree'
                print westVal + 1
        else:
            if northVal > eastVal:
                print 'north tree'
                print northVal + 1
            else:
                print 'east tree'
                print eastVal + 1
    else:
        if westVal > eastVal:
            if southVal > westVal:
                print 'south tree'
                print southVal + 1
            else:
                print 'west tree'
                print westVal + 1
        else:
            if southVal > eastVal:
                print 'south tree'
                print southVal + 1
            else:
                print 'east tree'
                print eastVal + 1"""

    #calculate threat north
    height_iterator = 0
    width_iterator = 0
    north_threat = 0

    #if invalidmove(arenaarray, RedSnakeX, RedSnakeY, constants.NORTH, arenaWidth, arenaHeight) == -1:
        #print "invalid move found!"
    #if invalidmove(arenaarray, RedSnakeX, RedSnakeY, constants.EAST, arenaWidth, arenaHeight) == -1:
        #print "invalid move found!"
    #if invalidmove(arenaarray, RedSnakeX, RedSnakeY, constants.WEST, arenaWidth, arenaHeight) == -1:
        #print "invalid move found!"
    #if invalidmove(arenaarray, RedSnakeX, RedSnakeY, constants.SOUTH, arenaWidth, arenaHeight) == -1:
        #print "invalid move found!"

    north_boundary_distance = RedSnakeY
    if north_boundary_distance <= 0:
        #print 'I think i am at north wall'
        north_threat = 1000000
    elif arenaarray[RedSnakeY - 1][RedSnakeX] > 1:
        #print 'I think theres something to my north'
        north_threat = 1000000
    else:
        north_threat += 1000 / north_boundary_distance

        while height_iterator < RedSnakeY:
            width_iterator = 0
            while width_iterator < arenaWidth:
                if arenaarray[height_iterator][width_iterator] >= 2 and height_iterator != RedSnakeY and width_iterator != RedSnakeX:
                    north_threat += 100 / (abs(width_iterator - RedSnakeX) + abs(height_iterator - RedSnakeY))
                if RedSnakeData ["health"] < 70:
                    if arenaarray[height_iterator][width_iterator] == 1:
                        north_threat -= 100 / (abs(width_iterator - RedSnakeX) + abs(height_iterator - RedSnakeY))
                width_iterator += 1
            height_iterator += 1

    print north_threat


#calculate threat east

    height_iterator = 0
    width_iterator = RedSnakeY
    east_threat = 0

    #print 'east move holds'
    #print arenaarray[RedSnakeY][RedSnakeX - 1]

    east_boundary_distance = arenaWidth - 1 - RedSnakeX
    if east_boundary_distance <= 0:
        east_threat = 1000000
        #print 'I think i am at east wall'
    elif arenaarray[RedSnakeY][RedSnakeX + 1] > 1:
        east_threat = 1000000
        #print 'I think my east square is filled'
    else:
        east_threat += 1000 / east_boundary_distance

        while width_iterator < arenaWidth - 1:
            height_iterator = 0
            while height_iterator < arenaHeight - 1:
                if arenaarray[height_iterator][width_iterator] >= 2 and height_iterator != RedSnakeY and width_iterator != RedSnakeX:
                    east_threat += 100 / (abs(width_iterator - RedSnakeX) + abs(height_iterator - RedSnakeY))
                if RedSnakeData ["health"] < 70:
                    if arenaarray[height_iterator][width_iterator] == 1:
                        east_threat -= 100 / (abs(width_iterator - RedSnakeX) + abs(height_iterator - RedSnakeY))
                height_iterator += 1
            width_iterator += 1

    print east_threat

#calculate threat west

    height_iterator = 0
    width_iterator = 0
    west_threat = 0

    print 'west move holds'
    print arenaarray[RedSnakeY][RedSnakeX + 1]

    west_boundary_distance = RedSnakeX
    if west_boundary_distance <= 0:
        west_threat = 1000000
        #print 'I think I am at west wall'
    elif arenaarray[RedSnakeY][RedSnakeX - 1] > 1:
        west_threat = 1000000
        #print 'I think west square is filled'
    else:
        west_threat += 1000 / west_boundary_distance

        while width_iterator <RedSnakeX:
            height_iterator = 0
            while height_iterator < arenaHeight - 1:
                if arenaarray[height_iterator][width_iterator] >= 2 and height_iterator != RedSnakeY and width_iterator != RedSnakeX:
                    west_threat += 100 / (abs(width_iterator - RedSnakeX) + abs(height_iterator - RedSnakeY))
                if RedSnakeData ["health"] < 70:
                    if arenaarray[height_iterator][width_iterator] == 1:
                        west_threat -= 100 / (abs(width_iterator - RedSnakeX) + abs(height_iterator - RedSnakeY))
                height_iterator += 1
            width_iterator += 1

    print west_threat

#calculate threat south

    height_iterator = RedSnakeY
    width_iterator =0
    south_threat = 0

    #print 'move south holds'
    #print arenaarray[RedSnakeY + 1][RedSnakeX]

    south_boundary_distance = arenaHeight  - 1 - RedSnakeY
    if south_boundary_distance <= 0:
        south_threat = 1000000
        #print 'I think I am at south wall'
    elif arenaarray[RedSnakeY + 1][RedSnakeX] > 1:
        south_threat = 1000000
        #print 'I think my south square is filled'
    else:
        south_threat += 1000 / south_boundary_distance

        while height_iterator < arenaHeight - 1:
            width_iterator = 0
            while width_iterator < arenaWidth - 1:
                if arenaarray[height_iterator][width_iterator] >= 2 and height_iterator != RedSnakeY and width_iterator != RedSnakeX:
                    south_threat += 100 / (abs(width_iterator - RedSnakeX) + abs(height_iterator - RedSnakeY))
                if RedSnakeData ["health"] < 70:
                    if arenaarray[height_iterator][width_iterator] == 1:
                        south_threat -= 100 / (abs(width_iterator - RedSnakeX) + abs(height_iterator - RedSnakeY))
                width_iterator += 1
            height_iterator += 1

    print south_threat

    if south_threat > north_threat:
       if east_threat > west_threat:
            if north_threat < west_threat:
                print 'want to move north'
                move = 'north'
            else:
                print 'want to move west'
                move = 'west'
       else:
            if north_threat < east_threat:
                print 'want to move north'
                move = 'north'
            else:
                print 'want to move east'
                move = 'east'
    else:
        if east_threat > west_threat:
            if south_threat < west_threat:
                print 'want to move south'
                move = 'south'
            else:
                print 'want to move west'
                move = 'west'
        else:
            if south_threat < east_threat:
                print 'want to move south'
                move = 'south'
            else:
                print 'want to move east'
                move = 'east'

    #print "\n\n"
    #print arenaarray
    #print "\n\n"

    return {
        'move': move,
        'taunt': 'interesting taunt here'
    }






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

def invalidmove_wall(direction, localArena, localSnakeX, localSnakeY, width, height):
        #print 'move_walling at', localSnakeX, localSnakeY

        if direction == constants.NORTH:
            north_boundary_distance = localSnakeY - 1
            if north_boundary_distance <= 0:
                #print 'I think i am at north wall'
                return constants.INVALID_MOVE

        elif direction == constants.EAST:
            east_boundary_distance = width - 1 - localSnakeX
            if east_boundary_distance <= 0:
                #print 'I think i am at east wall'
                return constants.INVALID_MOVE

        elif direction == constants.WEST:
            west_boundary_distance = localSnakeX - 1
            if west_boundary_distance <= 0:
                #print 'I think I am at west wall'
                return constants.INVALID_MOVE

        elif direction == constants.SOUTH:
            south_boundary_distance = height  - 1 - localSnakeY
            if south_boundary_distance <= 0:
                #print 'I think I am at south wall'
                return constants.INVALID_MOVE



def invalidmove(localArena, localSnakeX, localSnakeY, direction, width, height):
        if direction == constants.NORTH:
            north_boundary_distance = localSnakeY - 1
            if north_boundary_distance <= 0:
                #print 'I think i am at north wall'
                return constants.INVALID_MOVE
            elif localArena[localSnakeY - 1][localSnakeX] > 1:
                #print 'I think theres something to my north'
                return constants.INVALID_MOVE

        elif direction == constants.EAST:
            east_boundary_distance = width - 1 - localSnakeX    #double check that it's 2 when more thoughtful.
            if east_boundary_distance <= 0:
                #print 'I think i am at east wall'
                return constants.INVALID_MOVE
            elif localArena[localSnakeY][localSnakeX + 1] > 1:
                #print 'I think my east square is filled'
                return constants.INVALID_MOVE

        elif direction == constants.WEST:
            west_boundary_distance = localSnakeX - 1
            if west_boundary_distance <= 0:
                #print 'I think I am at west wall'
                return constants.INVALID_MOVE
            elif localArena[localSnakeY][localSnakeX - 1] > 1:
                #print 'I think west square is filled'
                return constants.INVALID_MOVE

        elif direction == constants.SOUTH:
            south_boundary_distance = height - 1 - localSnakeY     #double check that it's 2 when more thoughtful.
            if south_boundary_distance <= 0:
                #print 'I think I am at south wall'
                return constants.INVALID_MOVE
            elif localArena[localSnakeY + 1][localSnakeX] > 1:
                #print 'I think my south square is filled'
                return constants.INVALID_MOVE

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


@bottle.post('/end')
def end():
    data = bottle.request.json

    # TODO: Do things with data

    return {
        'taunt': 'All too easy'
    }


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))
