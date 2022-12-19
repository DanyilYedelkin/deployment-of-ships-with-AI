import numpy as np
import time
from gui import *

boats_array_in = np.array([2, 2, 2, 1])
boats_array = np.copy(boats_array_in)
boats_removed = np.array([0])
boats_removed = np.delete(boats_removed, 0)
row_array = np.array([3, 0, 2, 2])
col_array = np.array([3, 1, 2, 1])
explored = 0
expanded = 0
steps = 0
start = 0
end = 0 
boats_pos_array = np.copy(boats_array).reshape(1, len(boats_array))
game_array = np.stack((row_array, col_array))
game = np.zeros((len(game_array[0])+2, len(game_array[0])+2), int)
LEN = len(game_array[0, :])
for boat in boats_array:
    if(boat > LEN):
        print("ERROR: length of the boat is more than size of the map")

interupt = False

def setBckParams(b, r, c):
    global row_array, col_array, boats_array_in, game_array, LEN, interupt
    interupt = False
    row_array = np.array(r)
    col_array = np.array(c)
    boats_array_in = np.array(b)
    game_array = np.stack((row_array, col_array))
    LEN = len(game_array[0, :])
    retryData()
    setBoardParams(r, c)

def drawShips(array, x, y):
    global interupt ,explored , expanded,steps,start,end
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
                interupt = True
        if event.type == pg.QUIT:
            running = False
            pg.quit()

# function to test if boat can be at x,y possition horizontally
def canPutHor(x, y, boat):
    global game
    global game_array
    # can boat fit ?
    if(y-1+boat > LEN):
        return False
    # can boat be here ?
    if(game_array[0, x-1]-boat < 0):
        return False
    for i in range(boat):
        if(game_array[1, y-1+i]-1 < 0):
            return False
    # does boat intersect ?
    for row in range(3):
        for col in range(0, boat+2):
            if(game[x+row-1, y+col-1] > 0):
                return False
    return True

# function to test if boat can be at x,y possition vertically
def canPutVer(x, y, boat):
    global game
    global game_array
    # can boat fit ?
    if(x-1+boat > LEN):
        return False
    # can boat be here ?
    if(game_array[1, y-1]-boat < 0):
        return False
    for i in range(boat):
        if(game_array[0, x-1+i]-1 < 0):
            return False
    # does boat intersect ?
    for col in range(3):
        for row in range(boat+2):
            if(game[x+row-1, y+col-1] > 0):
                return False
    return True




# test if game is solved
def solved():
    global game_array
    if(np.all(game_array == 0)):
        return True
    return False


# function that returns array of possible positions for boat
def posPositions(boat):
    posit = []
    for row in range(1, LEN+1):
        for col in range(1, LEN+1):
            if(canPutHor(row, col, boat)):
                posit.append([row, col])
            if(canPutVer(row, col, boat) and boat > 1):
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


# puts boat on board horizontally
def putBoatHor(x, y, boat):
    global game
    global game_array
    if(not canPutHor(x, y, boat)):
        return False
    game_array[0, x-1] -= boat
    for i in range(boat):
        game[x, y+i] = 1
        game_array[1, y-1+i] -= 1
    game[x, y] = boat
    return True


def putBoatVer(x, y, boat):
    global game
    global game_array
    if(not canPutVer(x, y, boat)):
        return False
    game_array[1, y-1] -= boat
    for i in range(boat):
        game[x+i, y] = 1
        game_array[0, x-1+i] -= 1
    game[x, y] = boat+LEN
    return True

# remove boat from board
def putBoat(x, y, boat):
    global game
    if(x > LEN):
        putBoatVer(x % LEN, y, boat)
    else:
        putBoatHor(x, y, boat)


def boatBack(x, y):
    global game
    global game_array
    boat = game[x, y] % LEN
    if(boat < 1):
        return 0
    if(boat == 1 and (game[x-1, y] > 0 or game[x+1, y] > 0 or game[x, y-1] > 0 or game[x, y+1] > 0)):
        return 0
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

# removes boat from list when its placed
def removeBoat(boat):
    global boats_array
    global boats_removed
    for i in range(len(boats_array)):
        if(boats_array[i] == boat):
            boats_array = np.delete(boats_array, i)
            boats_removed = np.append(boats_removed, boat)
            return boat
    return -1

# adding back boat to the boat_array
def addBack(boat):
    global boats_array
    global boats_removed
    for i in range(len(boats_removed)):
        if(boats_removed[i] == boat):
            boats_removed = np.delete(boats_removed, i)
            boats_array = np.append(boats_array, boat)
            return boat
    return -1


def tryPutBoat(x, y, boats_array):
    global game
    global game_array
    for boat in boats_array:
        if(putBoatHor(x, y, boat) or putBoatVer(x, y, boat)):
            return removeBoat(boat)
    return 0


def switchBoats():
    global boats_array_in
    boats_array_in = np.append(boats_array_in, boats_array_in[0])
    boats_array_in = np.delete(boats_array_in, 0)


