def init(color, level, menu, player, Level, Booster, Platform, Enemy, Grass, GameText, Heart): # Restart level
    player.collisions_rects = [] # Reset colision rects for player
    player.velocity = [0, 0] # Reset colision rects for player
    player.dead = False
    player.win = False
    
    game_map = [Platform((80, 960)), Platform((120, 960)), Platform((160, 960)), Platform((200, 960)), Platform((240, 960)), Platform((280, 960)), Platform((320, 960)), Platform((360, 960)), Platform((400, 960)), Platform((440, 960)), Platform((480, 960)), Platform((520, 960)), Platform((560, 960)), Platform((600, 960)), Platform((640, 960)), Platform((680, 960)), Platform((720, 960)), Platform((760, 960)),
                Platform((0, 920)),
                Platform((0, 880)), Booster((40, 880), "right"),
                Platform((0, 840)), Platform((40, 840)), Platform((80, 840)), Platform((120, 840)), Platform((160, 840)), Platform((200, 840)), Platform((240, 840)), Platform((280, 840)), Platform((320, 840)), Platform((360, 840)), Platform((400, 840)), Platform((440, 840)), Platform((480, 840)), Platform((520, 840)), Platform((560, 840)), Platform((600, 840)), Platform((640, 840)), Platform((680, 840)), Platform((720, 840)),
                Platform((0, 800)), Platform((40, 800)), Platform((80, 800)), Platform((120, 800)), Platform((160, 800)), Platform((200, 800)), Platform((240, 800)), Platform((280, 800)), Platform((320, 800)), Platform((360, 800)), Platform((400, 800)), Platform((440, 800)), Platform((480, 800)), Platform((720, 800)),
                Platform((0, 760)), Platform((40, 760)), Platform((80, 760)), Platform((120, 760)), Platform((160, 760)), Platform((200, 760)), Platform((240, 760)), Platform((280, 760)), Platform((320, 760)), Platform((360, 760)), Platform((400, 760)), Platform((440, 760)), Platform((480, 760)), Platform((560, 760)), Platform((600, 760)), Platform((640, 760)), Platform((720, 760)),
                Platform((0, 720)), Platform((40, 720)), Platform((80, 720)), Platform((120, 720)), Platform((160, 720)), Platform((200, 720)), Platform((240, 720)), Platform((280, 720)), Platform((320, 720)), Platform((360, 720)), Platform((400, 720)), Platform((440, 720)), Platform((480, 720)), Platform((560, 720)), Platform((600, 720)), Platform((640, 720)), Platform((720, 720)),
                Platform((0, 680)), Platform((40, 680)), Platform((80, 680)), Platform((120, 680)), Platform((160, 680)), Platform((200, 680)), Platform((240, 680)), Platform((280, 680)), Platform((320, 680)), Platform((360, 680)), Platform((400, 680)), Platform((440, 680)), Platform((480, 680)), Platform((560, 680)), Platform((600, 680)), Platform((640, 680)), Platform((720, 680)),
                Platform((0, 640)), Platform((40, 640)), Platform((80, 640)), Platform((120, 640)), Platform((160, 640)), Platform((200, 640)), Platform((240, 640)), Platform((280, 640)), Platform((320, 640)), Platform((360, 640)), Platform((400, 640)), Platform((440, 640)), Platform((480, 640)), Platform((560, 640)), Platform((600, 640)), Platform((640, 640)), Platform((720, 640)),
                Platform((0, 600)), Platform((40, 600)), Platform((80, 600)), Platform((120, 600)), Platform((160, 600)), Platform((200, 600)), Platform((240, 600)), Platform((280, 600)), Platform((320, 600)), Platform((360, 600)), Platform((400, 600)), Platform((440, 600)), Platform((480, 600)), Platform((560, 600)), Platform((600, 600)), Platform((640, 600)), Platform((720, 600)),
                Platform((0, 560)), Platform((40, 560)), Platform((80, 560)), Platform((120, 560)), Platform((160, 560)), Platform((200, 560)), Platform((240, 560)), Platform((280, 560)), Platform((320, 560)), Platform((360, 560)), Platform((400, 560)), Platform((440, 560)), Platform((480, 560)), Platform((560, 560)), Platform((600, 560)), Platform((640, 560)), Platform((720, 560)),
                Platform((0, 520)), Platform((40, 520)), Platform((80, 520)), Platform((120, 520)), Platform((160, 520)), Platform((200, 520)), Platform((240, 520)), Platform((280, 520)), Platform((320, 520)), Platform((360, 520)), Platform((400, 520)), Platform((440, 520)), Platform((480, 520)), Platform((560, 520)), Platform((600, 520)), Platform((640, 520)), Platform((720, 520)),
                Booster((0, 480), "down"), Platform((560, 480)), Platform((600, 480)), Platform((640, 480)),
                Booster((440, 440), "left"), Booster((480, 440), "left"), Booster((560, 440), "slow"), Booster((600, 440), "slow"), Booster((640, 440), "slow"), Platform((720, 440)), Platform((760, 440)),
                Platform((80, 400)), Platform((120, 400)), Platform((160, 400)), Platform((200, 400)), Platform((240, 400)), Platform((280, 400)), Platform((320, 400)), Platform((360, 400)), Platform((400, 400)), Platform((440, 400)), Platform((480, 400)), Platform((520, 400)), Platform((560, 400)), Platform((600, 400)), Platform((640, 400)), Platform((680, 400)), Platform((720, 400)), Platform((760, 400)),
                Platform((80, 360)), Platform((120, 360)), Platform((160, 360)), Platform((200, 360)), Platform((240, 360)), Platform((280, 360)), Platform((320, 360)), Platform((360, 360)), Platform((400, 360)), Platform((440, 360)), Platform((480, 360)), Platform((520, 360)), Platform((560, 360)), Platform((600, 360)), Platform((640, 360)), Platform((680, 360)), Platform((720, 360)), Platform((760, 360)),
                Platform((80, 320)), Platform((120, 320)), Platform((160, 320)), Platform((200, 320)), Platform((240, 320)), Platform((280, 320)), Platform((320, 320)), Platform((360, 320)), Platform((400, 320)), Platform((440, 320)), Platform((480, 320)), Platform((520, 320)), Platform((560, 320)), Platform((600, 320)), Platform((640, 320)), Platform((680, 320)), Platform((720, 320)), Platform((760, 320)),
                Platform((80, 280)), Platform((120, 280)), Platform((160, 280)), Platform((200, 280)), Platform((240, 280)), Platform((280, 280)), Platform((320, 280)), Platform((360, 280)), Platform((400, 280)), Platform((440, 280)), Platform((480, 280)), Platform((520, 280)), Platform((560, 280)), Platform((600, 280)), Platform((640, 280)), Platform((680, 280)), Platform((720, 280)), Platform((760, 280)),
                Platform((760, 240)),
                Booster((0, 200), "right"), Enemy((720, 200)),
                Platform((0, 160)), Platform((40, 160)), Platform((80, 160)), Platform((120, 160)), Platform((160, 160)), Platform((200, 160)), Platform((240, 160)), Platform((280, 160)), Platform((320, 160)), Platform((360, 160)), Platform((400, 160)), Platform((440, 160)), Platform((480, 160)), Platform((520, 160)), Platform((560, 160)), Platform((600, 160)), Platform((640, 160)), Platform((680, 160)), Platform((720, 160)), Booster((760, 160), "slow"),
                Platform((0, 120)), Platform((40, 120)), Platform((80, 120)), Platform((120, 120)), Platform((160, 120)), Platform((200, 120)), Platform((240, 120)), Platform((280, 120)), Platform((320, 120)), Platform((360, 120)), Platform((400, 120)), Platform((440, 120)), Platform((480, 120)), Platform((520, 120)), Platform((560, 120)), Platform((600, 120)), Platform((640, 120)), Platform((680, 120)), Platform((720, 120)), Booster((760, 120), "slow"),
                Platform((0, 80)), Platform((40, 80)), Platform((80, 80)), Platform((120, 80)), Platform((160, 80)), Platform((200, 80)), Platform((240, 80)), Platform((280, 80)), Platform((320, 80)), Platform((360, 80)), Platform((400, 80)), Platform((440, 80)), Platform((480, 80)), Platform((520, 80)), Platform((560, 80)), Platform((600, 80)), Platform((640, 80)), Platform((680, 80)),
                Grass((0, 40)), Enemy((80, 40)), Enemy((120, 40)), Enemy((160, 40)), Enemy((200, 40)), Enemy((240, 40)), Enemy((280, 40)), Enemy((320, 40)), Enemy((360, 40)), Booster((520, 40), "left"), Booster((560, 40), "left"), Booster((600, 40), "left"), Booster((640, 40), "left"), Booster((680, 40), "left"), Booster((720, 40), "left"), Booster((760, 40), "left"),
                Platform((0, 0)), Platform((40, 0)), Platform((80, 0)), Platform((120, 0)), Platform((160, 0)), Platform((200, 0)), Platform((240, 0)), Platform((280, 0)), Platform((320, 
                0)), Platform((360, 0)), Platform((400, 0)), Platform((440, 0)), Platform((480, 0)), Platform((520, 0)), Platform((560, 0)), Platform((600, 0)), Platform((640, 0)), Platform((680, 0)), Platform((720, 0)), Platform((760, 0)),

                # Override
                Booster((520, 440), "left"),
                
                Booster((720, 80), "down"),
                Booster((760, 80), "down"),
                
                # Special
                Enemy((80, 480), False, 'y', 40),
                
                # Text
                GameText((0, 1020), "Boosters give you a boost!", color.GOLDENROD1),
                
                GameText((20, 720), "The faster you move,", color.GOLDENROD1),
                GameText((25, 670), "the larger the boost!", color.GOLDENROD1),
                
                GameText((200, 360), "Diamond shaped boosters", color.GOLDENROD1),
                GameText((260, 310), "make you slower!", color.GOLDENROD1),
                
                GameText((20, 120), "Chain boosters for speed!", color.GOLDENROD1),
            ]
    
    return Level((800, 1000), (0, 960), game_map) # (sizex, sizey), (spawn pos), [Enemy(), Platform()]
