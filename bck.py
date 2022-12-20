import numpy as np
import time
from gui import *

boats_array_in = np.array([2, 2, 2, 1])
boats_array = np.copy(boats_array_in)
boats_removed = np.array([0])
boats_removed = np.delete(boats_removed, 0)
row_array = np.array([3, 0, 2, 2])
col_array = np.array([3, 1, 2, 1])
steps = 0
start = 0
end = 0 
boats_pos_array = np.copy(boats_array).reshape(1, len(boats_array))
game_array = np.stack((row_array, col_array))
game = np.zeros((len(game_array[0])+2, len(game_array[0])+2), int)
LEN = len(game_array[0, :])

error = False

def setBacktrackingParams(boats, rows, columns):
    global row_array, col_array, boats_array_in, game_array, LEN, error
    error = False
    row_array = np.array(rows)
    col_array = np.array(columns)
    boats_array_in = np.array(boats)
    game_array = np.stack((row_array, col_array))
    LEN = len(game_array[0, :])
    retryData()
    setBoardParams(rows, columns)

def drawShips(array, x, y):
    global error, steps, start, end
    ans = np.copy(array[1:LEN+1, 1:LEN+1])
    horizontal = False
    clearScreen()
    for i in range(LEN):
        for j in range(LEN):
            lenght = 1
            if(ans[i, j] > 0):
                if(i+1 < LEN and ans[i+1, j] > 0):
                    horizontal = False
                    while(i+lenght < LEN and ans[i+lenght, j] > 0):
                        ans[i+lenght, j] = -1
                        lenght += 1
                    drawShip(i, i+lenght-1, j, horizontal)
                elif(j+1 < LEN and ans[i, j+1] > 0):
                    horizontal = True
                    while(j+lenght < LEN and ans[i, j+lenght] > 0):
                        ans[i, j+lenght] = -1
                        lenght += 1
                    drawShip(j, j+lenght-1, i, horizontal)
                else:
                    draw1x1Ship(j, i)
                    ans[i, j] = -1
    takeShot(x-1, y-1)
    end = time.time()
    drawStats(steps,end-start)
    refreshScreen()
    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                error = True
        if event.type == pg.QUIT:
            running = False
            pg.quit()


def canPutHorizontally(x, y, boat):
    global game, game_array
    if(y-1+boat > LEN) or (game_array[0, x-1]-boat < 0):
        return False
    for i in range(boat):
        if(game_array[1, y-1+i]-1 < 0):
            return False
    for row in range(3):
        for col in range(0, boat+2):
            if(game[x+row-1, y+col-1] > 0):
                return False
    return True

def canPutVertically(x, y, boat):
    global game, game_array
    if(x-1+boat > LEN) or (game_array[1, y-1]-boat < 0):
        return False
    for i in range(boat):
        if(game_array[0, x-1+i]-1 < 0):
            return False
    for col in range(3):
        for row in range(boat+2):
            if(game[x+row-1, y+col-1] > 0):
                return False
    return True

def isSolved():
    global game_array
    if(np.all(game_array == 0)):
        return True
    return False

def posPositions(boat):
    posit = []
    for row in range(1, LEN+1):
        for col in range(1, LEN+1):
            if(canPutHorizontally(row, col, boat)):
                posit.append([row, col])
            if(canPutVertically(row, col, boat) and boat > 1):
                posit.append([row+LEN, col])
    return posit

def MRV(boats_array):
    boats_sorted = np.array(sorted(boats_array, reverse=True)).reshape(len(boats_array), 1)
    return [{'boat': int(boat), 'pos': posPositions(int(boat))} for boat in boats_sorted]

def getLCV():
    global boats_array
    pos_boats = MRV(boats_array)
    out = 0
    for index in pos_boats:
        out += len((index['pos']))
    return out


def putBoatHorizontally(x, y, boat):
    global game, game_array
    if(not canPutHorizontally(x, y, boat)):
        return False
    game_array[0, x-1] -= boat
    for i in range(boat):
        game[x, y+i] = 1
        game_array[1, y-1+i] -= 1
    game[x, y] = boat
    return True


