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
num_basic_searching_herbivores = 20
num_fast_searching_herbivores = 5

bg = pygame.image.load("assets/background.png")

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Creating groups
# all_sprites is used for rendering
all_sprites = pygame.sprite.Group()
creatures = pygame.sprite.Group()
foods = pygame.sprite.Group()

# Layout base values for Creature parameters
base_max_size = 100
base_size = 15
base_jerk = .02
base_acc_max = .25
base_vel_max = 2.5
base_search_distance_multiplier = 10
base_num_offspring_divisor = 20

# Create objects 
for i in range(0, num_basic_searching_herbivores):
    size = int(base_size*random.uniform(.8,1.2))
    creature = SearchingHerbivore(
        SCREEN_WIDTH, 
        SCREEN_HEIGHT, 
        "searching_herbivore_" + str(i),
        max_size=int(base_max_size*random.uniform(.8,1.2)),
        width=size,
        height=size,
        jerk=base_jerk*random.uniform(.8,1.2),
        acc_max=base_acc_max*random.uniform(.8,1.2),
        vel_max=base_vel_max*random.uniform(.8,1.2),
        num_offspring_divisor=base_num_offspring_divisor*random.uniform(.8,1.2),
        search_distance_multiplier=base_search_distance_multiplier*random.uniform(.8,1.2)
    )
    all_sprites.add(creature)
    creatures.add(creature)
for i in range(0, num_fast_searching_herbivores):
    creature = SearchingHerbivore(
        SCREEN_WIDTH, 
        SCREEN_HEIGHT, 
        "searching_herbivore_" + str(i),
        color = (0,0,255),
        max_size=base_max_size,
        width=base_size,
        height=base_size,
        jerk=base_jerk * 1.5,
        acc_max=base_acc_max * 1.5,
        vel_max=base_vel_max * 1.5,
        num_offspring_divisor=base_num_offspring_divisor*random.uniform(.8,1.2),
        search_distance_multiplier=base_search_distance_multiplier
    )
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
    
    # Seed the new round
    if round_counter > 1:
        for creature in creatures:
            for i in range(0, max(1,int(creature.width/creature.num_offspring_divisor))):
                size = int(creature.birth_width * random.uniform(.8,1.2))
                offspring = SearchingHerbivore(
                    SCREEN_WIDTH, 
                    SCREEN_HEIGHT, 
                    creature.name,
                    color=creature.color,
                    max_size=int(creature.max_size * random.uniform(.8,1.2)),
                    width=size,
                    height=size,
                    jerk=creature.jerk * random.uniform(.8,1.2),
                    acc_max=creature.acc_max * random.uniform(.8,1.2),
                    vel_max=creature.vel_max * random.uniform(.8,1.2),
                    search_distance_multiplier=creature.search_distance_multiplier * random.uniform(.8,1.2)
                )
                all_sprites.add(offspring)
                creatures.add(offspring)
            creature.kill()

        for i in range(0,basic_food_amount):
            food = BasicFood(SCREEN_WIDTH, SCREEN_HEIGHT)
            all_sprites.add(food)
            foods.add(food) 
        for i in range(0, super_food_amount):
            food = SuperFood(SCREEN_WIDTH, SCREEN_HEIGHT)
            all_sprites.add(food)
            foods.add(food)

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
        #screen.fill((255, 255, 255))
        screen.blit(bg, (0, 0))

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
            # Dispose of creatures that did not eat enough
            for entity in creatures:
                # Make sure that death stuff is activated (color red)
                if entity.type == 'searcher':
                    entity.update_position(foods)
                screen.blit(entity.surf, entity.rect)
                if entity.width < entity.hunger:
                    entity.kill()
            simulation_running, round_running = pause_time(2)
            round_running = False
