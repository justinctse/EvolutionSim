import pygame 
from pygame.locals import (
    RLEACCEL,
    K_SPACE,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)
def pause():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == QUIT:
                paused = False
                running = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    paused = False
                    running = False
                if event.key == K_SPACE:
                    # unpause
                    paused = False