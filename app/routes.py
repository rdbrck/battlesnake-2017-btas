from constants import TAUNTS, SNAKE_NAME
from entities import Snake, Board
from strategy import general_direction

import random
import bottle
import operator


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

    GameBoard = Board(**data)
    RedSnake = GameBoard.get_snake(data['you'])

    ignore_food = (RedSnake.attributes['health_points'] > 60)
    move = general_direction(GameBoard, RedSnake.head, ignore_food)

    return {
        'move': move,
        'taunt': random.choice(TAUNTS)
    }
