#--------------------Imports--------------------

import pygame
pygame.init()

#--------------------Variables--------------------

IMAGE_FOLDER = "images/" #The folder that holds all the image files
DISPLAY_SIZE = (1920, 1080)
DEFAULT_TICK = 120 #FPS

clock = pygame.time.Clock()

velocity = [0, 0] # Players current velocity
velocity_increase = 0.2 # The amount the velocity increases each time
velocity_resistance = 0.989 # Air resistance
velocity_gravity = 0.12 # Gravity

player_cord = [0, 0] # Players cordinate

player_location = [1920/2, 1080/2]

screen = pygame.display.set_mode(DISPLAY_SIZE, pygame.NOFRAME) # Create screen 

#--------------------Classes--------------------

class sprite:
    player = pygame.image.load(IMAGE_FOLDER+"player.png") #Loads player
    tree = pygame.image.load(IMAGE_FOLDER+"tree.png") #Loads tree
    ground = pygame.image.load(IMAGE_FOLDER+"ground.png") #Loads ground

#--------------------Functions--------------------

def blit_image(image, pos, size=1):
    image_width = image.get_width() #Width
    image_height = image.get_height() #Height
    
    image = pygame.transform.scale(image, (round(image_width * size), round(image_height * size))) #Resize image to be relative to the screen, and change its size

    screen.blit(image, pos) #Draw resized image at position given

def render_ground(image, pos):
    for i in 1000:
        if pos[0] - i == miltiple(100)
            
    
        
#--------------------Main--------------------

running = True
while running:
    
    # Get Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN: # Checks for key pressed key
            if event.key == pygame.K_ESCAPE: # Checks if escape is pressed
                running = False

    # Get inputs

    keys_pressed = pygame.key.get_pressed() #Gets all pressed keys
    
    if keys_pressed[pygame.K_w]:
        velocity[1] += velocity_increase # Increase velocity
    if keys_pressed[pygame.K_a]:
        velocity[0] += velocity_increase # Increase velocity
    if keys_pressed[pygame.K_s]:
        velocity[1] -= velocity_increase # Increase velocity
    if keys_pressed[pygame.K_d]:
        velocity[0] -= velocity_increase # Increase velocity

    velocity[1] -= velocity_gravity
    
    velocity = [v * velocity_resistance for v in velocity] # Adds air resistance

    player_cord = [x + y for x, y in zip(player_cord, velocity)] # Makes player move
    
    if player_cord[1] < -220:
        player_cord[1] = -220
        velocity[1] = 0
    
    # Render Backround
    
    screen.fill((160, 255, 150))

    # Render 
    blit_image(sprite.player, player_location) # Draws player on the screen
    blit_image(sprite.tree, player_cord) # Draws player on the screen
    blit_image(sprite.ground, (player_cord[0] + 800, player_cord[1] + 800), 10) # Draws player on the screen

    pygame.display.flip()

    clock.tick(DEFAULT_TICK) #Tick Speed

#--------------------Quit--------------------

pygame.quit()
