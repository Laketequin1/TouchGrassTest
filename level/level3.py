def init(color, level, menu, player, Level, Booster, Platform, Enemy, Grass, GameText, Heart): # Restart level
    player.collisions_rects = [] # Reset colision rects for player
    player.velocity = [0, 0] # Reset colision rects for player
    player.dead = False
    player.win = False
    
    game_map = [Enemy((0, 200), True), Enemy((40, 200), True), Enemy((80, 200), True), Enemy((120, 200), True), Enemy((160, 200), True), Enemy((200, 200), True), Enemy((240, 200), True), 
                Enemy((280, 200), True), Enemy((320, 200), True), Enemy((360, 200), True), Enemy((400, 200), True), Enemy((440, 200), True), Enemy((480, 200), True), Enemy((520, 200), True), Enemy((560, 200), True), Enemy((600, 200), True), Enemy((640, 200), True), Enemy((680, 200), True), Enemy((720, 200), True), Enemy((760, 200), True), Enemy((800, 200), True), Enemy((840, 200), True), Enemy((880, 200), True), Enemy((920, 200), True), Enemy((960, 200), True), Enemy((1000, 200), True), Enemy((1040, 200), True), Enemy((1080, 200), True), Enemy((1120, 200), True), Enemy((1160, 200), True), Enemy((1200, 200), True), Enemy((1240, 200), True), Enemy((1280, 200), True), Enemy((1320, 200), True), 
                Enemy((1360, 200), True), Enemy((1400, 200), True), Enemy((1440, 200), True), Enemy((1480, 200), True), Enemy((1520, 200), True), Enemy((1560, 200), True), Enemy((1600, 200), True), Enemy((1640, 200), True), Enemy((1680, 200), True), Enemy((1720, 200), True), Enemy((1760, 200), True), Enemy((1800, 200), True), Enemy((1840, 200), True), Enemy((1880, 200), True), Enemy((1920, 200), True), Enemy((1960, 200), True),
                Enemy((960, 160), True),
                Enemy((480, 40), True), Enemy((1440, 40), True), Grass((1960, 40)),
                Platform((0, 0)), Platform((40, 0)), Platform((80, 0)), Enemy((120, 0), True), Enemy((160, 0), True), Enemy((200, 0), True), Enemy((240, 0), True), Enemy((280, 0), True), 
                Enemy((320, 0), True), Enemy((360, 0), True), Enemy((400, 0), True), Enemy((440, 0), True), Enemy((480, 0), True), Enemy((520, 0), True), Enemy((560, 0), True), Enemy((600, 0), True), Enemy((640, 0), True), Enemy((680, 0), True), Enemy((720, 0), True), Enemy((760, 0), True), Enemy((800, 0), True), Enemy((840, 0), True), Enemy((880, 0), True), Enemy((920, 0), True), Enemy((960, 0), True), Enemy((1000, 0), True), Enemy((1040, 0), True), Enemy((1080, 0), True), Enemy((1120, 0), True), Enemy((1160, 0), True), Enemy((1200, 0), True), Enemy((1240, 0), True), Enemy((1280, 0), True), Enemy((1320, 0), True), Enemy((1360, 0), True), Enemy((1400, 0), True), Enemy((1440, 0), True), Enemy((1480, 0), True), Enemy((1520, 0), True), Enemy((1560, 0), True), Enemy((1600, 0), True), Enemy((1640, 0), True), Enemy((1680, 0), True), Enemy((1720, 0), True), Enemy((1760, 0), True), Enemy((1800, 0), True), Enemy((1840, 0), True), Enemy((1880, 0), True), Platform((1920, 0)), Platform((1960, 0)),
                
                # Text
                GameText((0, -80), "Special enemys can't be killed!", color.GOLDENROD1),
            ]
    
    return Level((2000, 240), (0, 40), game_map) # (sizex, sizey), (spawn pos), [Enemy(), Platform()]
