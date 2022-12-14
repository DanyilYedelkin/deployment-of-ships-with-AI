
    
from gui import *
from the_real_dfs import *
from bck import *

class Map:
    def __init__(self, b,r,c):
        self.b = b
        self.r = r
        self.c = c
        
maps = np.zeros(10,Map)

# 4x4
maps [0] = Map([2,2,1],[1,2,0,2],[1,3,0,1])
maps [1] = Map([3,2,1],[1,2,1,2],[0,3,0,3])
maps [2] = Map([3,2,1],[3,0,2,1],[2,1,1,2])

# not solvable
maps [3] = Map([4,2,1],[4,1,1,1],[2,1,3,1])

# 5x5
maps [4] = Map([3,3,2,1,1],[1,2,2,2,3],[3,0,3,0,4])
maps [5] = Map([4,3,2,1,1],[2,1,4,0,4],[2,1,3,2,3])

# 7x7
#maps [6] = Map([4,3,2,2,1,1],[4,0,1,3,1,2,2],[0,5,1,1,3,1,2])
#maps [7] = Map([5,3,3,2,2,1,1],[3,0,4,2,1,1,6],[3,2,3,1,4,2,2])

# 10x10
maps [6] = Map([3,3,3,3,2,2,1,1,1],[4,0,2,3,1,1,2,2,1,3],[0,5,2,1,2,4,1,1,1,2])
maps [7] = Map([4,3,3,2,2,2,1,1,1,1],[6,1,2,1,0,2,3,0,1,4],[4,2,0,4,2,3,0,0,5,0])


drawMapMenu()
refreshScreen()

algo = 'none'

board = None

result = None

delay = 21




running = True
while running:
    if board != None and algo != 'none' and result == None:
        b = board.b
        r = board.r
        c = board.c
        if algo == 'dfs':
            setDfsParams(b,r,c)
            result = dfs(0, 0, 0)
            board = None
            algo = 'none'
            if result == 'interupt':
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
                if event.key == pg.K_SPACE:
                    result = None
                    
                    screen.fill(BG_COLOR)
                    drawMapMenu()
                    refreshScreen()
            elif board == None:
                if event.key == pg.K_0 or event.key == pg.K_KP0:
                    board = maps[0]
                    screen.fill(BG_COLOR)
                    drawAlgoMenu()
                    refreshScreen()
                if event.key == pg.K_1 or event.key == pg.K_KP1:
                    board = maps[1]
                    screen.fill(BG_COLOR)
                    drawAlgoMenu()
                    refreshScreen()
                if event.key == pg.K_2 or event.key == pg.K_KP2:
                    board = maps[2]
                    screen.fill(BG_COLOR)
                    drawAlgoMenu()
                    refreshScreen()
                if event.key == pg.K_3 or event.key == pg.K_KP3:
                    board = maps[3]
                    screen.fill(BG_COLOR)
                    drawAlgoMenu()
                    refreshScreen()
                if event.key == pg.K_4 or event.key == pg.K_KP4:
                    board = maps[4]
                    screen.fill(BG_COLOR)
                    drawAlgoMenu()
                    refreshScreen()
                if event.key == pg.K_5 or event.key == pg.K_KP5:
                    board = maps[5]
                    screen.fill(BG_COLOR)
                    drawAlgoMenu()
                    refreshScreen()
                if event.key == pg.K_6 or event.key == pg.K_KP6:
                    board = maps[6]
                    screen.fill(BG_COLOR)
                    drawAlgoMenu()
                    refreshScreen()
                if event.key == pg.K_7 or event.key == pg.K_KP7:
                    board = maps[7]
                    screen.fill(BG_COLOR)
                    drawAlgoMenu()
                    refreshScreen()
            elif algo == 'none':
                if event.key == pg.K_0 or event.key == pg.K_KP0:
                    algo = 'dfs'
                if event.key == pg.K_BACKSPACE:
                    board = None
                    screen.fill(BG_COLOR)
                    drawMapMenu()
                    refreshScreen()
