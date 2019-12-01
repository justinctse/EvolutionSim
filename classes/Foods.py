import pygame 
import random 
from config import *
from helper_functions.class_functions import get_distance
class BasicFood(pygame.sprite.Sprite):
    def __init__(self):
        super(BasicFood, self).__init__()
        self.type = 'basic'
        self.size = random.randint(8,12)
        self.value = int(self.size/3)
        self.surf = pygame.Surface((self.size, self.size))
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
                
class SuperFood(pygame.sprite.Sprite):
    def __init__(self):
        super(SuperFood, self).__init__()
        self.type = 'super'
        self.size = random.randint(10,15)
        self.value = int(self.size/2)
        self.surf = pygame.Surface((self.size, self.size))
        self.surf.fill((199, 89, 255))
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