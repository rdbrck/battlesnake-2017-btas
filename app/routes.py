from constants import TAUNTS, SNAKE_NAME, PING
from entities import Snake, Board
from strategy import general_direction
from utils import timing
from algorithms import bfs, fast_find_safest_position

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

    with timing("bottle shit", time_remaining):
        data = bottle.request.json

    with timing("data parsing", time_remaining):
        board = Board(**data)
        snake = board.get_snake(data['you'])

        ignore_food = (snake.attributes['health_points'] > 60)
        direction = general_direction(board, snake.head, ignore_food)

    with timing("fast_find_safest_position", time_remaining):
        go_to_position = fast_find_safest_position(snake.head, direction, board)

    # if time_remaining[0] > 145:
        # print time_remaining[0]
        # TODO: DO BETTER STUFF HERE

    return {
        'move': direction,
        'taunt': random.choice(TAUNTS)
    }
