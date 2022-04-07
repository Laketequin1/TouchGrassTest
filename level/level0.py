def init(player, Level, Booster, Platform, Enemy, Grass): # Restart level
    player.collisions_rects = [] # Reset colision rects for player
    player.velocity = [0, 0] # Reset colision rects for player
    player.dead = False
    player.win = False
    
    return Level((800, 200), (0, 0), [Grass((760, 0)), Platform(160, 0), Platform(160, 40), Platform(160, 80), Platform(240, 160), Platform(240, 120), Platform(240, 80), Platform(320, 0), Platform(320, 40), Platform(320, 80)]) # (sizex, sizey), (spawn pos), [Enemy(), Platform()]
