#--------------------Imports--------------------

from turtle import distance
from pygame import mixer
from sys import exit # Imports exit to prevent errors with exe
import pygame, threading, math, random

pygame.init()
mixer.init()

from src import collision # Imports a functions that test if boxes are colliding
from src import color # Imports lots of colors as RGB

print("\n")

#--------------------Variables--------------------

MUSIC_DEFAULT_VOLUME = 0.07 # Default music volume

SRC_FOLDER = "src/" # The source folder
ICON_FOLDER = SRC_FOLDER + "icon/" # The source folder
FONT_FOLDER = "font/" # The folder for fonts
IMAGE_FOLDER = "images/" # The folder that holds all the image files
SOUND_FOLDER = "sound/" # The sound folder to hold all sound filess
BUTTON_FOLDER = IMAGE_FOLDER+"buttons/"

DISPLAY_SIZE = (1920, 1080) # Screen size
DEFAULT_TICK = 120 # Game tick speed   -   120

DEFAULT_FPS = 160 # Game rendering FPS

RENDER_OFFSET = (1920 / 2 - 20, 1080 / 2 - 20) # The pos of items being rendered at 0, 0
GROUND_OFFSET = 800 # The ground pos relitive to top screen when player on y

clock = pygame.time.Clock() # Game tick handling

surface = pygame.display.set_mode(DISPLAY_SIZE, pygame.NOFRAME) # Create screen
pygame.display.set_icon(pygame.image.load(ICON_FOLDER + 'grass.ico')) # Set icon of window 
pygame.display.set_caption('Touch Grass') # Set name of window

background_color = color.SKYBLUE2 # Set background color
font = pygame.font.Font(FONT_FOLDER + "freesansbold.ttf", 95) # Font used in the game
game_text_font = pygame.font.Font(FONT_FOLDER + "freesansbold.ttf", 40) # Smaller font used in the game

finished = False # Game running

class sprite:
    player = [pygame.image.load(IMAGE_FOLDER + f"player_frames/{i}.png").convert() for i in range(11)] # Loads player frames (convert to be more efficient as non transparent)
    booster = [pygame.image.load(IMAGE_FOLDER + f"booster_frames/{i}.png").convert() for i in range(4)] # Loads booster frames (convert to be more efficient as non transparent)
    booster_slow = [pygame.image.load(IMAGE_FOLDER + f"booster_slow_frames/{i}.png").convert() for i in range(4)] # Loads booster frames (convert to be more efficient as non transparent)
    
    enemy = pygame.image.load(IMAGE_FOLDER + "enemy.png").convert() # Loads enemy (convert to be more efficient as non transparent)
    enemy_invincible = pygame.image.load(IMAGE_FOLDER + "enemy_invincible.png").convert() # Loads enemy (convert to be more efficient as non transparent)
    platform = pygame.image.load(IMAGE_FOLDER + "platform.png").convert() # Loads platform (convert to be more efficient as non transparent)
    
    grass = pygame.image.load(IMAGE_FOLDER + "grass.png") # Loads grass (finish line)
    
    cloud = pygame.image.load(IMAGE_FOLDER + "cloud.png") # Loads cloud
    start_button = pygame.image.load(BUTTON_FOLDER + "start.png") # Loads start button
    settings_button = pygame.image.load(BUTTON_FOLDER + "settings.png") # Loads settings button
    reset_button = pygame.image.load(BUTTON_FOLDER + "reset.png") # Loads reset button
    exit_button = pygame.image.load(BUTTON_FOLDER + "exit.png") # Loads exit button
    mute_button = pygame.image.load(BUTTON_FOLDER + "mute.png")
    unmute_button = pygame.image.load(BUTTON_FOLDER + "unmute.png")
    
    cancel_button = pygame.image.load(BUTTON_FOLDER + "cancel.png") # Loads cancel button
    pause_button = pygame.image.load(BUTTON_FOLDER + "pause.png") # Loads pause button
    
    heart = pygame.image.load(IMAGE_FOLDER + "heart.png") # Loads <3
    
#--------------------Functions--------------------

def blit_image(image, pos, size=1): # Displays (and resizes) image on screen
    image_width = image.get_width() #Width
    image_height = image.get_height() #Height
    
    image = pygame.transform.scale(image, (round(image_width * size), round(image_height * size))) #Resize image to be relative to the screen, and change its size
    
    surface.blit(image, pos) #Draw resized image at position given

def get_player_pos():
    return (player.get_rel_offset_rect()[0], player.get_rel_offset_rect()[3]) # Return player pos (bottom left)

