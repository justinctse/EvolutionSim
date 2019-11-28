import pygame 
import random 
class Creature(pygame.sprite.Sprite):
    def __init__(
        self, 
        SCREEN_WIDTH, 
        SCREEN_HEIGHT,
        max_size=100,
        width=25,
        height=25,
        acc_increment=.33,
        acc_max=1.0,
        vel_max=5.0,
        acc_vert=0,
        acc_hor=0,
        vel_vert=0,
        vel_hor=0
    ):
        super(Creature, self).__init__()
        self.SCREEN_WIDTH = SCREEN_WIDTH 
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.max_size = max_size
        self.width = width
        self.height = height
        self.surf = pygame.Surface((self.width, self.height))
        self.surf.fill((0, 0, 0))
        vertical_offset = random.randint(-1 * 50, 50)
        horizontal_offset = random.randint(-1 * 50, 50)
        self.rect = self.surf.get_rect(
                center=((SCREEN_WIDTH-self.surf.get_width())/2 + horizontal_offset, (SCREEN_HEIGHT-self.surf.get_height())/2 + vertical_offset))

        self.acc_increment = acc_increment
        self.acc_max = acc_max
        self.vel_max = vel_max

        self.acc_vert = acc_vert
        self.acc_hor = acc_hor
        self.vel_vert = vel_vert
        self.vel_hor = vel_hor
    
    # returns new speed, 
    def handle_max_speed(self, metric, max, increment):
        to_return = metric
        if abs(metric) > max:
            if metric > 0:
                to_return = to_return - increment
            else:
                to_return = to_return + increment
        return to_return

    def grow(self, growth_increment = 5):
        if (self.width < self.max_size) & (self.height < self.max_size):
            self.width = min(self.width + growth_increment, self.max_size)
            self.height = min(self.height + growth_increment, self.max_size)
            self.surf = pygame.Surface((self.width, self.height))
            self.surf.fill((0,0,0))
            # I'm not gonna lie this code is questionable
            self.rect = self.surf.get_rect(
                center=(self.rect[0] + self.width/2, self.rect[1] + self.height/2))