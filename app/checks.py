import constants

def invalidmove_wall(direction, localArena, localSnakeX, localSnakeY, width, height):
        #print 'move_walling at', localSnakeX, localSnakeY

        if direction == constants.NORTH:
            north_boundary_distance = localSnakeY - 1
            if north_boundary_distance <= 0:
                #print 'I think i am at north wall'
                return constants.INVALID_MOVE

        elif direction == constants.EAST:
            east_boundary_distance = width - 1 - localSnakeX
            if east_boundary_distance <= 0:
                #print 'I think i am at east wall'
                return constants.INVALID_MOVE

        elif direction == constants.WEST:
            west_boundary_distance = localSnakeX - 1
            if west_boundary_distance <= 0:
                #print 'I think I am at west wall'
                return constants.INVALID_MOVE

        elif direction == constants.SOUTH:
            south_boundary_distance = height  - 1 - localSnakeY
            if south_boundary_distance <= 0:
                #print 'I think I am at south wall'
                return constants.INVALID_MOVE



def invalidmove(localArena, localSnakeX, localSnakeY, direction, width, height):
        if direction == constants.NORTH:
            north_boundary_distance = localSnakeY - 1
            if north_boundary_distance <= 0:
                #print 'I think i am at north wall'
                return constants.INVALID_MOVE
            elif localArena[localSnakeY - 1][localSnakeX] > 1:
                #print 'I think theres something to my north'
                return constants.INVALID_MOVE

        elif direction == constants.EAST:
            east_boundary_distance = width - 1 - localSnakeX    #double check that it's 2 when more thoughtful.
            if east_boundary_distance <= 0:
                #print 'I think i am at east wall'
                return constants.INVALID_MOVE
            elif localArena[localSnakeY][localSnakeX + 1] > 1:
                #print 'I think my east square is filled'
                return constants.INVALID_MOVE

        elif direction == constants.WEST:
            west_boundary_distance = localSnakeX - 1
            if west_boundary_distance <= 0:
                #print 'I think I am at west wall'
                return constants.INVALID_MOVE
            elif localArena[localSnakeY][localSnakeX - 1] > 1:
                #print 'I think west square is filled'
                return constants.INVALID_MOVE

        elif direction == constants.SOUTH:
            south_boundary_distance = height - 1 - localSnakeY     #double check that it's 2 when more thoughtful.
            if south_boundary_distance <= 0:
                #print 'I think I am at south wall'
                return constants.INVALID_MOVE
            elif localArena[localSnakeY + 1][localSnakeX] > 1:
                #print 'I think my south square is filled'
                return constants.INVALID_MOVE