def relitive_object_pos(pos, size, player_pos): # Get render location of object on the screen from object pos relitive to player and size of object
    
    render_pos = [None, None] # Set list to change variebles
    
    render_pos[0] = pos[0] - player_pos[0] # x + player_pos_x 
    render_pos[1] = pos[1] + player_pos[1] # y + player_pos_y
    return (math.floor(RENDER_OFFSET[0] - player.SIZE[0] + render_pos[0]), math.floor(RENDER_OFFSET[1] - size[1] + render_pos[1])) # Return relitive pos

def move_collisions_x(cls):
    has_collided = False
    
    for collisions_rect in cls.collisions_rects:
            
            platform_left = collisions_rect[0] # Get sides of platform
            platform_right = collisions_rect[0] + collisions_rect[2]
            
            x_pos = cls.pos[0] + cls.velocity[0] # New to be position of player
            y_pos = cls.pos[1]
            
            if collision.CheckCollision(collisions_rect, (x_pos, y_pos, *cls.SIZE)): # Check if collideing
                if player.velocity[0] > 0: # Moving right
                    player.set_pos(right=platform_left) # Set position
                    x_pos = cls.pos[0]
                    player.velocity[0] = 0 # Cancel Velocity
                elif player.velocity[0] <= 0: # Moving left
                    player.set_pos(left=platform_right) # Set position
                    x_pos = cls.pos[0]
                    player.velocity[0] = 0 # Cancel Velocity
                
                has_collided = True
                
    if not has_collided:
        cls.pos[0] += cls.velocity[0] # Adds x velocity to the players x position to make it move if not collided

def move_collisions_y(cls):
    has_collided = False
    
    for collisions_rect in cls.collisions_rects: # For each platform rect
            
            platform_bottom = collisions_rect[1] # Vet values
            platform_top = collisions_rect[1] + collisions_rect[3]
            
            x_pos = cls.pos[0]
            y_pos = cls.pos[1] + cls.velocity[1] # New to be position of player
            
            if collision.CheckCollision(collisions_rect, (x_pos, y_pos, *cls.SIZE)): # Check if collideing
                if player.velocity[1] > 0: # Moving up
                    player.set_pos(top=platform_bottom) # Set position
                    y_pos = cls.pos[1]
                    player.velocity[1] = 0 # Cancel Velocity
                elif player.velocity[1] <= 0: # Moving down
                    player.set_pos(bottom=platform_top) # Set position
                    y_pos = cls.pos[1]
                    player.velocity[1] = 0 # Cancel Velocity
                    
                has_collided = True
                
    if not has_collided:
        cls.pos[1] += cls.velocity[1] # Adds y velocity to the players y position to make it move
    
#--------------------Classes--------------------

# Raise custom error setting player pos
class TwoInputsOfSameAxis(Exception):
    def __init__(self, value1, value2, x_or_y):
        super().__init__("The sides {} and {} are both being set on the {} axis".format(value1, value2, x_or_y))


# Raise custom error setting facing diection
class Facing(Exception):
    def __init__(self, facing, faces):
        super().__init__("The facing direction {} was not valid from possible faces {}.".format(facing, faces))


# Raise custom error channel value not int
class ChannelNotInt(Exception):
    def __init__(self, channel):
        super().__init__("The channel value {} is not and int.".format(channel))


class levels:
        current_level = 0 # Current level
        levels = [] # List of all levels
        
        from level import level0, level1, level2, level3, level4, level_c, level_f # Import levels
        
        levels.append(level0) # Add levels to list
        levels.append(level1)
        levels.append(level2)
        levels.append(level3)
        levels.append(level4)
        levels.append(level_c)
        levels.append(level_f)
        
        TOTAL_LEVELS = len(levels) # Get number of levels
        
        @classmethod
        def set_level(cls, value):
            cls.current_level = value # Set current level to value
            
        @classmethod
        def get_level(cls):
            return cls.current_level # Get current level value
            
        @classmethod
        def next_level(cls):
            cls.current_level += 1 # Set current level to value
            
            if cls.current_level > cls.TOTAL_LEVELS - 1: # Loop to first level if finished final level
                cls.current_level = 0
        
        @classmethod
        def start_level(cls):
            return cls.levels[cls.current_level].init(color, levels, Menu, player, Level, Booster, Platform, Enemy, Grass, GameText, Heart) # Restart level, giving it variables we are using


