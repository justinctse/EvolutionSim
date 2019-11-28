import pygame 
import random 
class BasicFood(pygame.sprite.Sprite):
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT):
        super(BasicFood, self).__init__()
        self.type = 'basic'
        self.size = random.randint(3,8)
        self.value = int(self.size/2)
        self.surf = pygame.Surface((self.size, self.size))
        self.surf.fill((65, 218, 101))
        self.rect = self.surf.get_rect(
            center=(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT))
        )
class SuperFood(pygame.sprite.Sprite):
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT):
        super(SuperFood, self).__init__()
        self.type = 'super'
        self.size = random.randint(4,10)
        self.value = int(self.size/1.5)
        self.surf = pygame.Surface((self.size, self.size))
        self.surf.fill((199, 89, 255))
        self.rect = self.surf.get_rect(
            center=(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT))
        )