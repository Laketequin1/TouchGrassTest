#--------------------Imports--------------------

import pygame, threading
pygame.init()

from src import color # Imports lots of colors as RGB

#--------------------Variables--------------------

ORIGINAL_THREAD_COUNT = threading.activeCount()

IMAGE_FOLDER = "images/" #The folder that holds all the image files
DISPLAY_SIZE = (1920, 1080) # Screen size
DEFAULT_TICK = 120 # Game tick speed

DEFAULT_FPS = 160 # Game rendering FPS

RENDER_Y_OFFSET = 800 # The ground pos relitive to top screen when player on y 0
RENDER_X_OFFSET = None # The left pos relitive to player on screen when player on x

clock = pygame.time.Clock() # Game tick handling

surface = pygame.display.set_mode(DISPLAY_SIZE, pygame.NOFRAME) # Create screen 

finished = False

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

def render_ground(): # Calculates positiion of ground, and displays    
    _, player_y = player.get_pos()
    
    pygame.draw.rect(surface, color.BURLYWOOD, pygame.Rect(0, RENDER_Y_OFFSET + player_y, DISPLAY_SIZE[0], DISPLAY_SIZE[1]))
    

def render_roof(): # Calculates positiion of roof, and displays
    pass

#--------------------Classes--------------------
'''
class Trail:
    def __init__(self, pos):
        self.pos = pos
        self.trails = []
        for i in range(50)
            self.trails.append(player)
'''
# Raise custom error
class TwoInputsOfSameAxis(Exception):
    def __init__(self, value1, value2, x_or_y):
        super().__init__("The sides {} and {} are both being set on the {} axis".format(value1, value2, x_or_y))

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
    def get_pos(cls): # Return centre of player with relitivity to screen
        return (cls.pos[0] + cls.PLAYER_CENTRE[0], cls.pos[1] + cls.PLAYER_CENTRE[1])
    
    @classmethod
    def get_rel_pos(cls): # Return centre of player with relitivity to screen
        return (cls.pos[0] + cls.PLAYER_CENTRE[0] + RENDER_X_OFFSET, cls.pos[1] + cls.PLAYER_CENTRE[1] + RENDER_Y_OFFSET)
    
    @classmethod
    def set_pos(cls, pos=(None, None), **kwargs):
        
        # Set player's position at its centre to pos.
        # Has ability to input left, right, top, bottom of player to a pos, which overides pos
        
        if kwargs:
            
            if 'left' in kwargs and 'right' in kwargs:
                raise TwoInputsOfSameAxis('left', 'right', 'x')
            elif 'left' in kwargs:
                cls.pos[0] = kwargs['left'] + cls.SIZE[0] / 2
            elif 'right' in kwargs:
                cls.pos[0] = kwargs['right'] - cls.SIZE[0] / 2
            elif pos[0]:
                cls.pos[0] = pos[0] - cls.PLAYER_CENTRE[0]
                
            if 'top' in kwargs and 'bottom' in kwargs:
                raise TwoInputsOfSameAxis('top', 'bottom', 'y')
            elif 'top' in kwargs:
                cls.pos[1] = kwargs['top'] + cls.SIZE[1] / 2
            elif 'bottom' in kwargs:
                cls.pos[1] = kwargs['bottom'] - cls.SIZE[1] / 2
            elif pos[1]:
                cls.pos[1] = pos[1] - cls.PLAYER_CENTRE[1]
    
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
        
        player_left, player_top, player_right, player_bottom = player.get_rect()
        
        if player_left < map_rect[0]:
            player.set_pos(left=map_rect[0])
        elif player_right < map_rect[2]:
            player.set_pos(right=map_rect[2])
        
        if player_top < map_rect[1]:
            player.set_pos(top=map_rect[1])
        if player_bottom < map_rect[3]:
            player.set_pos(bottom=map_rect[3])

        
    @classmethod
    def display(cls):
        blit_image(sprite.player, cls.PLAYER_CENTRE) # Draws player on the screen
    
    
class Level:
    def __init__(self, map_size, spawn_pos, *objects): # Get all parts of the level
        self.map_size = map_size
        self.map_rect = (0, RENDER_Y_OFFSET - map_size[1], map_size[0], map_size[1]) # Rect of map from 0, 0 to map_size
        self.spawn_pos = spawn_pos
        self.objects = objects
        
        player.set_pos(spawn_pos)
    
    def bind_player(self): # Player stays in map
        player.bind(self.map_rect)
    
    def display(self): # Display map
        pygame.draw.rect(surface, color.ORANGE, pygame.Rect(*self.map_rect))
        render_ground()
        render_roof()
    
#--------------------Main--------------------

current_level = Level((200, 250), (0, 0))

def main():
    running = True
    while running:
        # Get Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # If exit button pressed
                running = False # Exit loop
            elif event.type == pygame.KEYDOWN: # Checks for key pressed key
                if event.key == pygame.K_ESCAPE: # Checks if escape is pressed
                    running = False # Exit loop
        
        player.get_player_input()
        player.gravity()
        player.air_resistance()
        player.move()
        current_level.bind_player()

        clock.tick(DEFAULT_TICK) #FPS Speed

def render():
    
    while threading.main_thread().is_alive():
        
        # Render
        surface.fill(color.SKYBLUE)
        
        current_level.display()
        player.display()
        
        pygame.display.flip()
        clock.tick(DEFAULT_FPS) #FPS Speed
            
thread = threading.Thread(target=render)
thread.start()

main()