def init(player, Level, Booster, Platform, Enemy, Grass): # Restart level
    player.collisions_rects = [] # Reset colision rects for player
    player.velocity = [0, 0] # Reset colision rects for player
    player.dead = False
    player.win = False
    
    return Level((800, 1000), (0, 960), [Grass((0, 0)), Platform((0, 920)), Platform((40, 920)), Platform((40, 880)), Platform((40, 840)), Platform((120, 960)), Platform((120, 920)), Platform((120, 800)), Platform((80, 800)), Booster((80, 840), 'right')]) # (sizex, sizey), (spawn pos), [Enemy(), Platform()]
