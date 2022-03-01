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

class player:
    VELOCITY_INCREASE = 0.4 # The amount the player velocity increases each time
    DEFAULT_VELOCITY_RESISTANCE = 0.989 # Air resistance default
    GRAVITY = 0.12 # Gravity pulling downwards

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
    def bound(cls):
        if cls.cord[1] < -220: # If player under ground
            cls.cord[1] = -220 # Make player on ground
            cls.velocity[1] = 0 # Make player stop moving downward
    
    @classmethod
    def display(cls):
        blit_image(sprite.player, cls.player_location) # Draws player on the screen


#--------------------Functions--------------------

def blit_image(image, pos, size=1): # Displays (and resizes) image on screen
    image_width = image.get_width() #Width
    image_height = image.get_height() #Height
    
    image = pygame.transform.scale(image, (round(image_width * size), round(image_height * size))) #Resize image to be relative to the screen, and change its size

    screen.blit(image, pos) #Draw resized image at position given

def render_ground(image, pos): # Calculates positiion of ground, and displays
    pos_x = -1 * round(pos[0], -3) # Get the pos of player, round to nearest 1000, and make negitive as needs to go in opposite direction from player
    
    pos_x_offset = 300 # Offset of displaying ground reletive to player
    
    for x in range(3): # Display three ground tiles under, and to the left and right of the player 
        blit_image(sprite.ground, (player.cord[0] + pos_x + pos_x_offset, player.cord[1] + 800), 10) # Draws ground on the screen relitive to player
        pos_x_offset += 1000 # Distance between the ground tiles

def render_sky():
    if not round(player.cord[1]) or not round(player.cord[1]/500):
        screen.fill((255, 255, 255))
    else:
        print(round(255 - abs(255 / round(player.cord[1]/500))))
        screen.fill((round(255 - abs(255 / round(player.cord[1]/500))), round(255 - abs(255 / round(player.cord[1]/500))), round(255 - abs(255 / round(player.cord[1]/500)))))
        ############################Fix the ground make 0

    
#--------------------Main--------------------

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
    player.bound()
    
    # Render Backround
    
    render_sky()

    # Render 
    blit_image(sprite.tree, player.cord) # Draws player on the screen

    player.display()
    
    render_ground(sprite.ground, (player.cord[0] + 800, player.cord[1] + 800))
    
    pygame.display.flip()

    clock.tick(DEFAULT_TICK) #Tick Speed

#--------------------Quit--------------------

pygame.quit()
