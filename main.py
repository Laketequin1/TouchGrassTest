#--------------------Imports--------------------

from pygame import mixer
import pygame, threading, math
pygame.init()
mixer.init()

from src import line_intersection # Imports a function that can get the intersection of two lines
line_intersection = line_intersection.line_intersection # Imports function from import

from src import collision # Imports a functions that test if boxes are colliding
from src import color # Imports lots of colors as RGB

from level import level0, level1, level2 # Import levels

print("\n")

#--------------------Variables--------------------

ORIGINAL_THREAD_COUNT = threading.activeCount()

MUSIC_DEFAULT_VOLUME = 0.08 # Default music volume

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

font = pygame.font.Font("freesansbold.ttf", 95)

finished = False

class sprite:
    player = [pygame.image.load(IMAGE_FOLDER + f"player_frames/{i}.png").convert() for i in range(11)] # Loads player frames (convert to be more efficient as non transparent)
    booster = [pygame.image.load(IMAGE_FOLDER + f"booster_frames/{i}.png").convert() for i in range(4)] # Loads booster frames (convert to be more efficient as non transparent)
    
    ground = pygame.image.load(IMAGE_FOLDER + "ground.png").convert() # Loads ground (convert to be more efficient as non transparent)
    roof = pygame.image.load(IMAGE_FOLDER + "roof.png").convert() # Loads ground (convert to be more efficient as non transparent)
    enemy = pygame.image.load(IMAGE_FOLDER + "enemy.png").convert() # Loads enemy (convert to be more efficient as non transparent)
    platform = pygame.image.load(IMAGE_FOLDER + "platform.png").convert() # Loads platform (convert to be more efficient as non transparent)
    
    grass = pygame.image.load(IMAGE_FOLDER + "grass.png") # Loads grass (finish line)
    
    cloud = pygame.image.load(IMAGE_FOLDER + "cloud.png") # Loads cloud
    start_button = pygame.image.load(BUTTON_FOLDER + "start.png") # Loads start button
    settings_button = pygame.image.load(BUTTON_FOLDER + "settings.png") # Loads settings button
    reset_button = pygame.image.load(BUTTON_FOLDER + "reset.png") # Loads reset button
    exit_button = pygame.image.load(BUTTON_FOLDER + "exit.png") # Loads exit button
    
#--------------------Functions--------------------

def blit_image(image, pos, size=1): # Displays (and resizes) image on screen
    image_width = image.get_width() #Width
    image_height = image.get_height() #Height
    
    image = pygame.transform.scale(image, (round(image_width * size), round(image_height * size))) #Resize image to be relative to the screen, and change its size
    
    surface.blit(image, pos) #Draw resized image at position given

def get_player_pos():
    return (player.get_rel_offset_rect()[0], player.get_rel_offset_rect()[3]) # Return player pos (bottom left)

def relitive_object_pos(pos, size, player_pos): # Get render location of object on the screen from object pos relitive to player and size of object
    
    render_pos = [None, None]
    
    render_pos[0] = pos[0] - player_pos[0] # x + player_pos_x 
    render_pos[1] = pos[1] + player_pos[1] # y + player_pos_y
    return (RENDER_OFFSET[0] - player.SIZE[0] + render_pos[0], RENDER_OFFSET[1] - size[1] + render_pos[1]) # Return relitive pos

def move_collisions_x(cls):
    has_collided = False
    
    for collisions_rect in cls.collisions_rects:
            
            platform_left = collisions_rect[0] # Get sides of platform
            platform_bottom = collisions_rect[1]
            platform_right = collisions_rect[0] + collisions_rect[2]
            platform_top = collisions_rect[1] + collisions_rect[3]
            
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
        cls.pos[0] += cls.velocity[0] # Adds x velocity to the players x position to make it move

def move_collisions_y(cls):
    has_collided = False
    
    for collisions_rect in cls.collisions_rects:
            
            platform_left = collisions_rect[0] # Get sides of platform
            platform_bottom = collisions_rect[1]
            platform_right = collisions_rect[0] + collisions_rect[2]
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
    
    wind_sound = Sound(0, 'wind', 0)
    wind_sound.start()
    
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
        
        if keys_pressed[pygame.K_w]:
            cls.velocity[1] += cls.VELOCITY_INCREASE # Increase velocity
        if keys_pressed[pygame.K_a]:
            cls.velocity[0] -= cls.VELOCITY_INCREASE # Increase velocity
        if keys_pressed[pygame.K_s]:
            cls.velocity[1] -= cls.VELOCITY_INCREASE # Increase velocity
        if keys_pressed[pygame.K_d]:
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
        
        cls.wind_sound.set_volume( ( abs(cls.velocity[0]) + abs(cls.velocity[1]) ) / (cls.MAX_VELOCITY * 1) + 0.3) # Set volume of wind higher if moving faster
        
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
    def display(cls):
        blit_image(sprite.player[math.floor(cls.current_frame)], player.PLAYER_CENTRE) # Draws player on centre of the screen
        
        cls.current_frame += cls.FRAME_SPEED # Changes player frame
        if cls.current_frame > len(sprite.player): # If selected frame does not exist
            cls.current_frame = 0 # Start on first frame    