def putBoatVertically(x, y, boat):
    global game, game_array
    if(not canPutVertically(x, y, boat)):
        return False
    game_array[1, y-1] -= boat
    for i in range(boat):
        game[x+i, y] = 1
        game_array[0, x-1+i] -= 1
    game[x, y] = boat+LEN
    return True

def putBoat(x, y, boat):
    global game
    if(x <= LEN):
        putBoatHorizontally(x, y, boat)
    else:
        putBoatVertically(x % LEN, y, boat)


def boatBack(x, y):
    global game, game_array
    boat = game[x, y] % LEN
    if(boat < 1) or (boat == 1 and (game[x-1, y] > 0 or game[x+1, y] > 0 or game[x, y-1] > 0 or game[x, y+1] > 0)):
        return False
    if(game[x, y] > LEN):
        for i in range(boat):
            game[x+i, y] = 0
            game_array[0, x-1+i] += 1
        game_array[1, y-1] += boat
        return addBack(boat)
    else:
        for i in range(boat):
            game[x, y+i] = 0
            game_array[1, y-1+i] += 1
        game_array[0, x-1] += boat
        return addBack(boat)

def removeBoat(boat):
    global boats_array, boats_removed
    for i in range(len(boats_array)):
        if(boats_array[i] == boat):
            boats_array = np.delete(boats_array, i)
            boats_removed = np.append(boats_removed, boat)
            return boat
    return -1

def addBack(boat):
    global boats_array, boats_removed
    for i in range(len(boats_removed)):
        if(boats_removed[i] == boat):
            boats_removed = np.delete(boats_removed, i)
            boats_array = np.append(boats_array, boat)
            return boat
    return -1


def tryPutBoat(x, y, boats_array):
    global game, game_array
    for boat in boats_array:
        if(putBoatHorizontally(x, y, boat) or putBoatVertically(x, y, boat)):
            return removeBoat(boat)
    return False


def switchBoats():
    global boats_array_in
    boats_array_in = np.append(boats_array_in, boats_array_in[0])
    boats_array_in = np.delete(boats_array_in, 0)


def retryData():
    global game, boats_array, boats_removed, game_array
    game_array = np.stack((row_array, col_array))
    game = np.zeros((len(game_array[0])+2, len(game_array[0])+2), int)
    boats_array = np.copy(boats_array_in)
    boats_removed = np.array([0])
    boats_removed = np.delete(boats_removed, 0)
    
    
def putBoatLCV(x, y, boat):
    putBoat(x, y, boat)
    removeBoat(boat)
    out = getLCV()
    boatBack(x % LEN, y)
    return out



def sortLCV(pos_boats_pos):
    global game ,game_array, boats_array,boats_removed
    first = 0
    second = 0
    dummy_game = np.copy(game) 
    dummy_game_array = np.copy(game_array)
    dummy_boats_array = np.copy(boats_array)
    dummy_boats_removed = np.copy(boats_removed)
    retryData()
    for index in pos_boats_pos:
        array = index['pos']
        boat = index['boat']
        for i in range(len(array)-1):
            for j in range(len(array)-1-i):
                first = putBoatLCV(array[j][0], array[j][1], boat)
                second = putBoatLCV(array[j+1][0], array[j+1][1], boat)
                if(first < second):
                    buffer = array[j]
                    array[j] = array[j+1]
                    array[j+1] = buffer
            
        index['pos']=array
    retryData()
    game = dummy_game
    game_array = dummy_game_array
    boats_array = dummy_boats_array
    boats_removed = dummy_boats_removed
    return pos_boats_pos


cout = 0
solved_game = np.copy(game)
last_solved = np.zeros((len(game_array[0])+2, len(game_array[0])+2), int)


