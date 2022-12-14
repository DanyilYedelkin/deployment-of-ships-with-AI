import pygame as pg
import pandas as pd
import numpy as np
import time 

TILES_COUNT = 10

# dimensions
NAV_SIZE = 60
TILE_SIZE = 60 
BOARD_SIZE = TILES_COUNT * TILE_SIZE
SCREEN_SIZE = BOARD_SIZE + NAV_SIZE
SHIP_WIDTH = int(TILE_SIZE/2)
CIRCLE_WIDTH = int(SHIP_WIDTH/2)
SHOT_WIDTH = int(CIRCLE_WIDTH/2)

# offsets
OFFSET = TILE_SIZE/2
TEXT_Y_OFFSET = 14
ONE_DIGIT_X_OFFSET = 22
TWO_DIGIT_X_OFFSET = 12.5

# colors
COLORS = [(255,102,255),(255,0,0),(0,255,255),(255, 255, 0),(255, 0, 255),(255, 153, 0),(153, 102, 255),(255, 255, 255),(255, 153, 255),(153, 102, 51)]
BG_COLOR = (42, 42, 42)
SHOT_COLOR = (255,0,0)
LINE_COLOR = (196,57,255)
TEXT_COLOR = (231,65,255)
SHIP_COLOR = (255,102,255)

color_idx = 0
# reading from file
yValues = []
xValues = []

# dummy data
def setBoardParams(rows, cols):
    global TILES_COUNT, BOARD_SIZE, SCREEN_SIZE, yValues, xValues, color_idx
    TILES_COUNT = len(rows)
    BOARD_SIZE = TILES_COUNT * TILE_SIZE
    SCREEN_SIZE = BOARD_SIZE + NAV_SIZE
    yValues = rows
    xValues = cols
    color_idx = 0
    
def setColorIdx(idx):
    global color_idx
    color_idx = idx

array = np.array([[0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0],
         [0,0,1,1,0,0,0,0,0,0],
         [0,0,0,1,0,0,0,0,0,0],
         [0,0,0,1,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0]])

def drawMapMenu():
    screen.blit(textFont.render('Welcome to the ship deployment simulation', False, TEXT_COLOR),(2*TILE_SIZE + 20, 10))
    screen.blit(textFont.render('in the battleship game.', False, TEXT_COLOR),(5*TILE_SIZE, 40))
    screen.blit(textFont.render('Press the Key to choose a map size:', False, TEXT_COLOR),(4*TILE_SIZE - 10, 100))
    
    for i in range(6):
        if i < 2:
            size = '4x4'
        elif i < 4:
            size = '5x5'
        else:
            size = '10x10'
        screen.blit(textFont.render(str(i)+' - map size:  ' + size, False, TEXT_COLOR),(TILE_SIZE + 10, 153 + 30 * i))
        

def drawAlgoMenu():
    screen.blit(textFont.render('Press the Key:', False, TEXT_COLOR),(6*TILE_SIZE + 10, TILE_SIZE))
    screen.blit(textFont.render('to select the algorithm', False, TEXT_COLOR),(5*TILE_SIZE - 10, TILE_SIZE + 40))
    screen.blit(textFont.render('0 - DFS', False, TEXT_COLOR),(TILE_SIZE, TILE_SIZE*2 + 40))


def drawResult(solved):
    if solved:
        text = 'SOLVED'
    else:
        text = 'NOT SOLVED'
    pg.draw.line(screen, BG_COLOR, (SCREEN_SIZE+5,400),(SCREEN_SIZE+600,400), 300)
    screen.blit(textFont.render(text, False, TEXT_COLOR),(SCREEN_SIZE + 10, 260))
    screen.blit(textFont.render('Press SPACE to return to menu', False, TEXT_COLOR),(SCREEN_SIZE + 10, 310))
    
def drawDelay(value):
    screen.blit(textFont.render('Delay: ' + str(value), False, TEXT_COLOR),(SCREEN_SIZE + 10, 210))
    screen.blit(textFont.render('Press P to pause', False, TEXT_COLOR),(SCREEN_SIZE + 10, 260))
    screen.blit(textFont.render('Press Q to quit', False, TEXT_COLOR),(SCREEN_SIZE + 10, 310))
    
def drawStats(explored, expanded, steps, time):
    screen.blit(textFont.render('Expanded: ' + str(expanded), False, TEXT_COLOR),(SCREEN_SIZE + 10, 10))
    screen.blit(textFont.render('Explored: ' + str(explored), False, TEXT_COLOR),(SCREEN_SIZE + 10, 60))
    screen.blit(textFont.render('Steps: ' + str(steps), False, TEXT_COLOR),(SCREEN_SIZE + 10, 110))
    screen.blit(textFont.render('Time: ' + str(round(time,2)), False, TEXT_COLOR),(SCREEN_SIZE + 10, 160))
  