class Menu:
    def __init__(self, map_size):
        self.MAP_RECT = (0, 0, map_size[0], map_size[1])
        self.active = True

    def display(self):
        pygame.draw.rect(surface, color.SKYBLUE, pygame.Rect(0, 0, *DISPLAY_SIZE))


class Settings:
    def __init__(self, map_size):
        self.MAP_RECT = (0, 0, map_size[0], map_size[1])
    
    def display(self):
        pygame.draw.rect(surface, color.SKYBLUE, pygame.Rect(0, 0, *DISPLAY_SIZE))


class button:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False
        self.active = True

    def update(self):
        
        if self.active:

            clicked = False

            pos = pygame.mouse.get_pos()

            if self.rect.collidepoint(pos):
                    if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                        clicked = True
                        self.clicked = True
            
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
                         
            return clicked
    
    def display(self):
        surface.blit(self.image, self.rect)


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
    
    def display(self, player_pos): # Display map
        pygame.draw.rect(surface, color.SKYBLUE2, pygame.Rect(*relitive_object_pos((0, 0), self.MAP_SIZE, player_pos), self.MAP_RECT[2], self.MAP_RECT[3] - 1)) # Render level game square


class Enemy(): # Inherit from pygame sprite
    def __init__(self, x, y): # Initlizes enemy
       self.rect = sprite.enemy.get_rect() # Gets rectangle of enemy sprite
       self.rect.x = x # Gets enemys x coord 
       self.rect.y = -y # Gets enemys y coord
       self.move_direction = 1 # sets up var for movement from side to side
       self.move_counter = 0 # Tracks enemy movemnt direction

    def update(self):
        '''
        self.rect.x += self.move_direction 
        self.move_counter += 1 # Adds 1 to counter
        if abs(self.move_counter) > 50: # Checks if counter is above 50
            self.move_direction *= -1 # Changes movement direction
            self.move_counter *= -1 # Resets counter
        '''
        if pygame.Rect.colliderect(pygame.Rect(*relitive_object_pos((self.rect.x, self.rect.y), sprite.enemy.get_size(), get_player_pos()), *sprite.enemy.get_size()), pygame.Rect(*player.PLAYER_CENTRE, *player.SIZE)): # Checks for collision between player and enemy
            player.dead = True # Player dead

    def display(self, player_pos):
        blit_image(sprite.enemy, relitive_object_pos((self.rect.x, self.rect.y), sprite.enemy.get_size(), player_pos)) # Display enemy on screen relitive to player


class Platform:
    def __init__(self, x, y):
        self.image = sprite.platform # Gets sprite
        self.SIZE = sprite.platform.get_size() # Gets size of sprite
        self.rect = self.image.get_rect() # Gets rectangle of sprite
        self.rect.x = x # Gets platform x pos
        self.rect.y = y # Gets platform y pos
        
        player.collisions_rects.append(self.rect)

    def display(self, player_pos):
        blit_image(sprite.platform, relitive_object_pos((self.rect.x, -self.rect.y), sprite.platform.get_size(), player_pos)) # Displays platform on screen reletive to player 
    
    def update(self):
        pass
    
    
class Grass:
    def __init__(self, pos):
        self.pos = (pos[0], -pos[1]) # Position on map
    
    def display(self, player_pos):
        blit_image(sprite.grass, relitive_object_pos(self.pos, sprite.grass.get_size(), player_pos)) # Displays grass on screen reletive to player 
        
    def update(self):
        if pygame.Rect.colliderect(pygame.Rect(*relitive_object_pos(self.pos, sprite.grass.get_size(), get_player_pos()), *sprite.platform.get_size()), pygame.Rect(*player.PLAYER_CENTRE, *player.SIZE)): # Checks for collision between player and grass 
            player.win = True # If colliding with grass win
            

