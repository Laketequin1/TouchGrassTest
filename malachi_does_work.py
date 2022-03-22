 
from cmath import rect
import pygame

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0,0,255)

IMAGE_FOLDER = "sprites/"

velocity = [0, 0]
size = (1920, 1080)
screen = pygame.display.set_mode(size)


game_over = 0
enemys = [1]
main_menu = True

SCREEN_HEIGTH = screen.get_height()
SCREEN_WIDTH = screen.get_width()

GRAVITY = 0.15
 
pygame.display.set_caption("My Game")


class sprite:
    player = pygame.image.load(IMAGE_FOLDER+"player.png")
    enemy = pygame.image.load(IMAGE_FOLDER+"enemy.png")
    grass = pygame.image.load("platforms/grass.png")
    restart_img = pygame.image.load("buttons/reset.png")
    start_img = pygame.image.load("buttons/start.png")

class box:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self):
        screen.blit(self.image, self.rect)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)

class button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
       action = False

       pos = pygame.mouse.get_pos()

       if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True
       
       if pygame.mouse.get_pressed()[0] == 0:
           self.clicked = False
                

       screen.blit(self.image, self.rect) 
       return action



class player:
  
    def __init__(self, x, y):
        self.reset(x, y)

    def update(self, game_over):
        dx = 0 
        dy = 0
        
        if game_over == 0:
            key = pygame.key.get_pressed()

            if key[pygame.K_a]:
                dx -= 10
            if key[pygame.K_d]:
                dx += 10
            if key[pygame.K_w]:
                dy -= 10
            if key[pygame.K_s]:
                dy += 10

            self.rect.x += dx
            self.rect.y += dy
            
            if pygame.sprite.spritecollide(self, enemy_group, False):
                game_over = -1
        
        collide = pygame.Rect.colliderect(self.rect, grass_platform.rect)
        
        if collide:
            player.rect_bottom = grass_platform.rect_top

        screen.blit(self.image, (self.rect.x, self.rect.y))
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)
        
        return game_over
    def reset(self, x, y):
        self.image = sprite.player
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0


class enemy(pygame.sprite.Sprite):
    def __init__(self ,x , y):
       pygame.sprite.Sprite.__init__(self) 

       self.image = sprite.enemy
       self.rect = self.image.get_rect()
       self.rect.x = x
       self.rect.y = y
       self.move_direction = 1
       self.move_counter = 0


    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1

def make_enemy():
    E1 = enemy(500, 100)
    enemy_group.add(E1)
    print(enemy_group)
    
    
running = True

P1 = player(100, SCREEN_HEIGTH - 40)

enemy_group = pygame.sprite.Group()

#buttons
restart_button = button(SCREEN_WIDTH / 2  , SCREEN_HEIGTH / 2 , sprite.restart_img)
start_button = button(SCREEN_WIDTH / 2  , SCREEN_HEIGTH / 2 , sprite.start_img)

clock = pygame.time.Clock()
 
grass_platform = box(SCREEN_WIDTH / 2  , SCREEN_HEIGTH / 2 , sprite.grass)

make_enemy()

# -------- Main Program Loop -----------
while running:
    for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                running = False 
            elif event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_ESCAPE: 
                    running = False
 
    screen.fill(BLUE)
    
    if main_menu == True:
        if start_button.draw():
            main_menu = False
    else:

        game_over = P1.update(game_over)

        if game_over == 0:
            enemy_group.update()
        if game_over == -1:
            if restart_button.draw():
                P1 = player(100, SCREEN_HEIGTH - 40)
                game_over = 0
        
        enemy_group.draw(screen)
        box.draw(grass_platform)

    pygame.display.flip()
 

    clock.tick(60)

pygame.quit()