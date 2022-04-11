def init(color, level, menu, player, Level, Booster, Platform, Enemy, Grass, GameText, Heart): # Restart level
    player.collisions_rects = [] # Reset colision rects for player
    player.velocity = [0, 0] # Reset colision rects for player
    player.dead = False
    player.win = False
    
    game_map = [Enemy((0, 360), True), Enemy((40, 360), True), Enemy((80, 360), True), Enemy((120, 360), True), Enemy((160, 360), True), Enemy((200, 360), True), Enemy((240, 360), True), 
                Enemy((280, 360), True), Enemy((320, 360), True), Enemy((360, 360), True), Enemy((400, 360), True), Enemy((440, 360), True), Enemy((480, 360), True), Enemy((520, 360), True), Enemy((560, 360), True), Enemy((600, 360), True), Enemy((640, 360), True), Enemy((680, 360), True), Enemy((720, 360), True), Enemy((760, 360), True), Enemy((800, 360), True), Enemy((840, 360), True), Enemy((880, 360), True), Enemy((920, 360), True), Enemy((960, 360), True), Enemy((1000, 360), True), Enemy((1040, 360), True), Enemy((1080, 360), True), Enemy((1120, 360), True), Enemy((1160, 360), True), Enemy((1200, 360), True), Enemy((1240, 360), True), Enemy((1280, 360), True), Enemy((1320, 360), True), 
                Enemy((1360, 360), True), Enemy((1400, 360), True), Platform((1440, 360)), Platform((1480, 360)), Platform((1520, 360)), Platform((1560, 360)), Platform((1600, 360)), Platform((1640, 360)), Platform((1680, 360)), Platform((1720, 360)), Platform((1760, 360)), Platform((1800, 360)), Platform((1840, 360)), Platform((1880, 360)),
                Enemy((1400, 320), True), Platform((1440, 320)), Platform((1480, 320)), Platform((1520, 320)), Platform((1560, 320)), Platform((1600, 320)), Platform((1640, 320)), Platform((1680, 320)), Platform((1720, 320)), Platform((1760, 320)), Platform((1800, 320)), Platform((1840, 320)), Platform((1880, 320)),
                Platform((1400, 280)), Platform((1440, 280)), Platform((1480, 280)), Platform((1520, 280)), Platform((1560, 280)), Platform((1600, 280)), Platform((1640, 280)), Platform((1680, 280)), Platform((1720, 280)), Platform((1760, 280)), Platform((1800, 280)), Platform((1840, 280)), Platform((1880, 280)),
                Platform((1400, 240)), Platform((1440, 240)), Platform((1480, 240)), Platform((1520, 240)), Platform((1560, 240)), Platform((1600, 240)), Platform((1640, 240)), Platform((1680, 240)), Platform((1720, 240)), Platform((1760, 240)), Platform((1800, 240)), Platform((1840, 240)), Platform((1880, 240)),
                Booster((1400, 200), "right"), Booster((1440, 200), "right"), Booster((1480, 200), "right"), Enemy((1760, 200)),
                Booster((1400, 160), "right"), Booster((1440, 160), "right"), Booster((1480, 160), "right"), Enemy((1760, 160)),
                Platform((1400, 120)), Platform((1440, 120)), Platform((1480, 120)), Platform((1520, 120)), Platform((1560, 120)), Platform((1600, 120)), Platform((1640, 120)), Platform((1680, 120)), Platform((1720, 120)), Platform((1760, 120)),
                Platform((1400, 80)), Platform((1440, 80)), Platform((1480, 80)), Platform((1520, 80)), Platform((1560, 80)), Platform((1600, 80)), Platform((1640, 80)), Platform((1680, 80)), Platform((1720, 80)), Platform((1760, 80)),
                Enemy((1400, 40), True), Platform((1440, 40)), Platform((1480, 40)), Platform((1520, 40)), Platform((1560, 40)), Platform((1600, 40)), Platform((1640, 40)), Platform((1680, 40)), Platform((1720, 40)), Platform((1760, 40)),
                Platform((0, 0)), Platform((40, 0)), Platform((80, 0)), Enemy((120, 0), True), Enemy((160, 0), True), Enemy((200, 0), True), Enemy((240, 0), True), Enemy((280, 0), True), 
                Enemy((320, 0), True), Enemy((360, 0), True), Enemy((400, 0), True), Enemy((440, 0), True), Enemy((480, 0), True), Enemy((520, 0), True), Enemy((560, 0), True), Enemy((600, 0), True), Enemy((640, 0), True), Enemy((680, 0), True), Enemy((720, 0), True), Enemy((760, 0), True), Enemy((800, 0), True), Enemy((840, 0), True), Enemy((880, 0), True), Enemy((920, 0), True), Enemy((960, 0), True), Enemy((1000, 0), True), Enemy((1040, 0), True), Enemy((1080, 0), True), Enemy((1120, 0), True), Enemy((1160, 0), True), Enemy((1200, 0), True), Enemy((1240, 0), True), Enemy((1280, 0), True), Enemy((1320, 0), True), Enemy((1360, 0), True), Enemy((1400, 0), True), Platform((1440, 0)), Platform((1480, 0)), Platform((1520, 0)), Platform((1560, 0)), Platform((1600, 0)), Platform((1640, 0)), Platform((1680, 0)), Platform((1720, 0)), Platform((1760, 0)), Grass((1800, 0)), Grass((1840, 0)), Grass((1880, 0)),
                
                # Special
                Enemy((240, 320), True, 'y', 280, 5, 50),
                Enemy((540, 320), True, 'y', 280, 5),
                Enemy((840, 320), True, 'y', 280, 5, 50),
                Enemy((1140, 320), True, 'y', 280, 5)
            ]
    
    return Level((1920, 400), (0, 40), game_map) # (sizex, sizey), (spawn pos), [Enemy(), Platform()]
