import time
from contextlib import contextmanager

@contextmanager
def timing(label):
    start_time = time.time()
    yield
    elapsed = time.time() - start_time
    print('{} took {}ms'.format(label, elapsed * 1000))

def add(a, b):
    return (a[0] + b[0], a[1] + b[1])

def sub(a, b):
    return (a[0] - b[0], a[1] - b[1])

def dist(a, b):
    """ Returns the 'manhattan distance' between a and b """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def neighbours(pos):
    # Inlined for performance:
    return [
        (pos[0], pos[1] + 1),
        (pos[0] + 1, pos[1]),
        (pos[0], pos[1] - 1),
        (pos[0] + -1, pos[1])
    ]
