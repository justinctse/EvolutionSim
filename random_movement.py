import pygame
import random
import math
import numpy as np
import time
from helper_functions.utility_functions import pause, pause_time, adjust_frame_rate
from classes.Creature import Creature 
from classes.SearchingHerbivore import SearchingHerbivore
from classes.BasicHerbivore import BasicHerbivore
from classes.Foods import BasicFood, SuperFood

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    RLEACCEL,
    K_SPACE,
    K_ESCAPE,
    K_LEFT,
    K_RIGHT,
    KEYDOWN,
    QUIT,
)

# Define constants
SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 800
frame_rate = 60
basic_food_amount = 75
super_food_amount = 25
num_basic_herbivores = 0
num_searching_herbivores = 20

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
    creature = SearchingHerbivore(SCREEN_WIDTH, SCREEN_HEIGHT, "searching_herbivore_" + str(i))
    all_sprites.add(creature)
    creatures.add(creature)

for i in range(0,basic_food_amount):
    food = BasicFood(SCREEN_WIDTH, SCREEN_HEIGHT)
    all_sprites.add(food)
    foods.add(food) 

for i in range(0, super_food_amount):
    food = SuperFood(SCREEN_WIDTH, SCREEN_HEIGHT)
    all_sprites.add(food)
    foods.add(food)

round_counter = 0
simulation_running = True

while simulation_running:
    round_counter += 1
    round_running = True
    print('gothere start of new round')
    print(round_counter)
    while round_running:
        # This if statement makes sure that we can exit on quit command
        if not simulation_running: 
            round_running = False
        for event in pygame.event.get():
            if event.type == QUIT:
                simulation_running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    simulation_running = False
                elif event.key == K_SPACE:
                    simulation_running, round_running = pause(SCREEN_WIDTH, SCREEN_HEIGHT, screen)
                elif (event.key == K_LEFT) or (event.key == K_RIGHT):
                    frame_rate = adjust_frame_rate(frame_rate, event.key)

        # Fill the screen with white
        screen.fill((255, 255, 255))

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
                entity.update_position(foods)

        # Draw all our sprites
        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)

        # Ensure program maintains a constant frame rate
        clock.tick(frame_rate)

        # Flip everything to the display
        pygame.display.flip()

        # Round ends if there is no time left
        if len(foods) == 0:
            round_running = False
            simulation_running, round_running = pause_time(2)
            for entity in creatures:
                if entity.width < entity.hunger:
                    entity.kill()
