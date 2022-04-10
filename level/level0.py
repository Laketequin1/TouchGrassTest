def init(color, level, menu, player, Level, Booster, Platform, Enemy, Grass, GameText, Heart): # Restart level
    player.collisions_rects = [] # Reset colision rects for player
    player.velocity = [0, 0] # Reset colision rects for player
    player.dead = False
    player.win = False
    
    game_map = [Platform((240, 160)),
                Platform((240, 120)),
                Platform((160, 80)), Platform((240, 80)), Platform((320, 80)),
                Platform((160, 40)), Platform((320, 40)),
                Platform((160, 0)), Platform((320, 0)), Grass((760, 0)),
                
                # Text
                GameText((0, 220), "Move with WASD or arrow keys!", color.GOLDENROD1),
                GameText((420, -55), "Touch grass to win!", color.GOLDENROD1)
            ]
    
    return Level((800, 200), (0, 0), game_map) # (sizex, sizey), (spawn pos), [Enemy(), Platform()]