class Music:
    
    @staticmethod
    def start(): # Loads and plays music
        mixer.music.load(f"{SOUND_FOLDER}music.wav") # Selects 
        mixer.music.set_volume(MUSIC_DEFAULT_VOLUME) # Sets volume
        mixer.music.play(-1) # Loops forever
    
    @staticmethod
    def pause(): # Stops music
        mixer.music.pause()
    
    @staticmethod
    def unpause(): # Loads and plays music
        mixer.music.unpause()

    @staticmethod
    def get_volume(): # Returns volume of music
        return mixer.music.get_volume()

    @staticmethod
    def set_volume(volume): # Sets volume of music
        mixer.music.set_volume(volume)


class Sound:
    
    def __init__(self, channel, sound, default_volume = 1):
        
        if type(channel) == int: # If channel is int
            self.channel = int(channel) # Set value
        else: # Else
            raise ChannelNotInt(channel) # Raise error
        
        self.sound = pygame.mixer.Sound(f"{SOUND_FOLDER+sound}.wav")
        self.DEFAULT_VOLUME = default_volume
        
        pygame.mixer.Channel(self.channel).set_volume(self.DEFAULT_VOLUME) # Sets volume to default
    
    def start(self): # Loads and plays sound indefinatly
        pygame.mixer.Channel(self.channel).play(self.sound, -1) # Loops forever
    
    def play(self): # Loads and plays sound
        pygame.mixer.Channel(self.channel).play(self.sound, 0) # Plays once
    
    def pause(self): # Stops sound
        pygame.mixer.Channel(self.channel).pause()
    
    def unpause(self): # Loads and plays sound
        pygame.mixer.Channel(self.channel).unpause()

    def get_volume(self): # Returns volume of sound
        return pygame.mixer.Channel(self.channel).get_volume()

    def set_volume(self, volume): # Sets volume of sound
        pygame.mixer.Channel(self.channel).set_volume(volume)


