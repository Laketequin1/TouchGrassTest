#--------------------Imports--------------------

import pygame
pygame.init()

from src import color # Imports lots of colors as RGB

#--------------------Variables--------------------

IMAGE_FOLDER = "images/" #The folder that holds all the image files
DISPLAY_SIZE = (1920, 1080) # Screen size
DEFAULT_TICK = 120 # Game FPS

clock = pygame.time.Clock() # Game tick handling

surface = pygame.display.set_mode(DISPLAY_SIZE, pygame.NOFRAME) # Create screen 

class sprite:
    player = pygame.image.load(IMAGE_FOLDER+"player.png").convert() #Loads player (convert to be more efficient as non transparent)
    tree = pygame.image.load(IMAGE_FOLDER+"tree.png") #Loads tree image
    ground = pygame.image.load(IMAGE_FOLDER+"ground.png").convert() #Loads ground (convert to be more efficient as non transparent)
    roof = pygame.image.load(IMAGE_FOLDER+"roof.png").convert() #Loads ground (convert to be more efficient as non transparent)

#--------------------Classes--------------------
    
