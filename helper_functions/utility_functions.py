import pygame 
import pygame.freetype
from pygame.locals import (
    RLEACCEL,
    K_SPACE,
    K_ESCAPE,
    K_LEFT,
    K_RIGHT,
    KEYDOWN,
    QUIT,
)
def pause(SCREEN_WIDTH, SCREEN_HEIGHT, screen):
    GAME_FONT = pygame.freetype.SysFont("Times New Roman", 72)
    # You can use `render` and then blit the text surface ...
    text_surface, rect = GAME_FONT.render("Paused", (0, 0, 0))
    screen.blit(text_surface, (int((SCREEN_WIDTH - rect[2])/2), int((SCREEN_HEIGHT - rect[3])/2)))
    pygame.display.flip()

    running = True
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
    return running

def adjust_frame_rate(frame_rate, key):
    # move this to main game
    GAME_FONT = pygame.freetype.SysFont("Times New Roman", 72)
    if key == K_LEFT:
        to_return = frame_rate - 5
    elif key == K_RIGHT:
        to_return = frame_rate + 5
    print("Framerate: " + str(to_return))
    return max(1, to_return)