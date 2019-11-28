import pygame 
import random 
class Food(pygame.sprite.Sprite):
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT):
        super(Food, self).__init__()
        self.size = random.randint(5,15)
        self.value = int(self.size/2)
        self.surf = pygame.Surface((self.size, self.size))
        self.surf.fill((65, 218, 101))
        self.rect = self.surf.get_rect(
            center=(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT))
        )