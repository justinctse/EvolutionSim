import pygame 
import pygame.freetype
import time
import pandas as pd
from config import *
from pygame.locals import (
    RLEACCEL,
    K_SPACE,
    K_ESCAPE,
    K_LEFT,
    K_RIGHT,
    KEYDOWN,
    QUIT,
)
# Pause game until input recieved
def pause(screen):
    main_font = pygame.freetype.SysFont("Roboto", 72)
    # You can use `render` and then blit the text surface ...
    text_surface, rect = main_font.render("Paused", (0,0,0))
    screen.blit(text_surface, (int((SCREEN_WIDTH - rect[2])/2), int((SCREEN_HEIGHT - rect[3])/2)))
    pygame.display.flip()

    running = True
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == QUIT:
                paused = False
                simulation_running = False
                round_running = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    paused = False
                    simulation_running = False
                    round_running = False
                if event.key == K_SPACE:
                    # unpause
                    paused = False
                    simulation_running = True
                    round_running = True
    return simulation_running, round_running

# round transition screen for a specified amount of seconds
def round_transition_screen(seconds, screen, round_counter, num_surviving, num_dead):
    start_time = time.time()
    simulation_running = True
    round_running = True
    paused = True

    message_generation = "Starting Generation {generation}"
    message_survival = "{num_surviving} creatures survived"
    message_dead = "{num_dead} creatures died"
    
    main_font = pygame.freetype.SysFont("Roboto", 72)
    sub_font = pygame.freetype.SysFont("Roboto", 48)
    text_generation, rect_generation = main_font.render(message_generation.format(generation=round_counter+1), (0,0,0))
    text_survival, rect_survival = sub_font.render(message_survival.format(num_surviving=num_surviving), (0,0,0))
    text_dead, rect_dead = sub_font.render(message_dead.format(num_dead=num_dead), (0,0,0))

    screen.blit(text_generation, (int((SCREEN_WIDTH - rect_generation[2])/2), int((SCREEN_HEIGHT - rect_generation[3])/2) - 104))
    screen.blit(text_survival, (int((SCREEN_WIDTH - rect_survival[2])/2), int((SCREEN_HEIGHT - rect_survival[3])/2) - 12))
    screen.blit(text_dead, (int((SCREEN_WIDTH - rect_dead[2])/2), int((SCREEN_HEIGHT - rect_dead[3])/2) + 56))

    pygame.display.flip()

    while paused:

        if time.time() - start_time > seconds:
            break
        for event in pygame.event.get():
            if event.type == QUIT:
                simulation_running = False
                round_running = False
                paused = False
                break
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    simulation_running = False
                    round_running = False
                    paused = False
                    break
    return simulation_running, round_running

def adjust_frame_rate(frame_rate, key, increment = 30):
    # move this to main game
    main_font = pygame.freetype.SysFont("Times New Roman", 72)
    if key == K_LEFT:
        to_return = frame_rate - increment
    elif key == K_RIGHT:
        to_return = frame_rate + increment
    print("Framerate: " + str(to_return))
    return max(1, to_return)

# Returns a data frame of stats
# Input is a group of Creatures
def get_stats(creatures, round_counter):
    out = []
    for entity in creatures:
        attributes = entity.get_attributes()
        for key in skip_fields:
            attributes.pop(key, None)
        # Add sstatus for end of round
        if entity.width < entity.hunger:
            status = 'dead'
        else:
            status = 'alive'
        attributes['status'] = status
        attributes['round'] = round_counter
        out.append(attributes)
    return pd.DataFrame(out)
