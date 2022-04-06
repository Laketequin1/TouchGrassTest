def init(player, Level, Booster, Platform, Enemy, Grass): # Restart level
    player.collisions_rects = [] # Reset colision rects for player
    player.velocity = [0, 0] # Reset colision rects for player
    player.dead = False
    player.win = False
    
    return Level((800, 1000), (0, 9600), []) # (sizex, sizey), (spawn pos), [Enemy(), Platform()]