def backtrackAlgorithm(index, pos_boats_pos):
    global steps, solved_game, last_solved
    if error:
        return -1
    if(isSolved()):
        if(not np.array_equal(game, last_solved)):
            last_solved = np.copy(game)
        return isSolved()
    if(index >= len(boats_array)):
        return isSolved()
    a = index+1
    current_boat = pos_boats_pos[index]['boat']
    for pos in pos_boats_pos[index]['pos']:
        if error:
            return -1
        if(game[pos[0] % LEN, pos[1]] > 0): 
            continue
        drawShips(game, pos[1], pos[0] % LEN)
        if(pos[0] > LEN):
            if(putBoatVertically(pos[0]-LEN, pos[1], current_boat)):
                steps+=1
                backtrackAlgorithm(a, pos_boats_pos)
                if(isSolved()):
                    return isSolved()
                boatBack(pos[0]-LEN, pos[1])
        else:
            if(putBoatHorizontally(pos[0], pos[1], current_boat)):
                steps+=1
                backtrackAlgorithm(a, pos_boats_pos)

                if(isSolved()):
                    drawShips(game, pos[1], pos[0] % LEN)
                    return isSolved()
                boatBack(pos[0], pos[1])     
        print(steps,end - start)
    return isSolved()


def backtrackMRV():
    global steps,start
    start = time.time()
    steps = 0
    return backtrackAlgorithm(0, MRV(boats_array))

def backtrackLCV():
    global steps,start
    steps = 0
    pos = sortLCV(MRV(boats_array))
    start = time.time()
    return backtrackAlgorithm(0,pos )

def logicForwardMRV(index):
    global steps, last_solved, solved_game, boats_array
    pos_boats_pos = MRV(boats_array)
    if error:
        return -1
    if(isSolved()):
        if(not np.array_equal(game, last_solved)):
            last_solved = np.copy(game)
        return isSolved()
    if(index >= len(boats_array)):
        return isSolved()
    a = index+1
    for pos in pos_boats_pos[index]['pos']:
        if error:
            return -1
        current_boat = pos_boats_pos[index]['boat']
        steps+=1
        if(pos[0] > LEN):
            if(putBoatVertically(pos[0]-LEN, pos[1], current_boat)):
                drawShips(game, pos[1], pos[0]-LEN)
                steps+=1
                logicForwardMRV(a)
                if(isSolved()):
                    return isSolved()
                boatBack(pos[0]-LEN, pos[1])
        else:
            if(putBoatHorizontally(pos[0], pos[1], current_boat)):
                drawShips(game, pos[1], pos[0])
                steps+=1
                logicForwardMRV(a)
                if(isSolved()):
                    return isSolved()
                boatBack(pos[0], pos[1])
        print(steps,end - start)
    return isSolved()

def logicForwardLCV(index):
    global steps, solved_game, boats_array, last_solved
    pos_boats_pos = sortLCV(MRV(boats_array))
    if error:
        return -1
    if(isSolved()):
        if(not np.array_equal(game, last_solved)):
            last_solved = np.copy(game)
        return isSolved()
    if(index >= len(boats_array)):
        return isSolved()
    a = index+1
    for pos in pos_boats_pos[index]['pos']:
        if error:
            return -1
        current_boat = pos_boats_pos[index]['boat']
        if(pos[0] > LEN):
            if(putBoatVertically(pos[0]-LEN, pos[1], current_boat)):
                drawShips(game, pos[1], pos[0]-LEN)
                steps+=1
                logicForwardLCV(a)
                if(isSolved()):
                    return isSolved()
                boatBack(pos[0]-LEN, pos[1])
        else:
            if(putBoatHorizontally(pos[0], pos[1], current_boat)):
                drawShips(game, pos[1], pos[0])
                steps+=1
                logicForwardLCV(a)
                if(isSolved()):
                    return isSolved()
                boatBack(pos[0], pos[1])
        print(steps,end - start)
    return isSolved()
                
def forwardMRV():
   global steps, start
   start = time.time()
   steps = 0
   return logicForwardMRV(0)

def forwardLCV():
    global steps, start
    start = time.time()
    steps = 0
    return logicForwardLCV(0)
