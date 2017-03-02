import time
from contextlib import contextmanager
from constants import DIR_NAMES, DIR_VECTORS

@contextmanager
def timing(time_remaining):
    start_time = time.time()
    yield
    time_remaining[0] = time_remaining[0] - ((time.time() - start_time) * 1000)

def add(a, b):
    return (a[0] + b[0], a[1] + b[1])

def sub(a, b):
    return (a[0] - b[0], a[1] - b[1])

def mul(a, b):
    return (a[0] * b[0], a[1] * b[1])

def dist(a, b):
    """ Returns the 'manhattan distance' between a and b """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def surrounding(pos):
    return [
        (pos[0], pos[1] + 1),
        (pos[0] + 1, pos[1]),
        (pos[0] + 1, pos[1] + 1),
        (pos[0] + 1, pos[1] - 1),
        (pos[0], pos[1] - 1),
        (pos[0] - 1, pos[1]),
        (pos[0] - 1, pos[1] - 1),
        (pos[0] - 1, pos[1] + 1)
    ]

def neighbours(pos):
    """ Gets coordinates of neighbour coordinates to a coordinate. """

    return [
        (pos[0], pos[1] + 1),
        (pos[0] + 1, pos[1]),
        (pos[0], pos[1] - 1),
        (pos[0] + -1, pos[1])
    ]

def translate_to_direction(new_pos, old_pos):
    """ Translates the change between two positions into a direction name. """
    return DIR_NAMES[DIR_VECTORS.index(sub(new_pos, old_pos))]
