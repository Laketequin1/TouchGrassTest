def init(color, level, menu, player, Level, Booster, Platform, Enemy, Grass, GameText, Heart): # Restart level
    player.collisions_rects = [] # Reset colision rects for player
    player.velocity = [0, 0] # Reset colision rects for player
    player.dead = False
    player.win = False
    
    game_map = [Platform((0, 800)),
                Enemy((0, 80)), Enemy((40, 80)), Enemy((80, 80)),
                Grass((40, 0)),
                
                # Text
                GameText((-250, 1020), "You need lots of speed to kill enemys!", color.GOLDENROD1)
            ]
    
    return Level((120, 1000), (0, 800), game_map) # (sizex, sizey), (spawn pos), [Enemy(), Platform()]
