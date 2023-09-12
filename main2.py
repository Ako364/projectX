import pygame
import sys
import random
import time

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
CAR_WIDTH, CAR_HEIGHT = 50, 100
ROAD_WIDTH = 400
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Create the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2D Racing Game")

class Car:
    def __init__(self):
        self.image = pygame.Surface((CAR_WIDTH, CAR_HEIGHT))
        self.image.fill(RED)
        self.x = (SCREEN_WIDTH - CAR_WIDTH) // 2
        self.y = SCREEN_HEIGHT - CAR_HEIGHT - 20
        self.rect = pygame.Rect(self.x, self.y, CAR_WIDTH, CAR_HEIGHT)

    def move_left(self):
        if self.x > 0:
            self.x -= 5

    def move_right(self):
        if self.x < SCREEN_WIDTH - CAR_WIDTH:
            self.x += 5

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

class Obstacle:
    def __init__(self):
        self.width, self.height = 50, 100
        self.x = random.randint(0, SCREEN_WIDTH - self.width)
        self.y = -self.height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self, speed_multiplier):
        self.y += 5 * speed_multiplier

    def draw(self):
        pygame.draw.rect(screen, RED, self.rect)

class Game:
    def __init__(self):
        self.car = Car()
        self.obstacles = []
        self.score = 0
        self.spawn_delay = 4.0
        self.speed_multiplier = 1.0
        self.font = pygame.font.Font(None, 36)
        self.start_time = time.time()
        self.next_spawn_time = self.start_time + self.spawn_delay

    def create_obstacle(self):
        return Obstacle()

    def display_score(self):
        score_text = self.font.render("Score: " + str(self.score), True, GREEN)
        screen.blit(score_text, (10, 10))

    def run(self):
        clock = pygame.time.Clock()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.car.move_left()
            if keys[pygame.K_RIGHT]:
                self.car.move_right()

            current_time = time.time()
            if current_time >= self.next_spawn_time:
                self.obstacles.append(self.create_obstacle())
                self.next_spawn_time = current_time + self.spawn_delay
                self.speed_multiplier += 0.1
                self.spawn_delay /= 1.2

            self.obstacles = [obstacle for obstacle in self.obstacles if obstacle.y < SCREEN_HEIGHT]

            for obstacle in self.obstacles:
                obstacle.move(self.speed_multiplier)

            car_rect = pygame.Rect(self.car.x, self.car.y, CAR_WIDTH, CAR_HEIGHT)
            for obstacle in self.obstacles:
                if car_rect.colliderect(obstacle.rect):
                    pygame.quit()
                    sys.exit()

            # Clear the screen
            screen.fill(WHITE)

            # Draw obstacles
            for obstacle in self.obstacles:
                obstacle.draw()

            # Draw the car
            self.car.draw()

            # Display score
            self.display_score()

            # Update the display
            pygame.display.flip()

            # Limit the frame rate
            clock.tick(60)

if __name__ == "__main__":
    game = Game()
    game.run()
