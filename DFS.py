
# create game map (logic map)
game_map = [[0 for i in range(11)] for i in range(11)] 

# for X coordinate
game_map[1][0] = 4
game_map[2][0] = 2
game_map[3][0] = 0
game_map[4][0] = 4
game_map[5][0] = 2
game_map[6][0] = 3
game_map[7][0] = 0
game_map[8][0] = 0
game_map[9][0] = 5
game_map[10][0] = 0


# for Y coordinate
game_map[0][1] = 6
game_map[0][2] = 1
game_map[0][3] = 2
game_map[0][4] = 1
game_map[0][5] = 0
game_map[0][6] = 2
game_map[0][7] = 3
game_map[0][8] = 0
game_map[0][9] = 1
game_map[0][10] = 4
        
        
        
print(game_map)
