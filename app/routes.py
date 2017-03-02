from constants import TAUNTS
from entities import Snake, Board

import random
import bottle
import operator


global RedSnake
global GameBoard


SNAKE_NAME = 'Rdbrck-Python'


@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')


@bottle.route('/')
@bottle.post('/start')
def start():
    return {
        'color': '#BADA55',
        'taunt': random.choice(TAUNTS),
        'name': SNAKE_NAME,
        'head_url': ('http://%s/static/head.png' % bottle.request.get_header('host'))
    }


@bottle.post('/move')
def move():
    data = bottle.request.json

    #
    # GATHER REQUEST DATA
    #
    GameBoard = Board(**data)
    RedSnake = GameBoard.get_snake(data['you'])
    print GameBoard.format()

    # TODO: Remove these variables and replace them throughout code
    RedSnakeX = list(RedSnake.head)[0]
    RedSnakeY = list(RedSnake.head)[1]
    arenaarray = GameBoard.cells
    arenaWidth = GameBoard.width
    arenaHeight = GameBoard.height

    #
    # GATHER SECONDARY INFORMATION
    #
    general_direction = {
        "up": 0,
        "down": 0,
        "right": 0,
        "left": 0
    }

    max(stats.iteritems(), key=operator.itemgetter(1))[0]

    # calculate threat north
    height_iterator = 0
    width_iterator = 0
    north_threat = 0

    north_boundary_distance = RedSnakeY
    if north_boundary_distance <= 0:
        #print 'I think i am at north wall'
        north_threat = 1000000
    elif arenaarray[RedSnakeY - 1][RedSnakeX] == 1:
        #print 'I think theres something to my north'
        north_threat = 1000000
    else:
        north_threat += 1000 / north_boundary_distance

        while height_iterator < RedSnakeY:
            width_iterator = 0
            while width_iterator < arenaWidth:
                if arenaarray[height_iterator][width_iterator] == 1 and height_iterator != RedSnakeY and width_iterator != RedSnakeX:
                    north_threat += 100 / (abs(width_iterator - RedSnakeX) + abs(height_iterator - RedSnakeY))
                if RedSnake.attributes["health_points"] < 70:
                    if arenaarray[height_iterator][width_iterator] == 2:
                        north_threat -= (100000 / RedSnake.attributes["health_points"]) / (abs(width_iterator - RedSnakeX) + abs(height_iterator - RedSnakeY))
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
    elif arenaarray[RedSnakeY][RedSnakeX + 1] == 1:
        east_threat = 1000000
        #print 'I think my east square is filled'
    else:
        east_threat += 1000 / east_boundary_distance

        while width_iterator < arenaWidth - 1:
            height_iterator = 0
            while height_iterator < arenaHeight - 1:
                if arenaarray[height_iterator][width_iterator] == 1 and height_iterator != RedSnakeY and width_iterator != RedSnakeX:
                    east_threat += 100 / (abs(width_iterator - RedSnakeX) + abs(height_iterator - RedSnakeY))
                if RedSnake.attributes["health_points"] < 70:
                    if arenaarray[height_iterator][width_iterator] == 2:
                        east_threat -= (100000 / RedSnake.attributes["health_points"]) / (abs(width_iterator - RedSnakeX) + abs(height_iterator - RedSnakeY))
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
    elif arenaarray[RedSnakeY][RedSnakeX - 1] == 1:
        west_threat = 1000000
        #print 'I think west square is filled'
    else:
        west_threat += 1000 / west_boundary_distance

        while width_iterator <RedSnakeX:
            height_iterator = 0
            while height_iterator < arenaHeight - 1:
                if arenaarray[height_iterator][width_iterator] == 1 and height_iterator != RedSnakeY and width_iterator != RedSnakeX:
                    west_threat += 100 / (abs(width_iterator - RedSnakeX) + abs(height_iterator - RedSnakeY))
                if RedSnake.attributes["health_points"] < 70:
                    if arenaarray[height_iterator][width_iterator] == 2:
                        west_threat -= (100000 / RedSnake.attributes["health_points"]) / (abs(width_iterator - RedSnakeX) + abs(height_iterator - RedSnakeY))
                height_iterator += 1
            width_iterator += 1

    print west_threat


    # calculate threat south
    height_iterator = RedSnakeY
    width_iterator =0
    south_threat = 0

    south_boundary_distance = arenaHeight - 1 - RedSnakeY
    if south_boundary_distance <= 0:
        south_threat = 1000000
        #print 'I think I am at south wall'
    elif arenaarray[RedSnakeY + 1][RedSnakeX] == 1:
        south_threat = 1000000
        #print 'I think my south square is filled'
    else:
        south_threat += 1000 / south_boundary_distance

        while height_iterator < arenaHeight - 1:
            width_iterator = 0
            while width_iterator < arenaWidth - 1:
                if arenaarray[height_iterator][width_iterator] == 1 and height_iterator != RedSnakeY and width_iterator != RedSnakeX:
                    south_threat += 100 / (abs(width_iterator - RedSnakeX) + abs(height_iterator - RedSnakeY))
                if RedSnake.attributes["health_points"] < 70:
                    if arenaarray[height_iterator][width_iterator] == 2:
                        south_threat -= (100000 / RedSnake.attributes["health_points"]) / (abs(width_iterator - RedSnakeX) + abs(height_iterator - RedSnakeY))
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
                move = 'up'
            else:
                print 'want to move west'
                move = 'left'
       else:
            if north_threat < east_threat:
                print 'want to move north'
                move = 'up'
            else:
                print 'want to move east'
                move = 'right'
    else:
        if east_threat > west_threat:
            if south_threat < west_threat:
                print 'want to move south'
                move = 'down'
            else:
                print 'want to move west'
                move = 'left'
        else:
            if south_threat < east_threat:
                print 'want to move south'
                move = 'down'
            else:
                print 'want to move east'
                move = 'right'

    return {
        'move': move,
        'taunt': random.choice(TAUNTS)
    }
