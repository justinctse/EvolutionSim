import pygame
import random
import math
import numpy as np
import time
import pandas as pd
from config import *
from helper_functions.utility_functions import pause, round_transition_screen, adjust_frame_rate, get_stats, get_stats_eaten_creature
from classes.Creature import Creature 
from classes.SearchingHerbivore import SearchingHerbivore
from classes.BasicHerbivore import BasicHerbivore
from classes.Predator import Predator
from classes.Foods import Tomato, Grape, Pumpkin

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
herbivores = pygame.sprite.Group()
predators = pygame.sprite.Group()
foods = pygame.sprite.Group()

# Counters to name the creatures
searching_herbivore_counter = 0
predator_counter = 0

# Create objects 
for i in range(0, num_basic_searching_herbivores):
    size = int(base_size*random.uniform(round_trait_decrease_percent,round_trait_increase_percent))
    creature = SearchingHerbivore(
        "searching_herbivore_" + str(searching_herbivore_counter),
        max_size=int(base_max_size*random.uniform(round_trait_decrease_percent,round_trait_increase_percent)),
        width=size,
        height=size,
        defense=max(0, base_defense*random.uniform(round_trait_decrease_percent,round_trait_increase_percent)),
        jerk=base_jerk*random.uniform(round_trait_decrease_percent,round_trait_increase_percent),
        acc_max=base_acc_max*random.uniform(round_trait_decrease_percent,round_trait_increase_percent),
        vel_max=base_vel_max*random.uniform(round_trait_decrease_percent,round_trait_increase_percent),
        num_offspring_divisor=base_num_offspring_divisor*random.uniform(round_trait_decrease_percent,round_trait_increase_percent),
        generation=1,
        lineage=[],
        search_distance=base_search_distance*random.uniform(round_trait_decrease_percent,round_trait_increase_percent),
        fear=base_fear*random.uniform(round_trait_decrease_percent,round_trait_increase_percent)
    )
    searching_herbivore_counter += 1
    all_sprites.add(creature)
    creatures.add(creature)
    herbivores.add(creature)
