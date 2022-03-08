#--------------------Imports--------------------

import pygame, threading
pygame.init()

from src import color # Imports lots of colors as RGB

#--------------------Variables--------------------

IMAGE_FOLDER = "images/" #The folder that holds all the image files
DISPLAY_SIZE = (1920, 1080) # Screen size
DEFAULT_TICK = 120 # Game tick speed

DEFAULT_FPS = 160 # Game rendering FPS

clock = pygame.time.Clock() # Game tick handling

surface = pygame.display.set_mode(DISPLAY_SIZE, pygame.NOFRAME) # Create screen 

class sprite:
    player = pygame.image.load(IMAGE_FOLDER+"player.png").convert() #Loads player (convert to be more efficient as non transparent)
    tree = pygame.image.load(IMAGE_FOLDER+"tree.png") #Loads tree image
    ground = pygame.image.load(IMAGE_FOLDER+"ground.png").convert() #Loads ground (convert to be more efficient as non transparent)
    roof = pygame.image.load(IMAGE_FOLDER+"roof.png").convert() #Loads ground (convert to be more efficient as non transparent)

#--------------------Functions--------------------

def blit_image(image, pos, size=1): # Displays (and resizes) image on screen
    image_width = image.get_width() #Width
    image_height = image.get_height() #Height
    
    image = pygame.transform.scale(image, (round(image_width * size), round(image_height * size))) #Resize image to be relative to the screen, and change its size
    
    surface.blit(image, pos) #Draw resized image at position given

def render_ground(self): # Calculates positiion of ground, and displays
    pass

def render_roof(self): # Calculates positiion of roof, and displays
    pass

#--------------------Classes--------------------

class player:
    SCREEN_CENTRE = (1920/2, 1080/2) # Player location centred on screen
    SIZE = sprite.player.get_size() # Size of player
    PLAYER_CENTRE = (SCREEN_CENTRE[0] - SIZE[0] / 2, SCREEN_CENTRE[1] - SIZE[1] / 2)
    
    VELOCITY_INCREASE = 0.4 # The amount the player velocity increases each time
    DEFAULT_VELOCITY_RESISTANCE = 0.989 # Air resistance default
    GRAVITY = 0.15 # Gravity pulling downwards

    velocity_resistance = DEFAULT_VELOCITY_RESISTANCE # Current air resistance
    velocity = [0, 0] # Players current velocity
    pos = [0, 0] # Players cordinate
    
    @classmethod
    def get_rect(cls): # Return the left of player, top of player, right of player, bottom of player
        return (cls.pos[0] - cls.SIZE[0], cls.pos[1] - cls.SIZE[1], cls.pos[0] + cls.SIZE[0], cls.pos[1] + cls.SIZE[1])
    
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
        cls.pos = [x + y for x, y in zip(cls.pos, cls.velocity)] # Makes player move
    
    @classmethod
    def bind(cls, map_rect): # Binds player to map
        if cls.pos[1] < map_rect[1]: # If player under ground
            cls.pos[1] = map_rect[1] # Make player on ground
            cls.velocity[1] = 0 # Make player stop moving downward
        elif cls.pos[1] > map_rect[3]: # If player hitting roof
            cls.pos[1] = map_rect[3] # Player under roof
            cls.velocity[1] = 0 # Make player stop moving upward
        
        if cls.pos[0] < map_rect[0]: # If player hitting left wall
            cls.pos[0] = map_rect[0] # Make player be on left wall
            cls.velocity[0] = 0 # Make player stop moving left
        elif cls.pos[0] > map_rect[2]: # If player hitting right wall
            cls.pos[0] = map_rect[2] # Player right wall
            cls.velocity[0] = 0 # Make player stop moving right
    
    @classmethod
    def display(cls):
        blit_image(sprite.player, cls.PLAYER_CENTRE) # Draws player on the screen
    
    
class Level:
    def __init__(self, map_size, spawn_pos, *objects): # Get all parts of the level
        self.map_size = map_size
        self.map_rect = (0, 0, *map_size) # Rect of map from 0, 0 to map_size
        self.spawn_pos = spawn_pos
        self.objects = objects
    
    def bind_player(self):
        player.bind(self.map_rect)
    
    def display(self):
        pass
    
#--------------------Main--------------------

current_level = Level((50, 50), (5, 5), ())

def main():
    running = True
    while running:
        # Get Events
        p = pygame.event.get()
        if p:
            print(p)
        for event in pygame.event.get():
            #print(event.type)
            #print(pygame.KEYDOWN)
            if event.type == pygame.QUIT: # If exit button pressed
                running = False # Exit loop
            elif event.type == pygame.KEYDOWN: # Checks for key pressed key
                print("Keydown\ns")
                if event.key == pygame.K_ESCAPE: # Checks if escape is pressed
                    running = False # Exit loop
        
        player.get_player_input()
        player.gravity()
        player.air_resistance()
        player.move()
        current_level.bind_player()
        
    print("main finished")

def render():
    
    while thread.is_alive():
        surface.fill((230, 255, 120))
        pygame.display.flip()
        clock.tick(DEFAULT_FPS) #FPS Speed
            

print("go")
thread = threading.Thread(target=main)
thread.start()

render()
https://stackoverflow.com/questions/56717184/pygame-event-get-not-returning-any-events-when-inside-a-thread