class player:
    SCREEN_CENTRE = (1920/2, 1080/2) # Player location centred on screen
    SIZE = sprite.player[0].get_size() # Size of player

    PLAYER_CENTRE = (SCREEN_CENTRE[0] - SIZE[0] / 2, SCREEN_CENTRE[1] - SIZE[1] / 2)
    
    VELOCITY_INCREASE = 0.4 # The amount the player velocity increases each time
    DEFAULT_VELOCITY_RESISTANCE = 0.988 # Air resistance default
    GRAVITY = 0.15 # Gravity pulling downwards
    MAX_VELOCITY = 50 # Max speed
    
    velocity_resistance = DEFAULT_VELOCITY_RESISTANCE # Current air resistance
    velocity = [0, 0] # Players current velocity
    pos = [0, 0] # Players cordinate
    prev_pos = [0, 0] # Players previous cordinate
    
    current_frame = 0
    FRAME_SPEED = 0.05
    
    collisions_rects = []
    
    win = False
    dead = False
    
    wind_sound = Sound(0, 'wind', 0) # Wind sound
    wind_sound.start() # Start wind sound
    
    @classmethod
    def get_rel_offset_rect(cls): # Return the left of player, top of player, right of player, bottom of player with relitive to objects on screen
        return (cls.pos[0] - cls.SIZE[0], cls.pos[1], cls.pos[0], cls.pos[1] + cls.SIZE[1])

    @classmethod
    def get_rect(cls, prev=False): # Return the left of player, top of player, right of player, bottom of player cords in map (and previous cordinate)
        if not prev: # Current pos
            return (cls.pos[0], cls.pos[1] + cls.SIZE[1], cls.pos[0] + cls.SIZE[0], cls.pos[1])
        return (cls.prev_pos[0], cls.prev_pos[1] + cls.SIZE[1], cls.prev_pos[0] + cls.SIZE[0], cls.prev_pos[1]) # Previous pos

    @classmethod
    def get_pos(cls): # Return centre of player with relitivity to screen
        return (cls.pos[0], cls.pos[1])
    
    @classmethod
    def set_pos(cls, pos=(None, None), **kwargs):
        
        # Set player's position at its bottom left to position
        # Has ability to input left, right, top, bottom of player to a pos, which overides pos
        
        if kwargs:
            
            if 'left' in kwargs and 'right' in kwargs:
                raise TwoInputsOfSameAxis('left', 'right', 'x') # Error as there can't have two cords on same axis
            elif 'left' in kwargs: 
                cls.pos[0] = kwargs['left'] # Set left side of player to cord supplied
            elif 'right' in kwargs:
                cls.pos[0] = kwargs['right'] - cls.SIZE[0] # Set right side of player to cord supplied
            elif pos[0] != None:
                cls.pos[0] = pos[0] # If axis not stated then use pos coordinate
                
            if 'top' in kwargs and 'bottom' in kwargs:
                raise TwoInputsOfSameAxis('top', 'bottom', 'y') # Error as there can't have two cords on same axis
            elif 'top' in kwargs:
                cls.pos[1] = kwargs['top'] - cls.SIZE[1] # Set top of player to cord supplied
            elif 'bottom' in kwargs:
                cls.pos[1] = kwargs['bottom'] # Set bottom of player to cord supplied
            elif pos[1] != None:
                cls.pos[1] = pos[1] # If axis not stated then use pos coordinate
        else:
            if pos[0] != None:
                cls.pos[0] = pos[0] # If kwargs not supplied then set player pos to supplied pos
            if pos[1] != None:
                cls.pos[1] = pos[1]

        cls.prev_pos = cls.pos
        
    @classmethod
    def gravity(cls): # Player velocity moves down
        cls.velocity[1] -= cls.GRAVITY

    @classmethod
    def air_resistance(cls):
       cls.velocity = [v * (cls.velocity_resistance) for v in cls.velocity] # Adds air resistance

    @classmethod
    def get_player_input(cls):
        keys_pressed = pygame.key.get_pressed() #Gets all pressed keys
        
        if keys_pressed[pygame.K_w] or keys_pressed[pygame.K_UP]: # Move up
            cls.velocity[1] += cls.VELOCITY_INCREASE # Increase velocity
        if keys_pressed[pygame.K_a] or keys_pressed[pygame.K_LEFT]: # Move left
            cls.velocity[0] -= cls.VELOCITY_INCREASE # Increase velocity
        if keys_pressed[pygame.K_s] or keys_pressed[pygame.K_DOWN]: # Move down
            cls.velocity[1] -= cls.VELOCITY_INCREASE # Increase velocity
        if keys_pressed[pygame.K_d] or keys_pressed[pygame.K_RIGHT]: # Move right
            cls.velocity[0] += cls.VELOCITY_INCREASE # Increase velocity
    
    @classmethod
    def move(cls):
        if cls.velocity[0] > cls.MAX_VELOCITY: # Set player velocity to max if it is over
            cls.velocity[0] = cls.MAX_VELOCITY
        elif cls.velocity[0] < -cls.MAX_VELOCITY:
            cls.velocity[0] = -cls.MAX_VELOCITY
        
        if cls.velocity[1] > cls.MAX_VELOCITY: # Set player velocity to max if it is over
            cls.velocity[1] = cls.MAX_VELOCITY
        elif cls.velocity[1] < -cls.MAX_VELOCITY:
            cls.velocity[1] = -cls.MAX_VELOCITY
        
        cls.wind_sound.set_volume( ( abs(cls.velocity[0]) + abs(cls.velocity[1]) ) / (cls.MAX_VELOCITY * 0.9)) # Set volume of wind higher if moving faster
        
        cls.prev_pos = cls.pos # Save previous position of player
        
        if abs(cls.velocity[0]) > abs(cls.velocity[1]): # If moving faster on x velocity
            move_collisions_x(cls)
            move_collisions_y(cls)
        else: # If moving faster on y velocity or same
            move_collisions_y(cls)
            move_collisions_x(cls)

    @classmethod
    def bind(cls, map_rect): # Binds player to map
        
        player_left, player_top, player_right, player_bottom = player.get_rect() # Get cords of the players sides
        
        # If player side outside the wall, set player side to wall side and cancel velocity on x axis
        if player_left < map_rect[0]:
            cls.set_pos(left = map_rect[0])
            cls.velocity[0] = 0 # Cancel Velocity
        elif player_right > map_rect[2]:
            cls.set_pos(right = map_rect[2])
            cls.velocity[0] = 0 # Cancel Velocity
        
        # If player top/bottom outside the roof/ground, set player top/bottom to roof/ground and cancel velocity on y axis
        if player_bottom < map_rect[1]:
            cls.set_pos(bottom = map_rect[1])
            cls.velocity[1] = 0 # Cancel Velocity
        elif player_top > map_rect[3]:
            cls.set_pos(top = map_rect[3])
            cls.velocity[1] = 0 # Cancel Velocity
    
    @classmethod
    def set_wind_volume(cls, value): # Set wind volume for player
        cls.wind_sound.set_volume(value) # Set volume of wind to value
    
    @classmethod
    def display(cls):
        blit_image(sprite.player[math.floor(cls.current_frame)], player.PLAYER_CENTRE) # Draws player on centre of the screen
        
        cls.current_frame += cls.FRAME_SPEED # Changes player frame
        if cls.current_frame > len(sprite.player): # If selected frame does not exist
            cls.current_frame = 0 # Start on first frame    


