def init(color, level, menu, player, Level, Booster, Platform, Enemy, Grass, GameText, Heart): # Restart level
    player.collisions_rects = [] # Reset colision rects for player
    player.velocity = [0, 0] # Reset colision rects for player
    player.dead = False
    player.win = False
    
    game_map = [Booster((0, 760), "slow"),
                Booster((0, 720), "slow"),
                Booster((0, 680), "slow"),
                Booster((0, 640), "slow"),
                Booster((0, 600), "slow"),
                Booster((0, 560), "slow"),
                Booster((0, 520), "slow"),
                Booster((0, 480), "slow"),
                Booster((0, 440), "slow"),
                Booster((0, 400), "slow"),
                Booster((0, 360), "slow"),
                Booster((0, 320), "slow"),
                Booster((0, 280), "slow"),
                Booster((0, 240), "slow"),
                Booster((0, 200), "slow"),
                Booster((0, 160), "slow"),
                Booster((0, 120), "slow"),
                Booster((0, 80), "slow"),
                Booster((0, 40), "slow"),
                Grass((0, 0)),
        
                # Text
                GameText((0, 840), "Thanks for playing!", color.GOLDENROD1),
                
                GameText((60, 650), "Credit to...", color.GOLDENROD1),
                GameText((60, 600), "Tequin Lake", color.GOLDENROD1),
                GameText((60, 550), "Malachi Malachi", color.GOLDENROD1),
                
                GameText((60, 400), "Special thanks to...", color.GOLDENROD1),
                GameText((60, 350), "Lloyd", color.GOLDENROD1),
                GameText((60, 300), "Mrs Greeff", color.GOLDENROD1),
                
                # Heart
                Heart((60, 150))
            ]
    
    return Level((40, 800), (0, 760), game_map) # (sizex, sizey), (spawn pos), [Enemy(), Platform()]
