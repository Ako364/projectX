import pygame, sys
import random
import time
import math
import random

## - Global Constants

# -- Colours
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (150,50,255)
YELLOW = (255,255,0)
GREEN = (60, 170, 60)
RED = (100, 0 ,0)

# -- Global boolean variables 
done = False
game = False

# -- define lanes
first_lane = 297
second_lane = 367
third_lane = 442
fourth_lane = 522
fifth_lane = 592
sixth_lane = 667
lanes = [first_lane, second_lane, third_lane, fourth_lane, fifth_lane, sixth_lane]


## - define classes 

# -- Car class
class Car(pygame.sprite.Sprite):
    # - constructor 
    def __init__(self, width, height, speed):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image = pygame.image.load("car.png").convert_alpha()

        # self.image.fill(color)
        self.rect = self.image.get_rect()
        self.maska = pygame.mask.from_surface(self.image)

        # - positions 
        self.rect.x = random.randrange(400, 650)
        self.rect.y = 550
        self.speed = speed
        self.score_count = 0 

    # - getter mehtods
    def get_x(self):
        return self.rect.x

    def get_y(self):
        return self.rect.y

    # - setter method 
    def set_x(self, x_co):
        self.rect.x = x_co

    # - target hitting function 
    def hitTarget(self):
        self.score_count = self.score_count + 1

# -- Enemy class 
class Enemy(pygame.sprite.Sprite):
    # - constructor 
    def __init__(self, width, height, speed):
        super().__init__()
        self.image = pygame.Surface([width, height])
        # self.image = pygame.image.load("car.png").convert_alpha()
        # self.image.fill(color)
        self.rect = self.image.get_rect()

        # - positions 
        self.rect.x = random.randrange(400, 650)
        self.rect.y = 650
        self.speed = speed
        self.score_count = 0 

    # - Getter method 
    def get_x(self):
        return self.rect.x
    
    # def player_set_speed(self):
    #     self.rect.x = self.rect.x + self.speed

    # def hitTarget(self):
    #     self.score_count = self.score_count + 1

# -- Obstacle class 
class Obstacle(pygame.sprite.Sprite):
    # - constructor
    def __init__(self, color, width, height, speed):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image = pygame.image.load("carr.png").convert_alpha()
        # self.image.fill(color)

        # - for collisions 
        self.rect = self.image.get_rect()
        self.maska = pygame.mask.from_surface(self.image)

        # - positions 
        self.rect.x = random.choice(lanes)
        self.rect.y = random.randrange(-500,-200)

        # - speed
        self.speed = speed

    # - update function 
    def update(self):
        self.rect.y = self.rect.y + self.speed

    # - getter methods
    def get_x(self):
        return self.rect.x

    def get_y(self):
        return self.rect.y

    # - setter method 
    def set_x(self, x_co):
        self.rect.x = x_co

    # - obstacle hitting a player 
    # if pygame.sprite.groupcollide(Obstacle_group, car_group, True, True, collided = None):
    #     car.hitTarget()

