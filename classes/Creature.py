import pygame 
import random 
import numpy as np
from config import *
from helper_functions.class_functions import get_coordinates_from_angle
class Creature(pygame.sprite.Sprite):
    def __init__(
        self,
        name,
        color = (0,0,0), # Deprecate
        max_size=100,
        width=15,
        height=15,
        defense=0,
        jerk=.02,
        acc_max=.25,
        vel_max=2.5,
        acc_vert=0,
        acc_hor=0,
        vel_vert=0,
        vel_hor=0,
        num_offspring_divisor=15, # Default that every x in size results in 1 offspring
        generation=None,
        lineage=[]
    ):
        super(Creature, self).__init__()
        self.name = name
        self.generation = generation
        self.lineage = lineage

        self.max_size = max_size
        self.birth_width = width
        self.birth_height = height
        self.width = width
        self.height = height
        self.defense = defense
        self.hunger = int(self.max_size/4 + self.birth_width) # You need to eat 1/3 of max_size + initial size to survive
 
        self.surf = pygame.Surface((self.width, self.height))
        self.color = color # Deprecate
        self.alpha = 200 
        self.surf.fill(self.color)
        self.surf.set_alpha(self.alpha)

        # Spawn within 150 pixels of center
        theta = random.randint(0,360)
        distance_from_center = random.randint(0, 150)
        x_offset, y_offset = get_coordinates_from_angle(theta, distance_from_center)
        self.rect = self.surf.get_rect(
                center=((SCREEN_WIDTH-self.surf.get_width())/2 + x_offset, (SCREEN_HEIGHT-self.surf.get_height())/2 + y_offset))

        self.speed_inhibitor = 0
        self.birth_jerk = jerk
        self.birth_acc_max = acc_max
        self.birth_vel_max = vel_max
        self.jerk = jerk
        self.acc_max = acc_max
        self.vel_max = vel_max

        self.acc_vert = acc_vert
        self.acc_hor = acc_hor
        self.vel_vert = vel_vert
        self.vel_hor = vel_hor

        self.num_offspring_divisor = num_offspring_divisor

        # To save memory, consider replacing this with a the global 
        self.base_avatar = img_hungry
        self.avatar = pygame.transform.smoothscale(self.base_avatar, (self.width, self.height))
    
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
            # Update max speeds
            # 50% speed hit at 200
            self.speed_inhibitor = max(.5, 1 - width/(2*200))
            self.jerk = self.birth_jerk * self.speed_inhibitor
            self.acc_max = self.birth_acc_max * self.speed_inhibitor
            self.vel_max = self.birth_vel_max * self.speed_inhibitor
            
            # Update image size
            self.avatar = pygame.transform.smoothscale(self.base_avatar, (self.width, self.height))

    def end_of_round_logic(self):
        # If they didn't eat enough, color red
        if self.width < self.hunger:
            #self.surf.fill((255,0,0))
            #self.surf.set_alpha(self.alpha)
            self.avatar = pygame.transform.smoothscale(img_dead, (self.width, self.height))

    def get_attributes(self):
        return vars(self).copy()

    # I created this move function because if velocity is < 1
    # The creature won't move, this is because move_ip requires at least a value > 1 to move
    # Another method (better but more work) is to handle all the positioning within the class
    def move(self, vel_hor, vel_vert):
            if abs(vel_hor) > 1:
                final_vel_hor = vel_hor
            else:
                if random.random() < abs(vel_hor):
                    final_vel_hor = 1 * np.sign(vel_hor) # Move 1 pixel with probability vel_hor
                else:
                    final_vel_hor = vel_hor # The guy will not move
            if abs(vel_vert) > 1:
                final_vel_vert = vel_vert
            else:
                if random.random() < abs(vel_vert):
                    final_vel_vert = 1 * np.sign(vel_vert) # Move 1 pixel with probability vel_vert
                else:
                    final_vel_vert = vel_vert # The guy will not move
            self.rect.move_ip(final_vel_hor, final_vel_vert)