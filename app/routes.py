from constants import TAUNTS, SNAKE_NAME, PING
from entities import Snake, Board
from strategy import general_direction, need_food
from utils import timing, get_direction
from algorithms import bfs, fast_find_safest_position, find_food

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
        direction = general_direction(board, snake.head, snake.attributes['health_points'])

    with timing("need_food", time_remaining):
        food = need_food(board, snake.head, snake.attributes['health_points'])

    if food:
        with timing("find_food", time_remaining):
            food_positions = find_food(snake.head, snake.attributes['health_points'], board, food)
            positions = [ position[0] for position in food_positions ]
            print len(positions), "positions:", positions
    else:
        with timing("fast_find_safest_position", time_remaining):
            positions = fast_find_safest_position(snake.head, direction, board)
            positions = [ position[0] for position in positions ]
            print len(positions), "positions:", positions

    path = bfs(snake.head, positions[0], board)
    move = get_direction(snake.head, path[0])

    return {
        'move': move,
        'taunt': random.choice(TAUNTS)
    }
