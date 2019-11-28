import pygame as pygame
import random
import math

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

pygame.init()

class Creature(pygame.sprite.Sprite):
    def __init__(self):
        super(Creature, self).__init__()
        self.max_size = 100
        self.width = 25
        self.height = 25
        self.surf = pygame.Surface((self.width, self.height))
        self.surf.fill((0, 0, 0))
        # I'm not gonna lie, this code is questionable
        self.rect = self.surf.get_rect(
                center=((SCREEN_WIDTH-self.surf.get_width())/2, (SCREEN_HEIGHT-self.surf.get_height())/2))

        self.acc_increment = .33
        self.acc_max = 1.0
        self.vel_max = 5.0

        self.acc_vert = 0
        self.acc_hor = 0
        self.vel_vert = 0
        self.vel_hor = 0
    
    def grow(self, growth_increment = 10):
        if (self.width < self.max_size) & (self.height < self.max_size):
            self.width = min(self.width + growth_increment, self.max_size)
            self.height = min(self.height + growth_increment, self.max_size)
            self.surf = pygame.Surface((self.width, self.height))
            self.surf.fill((0,0,0))
            self.rect = self.surf.get_rect(
                center=(self.rect[0] + self.width/2, self.rect[1] + self.height/2))
            

    # returns new speed, 
    def handle_max_speed(self, metric, max, increment):
        to_return = metric
        if abs(metric) > max:
            if metric > 0:
                to_return = to_return - increment
            else:
                to_return = to_return + increment
        # if abs(metric) > max:
        #     to_return = 0
        return to_return

    def update_position(self):
        self.vel_vert = self.vel_vert + self.acc_vert
        self.vel_hor = self.vel_hor + self.acc_hor
        self.acc_vert = self.acc_vert + random.uniform(-1 * self.acc_increment, self.acc_increment)
        self.acc_hor = self.acc_hor + random.uniform(-1 * self.acc_increment, self.acc_increment)

        # handling max acceleration or velocity
        self.vel_vert = self.handle_max_speed(self.vel_vert, self.vel_max, abs(self.acc_vert))
        self.vel_hor = self.handle_max_speed(self.vel_hor, self.vel_max, abs(self.acc_hor))
        self.acc_vert = self.handle_max_speed(self.acc_vert, self.acc_max, abs(self.acc_increment))
        self.acc_hor = self.handle_max_speed(self.acc_hor, self.acc_max, abs(self.acc_increment))

        # hor, vert
        self.rect.move_ip(int(self.vel_hor), int(self.vel_vert))
        # Keep creature on the screen
        if self.rect.left < 0:
            self.rect.left = 0
            self.acc_hor = self.acc_hor * -1
            self.vel_hor = 1
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
            self.acc_hor = self.acc_hor * -1
            self.vel_hor = -1
        if self.rect.top <= 0:
            self.rect.top = 0
            self.acc_vert = self.acc_vert * -1
            self.vel_vert = 1
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.acc_vert = self.acc_vert * -1
            self.vel_vert = -1

class Food(pygame.sprite.Sprite):
    def __init__(self):
        super(Food, self).__init__()
        self.surf = pygame.Surface((10, 10))
        self.surf.fill((65, 218, 101))
        self.rect = self.surf.get_rect(
            center=(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT))
        )

# Define constants
SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 800
frame_rate = 60

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

clock = pygame.time.Clock()

# Creating groups
# all_sprites is used for rendering
all_sprites = pygame.sprite.Group()
creatures = pygame.sprite.Group()
foods = pygame.sprite.Group()

# Create our 'Creature'
creature1 = Creature()
all_sprites.add(creature1)
creatures.add(creature1)

for i in range(0,10):
    food = Food()
    all_sprites.add(food)
    foods.add(food)

    print(food.rect[0], food.rect[1])

running = True
# Our main loop
while running:
    # Look at every event in the queue
    for event in pygame.event.get():
        # Did the user hit a key?
        if event.type == KEYDOWN:
            # Was it the Escape key? If so, stop the loop
            if event.key == K_ESCAPE:
                running = False
        # Did the user click the window close button? If so, stop the loop
        elif event.type == QUIT:
            running = False

    # Fill the screen with black
    screen.fill((255, 255, 255))

    # Check for collisions
    collider = pygame.sprite.spritecollideany(creature1, foods)
    if collider:
        creature1.grow()
        collider.kill()
    #Move sprites
    for entity in creatures:
        entity.update_position()
    # Draw all our sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # Ensure program maintains a constant frame rate
    clock.tick(frame_rate)

    # Flip everything to the display
    pygame.display.flip()
