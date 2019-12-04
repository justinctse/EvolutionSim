import pygame
import random
import math
import numpy as np
import time
import pandas as pd
from config import *
from helper_functions.utility_functions import pause, round_transition_screen, adjust_frame_rate, get_stats
from classes.Creature import Creature 
from classes.SearchingHerbivore import SearchingHerbivore
from classes.BasicHerbivore import BasicHerbivore
from classes.Foods import Tomato, Grape, Pumpkin

#TODO: Change color based on primary stat
#TODO: Display round in corner

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

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

bg = pygame.image.load("assets/background_1600_900.png").convert_alpha()

# Creating groups
# all_sprites is used for rendering
all_sprites = pygame.sprite.Group()
creatures = pygame.sprite.Group()
foods = pygame.sprite.Group()

# Counters to name the creatures
searching_herbivore_counter = 0

# Create objects 
for i in range(0, num_basic_searching_herbivores):
    size = int(base_size*random.uniform(.8,1.2))
    creature = SearchingHerbivore(
        "searching_herbivore_" + str(searching_herbivore_counter),
        max_size=int(base_max_size*random.uniform(.8,1.2)),
        width=size,
        height=size,
        jerk=base_jerk*random.uniform(.8,1.2),
        acc_max=base_acc_max*random.uniform(.8,1.2),
        vel_max=base_vel_max*random.uniform(.8,1.2),
        num_offspring_divisor=base_num_offspring_divisor*random.uniform(.8,1.2),
        generation=1,
        lineage=[],
        search_distance=base_search_distance*random.uniform(.8,1.2)
    )
    searching_herbivore_counter += 1
    all_sprites.add(creature)
    creatures.add(creature)
# for i in range(0, num_fast_searching_herbivores):
#     creature = SearchingHerbivore(
#         "searching_herbivore_" + str(i),
#         color = (0,0,255),
#         max_size=base_max_size,
#         width=base_size,
#         height=base_size,
#         jerk=base_jerk * 1.5,
#         acc_max=base_acc_max * 1.5,
#         vel_max=base_vel_max * 1.5,
#         num_offspring_divisor=base_num_offspring_divisor*random.uniform(.8,1.2),
#         search_distance_multiplier=base_search_distance_multiplier
#     )
#     all_sprites.add(creature)
#     creatures.add(creature)

# TODO: Move randomness out of food and into the constructor
for i in range(0,num_tomato):
    food = Tomato()
    all_sprites.add(food)
    foods.add(food) 
for i in range(0, num_pumpkin):
    food = Pumpkin()
    all_sprites.add(food)
    foods.add(food)
for i in range(0, num_grape):
    food = Grape()
    all_sprites.add(food)
    foods.add(food)

round_counter = 0
simulation_running = True

logs = []

while simulation_running:
    round_counter += 1
    round_running = True
    
    if len(creatures) == 0:
        simulation_running = False
    # Seed the new round
    if round_counter > 1:
        for creature in creatures:
            # TODO: Move the num_offspring calculation to in the class
            for i in range(0, max(1,int(creature.width/creature.num_offspring_divisor))):
                size = int(creature.birth_width * random.uniform(.8,1.2))
                offspring = SearchingHerbivore(
                    "searching_herbivore_" + str(searching_herbivore_counter),
                    color=creature.color,
                    max_size=int(creature.max_size * random.uniform(.8,1.2)),
                    width=size,
                    height=size,
                    jerk=creature.birth_jerk * random.uniform(.8,1.2),
                    acc_max=creature.birth_acc_max * random.uniform(.8,1.2),
                    vel_max=creature.birth_vel_max * random.uniform(.8,1.2),
                    num_offspring_divisor=creature.num_offspring_divisor * random.uniform(.8,1.2),
                    generation=creature.generation + 1,
                    lineage = [*creature.lineage, *[creature.name]],
                    search_distance=creature.search_distance * random.uniform(.8,1.2)
                )
                print(offspring.lineage)
                print([*creature.lineage, *[creature.name]])
                searching_herbivore_counter += 1
                all_sprites.add(offspring)
                creatures.add(offspring)
            creature.kill()

        for i in range(0,num_tomato):
            food = Tomato()
            all_sprites.add(food)
            foods.add(food) 
        for i in range(0, num_pumpkin):
            food = Pumpkin()
            all_sprites.add(food)
            foods.add(food)
        for i in range(0, num_grape):
            food = Grape()
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
                    simulation_running, round_running = pause(screen)
                elif (event.key == K_LEFT) or (event.key == K_RIGHT):
                    frame_rate = adjust_frame_rate(frame_rate, event.key)

        # The background is the first thing that needs to be rendered
        # I want this after the Pause so the paused text shows on top
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
            screen.blit(entity.avatar, entity.rect)

        # Round ends if there is no time left
        if len(foods) == 0:
            # This block of code updates the state of each creature for the end of the round
            # Dispose of creatures that did not eat enough
            round_stats_dt = get_stats(creatures, round_counter)
            for entity in creatures:
                # Make sure that death stuff is activated (color red)
                entity.end_of_round_logic()
                screen.blit(entity.avatar, entity.rect)
                if entity.width < entity.hunger:
                    entity.kill()

            print(round_stats_dt)
            logs.append(round_stats_dt)

            num_surviving = len(round_stats_dt[round_stats_dt.status == 'alive'])
            num_dead = len(round_stats_dt[round_stats_dt.status == 'dead'])

            pygame.display.flip()
            simulation_running, round_running = round_transition_screen(2, screen, round_counter, num_surviving, num_dead)
            round_running = False
        
        # This is rendered last because I want it to be on top of everything else
        round_font = pygame.freetype.SysFont("Roboto", 32)
        text_surface, text_rect = round_font.render("Generation " + str(round_counter), (0,0,0))
        screen.blit(text_surface, (20,20))

        # Ensure program maintains a constant frame rate
        clock.tick(frame_rate)

        # Flip everything to the display
        pygame.display.flip()

logs_dt = pd.concat(logs)
print(logs_dt)
logs_dt.to_csv('logs/'+str(time.time())+'.csv', index=False)