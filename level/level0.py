def init(player, Level, Booster, Platform, Enemy, Grass):
    player.collisions_rects = [] # Reset colision rects for player
    player.velocity = [0, 0] # Reset colision rects for player
    
    return Level((1500, 1500), (0, 0), [Booster((600, 900), 'up'), Booster((500, 700), 'left'), Booster((600, 1200), 'down'), Platform(600, 560), Enemy(0, 80), Enemy(500, 0), Enemy(500, 200), Enemy(100, 500), Enemy(150, 500), Enemy(150, 200), Enemy(550, 0), Enemy(600, 0), Enemy(550, 200), Enemy(600, 200), Enemy(200, 200), Enemy(250, 200), Enemy(300, 200), Enemy(350, 200), Enemy(400, 200), Enemy(200, 200), Enemy(700, 700), Platform(500, 500), Platform(540, 500), Platform(580, 500), Platform(620, 500), Platform(660, 500), Platform(700, 540), Platform(700, 500), Platform(100, 0), Grass((520, 540))]) # (sizex, sizey), (spawn pos), [Enemy(), Platform()]
