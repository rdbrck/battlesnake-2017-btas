from constants import TAUNTS, SNAKE_NAME, PING
from entities import Snake, Board
from strategy import general_direction
from utils import timing

import random
import bottle


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
    # Timing Setup
    time_remaining = [200]
    time_remaining[0] = time_remaining[0] - 50
    #Timing Example
    # with timing ("testing timing function", time_remaining):
    #     loop = 0
    #     while loop < 100000:
    #         loop = loop + 1
    # print time_remaining

    data = bottle.request.json

    GameBoard = Board(**data)
    RedSnake = GameBoard.get_snake(data['you'])

    ignore_food = (RedSnake.attributes['health_points'] > 60)
    move = general_direction(GameBoard, RedSnake.head, ignore_food)

    return {
        'move': move,
        'taunt': random.choice(TAUNTS)
    }
