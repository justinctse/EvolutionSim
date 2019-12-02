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
    pause_font = pygame.freetype.SysFont("Roboto", 72)
    # You can use `render` and then blit the text surface ...
    text_surface, rect = pause_font.render("Paused", (0,0,0))
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

    message = """
    Starting Generation {generation}\n
    {num_surviving} creatures survived\n
    {num_dead} creatures died
    """
    message = message.format(
        generation=round_counter+1,
        num_surviving=num_surviving,
        num_dead=num_dead
    )
    pause_font = pygame.freetype.SysFont("Roboto", 72)
    text_surface, rect = pause_font.render(message, (0,0,0))
    screen.blit(text_surface, (int((SCREEN_WIDTH - rect[2])/2), int((SCREEN_HEIGHT - rect[3])/2)))
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
    pause_font = pygame.freetype.SysFont("Times New Roman", 72)
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
