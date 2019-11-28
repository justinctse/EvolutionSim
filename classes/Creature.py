import pygame 
import random 
class Creature(pygame.sprite.Sprite):
    def __init__(
        self, 
        SCREEN_WIDTH, 
        SCREEN_HEIGHT,
        max_size=100,
        width=15,
        height=15,
        jerk=.05,
        acc_max=.25,
        vel_max=2.5,
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
        self.hunger = int(self.max_size/3)

        self.surf = pygame.Surface((self.width, self.height))
        self.color = (0,0,0)
        self.alpha = 200
        self.surf.fill(self.color)
        self.surf.set_alpha(self.alpha)

        vertical_offset = random.randint(-1 * 50, 50)
        horizontal_offset = random.randint(-1 * 50, 50)
        self.rect = self.surf.get_rect(
                center=((SCREEN_WIDTH-self.surf.get_width())/2 + horizontal_offset, (SCREEN_HEIGHT-self.surf.get_height())/2 + vertical_offset))

        self.jerk = jerk
        self.acc_max = acc_max
        self.vel_max = vel_max

        self.acc_vert = acc_vert
        self.acc_hor = acc_hor
        self.vel_vert = vel_vert
        self.vel_hor = vel_hor
    
    # metric is speed
    # if we are over the max, then cap it at the max
    # increment is no longer needed
    def handle_max_speed(self, metric, max, increment):
        to_return = metric
        if abs(metric) > max:
            if metric > 0:
                to_return = max
            else:
                to_return = -1 * max
        return to_return

    def grow(self, growth_increment = 5):
        if (self.width < self.max_size) & (self.height < self.max_size):
            self.width = min(self.width + growth_increment, self.max_size)
            self.height = min(self.height + growth_increment, self.max_size)
            self.surf = pygame.Surface((self.width, self.height))
            self.surf.fill(self.color)
            self.surf.set_alpha(self.alpha)
            # I'm not gonna lie this code is questionable
            self.rect = self.surf.get_rect(
                center=(self.rect[0] + self.width/2, self.rect[1] + self.height/2))