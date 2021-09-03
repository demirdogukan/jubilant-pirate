level_map = ['9999999999999999999999999999',
             '9999999999999999999999999999',
             '9999999999999999999999999999',
             '0XX0000XXX000000000000XX0000',
             '9XXP                        ',
             ' XXXX         XX         XX ',
             ' XXXX       XX              ',
             ' XX    X  X1XX    11  11    ',
             '       X  XXXX    XX  XX1   ',
             '    X11X  XXXXXX  XX  XXXX  ',
             'X1111XXX  XXXXXX  XX  XXXX  ']

TILE_SIZE = 64
WIDTH = 1200
vertical_tile_size = 11
HEIGHT =  vertical_tile_size * TILE_SIZE

level_0 = {"terrain": "levels/0/level_0_terrain.csv",
           "bg_palms": "levels/0/level_0_bg_palms.csv",
           "coins": "levels/0/level_0_coins.csv",
           "crates": "levels/0/level_0_crates.csv",
           "enemies": "levels/0/level_0_enemies.csv",
           "grass": "levels/0/level_0_grass.csv",
           "player": "levels/0/level_0_player.csv",
           "constraints": "levels/0/level_0_constraints.csv",
           "fg_palms": "levels/0/level_0_fg_palms.csv",
           "node_pos": (110, 400),
           "unlock" : 1,
           "node_graphics": "graphics/overworld/0"}

level_1 = {"terrain": "levels/1/level_1_terrain.csv",
           "bg_palms": "levels/1/level_1_bg_palms.csv",
           "coins": "levels/1/level_1_coins.csv",
           "crates": "levels/1/level_1_crates.csv",
           "enemies": "levels/1/level_1_enemies.csv",
           "grass": "levels/1/level_1_grass.csv",
           "player": "levels/1/level_1_player.csv",
           "constraints": "levels/1/level_1_constraints.csv",
           "fg_palms": "levels/1/level_1_fg_palms.csv",
           "node_pos": (300, 220),
           "unlock" : 2,
           "node_graphics": "graphics/overworld/1"}

level_2 = {"terrain": "levels/2/level_2_terrain.csv",
           "bg_palms": "levels/2/level_2_bg_palms.csv",
           "coins": "levels/2/level_2_coins.csv",
           "crates": "levels/2/level_2_crates.csv",
           "enemies": "levels/2/level_2_enemies.csv",
           "grass": "levels/2/level_2_grass.csv",
           "player": "levels/2/level_2_player.csv",
           "constraints": "levels/2/level_2_constraints.csv",
           "fg_palms": "levels/2/level_2_fg_palms.csv",
           "node_pos": (400, 610),
           "unlock" : 3,
           "node_graphics": "graphics/overworld/2"}


level_3 = {"terrain": "levels/2/level_2_terrain.csv",
           "bg_palms": "levels/2/level_2_bg_palms.csv",
           "coins": "levels/2/level_2_coins.csv",
           "crates": "levels/2/level_2_crates.csv",
           "enemies": "levels/2/level_2_enemies.csv",
           "grass": "levels/2/level_2_grass.csv",
           "player": "levels/2/level_2_player.csv",
           "constraints": "levels/2/level_2_constraints.csv",
           "fg_palms": "levels/2/level_2_fg_palms.csv",
           "node_pos": (610, 350),
           "unlock" : 4,
           "node_graphics": "graphics/overworld/2"}

level_4 = {"terrain": "levels/2/level_2_terrain.csv",
           "bg_palms": "levels/2/level_2_bg_palms.csv",
           "coins": "levels/2/level_2_coins.csv",
           "crates": "levels/2/level_2_crates.csv",
           "enemies": "levels/2/level_2_enemies.csv",
           "grass": "levels/2/level_2_grass.csv",
           "player": "levels/2/level_2_player.csv",
           "constraints": "levels/2/level_2_constraints.csv",
           "fg_palms": "levels/2/level_2_fg_palms.csv",
           "node_pos": (610, 350),
           "unlock" : 4,
           "node_graphics": "graphics/overworld/2"}

level_5 =  {"terrain": "levels/2/level_2_terrain.csv",
           "bg_palms": "levels/2/level_2_bg_palms.csv",
           "coins": "levels/2/level_2_coins.csv",
           "crates": "levels/2/level_2_crates.csv",
           "enemies": "levels/2/level_2_enemies.csv",
           "grass": "levels/2/level_2_grass.csv",
           "player": "levels/2/level_2_player.csv",
           "constraints": "levels/2/level_2_constraints.csv",
           "fg_palms": "levels/2/level_2_fg_palms.csv",
           "node_pos": (1050, 400),
           "unlock" : 5,
           "node_graphics": "graphics/overworld/2"}

levels = {
    0:level_0,
    1:level_1,
    2:level_2,
    3:level_3,
    4:level_4,
    5:level_5}