class Menu:
    
    active = True

    @classmethod
    def activate(cls): # Set to active
        cls.active = True
    
    @classmethod
    def deactivate(cls): # Set to unactive
        cls.active = False
    
    @staticmethod
    def display(background_color): # Fill background with background_color
        surface.fill(background_color)


class Settings:
    def __init__(self, map_size):
        self.MAP_RECT = (0, 0, map_size[0], map_size[1])
        self.actve = False
    
    def display(background_color): # Fill background with background_color
        surface.fill(background_color)


class button:
    click_sound = Sound(5, 'click', 0.32) # Static (global) variable over button
    
    def __init__(self, x, y, image, size_multiplier = 1):
        self.image = image # Set image of self
        self.rect = self.image.get_rect() # Get rect of image
        self.rect.x = x
        self.rect.y = y
        self.clicked = False
        self.active = True
        
        self.rect.width *= size_multiplier # Change width
        self.rect.height *= size_multiplier # Change height
        
        self.size_multiplier = size_multiplier
        
        self.SIZE = image.get_size() # Get size of image

    def update(self):
        
        clicked = False # Not clicked 
        
        if self.active and not self.clicked: # If active and button not previously clicked

            pos = pygame.mouse.get_pos() # Get pos of mouse

            if self.rect.collidepoint(pos): # If mouse on button
                if pygame.mouse.get_pressed()[0] == 1: # If mouse down and not self.clicked
                    self.click_sound.play() # Play click sound
                    clicked = True # Set clicked to true
                    self.clicked = True # Set previous clicked to True

        if pygame.mouse.get_pressed()[0] == 0: # If not mousedown
            self.clicked = False # Set previous clicked to False
        
        return clicked # Return if clicked or not
    
    def set_clicked(self, bool): # Set clicked to True/False
        self.clicked = bool
    
    def display(self): # Optional Size Paramiter, default of 1
        
        image = pygame.transform.scale(self.image, (round(self.SIZE[0]  * self.size_multiplier), round(self.SIZE[1]  * self.size_multiplier))) # Resize image
        
        surface.blit(image, self.rect) # Display button at screen pos


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
        for object in self.objects: # Update all objects in level
            object.update()
    
    def display_objects(self, player_pos):
        for object in self.objects: # Display all objects in level
            object.display(player_pos)
    
    def display(self, player_pos, background_color): # Display map
        pygame.draw.rect(surface, background_color, pygame.Rect(*relitive_object_pos((0, 0), self.MAP_SIZE, player_pos), self.MAP_RECT[2], self.MAP_RECT[3])) # Render level game square


class Enemy(): # Inherit from pygame sprite
    enemy_death_sound = Sound(2, 'enemy_death', 0.32) # Static (global) variable over enemy
    player_death_sound = Sound(3, 'player_death', 0.35) # Static (global) variable over enemy
    
    def __init__(self, pos, invincible=False, move_direction=None, distance=0, speed = 1, delay = 0): # Initlizes enemy
        x, y = pos
        self.rect = sprite.enemy.get_rect() # Gets rectangle of enemy sprite
        self.rect.x = x # Gets enemys x coord 
        self.rect.y = -y # Gets enemys y coord
        self.move_direction = move_direction # sets up var for movement from side to side
        self.distance = distance # Distance enemy can move in that direction (pos is up and right)
        
        self.speed = speed # How fast it moves
        
        self.move_counter = 0 # Tracks enemy movemnt direction
        self.move_counter_direction = speed
        
        self.dead = False # Is dead
        
        if not invincible: # If can be killed
            self.DEATH_VELOCITY = 24 # Player velocity needed to kill self
            self.image = sprite.enemy
        else:
            self.DEATH_VELOCITY = 9999 # Player velocity needed to kill self impossibly high
            self.image = sprite.enemy_invincible
        
        # The best I can do without rewriting Malachi's code
        for x in range(delay):
            self.move_counter += self.move_counter_direction
        
            if self.move_direction == 'x':
                self.rect.x += self.move_counter_direction # Move x
            elif self.move_direction == 'y':
                self.rect.y += self.move_counter_direction # Move y
            elif self.move_direction != None:
                raise Exception(f"Enemy move direction {self.move_direction} not valid") # If something else error
            
            if self.move_counter + self.speed > self.distance: # Checks if counter is above distance
                self.move_counter_direction = -self.speed # Resets counter
            elif self.move_counter - self.speed < 0:
                self.move_counter_direction = self.speed # Resets counter
        
    def update(self):
        
        self.move_counter += self.move_counter_direction
        
        if self.move_direction == 'x':
            self.rect.x += self.move_counter_direction # Move x
        elif self.move_direction == 'y':
            self.rect.y += self.move_counter_direction # Move y
        elif self.move_direction != None:
            raise Exception(f"Enemy move direction {self.move_direction} not valid") # If something else error
        
        if self.move_counter + self.speed > self.distance: # Checks if counter is above distance
            self.move_counter_direction = -self.speed # Resets counter
        elif self.move_counter - self.speed < 0:
            self.move_counter_direction = self.speed # Resets counter
        
        if not self.dead:
            if pygame.Rect.colliderect(pygame.Rect(*relitive_object_pos((self.rect.x, self.rect.y), self.image.get_size(), get_player_pos()), *self.image.get_size()), pygame.Rect(*player.PLAYER_CENTRE, *player.SIZE)): # Checks for collision between player and enemy
                if abs(player.velocity[0]) + abs(player.velocity[1]) < self.DEATH_VELOCITY: # If slow
                    player.dead = True # Player dead
                    self.player_death_sound.play() # Play death sound
                else:
                    self.dead = True # Kill enemy
                    self.enemy_death_sound.play() # Play enemy death sound
                    

    def display(self, player_pos):
        if not self.dead:
            blit_image(self.image, relitive_object_pos((self.rect.x, self.rect.y), self.image.get_size(), player_pos)) # Display enemy on screen relitive to player


