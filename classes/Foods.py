import pygame 
import random 
from config import *
from helper_functions.class_functions import get_distance
# TODO: Consolidate everything into single class
# Formerly basic_food
class Tomato(pygame.sprite.Sprite):
    def __init__(self):
        super(Tomato, self).__init__()
        self.type = 'basic_food'
        self.size = random.randint(12,20)
        self.value = int(self.size/3)
        self.surf = pygame.Surface((self.size, self.size))
        self.avatar = pygame.transform.smoothscale(img_tomato, (self.size, self.size))
        x, y = 0, 0
        while True:
            x, y = random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)
            # If too close to the center reroll location
            if get_distance((x,y), (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)) < 200:
                x, y = random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)
            else:
                break
        self.rect = self.surf.get_rect(
                center=(x, y)
            )
        #self.surf.fill((65, 218, 101))
        self.surf.fill((255,116,136))

# Formerly super food
class Pumpkin(pygame.sprite.Sprite):
    def __init__(self):
        super(Pumpkin, self).__init__()
        self.type = 'super_food'
        self.size = random.randint(25,35)
        self.value = int(self.size/2)
        self.surf = pygame.Surface((self.size, self.size))
        self.surf.fill((199, 89, 255))
        self.avatar = pygame.transform.smoothscale(img_pumpkin, (self.size, self.size))
        x, y = 0, 0
        while True:
            x, y = random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)
            # If too close to the center reroll location
            if get_distance((x,y), (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)) < 200:
                x, y = random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)
            else:
                break
        self.rect = self.surf.get_rect(
                center=(x, y)
            )