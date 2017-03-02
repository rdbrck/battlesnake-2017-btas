import collections
import heapq
import time

from collections import deque
from utils import neighbours, surrounding, dist, mul, timing
from constants import DIR_NAMES, DIR_VECTORS, FOOD, EMPTY, SNAKE

def flood_fill(vacant_func, start_pos, allow_start_in_occupied_cell=False):
    """ Flood fill is an algorithm that expands from a starting position into adjacent
    vacant cells. Returns the set of all vacant cells found.

    If allow_start_in_occupied_cell is True, the flood fill start position may be occupied
    and the start position will be included in the resulting set. """
    visited = set()

    if not allow_start_in_occupied_cell and not vacant_func(start_pos):
        return visited

    visited.add(start_pos)
    todo = collections.deque([start_pos])

    while todo:
        current = todo.popleft()
        for p in neighbours(current):
            if p not in visited and vacant_func(p):
                visited.add(p)
                todo.append(p)

    return visited


def astar(vacant_func, start_pos, goal_pos, allow_start_in_occupied_cell=False):
    """ A*, a pathfinding algorithm for finding a shortest path from a start location
    to a goal.  Returns the list of positions comprising the path, or none if no path
    could be found.

    If allow_start_in_occupied_cell is True, the search may begin from an occupied cell
    (a snake's head, for eg).  However, if you do this, you'll probably want to trim off
    the first position in the resulting shortest path. """

    if not allow_start_in_occupied_cell and not vacant_func(start_pos):
        return None

    closed_set = set()
    min_cost_to = {start_pos: 0}
    parent_of = {start_pos: None}
    todo = [(dist(start_pos, goal_pos), start_pos)]

    while todo:
        priority, current = heapq.heappop(todo)
        closed_set.add(current)

        if current == goal_pos:
            # Found the goal - walk up the parent chain to build the final path
            path = [current]

            while parent_of[current]:
                path.append(parent_of[current])
                current = parent_of[current]

            return list(reversed(path))

        for p in neighbours(current):
            if p in closed_set or not vacant_func(p):
                continue

            new_cost = min_cost_to[current] + 1

            if p not in min_cost_to or new_cost < min_cost_to[p]:
                min_cost_to[p] = new_cost
                parent_of[p] = current
                priority = new_cost + dist(p, goal_pos)
                # Note that this is a simplification of A* where we don't reprioritize items
                # within the heap, we just push the same item again with a lower priority.
                # This is wasteful in terms of memory, but for a problem of our scope, it
                # doesn't really matter.
                heapq.heappush(todo, (priority, p))

    return None

def find_safe_position(current_position, direction, board):
    """ find a safe position in the direction :param direction: from
        :current_position: (usually the position of our snake's head

        :param current_position: current_position -> (x, y) tuple
        :param direction: direction -> one of ["up", "down", "left", "right"]
        :param board: board -> the current board"""

    def _print_board(board):
        for y in range(len(board)):
            print '|' + ' '.join(["%0.1f" % board[x][y] for x in range(len(board[y]))]) + '|';
        print # newline

    def _rate_cell(cell):
        # get surrounding cells
        cells = map(lambda cell: None if board.outside(cell) else board.get_cell(cell), surrounding(cell))
        cells = filter(lambda cell: cell is not None, cells) # filter outside board
        # [0.5, -1, 2] = [EMPTY, SNAKE, FOOD]
        return reduce(lambda carry, cell: carry + [0.5, -1, 2][cell], cells, 0)

    direction_vector = DIR_VECTORS[DIR_NAMES.index(direction)]
    opposite_vector = mul(direction_vector, (-1, -1))

    board_ratings = [
        [
            _rate_cell((x, y))
            for y in range(board.height)
        ] for x in range(board.width)
    ]

    _print_board(board.cells)
    _print_board(board_ratings)

    #for x in range(board.width):
    #    for y in range(board.height):
    #        cell = board.get_cell((x, y))

    return (0, 0)

# todo fix me so I don't actually use the board
def bfs(x, y, board):
    """ BFS implementation to search for path to food

        :param x: starting x coordinate
        :param y: starting y coordinate
        :param board: the board state
    """

    def get_path_from_nodes(node):
        path = []
        while(node != None):
            path.append((node[0], node[1]))
            node = node[2]

        return path

    board[x][y] = 0
    queue = deque([(x, y, None)])

    while len(queue) > 0:
        node = queue.popleft()
        x = node[0]
        y = node[1]

        if board[x][y] == 2: # If we reach food
            return get_path_from_nodes(node) # Rebuild path

        if (board[x][y] != 0):
            continue

        board[x][y]= -1 # Mark as explored
        for i in neighbours(node):
            queue.append((i[0], i[1] ,node))

    return []

def _longest_path(vacant_func, current, open_set, current_path, longest_path, deadline):
    if time.time() > deadline:
        return False, False  # (not-found, non-maximal)

    for p in neighbours(current):
        if p in open_set and vacant_func(p):
            current_path.append(p)
            open_set.discard(p)

            if len(current_path) > len(longest_path):
                longest_path.clear()
                longest_path.extend(current_path)

                if not open_set:
                    return True, True  # (found, maximal)

            found, maximal = _longest_path(vacant_func, p, open_set, current_path, longest_path, deadline)

            if found:
                return found, maximal

            open_set.add(p)
            current_path.pop()

    return False, False  # (not-found, non-maximal)


def longest_path(vacant_func, start_pos, allow_start_in_occupied_cell=False, max_wait_seconds=0.3):
    """ This is a backtracking algorithm that will try to find a path which travels through every vacant
    cell of the area in which you seed it.

    Set max_wait_seconds to control how long the algorithm will spend looking (In practice, it finds a very
    good solution extremely quickly, and then spends ages looking for the ideal one).

    If allow_start_in_occupied_cell is True, the search may begin from an occupied cell
    (a snake's head, for eg).  However, if you do this, you'll probably want to trim off
    the first position in the resulting longest path. """

    open_set = flood_fill(vacant_func, start_pos, allow_start_in_occupied_cell=allow_start_in_occupied_cell)
    current_path = [start_pos]
    longest_path = [start_pos]
    open_set.discard(start_pos)
    found, maximal = _longest_path(vacant_func, start_pos, open_set, current_path, longest_path, time.time() + max_wait_seconds)

    return longest_path, maximal


if __name__ == "__main__":
    from entities import Board
    import json

    with open('move_fixture.json', 'r') as f:
        data = json.load(f)
        board = Board(**data)
        snake = board.get_snake(data['you'])

    with timing("find_safe_position"):
        print find_safe_position(snake.head, "down", board)