class GameText:
    def __init__(self, pos, text, text_color):
        self.pos = pos
            
        self.display_text = game_text_font.render(text, True, text_color) # Set font to display
            
        self.text_color = text_color 
        
        self.SIZE = self.display_text.get_size() # Get width of image of text
        
    def display(self, player_pos):
        blit_image(self.display_text, relitive_object_pos((self.pos[0], -self.pos[1]), self.SIZE, player_pos)) # Displays text relitive to player
    
    def update(self):
        pass


class Platform:
    def __init__(self, pos):
        x, y = pos
        self.image = sprite.platform # Gets sprite
        self.SIZE = sprite.platform.get_size() # Gets size of sprite
        self.rect = self.image.get_rect() # Gets rectangle of sprite
        self.rect.x = x # Gets platform x pos
        self.rect.y = y # Gets platform y pos
        
        player.collisions_rects.append(self.rect) # Set player platforms collisions rects

    def display(self, player_pos):
        blit_image(sprite.platform, relitive_object_pos((self.rect.x, -self.rect.y), sprite.platform.get_size(), player_pos)) # Displays platform on screen reletive to player 
    
    def update(self):
        pass
    
    
class Grass:
    win_sound = Sound(4, 'win', 0.05) # Static (global) variable over grass
    
    def __init__(self, pos):
        self.pos = (pos[0], -pos[1]) # Position on map
    
    def display(self, player_pos):
        blit_image(sprite.grass, relitive_object_pos(self.pos, sprite.grass.get_size(), player_pos)) # Displays grass on screen reletive to player 
        
    def update(self):
        if pygame.Rect.colliderect(pygame.Rect(*relitive_object_pos(self.pos, sprite.grass.get_size(), get_player_pos()), *sprite.platform.get_size()), pygame.Rect(*player.PLAYER_CENTRE, *player.SIZE)): # Checks for collision between player and grass 
            player.win = True # If colliding with grass win
            self.win_sound.play()
            levels.next_level()


class Heart: # Displays a heart (aesthetics)
    def __init__(self, pos):
        self.pos = (pos[0], -pos[1]) # Position on map
    
    def display(self, player_pos):
        blit_image(sprite.heart, relitive_object_pos(self.pos, sprite.heart.get_size(), player_pos)) # Displays grass on screen reletive to player 
        
    def update(self):
        pass


