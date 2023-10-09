import pygame, sys
import random
import time
import math

# -- Global Constants

# -- Colours
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (150,50,255)
YELLOW = (255,255,0)
GREEN = (16, 20, 15)
RED = (100, 0 ,0)

a = False

## - define classes 
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


class Button():
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

	def update(self, SCREEN):
		if self.image is not None:
			SCREEN.blit(self.image, self.rect)
		SCREEN.blit(self.text, self.text_rect)

	def checkForInput(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True
		return False

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

# - spawn obstacles and a car
obstacle_amount = 5
for x in range(obstacle_amount):
    obstacle = Obstacle(WHITE, 20, 25, 5)
    Obstacle_group.add(obstacle)
    all_sprites_group.add(obstacle)

# -- create a player
car = Car(30, 75, 1)
car_group.add(car)
all_sprites_group.add(car)

# -- Title of new window/SCREEN
pygame.display.set_caption("Race")

#  -- BG
BG = pygame.image.load("Background.png")

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

# -- background image loading 
road = pygame.image.load("image.png").convert_alpha()
road_height = road.get_height()

# -- ca rimage loading
# car_image = pygame.image.load("carr.png").convert()

# -- define game vars
scroll = 0
tiles = math.ceil(800 / road_height) + 2

def play(): 
    done = False  
    if done == False:

        # if player.lives == 0:
        #     pygame.quit()
        # else:

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
                if car.rect.x <= 300:
                    car.rect.x = 300
                else:
                    car.rect.x = car.rect.x - 5
            if keys[pygame.K_RIGHT]:
                if car.rect.x >= 700 - 40:
                    car.rect.x = 670
                else:
                    car.rect.x = car.rect.x + 5
            
            # -- SCREEN background is GREEN
            SCREEN.fill(GREEN)

            # -- background image loading 
            road = pygame.image.load("image.png").convert_alpha()
            road_height = road.get_height()

            # -- define game vars
            scroll = 0
            tiles = math.ceil(800 / road_height) + 2    
            
            # -- Game logic goes after this comment
            all_sprites_group.update()

            # -- draw a scrolling background
            for i in range(0, tiles):
                SCREEN.blit(road, (300, i * road_height + scroll - 600))

            # -- scroll  
            scroll += 7

            # -- reset scroll
            if scroll > road_height:
                scroll = 0

            # -- car image drawing 
            # SCREEN.blit(car_image, (car.rect.x, car.rect.y))

            # -- Draw here
            all_sprites_group.draw(SCREEN)

            # -- score
            score_board = font.render("SCORE: " + str(car.score_count), True, (255, 255, 255))
            SCREEN.blit(score_board, (50, 150))

            # -- flip display to reveal new position of objects
            pygame.display.flip()
            
            # - The clock ticks over
            clock.tick(40)


while True:

    SCREEN.blit(BG, (0, 0))

    MENU_MOUSE_POS = pygame.mouse.get_pos()
    MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
    MENU_RECT = MENU_TEXT.get_rect(center=(500, 100))

    PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(500, 250), 
                        text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
    OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(500, 400), 
                        text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
    QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(500, 550), 
                        text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

    SCREEN.blit(MENU_TEXT, MENU_RECT)

    for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
        button.changeColor(MENU_MOUSE_POS)
        button.update(SCREEN)
            
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                play()
            if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                options()
            if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                pygame.quit()
                sys.exit()

    pygame.display.update()
        



#End While - End of game loop
pygame.quit()