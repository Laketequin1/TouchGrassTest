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

RENDER_OFFSET = (1920 / 2 - 20, 1080 / 2 - 20) # The pos of items being rendered at 0, 0
GROUND_OFFSET = 800 # The ground pos relitive to top screen when player on y

clock = pygame.time.Clock() # Game tick handling

surface = pygame.display.set_mode(DISPLAY_SIZE, pygame.NOFRAME) # Create screen 

finished = False

class sprite:
    player = pygame.image.load(IMAGE_FOLDER+"player.png").convert() #Loads player (convert to be more efficient as non transparent)
    tree = pygame.image.load(IMAGE_FOLDER+"tree.png") #Loads tree image
    ground = pygame.image.load(IMAGE_FOLDER+"ground.png").convert() #Loads ground (convert to be more efficient as non transparent)
    roof = pygame.image.load(IMAGE_FOLDER+"roof.png").convert() #Loads ground (convert to be more efficient as non transparent)
    enemy = pygame.image.load(IMAGE_FOLDER+"enemy.png").convert()
#--------------------Functions--------------------

def blit_image(image, pos, size=1): # Displays (and resizes) image on screen
    image_width = image.get_width() #Width
    image_height = image.get_height() #Height
    
    image = pygame.transform.scale(image, (round(image_width * size), round(image_height * size))) #Resize image to be relative to the screen, and change its size
    
    surface.blit(image, pos) #Draw resized image at position given

#--------------------Classes--------------------

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
    def get_rel_offset_rect(cls): # Return the left of player, top of player, right of player, bottom of player with relitive to objects on screen
        return (cls.pos[0] - cls.SIZE[0], cls.pos[1], cls.pos[0], cls.pos[1] + cls.SIZE[1])

    @classmethod
    def get_rect(cls): # Return the left of player, top of player, right of player, bottom of player cords in map
        return (-1 * cls.pos[0], cls.pos[1] + cls.SIZE[1], -1 * cls.pos[0] + cls.SIZE[0], cls.pos[1])

    @classmethod
    def get_pos(cls): # Return centre of player with relitivity to screen
        return (cls.pos[0], cls.pos[1])
    
    @classmethod
    def set_pos(cls, pos=(None, None), **kwargs):
        
        # Set player's position at its centre to pos.
        # Has ability to input left, right, top, bottom of player to a pos, which overides pos
        
        if kwargs:
            
            if 'left' in kwargs and 'right' in kwargs:
                raise TwoInputsOfSameAxis('left', 'right', 'x')
            elif 'left' in kwargs:
                cls.pos[0] = -kwargs['left']
            elif 'right' in kwargs:
                cls.pos[0] = -kwargs['right'] + cls.SIZE[0]
            elif pos[0]:
                cls.pos[0] = pos[0] - cls.SIZE[0] / 2
                
            if 'top' in kwargs and 'bottom' in kwargs:
                raise TwoInputsOfSameAxis('top', 'bottom', 'y')
            elif 'top' in kwargs:
                cls.pos[1] = kwargs['top'] - cls.SIZE[1]
            elif 'bottom' in kwargs:
                cls.pos[1] = kwargs['bottom']
            elif pos[1]:
                cls.pos[1] = pos[1] - cls.SIZE[1] / 2
        else:
            cls.pos[0] = pos[0] - cls.SIZE[0] / 2
            cls.pos[1] = pos[1] - cls.SIZE[1] / 2
    
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
        
        print(f"\nplayer rect: {player_left, player_top, player_right, player_bottom}")
        
        print(f"map: {map_rect}\n")
        
        if player_left < map_rect[0]:
            print("left")
            player.set_pos(left=map_rect[0])
        elif player_right > map_rect[2]:
            print("right")
            player.set_pos(right=map_rect[2])
        
        if player_top < map_rect[1]:
            print("top")
            player.set_pos(top=map_rect[1])
        elif player_bottom > map_rect[3]:
            print("bottom")
            player.set_pos(bottom=map_rect[3])

        
    @classmethod
    def display(cls):
        blit_image(sprite.player, player.PLAYER_CENTRE) # Draws player on centre of the screen
    
    
class Level:
    def __init__(self, map_size, spawn_pos, *objects): # Get all parts of the level
        self.map_size = map_size
        self.map_rect = (0, 0, map_size[0], map_size[1]) # Rect of map from 0, 0 to map_size
        self.spawn_pos = spawn_pos
        self.objects = objects
        
        player.set_pos(left=spawn_pos[0], bottom=spawn_pos[1])
    
    def get_player_pos(self):
        return (player.get_rel_offset_rect()[0], player.get_rel_offset_rect()[3])
    
    def bind_player(self): # Player stays in map
        player.bind(self.map_rect)
    
    def display(self): # Display map
        pygame.draw.rect(surface, color.ORANGE, pygame.Rect(RENDER_OFFSET[0] + player.SIZE[0] + self.get_player_pos()[0], RENDER_OFFSET[1] - self.map_size[1] + self.get_player_pos()[1], self.map_rect[2], self.map_rect[3]))

class enemy:
    SIZE = sprite.enemy.get_size()
    
    @classmethod
    def display(cls):
        blit_image(sprite.enemy, player.PLAYER_CENTRE)
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
        
        print(player.get_rect())

        clock.tick(DEFAULT_TICK) #FPS Speed

def render():
    
    while threading.main_thread().is_alive():
        
        # Render
        surface.fill(color.SKYBLUE)
        
        current_level.display()
        player.display()
        #enemy.display()
        pygame.display.flip()
        clock.tick(DEFAULT_FPS) #FPS Speed
            
thread = threading.Thread(target=render)
thread.start()

main()