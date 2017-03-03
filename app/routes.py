from constants import TAUNTS, SNAKE_NAME, PING
from entities import Snake, Board
from strategy import general_direction
from utils import timing, get_direction
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
        'head_url': ('http://%s/static/head.png' % bottle.request.get_header('host')),
        'head_type': 'safe',
        'tail_type': 'freckled'
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
        print snake.head

    with timing("fast_find_safest_position", time_remaining):
        go_to_position, rating = fast_find_safest_position(snake.head, direction, board)

    # print go_to_position
    #print get_direction(snake.head, bfs(snake.head, go_to_position, board)[0])

    # print bfs(snake.head, go_to_position, board)
    # if time_remaining[0] > 145:
        # print time_remaining[0]
        # TODO: DO BETTER STUFF HERE

    return {
        'move': get_direction(snake.head, bfs(snake.head, go_to_position, board)[0]),
        'taunt': random.choice(TAUNTS)
    }
