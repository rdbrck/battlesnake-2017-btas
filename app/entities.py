from utils import sub, add
from constants import DIR_VECTORS, EMPTY, FOOD, SNAKE

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

    def potential_positions(self):
        return [add(self.head, d) for d in DIR_VECTORS if d != sub((0, 0), self.direction)]


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
            #Do we need to clone over food that is marked as 'spoiled'?


        else:
            # Initialize a board from a battlesnake gamestate dict
            self.width = kwargs['width']
            self.height = kwargs['height']
            self.cells = []
            self.meta_cells = []
            for x in range(self.width):
                self.cells.append([EMPTY] * self.height)
                self.meta_cells.append([None] * self.height)
            # Only take snakes that are alive
            self.snakes = [Snake(**s) for s in kwargs['snakes']]
            self.food = list(map(tuple, kwargs['food']))

            # Fill out initially occupied cells on board
            for snake in self.snakes:
                for pos in snake.coords:
                    self.set_cell(pos, SNAKE, snake)

            for fud in self.food:
                if true == raceable_food(fud.pos):
                    self.set_cell(fud, FOOD)
                else:
                    self.set_cell(fud, SPOILED)



    #Raceable food does a bfs search to see which snake is closest in moves.
    #returns true if the food is closest to RedSnake
    #returns false if the food is closest to an AdvSnake
    #In a Tie, the largest snake wins
    def raceable_food (self, pos):
        #Add the first position to the perimeter

        #While there are values in the perimeter
            #Look at the square
            #If Run into a snake tail - Don't add any squares from this square
            #If Run into a snake head - Don't add any squares from any square, but finish perimeter, and add this snake to a list

        #After looking at all perimeter
            #If No heads encountered, return false

            #If the closest head is RedSnake, return true

            #If closest head is AdvSnake, return false

            #If there are multiple snakes, choose largest one
                #If largest one is us, return true
                
                #Else return false



    def get_snake(self, snake_id):
        try:
            return next(s for s in self.snakes if s.attributes['id'] == snake_id)
        except StopIteration:
            return None

    def set_cell(self, pos, value, meta = None):
        self.cells[pos[0]][pos[1]] = value
        self.meta_cells[pos[0]][pos[1]] = meta

    def get_cell(self, pos):
        return self.cells[pos[0]][pos[1]]

    def get_cell_meta(self, pos):
        return self.meta_cells[pos[0]][pos[1]]

    def outside(self, pos):
        return pos[0] < 0 or pos[0] >= self.width or pos[1] < 0 or pos[1] >= self.height

    def inside(self, pos):
        return not self.outside(pos)

    def vacant(self, pos):
        # Inlined for performance:
        return not (pos[0] < 0 or pos[0] >= self.width or pos[1] < 0 or pos[1] >= self.height) and self.cells[pos[0]][pos[1]] != 1

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
        return ' '.join(s)