class Booster:
    def __init__(self, pos, facing):
        self.SIZE = sprite.platform.get_size() # Gets size of sprite
        self.FRAME_SPEED = 0.03 # Frame speed
        
        self.SLOW_AMOUNT = 0.8 # Amount player slows
        self.EXTRA_BOOST = 1.03 # Multiplier for boost
        self.STATIC_BOOST = 0.5 # Definite speed for boost
        
        self.current_frame = 0
        self.image_frames = [*sprite.booster] # Set image frames to contents of sprite.booster, not the pointer of sprite.booster
        self.slow_image_frames = [*sprite.booster_slow] # Set image frames to contents of sprite.booster, not the pointer of sprite.booster
        
        self.pos = pos # Position
        self.display_pos = (pos[0], -pos[1]) # Render position needs negitive y
        self.rect = [*self.pos, self.SIZE[0], self.SIZE[1]] # Rect of booster
        
        self.slow_name = 'slow'
        self.faces = ['up', 'down', 'left', 'right'] # Possible directions
        self.faces_angle = { 'up': 270, 'down': 90, 'left': 0, 'right': 180} # Possible directions
        
        self.wind_sound = Sound(1, 'swish', 0.06)
        
        if facing in self.faces or facing == self.slow_name: # If input for facing direction exists, or is slow
            self.facing = facing
        else:
            raise Facing(facing, self.faces) # Error, as variable is not in direction
        
        if self.facing == self.slow_name: # If slow booster
            self.image_frames = self.slow_image_frames # Set frames to slow
        else:
            for i, image in enumerate(self.image_frames): # Enumerate through each frame
                for face in self.faces: # Go through each possible facing direction
                    if facing == face: # If facing this direction
                        self.image_frames[i] = pygame.transform.rotate(image, self.faces_angle[facing]) # Rotate image of booster by set angle from self.faces_angle using facing direction, and change image in frames
                    
    def update(self):
        
        player_left, _, _, player_bottom = player.get_rect() # Get sides of player we need, discard the rest (_)
        
        if collision.CheckCollision(self.rect, [player_left, player_bottom, *player.SIZE]): # If player colliding with booster
            
            if self.facing == 'left': # If booster facing left
                player.velocity = [-(abs(player.velocity[0]) + abs(player.velocity[1]) + self.STATIC_BOOST) * self.EXTRA_BOOST, 0] # Player goes vroom left
                self.wind_sound.play() # Play sound
            elif self.facing == 'right': # If booster facing right
                player.velocity = [(abs(player.velocity[0]) + abs(player.velocity[1]) + self.STATIC_BOOST) * self.EXTRA_BOOST, 0] # Player goes vroom right
                self.wind_sound.play() # Play sound
            elif self.facing == 'up': # If booster facing up
                player.velocity = [0, (abs(player.velocity[0]) + abs(player.velocity[1]) + self.STATIC_BOOST) * self.EXTRA_BOOST] # Player goes vroom up
                self.wind_sound.play() # Play sound
            elif self.facing == 'down': # If booster facing down
                player.velocity = [0, -(abs(player.velocity[0]) + abs(player.velocity[1]) + self.STATIC_BOOST) * self.EXTRA_BOOST] # Player goes vroom down
                self.wind_sound.play() # Play sound
            else: # Slow booster:
                player.velocity = [player.velocity[0] * self.SLOW_AMOUNT, player.velocity[1] * self.SLOW_AMOUNT] # Slow player

    def display(self, player_pos):
        
        blit_image(self.image_frames[math.floor(self.current_frame)], relitive_object_pos(self.display_pos, self.SIZE, player_pos)) # Draws booster frame relitive to player on screen
        
        self.current_frame += self.FRAME_SPEED # Changes player frame
        if self.current_frame > len(self.image_frames): # If selected frame does not exist
            self.current_frame = 0 # Start on first frame


#--------------------Main--------------------

player.current_level = levels.start_level() # Start first level

# Create buttons, setting pos, sprite, and size
start_button = button(1920 / 2 - 460, 1080 / 2, sprite.start_button)
next_button = button(1920 / 2 - sprite.start_button.get_width() / 2, 1080 / 2, sprite.start_button)
settings_button = button(1920 / 2 + 120, 1080 / 2, sprite.settings_button)
reset_button = button(DISPLAY_SIZE[0] / 2 - sprite.reset_button.get_width() * 1.5 / 2, DISPLAY_SIZE[1] - sprite.reset_button.get_height() * 1.5 - 350, sprite.reset_button, 1.5)
exit_button = button(1920 / 2 - 165, 1080 / 2 + 225, sprite.exit_button)
mute_button = button(1920/ 2 - 285  , 1080 / 2 , sprite.mute_button)
unmute_button = button(1920 / 2 + 175, 1080 / 2 , sprite.unmute_button)
cancel_button = button(1920 / 2 - 165, 1080 / 2 + 225, sprite.cancel_button)
pause_button = button(5, 5, sprite.pause_button, 0.5)
cloud_button = button(100, 100, sprite.cloud)

# Set cloud_button background_color to to access over threads
cloud_button.background_color = background_color

#--------------------Main--------------------

