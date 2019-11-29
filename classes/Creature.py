import pygame 
import random 
from helper_functions.class_functions import get_coordinates_from_angle
class Creature(pygame.sprite.Sprite):
    def __init__(
        self, 
        SCREEN_WIDTH, 
        SCREEN_HEIGHT,
        name,
        color = (0,0,0),
        max_size=100,
        width=15,
        height=15,
        jerk=.02,
        acc_max=.25,
        vel_max=2.5,
        acc_vert=0,
        acc_hor=0,
        vel_vert=0,
        vel_hor=0,
        num_offspring_divisor=20 # Default that every 20 in size results in 1 offspring
    ):
        super(Creature, self).__init__()
        self.name = name
        self.SCREEN_WIDTH = SCREEN_WIDTH 
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.max_size = max_size
        self.birth_width = width
        self.birth_height = height
        self.width = width
        self.height = height
        self.hunger = int(self.max_size/4 + self.birth_width) # You need to eat 1/3 of max_size + initial size to survive
 
        self.surf = pygame.Surface((self.width, self.height))
        self.color = color
        self.alpha = 200
        self.surf.fill(self.color)
        self.surf.set_alpha(self.alpha)

        # Spawn within 150 pixels of center
        theta = random.randint(0,360)
        distance_from_center = random.randint(0, 150)
        x_offset, y_offset = get_coordinates_from_angle(theta, distance_from_center)
        self.rect = self.surf.get_rect(
                center=((SCREEN_WIDTH-self.surf.get_width())/2 + x_offset, (SCREEN_HEIGHT-self.surf.get_height())/2 + y_offset))

        self.jerk = jerk
        self.acc_max = acc_max
        self.vel_max = vel_max

        self.acc_vert = acc_vert
        self.acc_hor = acc_hor
        self.vel_vert = vel_vert
        self.vel_hor = vel_hor

        self.num_offspring_divisor = num_offspring_divisor
    
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