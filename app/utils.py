from constants import DIR_NAMES, DIR_VECTORS


def add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def sub(a, b):
    return (a[0] - b[0], a[1] - b[1])


def dist(a, b):
    """ Returns the 'manhattan distance' between a and b. """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


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