def main():

    running = True
    while running:
        # Get Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # If exit button pressed
                running = False # Exit loop
            elif event.type == pygame.KEYDOWN: # Checks for key pressed key
                if event.key == pygame.K_ESCAPE: # Checks if escape is pressed
                    Menu.active = True # Open menu
                    Settings.active = False # Exit settings
        
        if Menu.active: # If menu active
            player.set_wind_volume(0) # Stop player wind noise
            if cloud_button.update(): # If cloud_button clicked
                cloud_button.background_color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)) # Set background color to random color
            if start_button.update(): # If start_button clicked
                Menu.active = False # Deactivate menu
                player.current_level = levels.start_level() # Start level
            if exit_button.update(): # Exit button pressed
                exit() # Exit
            if settings_button.update(): # Settings button pressed
                unmute_button.set_clicked(True) # Setclicked for unmute button to true so it can't be immediately pressed
                Menu.active = False # Close menu
                Settings.active = True # Activate settings
        elif Settings.active: # If settings active
            if cancel_button.update(): # If cancel button pressed
                exit_button.set_clicked(True) # Setclicked for exit button to true so it can't be immediately pressed
                Settings.active = False # Exit settings
                Menu.active = True # Open menu
            if mute_button.update(): # If mute button pressed
                Music.pause() # Pause music
            if unmute_button.update(): # If unmute button pressed
                Music.unpause() # Unpause music
        elif player.dead: # If player dead
            player.set_wind_volume(0) # Stop wind
            if reset_button.update(): # If reset button clicked
                player.current_level = levels.start_level() # Restart level
            elif pause_button.update(): # If pause button clicked
                Menu.active = True # Go to main menu
        elif player.win: # If player won
            if next_button.update(): # If next_button clicked
                player.current_level = levels.start_level() # Restart level
            elif pause_button.update(): # If pause button clicked
                Menu.active = True # Go to main menu
        else:
            player.get_player_input() # Update player
            player.gravity()
            player.air_resistance()
            player.move()
        
            player.current_level.bind_player() # Run first time to calculate for object
            player.current_level.update_objects() # Update level
            player.current_level.bind_player() # Then after objects changed pos
            
            if pause_button.update(): # If pause button clicked
                Menu.active = True # Go to main menu

        clock.tick(DEFAULT_TICK) #FPS Speed

#--------------------Render--------------------

def render():
    Music.start() # Play music

    Menu.active = True # Menu open
    Settings.active = False # Settings closed

    # Create text for player
    menu_text = font.render("Touch Grass", True, color.WHITE)
    win_text = font.render("Level Complete!", True, color.WHITE)
    dead_text = font.render("YOU DIED!", True, color.WHITE)
    settings_text = font.render("Settings", True, color.WHITE)

    # While the main thread running
    while threading.main_thread().is_alive():
        
        player_pos = get_player_pos() # Get player position, so its synced throughout render
        
        # Render
        surface.fill(color.GRAY20) # Normal background
        
        if Menu.active == True: # If menu active, display menu
            Menu.display(cloud_button.background_color)
            if start_button.active and exit_button.active and settings_button.active == True: # If buttons active display text, and buttons
                surface.blit(menu_text, (1920 / 2 - 300, 250))
                button.display(cloud_button)
                button.display(start_button)
                button.display(settings_button)
                button.display(exit_button)
        elif Settings.active: # If menu active, display settings, text and buttons
            Settings.display(cloud_button.background_color)
            surface.blit(settings_text, (1920 / 2 - settings_text.get_width() / 2, 250))
            button.display(cloud_button)
            button.display(mute_button)
            button.display(unmute_button)
            button.display(cancel_button)
        elif player.dead == True: # If player dead display background, dead text, and button
            surface.fill(color.RED2) # If dead background red
            surface.blit(dead_text, (1920 / 2 - 250, 200))
            button.display(reset_button)
            
            pause_button.display() # Display pause button at half size
        elif player.win == True:
            surface.fill(color.GREEN2) # Normal background
            button.display(next_button)
            surface.blit(win_text, (1920 / 2 - win_text.get_width()/2, 200))
            
            pause_button.display() # Display pause button at half size
        else:
            player.current_level.display(player_pos, cloud_button.background_color) # Display level with background color
            player.current_level.display_objects(player_pos) # Display everything in level
            player.display()
            
            pause_button.display() # Display pause button at half size

        pygame.display.flip()
        clock.tick(DEFAULT_FPS) #FPS Speed

#--------------------Start--------------------

# Create a thread for rendering
thread = threading.Thread(target=render)
thread.start()

# Start main code
main()
