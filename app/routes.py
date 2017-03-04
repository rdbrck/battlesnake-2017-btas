from constants import TAUNTS, SNAKE_NAME, PING
from entities import Snake, Board
from strategy import general_direction, need_food
from utils import timing, get_direction
from algorithms import bfs, fast_find_safest_position, find_food, flood_fill
from multiprocessing.pool import ThreadPool
import Queue
from threading import Thread, Lock

import random
import bottle
import json
import os

_db_lock = Lock()

@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')


@bottle.route('/')
@bottle.post('/start')
def start():
    # port = bottle.request.get_header('port')
    port = os.getenv('PORT', '8080')

    port_colors = {
        '8080': '#f00000',
        '8081': '#ff0000',
        '8082': '#fff000',
        '8083': '#ffff00',
        '8084': '#fffff0',
        '8085': '#ffffff',
        '8086': '#f0f0f0',
        '8087': '#0f0f0f'
    }

    try:
        color = port_colors[str(port)]
    except:
        color = "#123456"

    return {
        'color': '#ff0000',
        'taunt': random.choice(TAUNTS),
        'head_url': ('http://%s/static/uneil.gif' % bottle.request.get_header('host')),
        'name': 'BETTER THAN ALEKSIY\'S SNAKE',
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

    position = None
    path = None
    move = direction
    next_move = list()
    thread_pool = list()
    potential_snake_positions = list()

    number_of_squares = []
    iterator_floodfill = 0
    #Find number of empty squares in every direction.
    for move_point in neighbours(snake.head):
        number_of_squares[iterator_floodfill] = (move_point, len(floodfill(vacant_func, move_point, False)))
        if number_of_squares[iterator_floodfill][1] <= 10:
            potential_snake_positions.append(move_point)
        iterator_floodfill = iterator_floodfill + 1

    #if all <= 10, move into largest
    if number_of_squares[0][1] <= 10 and number_of_squares[1][1] <= 10 and number_of_squares[2][1] <= 10 and number_of_squares[3][1] <= 10:
        largest = reduce(lambda carry, direction: carry if carry[1] > direction[1] else direction, number_of_squares, number_of_squares[0])
        # remove from invalid
        potential_snake_positions.remove(largest[0])

    for enemy_snake in board.snakes:
        if enemy_snake.attributes['id'] != snake.attributes['id'] and enemy_snake.attributes['health_points'] >= snake.attributes['health_points']:
            potential_snake_positions.append(enemy_snake.potential_positions())

    if food:
        with timing("find_food", time_remaining):
            food_positions = find_food(snake.head, snake.attributes['health_points'], board, food)
            positions = [ position[0] for position in food_positions ]

            for i in range(len(positions)):
                t = Thread(target=bfs(snake.head, positions[i], board, potential_snake_positions, next_move))
                thread_pool.append(t)

            for thread in thread_pool:
                thread.start()
                thread.join()

            next_move = filter(lambda path: not len(path) == 0, next_move)
            path = min(next_move, key=len)
            move = get_direction(snake.head, path[0])
    else:
        with timing("fast_find_safest_position", time_remaining):
            positions = fast_find_safest_position(snake.head, direction, board)
            positions = [ position[0] for position in positions ]

            for i in range(len(positions)):
                t = Thread(target=bfs(snake.head, positions[i], board, potential_snake_positions, next_move))
                thread_pool.append(t)

            for thread in thread_pool:
                thread.start()
                thread.join()

    if len(next_move) == 0:
        with timing("floodfill", time_remaining):
            floods = {
                "up": len(flood_fill(board, (snake.head[0],snake.head[1]-1))),
                "down": len(flood_fill(board, (snake.head[0],snake.head[1]+1))),
                "right": len(flood_fill(board, (snake.head[0]+1,snake.head[1]))),
                "left": len(flood_fill(board, (snake.head[0]-1,snake.head[1])))
            }
            move = max(floods.iterkeys(), key=(lambda key: floods[key]))
    else:
        path = max(next_move, key=len)
        move = get_direction(snake.head, path[0])

    print "moving", move
    return {
        'move': move,
        'taunt': random.choice(TAUNTS)
    }
