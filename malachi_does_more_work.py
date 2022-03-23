#--------------------Imports--------------------

from re import X
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
    player = player = [pygame.image.load(IMAGE_FOLDER+f"player_frames/{i}.png").convert() for i in range(11)] #Loads player frames (convert to be more efficient as non transparent)
    tree = pygame.image.load(IMAGE_FOLDER+"tree.png") #Loads tree image
    ground = pygame.image.load(IMAGE_FOLDER+"ground.png").convert() #Loads ground (convert to be more efficient as non transparent)
    roof = pygame.image.load(IMAGE_FOLDER+"roof.png").convert() #Loads ground (convert to be more efficient as non transparent)
    enemy = pygame.image.load(IMAGE_FOLDER+"enemy.png").convert()
    grass_platform = pygame.image.load(IMAGE_FOLDER+"enemy.png")
#--------------------Functions--------------------

def blit_image(image, pos, size=1): # Displays (and resizes) image on screen
    image_width = image.get_width() #Width
    image_height = image.get_height() #Height
    
    image = pygame.transform.scale(image, (round(image_width * size), round(image_height * size))) #Resize image to be relative to the screen, and change its size
    
    surface.blit(image, pos) #Draw resized image at position given

def get_player_pos():
    return (player.get_rel_offset_rect()[0], player.get_rel_offset_rect()[3]) # Return player pos (bottom left)

def relitive_object_pos(pos, size, player_pos): # Get render location of object on the screen from object pos relitive to player and size of object
    pos = [i + j for i, j in zip(pos, player_pos)] # x + player_pos_x     and     y + player_pos_y
    return (RENDER_OFFSET[0] + player.SIZE[0] + pos[0], RENDER_OFFSET[1] - size[1] + pos[1]) # Return relitive pos

#--------------------Classes--------------------

# Raise custom error setting player pos
class TwoInputsOfSameAxis(Exception):
    def __init__(self, value1, value2, x_or_y):
        super().__init__("The sides {} and {} are both being set on the {} axis".format(value1, value2, x_or_y))

class Platform:
    def __init__(self, x, y):
        self.image = sprite.grass_platform
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def display(self, player_pos):
        blit_image(sprite.grass_platform, relitive_object_pos((self.rect.x, self.rect.y), sprite.grass_platform.get_size(), player_pos))
    
    def update(self):
        collide = pygame.Rect.colliderect(pygame.Rect(*relitive_object_pos((self.rect.x, self.rect.y), sprite.grass_platform.get_size(), get_player_pos()), *sprite.enemy.get_size()), pygame.Rect(*player.PLAYER_CENTRE, *player.SIZE))

        if collide:
            print("hit")
            
           

