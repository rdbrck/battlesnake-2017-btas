from collections import deque

#   Breadth-firs Search
#
#   Parameter:
#               x = x coordinate of mySnake
#               y = y coordinate of mySnake
#
#               Map: Pre-made 2D array with following attributes
#                       Wall, Snake body = 1
#                       Food = 2
#                       Empty space = 0
#
#   Return: An array contains shortet path from snake head to food

def BFS(x,y,Map):
    Map[x][y] = 0
    queue = deque( [(x,y,None)])
    while len(queue)>0:
        node = queue.popleft()
        x = node[0]
        y = node[1]
        if Map[x][y] == 2: # If we reach food
            return GetPathFromNodes(node) # Rebuild path
        if (Map[x][y] != 0):
            continue
        Map[x][y]= -1 # Mark as explored
        for i in [[x-1,y],[x+1,y],[x,y-1],[x,y+1]]:
            queue.append((i[0],i[1],node))
    return []

def GetPathFromNodes(node):
    path = []
    while(node != None):
        path.append((node[0],node[1]))
        node = node[2]
    return path
