def init(player, Level, Booster, Platform, Enemy, Grass): # Restart level
    player.collisions_rects = [] # Reset colision rects for player
    player.velocity = [0, 0] # Reset colision rects for player
    player.dead = False
    player.win = False
    
    return Level((120, 840), (0, 740), [Grass((40, 0)), Platform(0, 720), Enemy(0, 80), Enemy(40, 80), Enemy(80, 80)]) # (sizex, sizey), (spawn pos), [Enemy(), Platform()]
