import pygame 
import pygame.freetype
import time
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
    pause_font = pygame.freetype.SysFont("Times New Roman", 72)
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

# pause game for a specified amount of seconds
def pause_time(seconds):
    start_time = time.time()
    simulation_running = True
    round_running = True
    paused = True
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

def adjust_frame_rate(frame_rate, key):
    # move this to main game
    pause_font = pygame.freetype.SysFont("Times New Roman", 72)
    if key == K_LEFT:
        to_return = frame_rate - 5
    elif key == K_RIGHT:
        to_return = frame_rate + 5
    print("Framerate: " + str(to_return))
    return max(1, to_return)