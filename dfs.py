import numpy as np
from gui import *
import time


start = time.time()

class Lode:
    def __init__(self, length, y, x, state):
        self.length = length
        self.y = y
        self.x = x
        self.state = state


def setDfsParams(b,r,c):
    global solved, error, lodes, row_rules, col_rules, field_len, field, lodes_len, lodes_info
    global steps, start
    solved = False
    error = False
    lodes = b
    row_rules = r
    col_rules = c
    field_len = len(row_rules)
    lodes_len = len(lodes)
    field = np.zeros((field_len,field_len),int)
    lodes_info = np.zeros(lodes_len,Lode)
    steps = 0
    start = time.time()
    setBoardParams(r, c)

def setVisited(lode,y,x,state,idx):
    global lodes_info
    if state:
        field[y,x:x+lode] += 1
    else:
        field[y:y+lode,x] += 1
    lodes_info[idx] = Lode(lode,y,x,state)
    
def removeVisited(lode,y,x,state):
    if state:
        field[y,x:x+lode] -= 1
    else:
        field[y:y+lode,x] -= 1


def checkHorizontal(lode, y, x):
    if field_len >= x + lode:
        return True
    return False

def checkVertical(lode, y, x):
    if field_len >= y + lode:
        return True
    return False

def drawLodes():
    global lodes_info,  error,  steps, start
    idx = 0
    clearScreen()
    for lode in lodes_info:
        idx += 1
        length = lode.length
        y = lode.y
        x = lode.x
        state = lode.state
        if length == 1:
            draw1x1Ship(x, y)
        else:
            drawShip(x if state else y, x + length -1 if state else y + length -1, y if state else x, True if state else False)
        setColorIdx(idx)
    setColorIdx(0)
    drawDelay(0)
    end = time.time()
    drawStats(steps, end-start)
    refreshScreen()
    pg.time.delay(0)
    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                error = True
        if event.type == pg.QUIT:
            running = False
            pg.quit()

def isSolved():
    global field_len,  lodes_info
    if np.count_nonzero(field[:] > 1) > 0:
        return False
    for row in range(field_len):
        if row_rules[row] != np.count_nonzero(field[row,:]):
            return False
    for col in range(field_len):
        if col_rules[col] != np.count_nonzero(field[:,col]):
            return False
    for idx in range(lodes_len):
        length = lodes_info[idx].length
        y = lodes_info[idx].y
        x = lodes_info[idx].x
        if lodes_info[idx].state:
            left = x - 1 if x > 0 else x
            right = x + length  if x + length < field_len else x + length -1
            # check if horizontal ship have neighbour
            if y > 0 and np.count_nonzero(field[y-1,left:right]) > 0:
                return False
            if y < field_len - 1 and np.count_nonzero(field[y + 1,left:right]) > 0:
                return False
            if left < x and field[y,left] > 0:
                return False
            if right == x + length and field[y,right] > 0:
                return False
        else:
            top = y - 1 if y > 0 else y
            bottom = y + length  if y + length < field_len else y + length -1
            # check if vertical ship have neighbour
            if x > 0 and np.count_nonzero(field[top:bottom,x-1]) > 0:
                return False
            if x < field_len - 1 and np.count_nonzero(field[top:bottom,x+1]) > 0:
                return False
            if top < y and field[top,x] > 0:
                return False
            if bottom == y + length and field[bottom,x] > 0:
                return False
    return True     
    

def dfs(idx, y, x):
    global field_len, counter, solved, steps, start
    for row in range(field_len):
        for col in range(field_len):
            if solved :
                return solved 
            if error:
                return -1
            if checkHorizontal(lodes[idx], row, col) and not solved:
                setVisited(lodes[idx], row, col, 1, idx)
                if idx == lodes_len - 1:
                    if isSolved():
                        solved = True
                        return solved
                    removeVisited(lodes[idx], row, col, 1)
                else:
                    dfs(idx+1, 0, 0)
                    removeVisited(lodes[idx], row, col, 1)
                drawLodes()
            if lodes[idx] > 1 and checkVertical(lodes[idx], row, col) and not solved:
                setVisited(lodes[idx], row, col, 0, idx)
                if idx == lodes_len - 1:
                    if isSolved():
                        solved = True
                        return solved
                    explored += 1
                    removeVisited(lodes[idx], row, col, 0)
                else:  
                    dfs(idx+1, 0, 0)
                    removeVisited(lodes[idx], row, col, 0)
                drawLodes()
            steps += 1
    end = time.time()
    print(steps,end - start)
    if (error):
        return -1 
    return solved