# -- button class
class Button():
    # - constructor 
	def __init__(self, image, pos, text_input, font, base_color, hovering_color):
		self.image = image
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		self.font = font
		self.base_color, self.hovering_color = base_color, hovering_color
		self.text_input = text_input
		self.text = self.font.render(self.text_input, True, self.base_color)
		if self.image is None:
			self.image = self.text
		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
		self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    # - updtae finction for the screen 
	def update(self, SCREEN):
		if self.image is not None:
			SCREEN.blit(self.image, self.rect)
		SCREEN.blit(self.text, self.text_rect)

    # - input check 
	def checkForInput(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True
		return False

    # - hover
	def changeColor(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			self.text = self.font.render(self.text_input, True, self.hovering_color)
		else:
			self.text = self.font.render(self.text_input, True, self.base_color)


# -- Initialise PyGame
pygame.init()

# --- set font for the scoreboard
font = pygame.font.Font('freesansbold.ttf', 32)

# -- Blank SCREEN
size = (1000, 800)
SCREEN = pygame.display.set_mode(size)

# Create a list of the obstacle blocks
Obstacle_group = pygame.sprite.Group()

# Create a list of the cars
car_group = pygame.sprite.Group()

# Create a list of all sprites
all_sprites_group = pygame.sprite.Group()

# -- Manages how fast SCREEN refreshes
clock = pygame.time.Clock()

# -- create a player
car = Car(5, 20, 1)
car_group.add(car)
all_sprites_group.add(car)

## - masks
# CAR_BOARDER = pygame.surface.Surface(car)

# -- Title of new window/SCREEN
pygame.display.set_caption("Race")

# -- for font (Returns Press-Start-2P in the desired size)
def get_font(size): 
    return pygame.font.Font("assets/font.ttf", size)

## - Road image loading 
road = pygame.image.load("image.png").convert_alpha()
road_height = road.get_height()

# -- background for the road  
background = pygame.image.load("bush2.png").convert_alpha()
background_height = background.get_height()

# -- define game vars
scroll = 0
scroll2 = 0
tiles = math.ceil(800 / road_height) + 2
tiles2 = math.ceil(800 / background_height) 

# -- setting random number udentifiers for images
x_random = random.randrange(0, 350)    
x_random2 = random.randrange(750, 1000)


## - GAME LOOP
while done == False:
    SCREEN.fill(BLACK)

    MENU_MOUSE_POS = pygame.mouse.get_pos()

    MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
    MENU_RECT = MENU_TEXT.get_rect(center=(500, 100))

    PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(500, 300), 
                        text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
    # OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(500, 400), 
    #                     text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
    QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(500, 450), 
                        text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

    SCREEN.blit(MENU_TEXT, MENU_RECT)

    for button in [PLAY_BUTTON, QUIT_BUTTON]:
        button.changeColor(MENU_MOUSE_POS)
        button.update(SCREEN)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                game = True
            if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                pygame.quit()
                sys.exit()

    if game == True:
        # User input and controls
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        #     elif event.type == pygame.KEYDOWN:
        #         if event.key == pygame.K_LEFT:
        #             a = True
        #         elif event.key == pygame.K_RIGHT:
        #             a = True
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            if car.get_x() <= 300:
                car.set_x(300)
            else:
                car.set_x(car.get_x() - 7)
        if keys[pygame.K_RIGHT]:
            if car.get_x() >= 700 - 40:
                car.set_x(670)
            else:
                car.set_x(car.get_x() + 7)
            
        # -- SCREEN background is GREEN
        SCREEN.fill(GREEN)  

        # -- creating obstacles (if there are less then three obstacles)
        if len(Obstacle_group) < 5:
            obstacle = Obstacle(WHITE, 5, 20, 8)
            Obstacle_group.add(obstacle)
            all_sprites_group.add(obstacle)

        # -- checking if the obstacle has left the visible part of the road
        if obstacle.rect.y >= 800:
            obstacle.kill()

        # -- Game logic goes after this comment
        all_sprites_group.update()

        # -- draw a scrolling background
        for i in range(0, tiles):
            SCREEN.blit(road, (300, i * road_height + scroll - 600))

        for i in range(0, 3):
            SCREEN.blit(background, (120, i * road_height + scroll2 - 210))
            
        for i in range(0, 3):
            SCREEN.blit(background, (770, i * road_height + scroll2 - 150))

        # -- scroll  
        scroll += 7
        scroll2 += 7

        # -- reset scroll
        if scroll > road_height:
            scroll = 0

        if scroll2 > road_height:
            scroll2 = 0

        # - collisions 
        # if car.maska.overlap(obstacle.maska, (car.get_x() - obstacle.get_x(), car.get_y() - obstacle.get_y())):
        #     game = False

        # - collisions 
        if pygame.sprite.spritecollide(car, Obstacle_group, False, pygame.sprite.collide_mask):
            game = False

        # -- Draw here
        all_sprites_group.draw(SCREEN)

        # -- score
        score_board = font.render("SCORE: " + str(car.score_count), True, (255, 255, 255))
        SCREEN.blit(score_board, (50, 150))

        # -- menu button option 
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        MENU_BUTTON = Button(image=pygame.image.load("assets/61180.png"), pos=(80, 70), 
                        text_input="", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        for button in [MENU_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if MENU_BUTTON.checkForInput(MENU_MOUSE_POS):
                    game = False

        # -- flip display to reveal new position of objects
        pygame.display.flip()
        
        # - The clock ticks over
        clock.tick(40)

    pygame.display.update()
        
## - End While - End of game loop
pygame.quit()