def init(color, player, Level, Booster, Platform, Enemy, Grass, GameText): # Restart level
    player.collisions_rects = [] # Reset colision rects for player
    player.velocity = [0, 0] # Reset colision rects for player
    player.dead = False
    player.win = False
    
    return Level((120, 1000), (0, 800), [Grass((40, 0)), Platform((0, 760)), Enemy((0, 80)), Enemy((40, 80)), Enemy((80, 80)), GameText((-250, 1020), "You need lots of speed to kill enemys!", color.GOLDENROD1)]) # (sizex, sizey), (spawn pos), [Enemy(), Platform()]
