import pygame
import random
import time
import math

# -- Global Constants

# -- Colours
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (150,50,255)
YELLOW = (255,255,0)
GREEN = (0, 20, 15)
RED = (100, 0 ,0)

a = False

## - define a class car 
class Car(pygame.sprite.Sprite):
    # - constructor 
    def __init__(self, width, height, speed):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image = pygame.image.load("car.png").convert_alpha()
        # self.image.fill(color)
        self.rect = self.image.get_rect()

        # - positions 
        self.rect.x = random.randrange(400, 650)
        self.rect.y = 550
        self.speed = speed
        self.score_count = 0 

    def get_x(self):
        return self.rect.x
    
    # def player_set_speed(self):
    #     self.rect.x = self.rect.x + self.speed

    def hitTarget(self):
        self.score_count = self.score_count + 1



class Obstacle(pygame.sprite.Sprite):
    # - constructor
    def __init__(self, color, width, height, speed):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        # - positions 
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(300, 600)
        self.rect.y = random.randrange(-300,0)

        # - speed
        self.speed = speed

    def update(self):
        self.rect.y = self.rect.y + self.speed

        # -- bullet hitting the invader
        if pygame.sprite.groupcollide(Obstacle_group, car_group, True, True, collided = None):
            car.hitTarget()

# -- Initialise PyGame
pygame.init()

# --- set font for the scoreboard
font = pygame.font.Font('freesansbold.ttf', 32)

# -- Blank Screen
size = (1000, 800)
screen = pygame.display.set_mode(size)

# Create a list of the obstacle blocks
Obstacle_group = pygame.sprite.Group()

# Create a list of the cars
car_group = pygame.sprite.Group()

# Create a list of all sprites
all_sprites_group = pygame.sprite.Group()

# -- Manages how fast screen refreshes
clock = pygame.time.Clock()

# - spawn obstacles and a car
obstacle_amount = 5
for x in range(obstacle_amount):
    obstacle = Obstacle(WHITE, 20, 25, 5)
    Obstacle_group.add(obstacle)
    all_sprites_group.add(obstacle)

# -- create a player
car = Car(50, 110, 1)
car_group.add(car)
all_sprites_group.add(car)

# -- Title of new window/screen
pygame.display.set_caption("Race")

# -- background image loading 
road = pygame.image.load("image.png").convert_alpha()
road_height = road.get_height()

# -- ca rimage loading
# car_image = pygame.image.load("carr.png").convert()

# -- define game vars
scroll = 0
tiles = math.ceil(800 / road_height) + 2

# -- Exit game flag set to false
done = False
        
while not done:

    # if player.lives == 0:
    #     pygame.quit()
    # else:

        # User input and controls
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    a = True
                elif event.key == pygame.K_RIGHT:
                    a = True
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            if car.rect.x < 330:
                car.rect.x = 330
            else:
                car.rect.x = car.rect.x - 20
        if keys[pygame.K_RIGHT]:
            if car.rect.x >= 700 - 40:
                car.rect.x = 670
            else:
                car.rect.x = car.rect.x + 20
        
        # -- Game logic goes after this comment
        all_sprites_group.update()

        # -- draw a scrolling background
        for i in range(0, tiles):
            screen.blit(road, (300, i * road_height + scroll - 400))

        # -- scroll  
        scroll += 5

        # -- reset scroll
        if scroll > road_height:
            scroll = 0

        # -- car image drawing 
        # screen.blit(car_image, (car.rect.x, car.rect.y))

        # -- Screen background is GREEN
        # screen.fill(GREEN)

        # -- Draw here
        all_sprites_group.draw(screen)

        # -- score
        score_board = font.render("SCORE: " + str(car.score_count), True, (255, 255, 255))
        screen.blit(score_board, (50, 150))

        # -- flip display to reveal new position of objects
        pygame.display.flip()
        
        # - The clock ticks over
        clock.tick(40)
    
#End While - End of game loop
pygame.quit()