def retryData():
    global game
    global boats_array
    global boats_removed
    global game_array
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
    first = 0
    second = 0
    global game ,game_array, boats_array,boats_removed
    dummy_game = np.copy(game) 
    dummy_game_array = np.copy(game_array)
    dummy_boats_array = np.copy(boats_array)
    dummy_boats_removed = np.copy(boats_removed)
    retryData()
    #print("running")
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

#print(LEN)


cout = 0
solved_game = np.copy(game)
last_solved = np.zeros((len(game_array[0])+2, len(game_array[0])+2), int)


def bckAdvanced(index, pos_boats_pos):
    global expanded,explored,steps
    global solved_game

    global last_solved
    expanded+=1
    if interupt:
        return 'interupt'
    if(solved()):
        print("the task is solved")
        if(not np.array_equal(game, last_solved)):
            last_solved = np.copy(game)
        return solved()
    if(index >= len(boats_array)):
        print("end of the boats")
        return solved()
    if(len(boats_array)==1):
        explored+=1
    a = index+1
    current_boat = pos_boats_pos[index]['boat']
    for pos in pos_boats_pos[index]['pos']:
        if interupt:
            return 'interupt'
        if(game[pos[0] % LEN, pos[1]] > 0): 
            continue
        drawShips(game, pos[1], pos[0] % LEN)
        if(pos[0] > LEN):
            if(putBoatVer(pos[0]-LEN, pos[1], current_boat)):
                steps+=1
                bckAdvanced(a, pos_boats_pos)
                if(solved()):
                    return solved()
                boatBack(pos[0]-LEN, pos[1])
        else:
            if(putBoatHor(pos[0], pos[1], current_boat)):
                steps+=1
                bckAdvanced(a, pos_boats_pos)

                if(solved()):
                    drawShips(game, pos[1], pos[0] % LEN)
                    return solved()
                boatBack(pos[0], pos[1])     
        print(steps,end - start)
    return solved()


def backtrackMRV():
    global expanded,explored,steps,start
    start = time.time()
    expanded,explored,steps = 0,0,0
    return bckAdvanced(0, MRV(boats_array))

def backtrackLCV():
    global expanded,explored,steps,start
    expanded,explored,steps = 0,0,0
    pos= sortLCV(MRV(boats_array))
    start = time.time()
    return bckAdvanced(0,pos )

def frwMRV(index):
    global expanded,explored,steps
    global solved_game
    global boats_array
    pos_boats_pos = MRV(boats_array)
    global last_solved
    expanded+=1
    if interupt:
        return 'interupt'
    if(solved()):
        print("the task is solved")
        if(not np.array_equal(game, last_solved)):
            last_solved = np.copy(game)
        return solved()

    if(index >= len(boats_array)):
        print("end of the boats")
        return solved()
    if(len(boats_array)==1):
        explored+=1
    a = index+1
    for pos in pos_boats_pos[index]['pos']:
        if interupt:
            return 'interupt'
        current_boat = pos_boats_pos[index]['boat']
        steps+=1
        if(pos[0] > LEN):
            if(putBoatVer(pos[0]-LEN, pos[1], current_boat)):
                drawShips(game, pos[1], pos[0]-LEN)
                steps+=1
                frwMRV(a)
                if(solved()):
                    return solved()
                boatBack(pos[0]-LEN, pos[1])
        else:
            if(putBoatHor(pos[0], pos[1], current_boat)):
                drawShips(game, pos[1], pos[0])
                steps+=1
                frwMRV(a)
                if(solved()):
                    return solved()
                boatBack(pos[0], pos[1])
        print(steps,end - start)
    return solved()

def frwLCV(index):
    global expanded,explored,steps
    global solved_game
    global boats_array
    expanded+=1
    pos_boats_pos = sortLCV(MRV(boats_array))
    global last_solved
    if interupt:
        return 'interupt'
    if(solved()):
        print("the task is solved")
        if(not np.array_equal(game, last_solved)):
            last_solved = np.copy(game)
        return solved()

    if(index >= len(boats_array)):
        print("end of the boats")
        return solved()
    if(len(boats_array)==1):
        explored+=1
    a = index+1
    for pos in pos_boats_pos[index]['pos']:
        if interupt:
            return 'interupt'
        current_boat = pos_boats_pos[index]['boat']
        if(pos[0] > LEN):
            if(putBoatVer(pos[0]-LEN, pos[1], current_boat)):
                drawShips(game, pos[1], pos[0]-LEN)
                steps+=1
                frwLCV(a)
                if(solved()):
                    return solved()
                boatBack(pos[0]-LEN, pos[1])
        else:
            if(putBoatHor(pos[0], pos[1], current_boat)):
                drawShips(game, pos[1], pos[0])
                steps+=1
                frwLCV(a)
                if(solved()):
                    return solved()
                boatBack(pos[0], pos[1])
        print(steps,end - start)
    return solved()
                
def forwardMRV():
   global expanded,explored,steps,start
   start = time.time()
   expanded,explored,steps = 0,0,0
   return frwMRV(0)

def forwardLCV():
    global expanded,explored,steps,start
    start = time.time()
    expanded,explored,steps = 0,0,0
    return frwLCV(0)
