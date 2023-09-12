import pygame
import random

# -- Global Constants

# -- Colours
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (150,50,255)
YELLOW = (255,255,0)
GREEN = (0, 20, 15)
RED = (100, 0 ,0)

# a = True

## -- Define the class Obstacle which is a sprite 
class Obstacle(pygame.sprite.Sprite):
    # Define the cnostructor for Obstacle
    def __init__(self, color, width, height, speed):
        # Call the sprtite constructor
        super().__init__()
        # Create a sprite and fill it with colour
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        # Set the psoition of the sprite 
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, 1000)
        self.rect.y = random.randrange(-300,0)
        # Set speed of the sprite
        self.speed = speed
    # End Proceure

    # Class update function - runs for each pass through the game loop
    # def update(self):
    #     self.rect.y = self.rect.y + self.speed
    #     if self.rect.y >= 1000:
    #         # Spawn a Obstacleflake randomly on x-axis and on 0 on y-axis
    #         self.rect.x = random.randrange(0, 1000)
    #         self.rect.y = 0 + self.speed   

# End class

## -- Define the class Obstacle which is a sprite 
class Player(pygame.sprite.Sprite):
    # Define the cnostructor for Obstacle
    def __init__(self, color, width, height):
        # Call the sprtite constructor
        super().__init__()
        # Create a sprite and fill it with colour
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        # Set the psoition of the sprite 
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(400, 800)
        self.rect.y = 650
        # Set speed of the sprite
        self.speed = 0
        # self.lives = 5 
        # self.bullet_count = 50
        # self.score_count = 0
    # End Proceure

    def get_x(self):
        return self.rect.x

    # Score
    # def hitTarget(self):
    #     self.score_count = self.score_count + 1

    # Class update function - runs for each pass through the game loop
    # def player_set_speed(self):
    #     self.rect.x = self.rect.x + self.speed
        # if self.rect.y >= 1000:
            # Spawn a Obstacleflake randomly on x-axis and on 0 on y-axis
            # self.rect.x = random.randrange(0, 1200)
            # self.rect.y = 0 + self.speed   

# End class


# class Bullet(pygame.sprite.Sprite):
#     # Define the constructor for Obstacle
#     def __init__(self, color, width, height):
#         # Call the sprite constructor
#         super().__init__()
#         # Create a sprite and fill it with colour
#         self.image = pygame.Surface([width, height])
#         self.image.fill(color)
#         # Set the position of the sprite
#         self.rect = self.image.get_rect()
#         self.rect.x = player.get_x() + 10
#         self.rect.y = 775 - 20
#     def update(self):
#         # Move bullet up 
#         self.rect.y = self.rect.y - 5
#         # -- bullet hitting the Obstacle
#         if pygame.sprite.groupcollide(bullet_list, Obstacle_group, True, True, collided = None):
#             player.hitTarget()
        

## -- Initialise PyGame
pygame.init()

# --- set font for the scoreboard
font = pygame.font.Font('freesansbold.ttf', 32)

# -- Blank Screen
size = (1000, 800)
screen = pygame.display.set_mode(size)

# -- Title of new window/screen
pygame.display.set_caption("Obstacle")

# -- Exit game flag set to false
done = False


# Create a list of the Obstacle blocks
Obstacle_group = pygame.sprite.Group()
# Create a list of all sprites
all_sprites_group = pygame.sprite.Group()


# -- Manages how fast screen refreshes
clock = pygame.time.Clock()

## -- Create the Obstacles
num_of_Obstacles = 20
for x in range(num_of_Obstacles):
    my_Obstacle = Obstacle(WHITE, 20, 5, 5)
    Obstacle_group.add(my_Obstacle)
    all_sprites_group.add(my_Obstacle)

## -- create a player
player = Player(YELLOW, 30, 30)
all_sprites_group.add(player)

# Create a list of all bullets
bullet_list = pygame.sprite.Group()

def fire():
    ## -- check if u still have bullets
    if player.bullet_count == 0:
        print("OUT OF BULLETS!!!")
    else:
        mybullet = Bullet(RED,7, 14)
        all_sprites_group.add(mybullet)
        bullet_list.add(mybullet)
        player.bullet_count = player.bullet_count - 1

## -- game loop
while not done:
    if player.lives == 0:
        pygame.quit()
    else:
        # User input and controls
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    a = True
                elif event.key == pygame.K_RIGHT:
                    a = True
                elif event.key == pygame.K_UP:
                    # -- fire a bullet
                    fire()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            if player.rect.x < 0:
                player.rect.x = 0
            else:
                player.rect.x = player.rect.x - 20
        if keys[pygame.K_RIGHT]:
            if player.rect.x >= 1200 - 25:
                player.rect.x = 1200 - 25
            else:
                player.rect.x = player.rect.x + 20
        
        # -- Game logic goes after this comment
        all_sprites_group.update()

        # -- player hitting the Obstacle
        player_hit_group = pygame.sprite.spritecollide(player, Obstacle_group, True)

        # -- lives scorebord working 
        for foo in player_hit_group:
            player.lives = player.lives - 1

        # -- Screen background is BLACK
        screen.fill(GREEN)

        # -- Draw here
        all_sprites_group.draw(screen)

        # -- lives 
        lives = font.render("LIVES : " + str(player.lives), True, (255, 255, 255))
        screen.blit(lives, (50, 50))

        # -- bullets
        bullets = font.render("BULLETS LEFT : " + str(player.bullet_count), True, (255, 255, 255))
        screen.blit(bullets, (50, 100))

        # -- score
        score_board = font.render("SCORE: " + str(player.score_count), True, (255, 255, 255))
        screen.blit(score_board, (50, 150))

        # -- flip display to reveal new position of objects
        pygame.display.flip()
        
        # - The clock ticks over
        clock.tick(40)
    
#End While - End of game loop
pygame.quit()

