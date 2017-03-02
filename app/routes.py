from constants import TAUNTS, SNAKE_NAME, PING
from entities import Snake, Board
from strategy import general_direction
from utils import timing
from algorithms import bfs

import random
import bottle
import json


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
    time_remaining = [150]

    with timing(time_remaining):
        data = bottle.request.json

    print time_remaining[0]

    with timing(time_remaining):
        GameBoard = Board(**data)
        RedSnake = GameBoard.get_snake(data['you'])

        ignore_food = (RedSnake.attributes['health_points'] > 60)
        move = general_direction(GameBoard, RedSnake.head, ignore_food)

    a = bfs((0, 0), (15, 15), GameBoard)

    if time_remaining[0] > 145:
        print time_remaining[0]
        # TODO: DO BETTER STUFF HERE

    return {
        'move': move,
        'taunt': random.choice(TAUNTS)
    }