class Booster:
    def __init__(self, pos, facing):
        self.SIZE = sprite.platform.get_size() # Gets size of sprite
        self.FRAME_SPEED = 0.03 # Frame speed
        
        self.EXTRA_BOOST = 1.04 # Multiplier for boost
        self.STATIC_BOOST = 1 # Definite speed for boost
        
        self.current_frame = 0
        self.image_frames = [*sprite.booster] # Set image frames to contents of sprite.booster, not the pointer of sprite.booster
        
        self.pos = pos # Position
        self.display_pos = (pos[0], -pos[1]) # Render position needs negitive y
        self.rect = [*self.pos, self.SIZE[0], self.SIZE[1]] # Rect of booster
        
        self.faces = ['up', 'down', 'left', 'right'] # Possible directions
        self.faces_angle = { 'up': 270, 'down': 90, 'left': 0, 'right': 180} # Possible directions
        
        self.wind_sound = Sound(1, 'swish', 0.06)
        
        if facing in self.faces: # If input for facing direction is allowed
            self.facing = facing
        else:
            raise Facing(facing, self.faces) # Error, as variable is not in direction
        
        for i, image in enumerate(self.image_frames): # Enumerate through each frame
            for face in self.faces: # Go through each possible facing direction
                if facing == face: # If facing this direction
                    self.image_frames[i] = pygame.transform.rotate(image, self.faces_angle[facing]) # Rotate image of booster by set angle from self.faces_angle using facing direction, and change image in frames
                    
    def update(self):
        
        player_left, _, _, player_bottom = player.get_rect() # Get sides of player we need, discard the rest (_)
        
        if collision.CheckCollision(self.rect, [player_left, player_bottom, *player.SIZE]): # If player colliding with booster
            self.wind_sound.play() # Play sound
            
            if self.facing == 'left': # If booster facing left
                player.velocity = [-(abs(player.velocity[0]) + abs(player.velocity[1]) + self.STATIC_BOOST) * self.EXTRA_BOOST, 0] # Player goes vroom left
            elif self.facing == 'right': # If booster facing right
                player.velocity = [(abs(player.velocity[0]) + abs(player.velocity[1]) + self.STATIC_BOOST) * self.EXTRA_BOOST, 0] # Player goes vroom right
            elif self.facing == 'up': # If booster facing up
                player.velocity = [0, (abs(player.velocity[0]) + abs(player.velocity[1]) + self.STATIC_BOOST) * self.EXTRA_BOOST] # Player goes vroom up
            else: # If booster facing down
                player.velocity = [0, -(abs(player.velocity[0]) + abs(player.velocity[1]) + self.STATIC_BOOST) * self.EXTRA_BOOST] # Player goes vroom down

    def display(self, player_pos):
        
        blit_image(self.image_frames[math.floor(self.current_frame)], relitive_object_pos(self.display_pos, self.SIZE, player_pos)) # Draws booster frame relitive to player on screen
        
        self.current_frame += self.FRAME_SPEED # Changes player frame
        if self.current_frame > len(self.image_frames): # If selected frame does not exist
            self.current_frame = 0 # Start on first frame


#--------------------Main--------------------

current_level = level2.init(player, Level, Booster, Platform, Enemy, Grass)

menu = Menu((1000, 1000))

start_button = button(1920 / 2 - 460, 1080 / 2, sprite.start_button)
settings_button = button(1920 / 2 + 120, 1080 / 2, sprite.settings_button)
reset_button = button(DISPLAY_SIZE[0] / 2 - sprite.reset_button.get_width(), DISPLAY_SIZE[1] / 2 - sprite.reset_button.get_height(), sprite.reset_button)
exit_button = button(1920 / 2 - 165, 1080 / 2 + 225, sprite.exit_button)

def main():
    running = True
    while running:
        # Get Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # If exit button pressed
                running = False # Exit loop
            elif event.type == pygame.KEYDOWN: # Checks for key pressed key
                if event.key == pygame.K_ESCAPE: # Checks if escape is pressed
                    menu.active = True
        
        if menu.active == True:
            if start_button.update():
                menu.active = False
                current_level = level2.init(player, Level, Booster, Platform, Enemy, Grass)
            if exit_button.update():
                exit()
        elif player.dead:
            if reset_button.update():
                current_level = level2.init(player, Level, Booster, Platform, Enemy, Grass)
        else:
            player.get_player_input()
            player.gravity()
            player.air_resistance()
            if not player.win:
                player.move()
        
            current_level.update_objects()
            current_level.bind_player()

        clock.tick(DEFAULT_TICK) #FPS Speed


def render(current_level):
    Music.start()
    win = False
    settings = False

    menu_text = font.render("Touch Grass", True, color.WHITE)
    win_text = font.render("YOU WIN!", True, color.WHITE)
    dead_text = font.render("YOU DIED!", True, color.WHITE)

    # While the main thread running
    while threading.main_thread().is_alive():
        
        player_pos = get_player_pos()
        
        # Render
        if player.win:
            surface.fill(color.GREEN1) # If win background green
        else:
            surface.fill(color.GRAY20) # Normal background
        
        if menu.active == True:
            menu.display()
            if start_button.active and exit_button.active == True:
                surface.blit(menu_text, (1920 / 2 - 300, 250))
                surface.blit(sprite.cloud, (100, 100))
                button.display(start_button)
                button.display(settings_button)
                button.display(exit_button)
        elif player.dead == True:
            current_level.display(player_pos)
            current_level.display_objects(player_pos)
            player.display()
            surface.fill(color.RED2) # If dead background red
            surface.blit(dead_text, (1920 / 2 - 250, 200))
            button.display(reset_button)
        elif player.win == True:
            current_level.display(player_pos)
            current_level.display_objects(player_pos)
            player.display()
            surface.blit(win_text, (1920 / 2 - 250, 200))
        else:
            current_level.display(player_pos)
            current_level.display_objects(player_pos)
            player.display()

        pygame.display.flip()
        clock.tick(DEFAULT_FPS) #FPS Speed

# Create a thread for rendering
thread = threading.Thread(target=render, args=(current_level,))
thread.start()

# Start main code
main()
