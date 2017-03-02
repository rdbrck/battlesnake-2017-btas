from utils import dist


def general_direction(board, head, ignore_food):
    """ Returns the most 'beneficial' direction to move in """

    # start with general area
    direction = {
        "up": 1000 / (dist(head, (head[0],0))+1),
        "down": 1000 / (dist(head, (head[0],board.height))+1),
        "right": 1000 / (dist((board.width,head[1]), head)+1),
        "left": 1000 / (dist((0,head[1]), head)+1)
    }

    # close to a border or snake?
    if not board.vacant((head[0]-1,head[1])):
        direction["left"] += 100000
    
    if not board.vacant((head[0]+1,head[1])):
        direction["right"] += 100000

    if not board.vacant((head[0],head[1]-1)):
        direction["up"] += 100000
    
    if not board.vacant((head[0],head[1]+1)):
        direction["down"] += 100000

    # snakes in area
    for snake in board.snakes:
        for pos in snake.coords:
            if pos == head: continue
            #right
            if pos[0] > head[0]:
                direction['right'] += 200 / dist(pos, head)
            #left
            elif pos[0] < head[0]:
                direction['left'] += 200 / dist(pos, head)
            #up
            if pos[1] < head[1]:
                direction['up'] += 200 / dist(pos, head)
            #down
            elif pos[1] > head[1]:
                direction['down'] += 200 / dist(pos, head)

    # food in area
    if not ignore_food:
        for pos in board.food:
            #right
            if pos[0] > head[0]:
                direction['right'] -= 2000 / dist(pos, head)
            #left
            elif pos[0] < head[0]:
                direction['left'] -= 2000 / dist(pos, head)
            #up
            if pos[1] < head[1]:
                direction['up'] -= 2000 / dist(pos, head)
            #down
            elif pos[1] > head[1]:
                direction['down'] -= 2000 / dist(pos, head)

    return min(direction.iterkeys(), key=(lambda key: direction[key]))