for i in range(0, num_predator):
    size = int(base_predator_size*random.uniform(round_trait_decrease_percent,round_trait_increase_percent))
    creature = Predator(
        "predator_" + str(predator_counter),
        max_size=int(base_predator_max_size*random.uniform(round_trait_decrease_percent,round_trait_increase_percent)),
        width=size,
        height=size,
        defense=max(0, base_predator_defense*random.uniform(round_trait_decrease_percent,round_trait_increase_percent)),
        jerk=base_predator_jerk*random.uniform(round_trait_decrease_percent,round_trait_increase_percent),
        acc_max=base_predator_acc_max*random.uniform(round_trait_decrease_percent,round_trait_increase_percent),
        vel_max=base_predator_vel_max*random.uniform(round_trait_decrease_percent,round_trait_increase_percent),
        num_offspring_divisor=base_predator_num_offspring_divisor*random.uniform(round_trait_decrease_percent,round_trait_increase_percent),
        generation=1,
        lineage=[],
        search_distance=base_predator_search_distance*random.uniform(round_trait_decrease_percent,round_trait_increase_percent),
        attack=max(0, base_predator_attack*random.uniform(round_trait_decrease_percent,round_trait_increase_percent))
    )
    predator_counter += 1
    all_sprites.add(creature)
    creatures.add(creature)
    predators.add(creature)

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
            if creature.type == 'searcher':
                for i in range(0, max(1,int(creature.width/creature.num_offspring_divisor))):
                    size = max(8, int(creature.birth_width * random.uniform(round_trait_decrease_percent,round_trait_increase_percent)))
                    offspring = SearchingHerbivore(
                        "searching_herbivore_" + str(searching_herbivore_counter),
                        color=creature.color,
                        max_size=int(creature.max_size * random.uniform(round_trait_decrease_percent,round_trait_increase_percent)),
                        width=size,
                        height=size,
                        defense=max(0,creature.defense * random.uniform(round_trait_decrease_percent,round_trait_increase_percent)),
                        jerk=creature.birth_jerk * random.uniform(round_trait_decrease_percent,round_trait_increase_percent),
                        acc_max=creature.birth_acc_max * random.uniform(round_trait_decrease_percent,round_trait_increase_percent),
                        vel_max=max(1,creature.birth_vel_max * random.uniform(round_trait_decrease_percent,round_trait_increase_percent)),
                        num_offspring_divisor=max(8,creature.num_offspring_divisor * random.uniform(round_trait_decrease_percent,round_trait_increase_percent)),
                        generation=creature.generation + 1,
                        lineage=[*creature.lineage, *[creature.name]],
                        search_distance=creature.search_distance * random.uniform(round_trait_decrease_percent,round_trait_increase_percent),
                        fear = creature.fear * random.uniform(round_trait_decrease_percent,round_trait_increase_percent)
                    )
                    searching_herbivore_counter += 1
                    all_sprites.add(offspring)
                    creatures.add(offspring)
                    herbivores.add(offspring)
            elif creature.type == 'predator':
                for i in range(0, max(1,int(creature.width/creature.num_offspring_divisor))):
                    size = max(8, int(creature.birth_width * random.uniform(round_trait_decrease_percent,round_trait_increase_percent)))
                    offspring = Predator(
                        "predator_" + str(predator_counter),
                        max_size=int(creature.max_size*random.uniform(round_trait_decrease_percent,round_trait_increase_percent)),
                        width=size,
                        height=size,
                        defense=max(0, creature.defense*random.uniform(round_trait_decrease_percent,round_trait_increase_percent)),
                        jerk=creature.jerk*random.uniform(round_trait_decrease_percent,round_trait_increase_percent),
                        acc_max=creature.birth_acc_max*random.uniform(round_trait_decrease_percent,round_trait_increase_percent),
                        vel_max=max(1,creature.birth_vel_max*random.uniform(round_trait_decrease_percent,round_trait_increase_percent)),
                        num_offspring_divisor=max(8,creature.num_offspring_divisor*random.uniform(round_trait_decrease_percent,round_trait_increase_percent)),
                        generation=creature.generation + 1,
                        lineage=[*creature.lineage, *[creature.name]],
                        search_distance=creature.search_distance*random.uniform(round_trait_decrease_percent,round_trait_increase_percent),
                        attack=max(0, creature.attack*random.uniform(round_trait_decrease_percent,round_trait_increase_percent))
                    )
                    predator_counter += 1
                    all_sprites.add(offspring)
                    creatures.add(offspring)
                    predators.add(offspring)
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

    num_eaten = 0 

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
            # Herbivores colliding with food
            if entity.type == 'searcher':
                food_collider = pygame.sprite.spritecollideany(entity, foods)
                if food_collider:
                    entity.grow(food_collider.value)
                    food_collider.kill()
            # Predator colliding with creature
            if entity.type == 'predator':
                # He can collide with himself
                creature_collisions = pygame.sprite.spritecollide(entity, creatures, dokill=False)
                for creature_collider in creature_collisions:
                    if (not predators_can_eat_each_other) and creature_collider.type == 'predator':
                        continue
                    if creature_collider.name != entity.name:
                        # See if entity can eat the creature
                        if (entity.width + entity.attack) > (creature_collider.width + creature_collider.defense):
                            # Only eat the other creature if hungry
                            if entity.width < entity.max_size:
                                # Logging creature who was eaten
                                logs.append(get_stats_eaten_creature(creature_collider, round_counter))
                                num_eaten += 1
                                entity.grow(int(creature_collider.width/1.25))
                                creature_collider.kill()
            # Move sprites
            if entity.type == 'searcher':
                entity.update_position(foods, predators)
            if entity.type == 'predator':
                entity.update_position(creatures)

        # Draw all our sprites
        for entity in all_sprites:
            screen.blit(entity.avatar, entity.rect)
        if len(herbivores) == 0:
            for food in foods:
                food.kill()
            for entity in all_sprites:
                screen.blit(entity.avatar, entity.rect)
            round_running = False
            pygame.display.flip()
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
            if len(round_stats_dt) > 0:
                logs.append(round_stats_dt)

                num_surviving = len(round_stats_dt[round_stats_dt.status == 'alive'])
                num_dead = len(round_stats_dt[round_stats_dt.status == 'dead'])

            pygame.display.flip()
            simulation_running, round_running = round_transition_screen(2, screen, round_counter, num_surviving, num_dead, num_eaten)
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
logs_dt = logs_dt.sort_values(by=['generation', 'type', 'status'], ascending=[True, False, False])
print(logs_dt)
logs_dt.to_csv('logs/'+str(time.time())+'.csv', index=False)