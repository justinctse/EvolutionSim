import pygame 
import random 
from helper_functions.class_functions import get_distance
class BasicFood(pygame.sprite.Sprite):
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT):
        super(BasicFood, self).__init__()
        self.type = 'basic'
        self.size = random.randint(3,8)
        self.value = int(self.size/2)
        self.surf = pygame.Surface((self.size, self.size))
        self.surf.fill((65, 218, 101))
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
                
class SuperFood(pygame.sprite.Sprite):
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT):
        super(SuperFood, self).__init__()
        self.type = 'super'
        self.size = random.randint(4,10)
        self.value = int(self.size/1.5)
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