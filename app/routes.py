from constants import TAUNTS

import random
import bottle


global RedSnakeData


@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')


@bottle.route('/')
@bottle.post('/start')
def start():
    return {
        'color': '#BADA55',
        'taunt': TAUNTS[random.randint(0, len(TAUNTS)-1)],
        'name': 'Rdbrck-Python',
        'head_url': ('http://%s/static/head.png' % bottle.request.get_header('host'))
    }


@bottle.post('/move')
def move():
    data = bottle.request.json

    #
    # GATHER REQUEST DATA
    #
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


    #
    # GATHER SECONDARY INFORMATION
    #

    # calculate threat north
    height_iterator = 0
    width_iterator = 0
    north_threat = 0

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


    # calculate threat east
    height_iterator = 0
    width_iterator = RedSnakeY
    east_threat = 0

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


    # calculate threat west
    height_iterator = 0
    width_iterator = 0
    west_threat = 0

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


    # calculate threat south
    height_iterator = RedSnakeY
    width_iterator =0
    south_threat = 0

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


    #
    # MAKE DECISION ON DATA
    #

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

    return {
        'move': move,
        'taunt': TAUNTS[random.randint(0, len(TAUNTS)-1)]
    }
