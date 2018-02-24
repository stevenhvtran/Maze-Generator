from pprint import pprint
import random 
import numpy as np

#Generates the grid needed to start a maze
def gridGen(x):
    if x%2 != 0:
        #Creates the grid being used
        grid = [[0 for i in range(0,x)] for i in range(0,x)]
        grid = walls(walls(grid, x), x)
        return(list(map(list, grid)))
    else:
        #Forces an odd number for dimensions of grid
        gridGen(x+1)
    
#Creates the walls of the maze
def walls(grid, x):
    grid[::2] = [[i+1 for i in grid[i]] for i in range(0,int((x+1)/2))]
    grid = list(zip(*grid))
    return grid

#Sets the starting point of the maze to a random co-ordinate on the edge of the grid
def start(grid):
    randCoord = [1, 2*random.randint(0, (len(grid)-3)/2)+1] #Randomizing a point in first row
    grid[0][randCoord[1]] = 4 #Sets starting point to 3
    grid[1][randCoord[1]] = 3 #Sets predetermined first step to 3 too
    #Randomly reflects grid across diagonal to change starting edge
    if random.getrandbits(1) == 0:
        grid = transpose(grid)
        randCoord = transposeC(randCoord)
    #Randomly reflects the grid across the horizontal to change starting edge
    if random.getrandbits(1) == 0:
        grid = reverse(grid)
        randCoord = reverseC(randCoord, grid)
    return [grid, randCoord]
    
#Reflects a square array across its diagonal (top left to bottom right)
def transpose(grid):
    return list(map(list, zip(*grid)))
    
#Changes co-ordinate of a point on a transposed array to match transformation
def transposeC(coord):
    return [coord[1], coord[0]]
    
#Reflects an array across its horizontal
def reverse(grid):
    return grid[::-1]
    
#Changes co-ordinate of a point on a reflected array to match transformation
def reverseC(coord, grid):
    return [len(grid) - 1 - coord[0], coord[1]]
    
#Picks a random direction for the maze's path to go on
def goto(grid, invDir, squigFactor):
    #Picks directions that aren't already flagged as being 'invalid' previously
    direction = random.choice([dir for dir in ['n','s','e','w'] if dir not in invDir]) #Direction randomizer
    length = random.randint(0, int(np.sqrt(len(grid))/squigFactor))*2 
    return [length, direction]

#Checks to see if path is clear and if so, moves current position to a new one as determined
#by goto function    
def go(pos, grid, length, direction):
    #Moves the current position to the new place turning all those in path to 3's
    global invDir
    
    ''' Creates the path
    
    For every input from the goto randomizer...
    Transform the grid so that Easterly movement on the transformed
    grid is equivalent to the input direction.
    Then move the path to the east in accordance to goto randomizer
    if path is valid, if not add compass direction to invDir list.
    Then transform the grid back to its original form and return
    the grid and the new active co-ordinate.
    '''
    
    if direction == 'n':
        grid = transpose(reverse(grid))
        pos = transposeC(reverseC(pos, grid))
        if isClear(grid, pos , length) == True:
            for i in range(1, length+1):
                grid[pos[0]][pos[1]+i] = 3
            pos[1] += length
        else:
            invDir.append('n')
        grid = reverse(transpose(grid))
        pos = reverseC(transposeC(pos), grid)    
                
    if direction == 'e':
        if isClear(grid, pos , length) == True:
            for i in range(1, length+1):
                grid[pos[0]][pos[1]+i] = 3
            pos[1] += length
        else:
            invDir.append('e')            
    
    if direction == 's':
        grid = transpose(grid)
        pos = transposeC(pos)
        if isClear(grid, pos , length) == True:
            for i in range(1, length+1):
                grid[pos[0]][pos[1]+i] = 3             
            pos[1] += length
        else:
            invDir.append('s')
        grid = transpose(grid)
        pos = transposeC(pos)                
    
    if direction == 'w':
        grid = transpose(reverse(transpose(grid)))
        pos = transposeC(reverseC(transposeC(pos), grid))
        if isClear(grid, pos , length) == True:
            for i in range(1, length+1):
                grid[pos[0]][pos[1]+i] = 3
            pos[1] += length
        else:
            invDir.append('w')
        grid = transpose(reverse(transpose(grid)))
        pos = transposeC(reverseC(transposeC(pos), grid))    
            
    return [grid, pos, invDir]

def isClear(grid, pos, length):
    global invDir
    if sum(grid[pos[0]][pos[1]:pos[1]+length+1]) == (length/2)+3 and pos[1]+length < len(grid):
        invDir = []
        return True
    else:
        return False
    
invDir = []
def mazeGen(x):
    global invDir
    result = start(gridGen(x))
    grid, pos = result[0], result[1]
    hist = []
    return createPath(x, grid, pos, hist)
    
def createPath(x, grid, pos, hist):
    global invDir
    #6-2 is best configuration so far for speed and no gaps
    squigFactor = 6 #Medium effect on time, increasing will increase density of maze and reduce gaps
    retries = 2 #IDK effect on time but increasing value decreases black gaps
    while True:
        for i in range(0, 8): #Optimally only needs to loop 4 times to get all compass directions
            #If all moves in every direction are invalid retries with smaller path
            #Breaks after all retries are used up
            if len(invDir) == 4:
                invDir = []
                if retries > 0:
                    retries -= 1
                    continue
                if retries == 0:
                    retries += 2 #SHOULD BE THE SAME AS RETRIES STARTING VALUE
                hist.remove(pos)                
                if len(hist) < 2:
                    break
                pos = random.choice(hist)                
            step = goto(grid, invDir, squigFactor)
            grid, pos, invDir = go(pos, grid, step[0], step[1])
            if pos not in hist:
                hist.append(pos)
        invDir = []
        if len(hist) < 2:
            break
    #Re-use the start function to pick an endpoint for the maze
    return start(grid)[0]
    
