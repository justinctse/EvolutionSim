import pygame
import random
import math
import numpy as np
from classes.Creature import Creature 
from classes.SearchingHerbivore import SearchingHerbivore
from classes.BasicHerbivore import BasicHerbivore
from classes.Food import Food

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

# Define constants
SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 800
frame_rate = 60
food_amount = 100
num_basic_herbivores = 1
num_searching_herbivores = 5

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Creating groups
# all_sprites is used for rendering
all_sprites = pygame.sprite.Group()
creatures = pygame.sprite.Group()
foods = pygame.sprite.Group()

# Create objects 
for i in range(0, num_basic_herbivores):
    creature = BasicHerbivore(SCREEN_WIDTH, SCREEN_HEIGHT)
    all_sprites.add(creature)
    creatures.add(creature)

for i in range(0, num_searching_herbivores):
    creature = SearchingHerbivore(SCREEN_WIDTH, SCREEN_HEIGHT)
    all_sprites.add(creature)
    creatures.add(creature)

for i in range(0,food_amount):
    food = Food(SCREEN_WIDTH, SCREEN_HEIGHT)
    all_sprites.add(food)
    foods.add(food) 

running = True
while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False

    # Fill the screen with white
    screen.fill((255, 255, 255))
    
    # Get coordinates of food so that Creatures can track
    food_coordinates = []
    for food in foods:
        food_coordinates.append((food.rect[0], food.rect[1]))

    for entity in creatures:
        # Check for collisions
        collider = pygame.sprite.spritecollideany(entity, foods)
        if collider:
            entity.grow(collider.value)
            collider.kill()
        # Move sprites
        if entity.type == 'basic':
            entity.update_position()
        if entity.type == 'searcher':
            entity.update_position(food_coordinates)

    # Draw all our sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # Ensure program maintains a constant frame rate
    clock.tick(frame_rate)

    # Flip everything to the display
    pygame.display.flip()