def drawPause():
    screen.blit(textFont.render('PAUSED', False, TEXT_COLOR),(SCREEN_SIZE + 10, 360))



# draw grid
def drawGrid():
    for lineIndex in range(TILES_COUNT):
        pos = lineIndex*TILE_SIZE
        boardSize = TILES_COUNT * TILE_SIZE
        pg.draw.line(screen, LINE_COLOR, (0, pos), (boardSize, pos), 1)
        pg.draw.line(screen, LINE_COLOR, (pos, 0), (pos, boardSize), 1)
    
# draw values
def drawValues():
    for dimension in range(2):
        for lineIndex in range(TILES_COUNT):
            #print(lineIndex, xValues, yValues)
            horizontal = dimension == 0
            value = xValues[lineIndex] if horizontal else yValues[lineIndex]
            xOffset = ONE_DIGIT_X_OFFSET if value < 10 else TWO_DIGIT_X_OFFSET
            digitText = textFont.render(str(value), False, TEXT_COLOR)
            xPos = lineIndex*TILE_SIZE+xOffset if horizontal else BOARD_SIZE+xOffset
            yPos = BOARD_SIZE+TEXT_Y_OFFSET if horizontal else lineIndex*TILE_SIZE+TEXT_Y_OFFSET
            
            screen.blit(digitText,(xPos, yPos))
     
# draw ship longer than 1x1
def drawShip(start, end, line, horizontal):
    lineCoordinate = line*TILE_SIZE+OFFSET
    circleCoordinate = lineCoordinate+1
    startCoordinate = start*TILE_SIZE+OFFSET
    endCoordinate = end*TILE_SIZE+OFFSET
    
    if horizontal:
        startPos = (startCoordinate, lineCoordinate)
        endPos = (endCoordinate, lineCoordinate)
        startCirclePos = (startCoordinate, circleCoordinate)
        endCirclePos = (endCoordinate, circleCoordinate)
    else:
        startPos = (lineCoordinate, startCoordinate)
        endPos = (lineCoordinate, endCoordinate)
        startCirclePos = (circleCoordinate, startCoordinate)
        endCirclePos = (circleCoordinate, endCoordinate)
    
    pg.draw.circle(screen, COLORS[color_idx], startCirclePos, CIRCLE_WIDTH)
    pg.draw.circle(screen, COLORS[color_idx], endCirclePos, CIRCLE_WIDTH)
    pg.draw.line(screen, COLORS[color_idx], startPos, endPos, SHIP_WIDTH)
    
def draw1x1Ship(x, y):
    pos = (x*TILE_SIZE+OFFSET+1, y*TILE_SIZE+OFFSET+1)
    
    pg.draw.circle(screen, COLORS[color_idx], pos, CIRCLE_WIDTH)
    
def refreshScreen():
    pg.display.update()
    
def clearScreen():
    screen.fill(BG_COLOR)
    drawGrid()
    drawValues()

def readValues(string: str):
    values = pd.read_csv(string+'/inputs.txt')
    xValues = np.array(values["columns"])
    yValues = np.array(values["rows"])
    return (xValues,yValues)

def drawSolution(array):
    ans = array
    horizontal= False
    for i in range(1,len(array)-1):
        for j in range(1,len(array)-1):
            lenght = 1
            if(ans[i,j]==1):
                if(i+1<TILES_COUNT and ans[i+1,j]==1):
                    horizontal=False
                    while( i+lenght<TILES_COUNT and ans[i+lenght,j]==1 ):
                        ans[i+lenght,j]=2
                        lenght+=1
                    drawShip(i, i+lenght-1, j, horizontal)   
                elif(j+1<TILES_COUNT and ans[i,j+1]==1):
                    horizontal=True
                    while(j+lenght<TILES_COUNT and ans[i,j+lenght]==1):
                        ans[i,j+lenght]=2
                        lenght+=1
                    drawShip(j, j+lenght-1, i, horizontal)
                else :
                    draw1x1Ship(i, j)
                    ans[i,j]=2
                    
def takeShot(x, y):
    pos = (x*TILE_SIZE+OFFSET+1, y*TILE_SIZE+OFFSET+1)
    
    pg.draw.circle(screen, SHOT_COLOR, pos, SHOT_WIDTH)

#init screen
pg.init()
screen = pg.display.set_mode((SCREEN_SIZE + 400, SCREEN_SIZE))
screen.fill(BG_COLOR)
pg.display.update()
textFont = pg.font.SysFont('Console', 30)