class player:
    SCREEN_CENTRE = (1920/2, 1080/2) # Player location centred on screen
    SIZE = sprite.player[0].get_size() # Size of player

    PLAYER_CENTRE = (SCREEN_CENTRE[0] - SIZE[0] / 2, SCREEN_CENTRE[1] - SIZE[1] / 2)
    
    VELOCITY_INCREASE = 0.4 # The amount the player velocity increases each time
    DEFAULT_VELOCITY_RESISTANCE = 0.989 # Air resistance default
    GRAVITY = 0.15 # Gravity pulling downwards

    velocity_resistance = DEFAULT_VELOCITY_RESISTANCE # Current air resistance
    velocity = [0, 0] # Players current velocity
    pos = [0, 0] # Players cordinate
    
    current_frame = 0
    FRAME_SPEED = 0.05
    
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
                raise TwoInputsOfSameAxis('left', 'right', 'x') # Error as there can't have two cords on same axis
            elif 'left' in kwargs: 
                cls.pos[0] = -kwargs['left'] # Set left side of player to cord supplied
            elif 'right' in kwargs:
                cls.pos[0] = -kwargs['right'] + cls.SIZE[0] # Set right side of player to cord supplied
            elif pos[0]:
                cls.pos[0] = pos[0] - cls.SIZE[0] / 2 # If axis not stated then use pos coordinate
                
            if 'top' in kwargs and 'bottom' in kwargs:
                raise TwoInputsOfSameAxis('top', 'bottom', 'y') # Error as there can't have two cords on same axis
            elif 'top' in kwargs:
                cls.pos[1] = kwargs['top'] - cls.SIZE[1] # Set top of player to cord supplied
            elif 'bottom' in kwargs:
                cls.pos[1] = kwargs['bottom'] # Set bottom of player to cord supplied
            elif pos[1]:
                cls.pos[1] = pos[1] - cls.SIZE[1] / 2 # If axis not stated then use pos coordinate
        else:
            cls.pos[0] = pos[0] - cls.SIZE[0] / 2 # If kwargs not supplied then set player pos to supplied pos
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
        cls.pos = [i + j for i, j in zip(cls.pos, cls.velocity)] # Adds velocity to the players position to make it move

    @classmethod
    def bind(cls, map_rect): # Binds player to map
        
        player_left, player_top, player_right, player_bottom = player.get_rect() # Get cords of the players sides
        
        # If player side outside the wall, set player side to wall side and cancel velocity on x axis
        if player_left < map_rect[0]:
            player.set_pos(left=map_rect[0])
            player.velocity[0] = 0
        elif player_right > map_rect[2]:
            player.set_pos(right=map_rect[2])
            player.velocity[0] = 0
        
        # If player top/bottom outside the roof/ground, set player top/bottom to roof/ground and cancel velocity on y axis
        if player_bottom < map_rect[1]:
            player.set_pos(bottom=map_rect[1])
            player.velocity[1] = 0
        elif player_top > map_rect[3]:
            player.set_pos(top=map_rect[3])
            player.velocity[1] = 0

    @classmethod
    def display(cls):
        blit_image(sprite.player[round(cls.current_frame)], player.PLAYER_CENTRE) # Draws player on centre of the screen
        cls.current_frame += cls.FRAME_SPEED
        if cls.current_frame > 10:
            cls.current_frame = 0
    


class Level:
    def __init__(self, map_size, spawn_pos, objects): # Get all parts of the level
        self.MAP_SIZE = map_size
        self.MAP_RECT = (0, 0, map_size[0], map_size[1]) # Rect of map from 0, 0 to map_size
        self.SPAWN_POS = spawn_pos
        self.objects = objects
        
        self.set_player_pos(spawn_pos) # Set player to spawn position
    
    def set_player_pos(self, pos):
        player.set_pos(left=pos[0], bottom=pos[1]) # Set player position (bottom left) to pos
    
    def bind_player(self): # Player stays in map
        player.bind(self.MAP_RECT)
    
    def update_objects(self):
        for object in self.objects:
            object.update()
    
    def display_objects(self, player_pos):
        for object in self.objects:
            object.display(player_pos)
    
    def display(self, player_pos): # Display map
        pygame.draw.rect(surface, color.SKYBLUE2, pygame.Rect(*relitive_object_pos((0, 0), self.MAP_SIZE, player_pos), self.MAP_RECT[2], self.MAP_RECT[3] - 1)) # Render level game square


class Enemy(): # Inherit from pygame sprite
    def __init__(self, x, y):
       self.rect = sprite.enemy.get_rect()
       self.rect.x = x
       self.rect.y = -y
       self.move_direction = 1
       self.move_counter = 0

    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1
		    
    def display(self, player_pos):
        blit_image(sprite.enemy, relitive_object_pos((self.rect.x, self.rect.y), sprite.enemy.get_size(), player_pos)) # Display enemy on screen relitive to player


#--------------------Main--------------------

current_level = Level((1000, 1000), (0, 0), [Enemy(500, 0), Enemy(500, 200), Enemy(100, 500), Enemy(150, 500), Enemy(150, 200), Enemy(550, 0), Enemy(600, 0), Enemy(550, 200), Enemy(600, 200), Enemy(700, 700), Platform(500, -500)]) # (sizex, sizey), (spawn pos), [Enemy(), Platform()]

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
        
        current_level.update_objects()
        
        current_level.bind_player()

        clock.tick(DEFAULT_TICK) #FPS Speed

def render():
    
    
    # While the main thread running
    while threading.main_thread().is_alive():
        
        player_pos = get_player_pos()
        
        # Render
        surface.fill(color.GRAY20)
        
        current_level.display(player_pos)
        current_level.display_objects(player_pos)
        player.display()
        
    
        
        pygame.display.flip()
        clock.tick(DEFAULT_FPS) #FPS Speed

# Create a thread for rendering
thread = threading.Thread(target=render)
thread.start()

# Start main code
main()
