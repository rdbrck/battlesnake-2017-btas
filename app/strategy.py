from utils import dist


def general_direction(board, head, health):
    """ Returns the most 'beneficial' direction to move in """

    # start with general area
    direction = {
        "up": 5000 / (dist(head, (head[0],0))+1),
        "down": 5000 / (dist(head, (head[0],board.height))+1),
        "right": 5000 / (dist((board.width,head[1]), head)+1),
        "left": 5000 / (dist((0,head[1]), head)+1)
    }

    # close to a border or snake?
    if not board.vacant((head[0]-1,head[1])):
        direction["left"] += 1000000
    
    if not board.vacant((head[0]+1,head[1])):
        direction["right"] += 1000000

    if not board.vacant((head[0],head[1]-1)):
        direction["up"] += 1000000
    
    if not board.vacant((head[0],head[1]+1)):
        direction["down"] += 1000000

    # snakes in area
    for snake in board.snakes:
        for pos in snake.coords:
            if pos == head: continue
            #right
            if pos[0] > head[0]:
                direction['right'] += 1000 / dist(pos, head)
            #left
            elif pos[0] < head[0]:
                direction['left'] += 1000 / dist(pos, head)
            #up
            if pos[1] < head[1]:
                direction['up'] += 1000 / dist(pos, head)
            #down
            elif pos[1] > head[1]:
                direction['down'] += 1000 / dist(pos, head)

    # food in area
    if health < 60:
        for pos in board.food:
            if board.get_cell(pos) == 3 and (health - dist(pos, head) > 15): continue
            #right
            if pos[0] > head[0]:
                direction['right'] -= (10000 / ((health / 10) + 1)) / dist(pos, head)
            #left
            elif pos[0] < head[0]:
                direction['left'] -= (10000 / ((health / 10) + 1)) / dist(pos, head)
            #up
            if pos[1] < head[1]:
                direction['up'] -= (10000 / ((health / 10) + 1)) / dist(pos, head)
            #down
            elif pos[1] > head[1]:
                direction['down'] -= (10000 / ((health / 10) + 1)) / dist(pos, head)

    return min(direction.iterkeys(), key=(lambda key: direction[key]))
