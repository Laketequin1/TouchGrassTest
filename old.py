#--------------------Imports--------------------

import pygame
pygame.init()

#--------------------Variables--------------------

IMAGE_FOLDER = "images/" #The folder that holds all the image files
DISPLAY_SIZE = (1920, 1080) # Screen size
DEFAULT_TICK = 120 #FPS

clock = pygame.time.Clock()

screen = pygame.display.set_mode(DISPLAY_SIZE, pygame.NOFRAME) # Create screen 

#--------------------Classes--------------------

class sprite:
    player = pygame.image.load(IMAGE_FOLDER+"player.png").convert() #Loads player (convert to be more efficient as non transparent)
    tree = pygame.image.load(IMAGE_FOLDER+"tree.png") #Loads tree image
    ground = pygame.image.load(IMAGE_FOLDER+"ground.png").convert() #Loads ground (convert to be more efficient as non transparent)
    roof = pygame.image.load(IMAGE_FOLDER+"roof.png").convert() #Loads ground (convert to be more efficient as non transparent)

class player:
    VELOCITY_INCREASE = 0.4 # The amount the player velocity increases each time
    DEFAULT_VELOCITY_RESISTANCE = 0.989 # Air resistance default
    GRAVITY = 0.15 # Gravity pulling downwards

    velocity_resistance = DEFAULT_VELOCITY_RESISTANCE # Current air resistance
    velocity = [0, 0] # Players current velocity
    cord = [0, 0] # Players cordinate
    player_location = [1920/2, 1080/2] # Player location centred on screen
    
    @classmethod
    def gravity(cls): # Player velocity moves down
        cls.velocity[1] -= cls.GRAVITY

    @classmethod
    def air_resistance(cls):
       cls.velocity = [v * cls.velocity_resistance for v in cls.velocity] # Adds air resistance

    @classmethod
    def get_player_input(cls):
        keys_pressed = pygame.key.get_pressed() #Gets all pressed keys
        
        if keys_pressed[pygame.K_w]:
            cls.velocity[1] += cls.VELOCITY_INCREASE # Increase velocity
        if keys_pressed[pygame.K_a]:
            cls.velocity[0] += cls.VELOCITY_INCREASE # Increase velocity
        if keys_pressed[pygame.K_s]:
            cls.velocity[1] -= cls.VELOCITY_INCREASE # Increase velocity
        if keys_pressed[pygame.K_d]:
            cls.velocity[0] -= cls.VELOCITY_INCREASE # Increase velocity
    
    @classmethod
    def move(cls):
        cls.cord = [x + y for x, y in zip(cls.cord, cls.velocity)] # Makes player move
        
    @classmethod
    def bound(cls, map_rect):
        if cls.cord[1] < map_rect[1]: # If player under ground
            cls.cord[1] = map_rect[1] # Make player on ground
            cls.velocity[1] = 0 # Make player stop moving downward
        elif cls.cord[1] > map_rect[3]: # If player hitting roof
            cls.cord[1] = map_rect[3] # Player under roof
            cls.velocity[1] = 0 # Make player stop moving upward
        
        if cls.cord[0] < map_rect[0]: # If player hitting left wall
            cls.cord[0] = map_rect[0] # Make player be on left wall
            cls.velocity[0] = 0 # Make player stop moving left
        elif cls.cord[0] > map_rect[2]: # If player hitting right wall
            cls.cord[0] = map_rect[2] # Player right wall
            cls.velocity[0] = 0 # Make player stop moving right
    
    @classmethod
    def display(cls):
        blit_image(sprite.player, cls.player_location) # Draws player on the screen


class Level:
    
    def __init__(self, map_rect, spawn_pos, *objects):
        self.map_rect = map_rect
        self.spawn_pos = spawn_pos
        self.objects = objects
    
    def render_ground(self): # Calculates positiion of ground, and displays
        
        pos_x = -1 * round(player.cord[0] + 800, -3) # Get the pos of player, round to nearest 1000, and make negitive as needs to go in opposite dimap_rection from player
        
        pos_x_offset = 300 # Offset of displaying ground reletive to player
        
        for x in range(3): # Display three ground tiles under, and to the left and right of the player 
            blit_image(sprite.ground, (player.cord[0] + pos_x + pos_x_offset, player.cord[1] + 580), 10) # Draws ground on the screen relitive to player
            pos_x_offset += 1000 # Distance between the ground tiles
    
    def render_roof(self):
        
        pos_x = -1 * round(player.cord[0] + 800, -3) # Get the pos of player, round to nearest 1000, and make negitive as needs to go in opposite dimap_rection from player
        
        pos_x_offset = 300 # Offset of displaying ground reletive to player
        
        for x in range(3): # Display three ground tiles under, and to the left and right of the player 
            blit_image(sprite.roof, (player.cord[0] + pos_x + pos_x_offset, player.cord[1] - current_level.map_rect[3] - sprite.roof.get_height() - 180), 10) # Draws ground on the screen relitive to player
            pos_x_offset += 1000 # Distance between the ground tiles
    
    def bound_player(self):
        player.bound(self.map_rect)

#--------------------Functions--------------------

def blit_image(image, pos, size=1): # Displays (and resizes) image on screen
    image_width = image.get_width() #Width
    image_height = image.get_height() #Height
    
    image = pygame.transform.scale(image, (round(image_width * size), round(image_height * size))) #Resize image to be relative to the screen, and change its size
    
    screen.blit(image, pos) #Draw resized image at position given

def display_sky():
    if not round(player.cord[1]) or not round(player.cord[1]/1000):
        screen.fill((183, 226, 240))
    else:
        screen.fill((round(20 + abs(173 / round(player.cord[1]/1000))), round(25 + abs(216 / round(player.cord[1]/1000))), round(25 + abs(230 / round(player.cord[1]/1000)))))

def display_walls():
    
    pygame.draw.rect(screen, (50, 50, 50), (player.cord[0], 0, 20, 5000))

    
#--------------------Main--------------------

current_level = Level((-2000, 0, 1000, 1000), (50, 50), [])

running = True
while running:
    
    # Get Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # If exit button pressed
            running = False # Exit loop
        elif event.type == pygame.KEYDOWN: # Checks for key pressed key
            if event.key == pygame.K_ESCAPE: # Checks if escape is pressed
                running = False # Exit loop

    # Get inputs

    player.get_player_input()
    player.gravity()
    player.air_resistance()
    player.move()
    current_level.bound_player()
    
    # Render Backround
    
    display_sky()

    # Render 
    blit_image(sprite.tree, (player.cord[0], player.cord[1] + 540)) # Draws player on the screen

    player.display()

    display_walls()    
    current_level.render_ground()
    current_level.render_roof()
    
    pygame.display.flip()

    clock.tick(DEFAULT_TICK) #Tick Speed

#--------------------Quit--------------------

pygame.quit()
