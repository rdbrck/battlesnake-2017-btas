from utils import sub, add


class Snake(object):
    ATTRIBUTES = ('id', 'health_points')

    def __init__(self, clone=None, **kwargs):
        if clone:
            # Clone another snake
            self.attributes = other_snake.attributes.copy()
            self.coords = other_snake.coords.copy()
        else:
            # Create a snake from a battlesnake snake dict
            self.attributes = {k: kwargs[k] for k in Snake.ATTRIBUTES}
            self.coords = list(map(tuple, kwargs['coords']))

    def _get_direction(self):
        assert len(self.coords) > 1
        return sub(self.coords[0], self.coords[1])
    direction = property(_get_direction)

    def __len__(self):
        return len(self.coords)

    def _get_head(self):
        return self.coords[0]
    head = property(_get_head)

    def _get_tail(self):
        return self.coords[-1]
    tail = property(_get_tail)


class Board(object):
    """
    Basically a 2d grid of cells represented by integers.
    A zero cell is unoccupied. 1 is snake. 2 is food.
    """

    def __init__(self, clone=None, **kwargs):
        """
        Conceptually, grid is indexed as board[x][y], that is, the board is in column-major layout.
        """
        if clone:
            # Clone another board
            self.width = clone.width
            self.height = clone.height
            self.cells = []
            for x in range(self.width):
                self.cells.append(clone.cells[x].copy())
            self.snakes = [Snake(s) for s in clone.snakes]
            self.food = clone.food.copy()
        else:
            # Initialize a board from a battlesnake gamestate dict
            self.width = kwargs['width']
            self.height = kwargs['height']
            self.cells = []
            for x in range(self.width):
                self.cells.append([0] * self.height)
            # Only take snakes that are alive
            self.snakes = [Snake(**s) for s in kwargs['snakes']]
            self.food = list(map(tuple, kwargs['food']))

            # Fill out initially occupied cells on board
            for snake in self.snakes:
                for pos in snake.coords:
                    self.set_cell(pos, 1)

            for fud in self.food:
                self.set_cell(fud, 2)

    def get_snake(self, snake_id):
        try:
            return next(s for s in self.snakes if s.attributes['id'] == snake_id)
        except StopIteration:
            return None

    def set_cell(self, pos, value):
        self.cells[pos[0]][pos[1]] = value

    def get_cell(self, pos):
        return self.cells[pos[0]][pos[1]]

    def outside(self, pos):
        return pos[0] < 0 or pos[0] >= self.width or pos[1] < 0 or pos[1] >= self.height

    def inside(self, pos):
        return not self.outside(pos)

    def vacant(self, pos):
        # Inlined for performance:
        return not (pos[0] < 0 or pos[0] >= self.width or pos[1] < 0 or pos[1] >= self.height) and self.cells[pos[0]][pos[1]] == 0

    def has_snake(self, pos):
        return (self.cells[pos[0]][pos[1]] == 1)

    def has_food(self, pos):
        return (self.cells[pos[0]][pos[1]] == 2)

    def __str__(self):
        return self.format(lambda v: ' ' if v == 0 else '{:d}'.format(v))

    def format(self):
        s = []
        for y in range(self.height):
            s.append('|')
            for x in range(self.width):
                v = str(self.cells[x][y])
                s.append(v)
            s.append('|\n')
        bar = '-' * (len(self.cells) * len(v) + 2) + '\n'
        s.insert(0, bar)
        s.append(bar)
        return ''.join(s)
