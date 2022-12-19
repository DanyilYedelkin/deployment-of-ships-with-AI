from gui import *
from dfs import *
from bck import *

class Map:
    def __init__(self, boats, rows, columns):
        self.boats = boats
        self.rows = rows
        self.columns = columns

# fill 0 in each map's point
maps = np.zeros(10, Map)


# Create game maps with different sizes 
# 4x4
maps [0] = Map([3,2,1],[3,0,2,1],[3,1,2,0])
maps [1] = Map([4,2,1],[4,1,1,1],[2,1,3,1]) # not solvable

# 5x5
maps [2] = Map([4,3,2,1],[4,0,3,1,2],[1,4,1,3,1])
maps [3] = Map([4,3,2,1,1],[2,1,4,0,4],[2,1,3,2,3])

# 10x10
maps [4] = Map([4,3,3,2,2,2,1,1,1,1],[0,3,2,1,4,0,4,1,1,4],[0,5,3,1,2,4,2,1,2,0])
maps [5] = Map([4,3,3,2,2,2,1,1,1,1],[6,1,2,1,0,2,3,0,1,4],[4,2,0,4,2,3,0,0,5,0])


# create and draw game map from GUI file
drawMapMenu()
refreshScreen()

# set default parameters
algorithm = 'none'
map_board = None
result = None
running = True

while running:
    if map_board != None and algorithm != 'none' and result == None:
        boats = map_board.boats
        rows = map_board.rows
        columns = map_board.columns
        if algorithm == 'dfs':
            setDfsParams(boats, rows, columns)
            result = dfs(0, 0, 0)
            map_board = None
            algorithm = 'none'
            if result == -1:
                result = None
                screen.fill(BG_COLOR)
                drawMapMenu()
                refreshScreen()
            else:
                drawResult(result)
                refreshScreen()
        if algorithm == 'btMRV':
            setBckParams(boats, rows, columns)
            result = backtrackMRV()
            map_board = None
            algorithm = 'none'
            if result == -1:
                result = None
                screen.fill(BG_COLOR)
                drawMapMenu()
                refreshScreen()
            else:  
                drawResult(result)
                refreshScreen()
        if algorithm == 'btLCV':
            setBckParams(boats, rows, columns)
            result = backtrackLCV()
            map_board = None
            algorithm = 'none'
            if result == -1:
                result = None
                screen.fill(BG_COLOR)
                drawMapMenu()
                refreshScreen()
            else:  
                drawResult(result)
                refreshScreen()
        if algorithm == 'fcMRV':
            setBckParams(boats, rows, columns)
            result = forwardMRV()
            map_board = None
            algorithm = 'none'
            if result == -1:
                result = None
                screen.fill(BG_COLOR)
                drawMapMenu()
                refreshScreen()
            else:  
                drawResult(result)
                refreshScreen()
        if algorithm == 'fcLCV':
            setBckParams(boats, rows, columns)
            result = forwardLCV()
            map_board = None
            algorithm = 'none'
            if result == -1:
                result = None
                screen.fill(BG_COLOR)
                drawMapMenu()
                refreshScreen()
            else:  
                drawResult(result)
                refreshScreen()
        
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
            pg.quit()
        if event.type == pg.KEYDOWN:
            if result != None:
                if event.key == pg.K_ESCAPE:
                    result = None
                    
                    screen.fill(BG_COLOR)
                    drawMapMenu()
                    refreshScreen()
            elif map_board == None:
                if event.key == pg.K_0 or event.key == pg.K_KP0:
                    map_board = maps[0]
                    screen.fill(BG_COLOR)
                    drawAlgoMenu()
                    refreshScreen()
                if event.key == pg.K_1 or event.key == pg.K_KP1:
                    map_board = maps[1]
                    screen.fill(BG_COLOR)
                    drawAlgoMenu()
                    refreshScreen()
                if event.key == pg.K_2 or event.key == pg.K_KP2:
                    map_board = maps[2]
                    screen.fill(BG_COLOR)
                    drawAlgoMenu()
                    refreshScreen()
                if event.key == pg.K_3 or event.key == pg.K_KP3:
                    map_board = maps[3]
                    screen.fill(BG_COLOR)
                    drawAlgoMenu()
                    refreshScreen()
                if event.key == pg.K_4 or event.key == pg.K_KP4:
                    map_board = maps[4]
                    screen.fill(BG_COLOR)
                    drawAlgoMenu()
                    refreshScreen()
                if event.key == pg.K_5 or event.key == pg.K_KP5:
                    map_board = maps[5]
                    screen.fill(BG_COLOR)
                    drawAlgoMenu()
                    refreshScreen()

            elif algorithm == 'none':
                if event.key == pg.K_0 or event.key == pg.K_KP0:
                    algorithm = 'dfs'
                if event.key == pg.K_1 or event.key == pg.K_KP1:
                    algorithm = 'btMRV'
                if event.key == pg.K_2 or event.key == pg.K_KP2:
                    algorithm = 'btLCV'
                if event.key == pg.K_3 or event.key == pg.K_KP3:
                    algorithm = 'fcMRV'
                if event.key == pg.K_4 or event.key == pg.K_KP4:
                    algorithm = 'fcLCV'
                if event.key == pg.K_BACKSPACE:
                    map_board = None
                    screen.fill(BG_COLOR)
                    drawMapMenu()
                    refreshScreen()