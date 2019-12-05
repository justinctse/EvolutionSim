import pygame
import math
import numpy as np 
import random
from config import *
from classes.Creature import Creature
from helper_functions.class_functions import get_distance
# This is a creature eats other creatures
# It should stop once it has had enough food
class Predator(Creature):
    def __init__(
        self,
        name,
        color = (0,0,0),
        max_size=100,
        width=25,
        height=25,
        defense=0,
        jerk=.05,
        acc_max=.25,
        vel_max=2.5,
        acc_vert=0,
        acc_hor=0,
        vel_vert=0,
        vel_hor=0,
        num_offspring_divisor=20,
        generation=None,
        lineage=None,
        search_distance = 100,
        attack=0
    ):
        Creature.__init__(
            self,
            name,
            color=color,
            max_size=max_size,
            width=width,
            height=height,
            defense=defense,
            jerk=jerk,
            acc_max=acc_max,
            vel_max=vel_max,
            acc_vert=acc_vert,
            acc_hor=acc_hor,
            vel_vert=vel_vert,
            vel_hor=vel_hor,
            num_offspring_divisor=num_offspring_divisor,
            generation=generation,
            lineage=lineage
        )
        self.type = 'predator'
        self.search_distance = search_distance
        self.avatar = pygame.transform.smoothscale(img_hungry_predator, (self.width, self.height))
        self.attack = attack

        # Overwriting code in the base class
        # Spawn away from the center
        x, y = 0, 0
        while True:
            x, y = random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)
            # If too close to the center reroll location
            if get_distance((x,y), (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)) < 400:
                x, y = random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)
            else:
                break
        self.rect = self.surf.get_rect(
                center=(x, y)
            )

    # Get the closest edible creature
    def get_closest_food(self, creatures):
        if len(creatures) == 0:
            return None
        closest_point = None
        min_distance = 99999
        for creature in creatures:
            if creature.name == self.name:
                continue
            coordinates = (creature.rect[0], creature.rect[1])
            distance = get_distance((self.rect[0], self.rect[1]), coordinates)
            if (self.width + self.attack) > (creature.width + creature.defense): # Check if they are edible
                if distance < min_distance:
                    closest_point = coordinates
                    min_distance = distance 
        return closest_point
    
    # Don't move if full
    def update_position(self, creatures):
        closest_point = self.get_closest_food(creatures)
        if (self.width >= self.max_size) & (self.height >= self.max_size):
            self.acc_vert = 0
            self.acc_hor = 0
            self.vel_vert = 0
            self.vel_hor = 0
        elif closest_point is None:
            # random movement
            self.acc_vert = self.acc_vert + random.uniform(-1 * self.jerk, self.jerk)
            self.acc_hor = self.acc_hor + random.uniform(-1 * self.jerk, self.jerk)
            self.vel_vert = self.vel_vert + self.acc_vert
            self.vel_hor = self.vel_hor + self.acc_hor
        elif get_distance((self.rect[0], self.rect[1]), closest_point) < self.search_distance:
            # get right direction
            self.acc_vert = self.acc_vert + self.jerk * np.sign(closest_point[1] - self.rect[1])
            self.acc_hor = self.acc_hor + self.jerk * np.sign(closest_point[0] - self.rect[0])
            self.vel_vert = self.vel_vert + self.acc_vert
            self.vel_hor = self.vel_hor + self.acc_hor
        else:
            # random movement
            self.acc_vert = self.acc_vert + random.uniform(-1 * self.jerk, self.jerk)
            self.acc_hor = self.acc_hor + random.uniform(-1 * self.jerk, self.jerk)
            self.vel_vert = self.vel_vert + self.acc_vert
            self.vel_hor = self.vel_hor + self.acc_hor
        
        # handling max acceleration or velocity
        self.vel_vert = self.handle_max_speed(self.vel_vert, self.vel_max, abs(self.acc_vert))
        self.vel_hor = self.handle_max_speed(self.vel_hor, self.vel_max, abs(self.acc_hor))
        self.acc_vert = self.handle_max_speed(self.acc_vert, self.acc_max, abs(self.jerk))
        self.acc_hor = self.handle_max_speed(self.acc_hor, self.acc_max, abs(self.jerk))

        # hor, vert
        self.rect.move_ip(int(self.vel_hor), int(self.vel_vert))
        # Keep creature on the screen
        if self.rect.left < 0:
            self.rect.left = 0
            self.acc_hor = self.acc_hor * -1
            self.vel_hor = 1
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
            self.acc_hor = self.acc_hor * -1
            self.vel_hor = -1
        if self.rect.top <= 0:
            self.rect.top = 0
            self.acc_vert = self.acc_vert * -1
            self.vel_vert = 1
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.acc_vert = self.acc_vert * -1
            self.vel_vert = -1

    # Overriding the original function
    def grow(self, growth_increment = 5):
        if (self.width < self.max_size) & (self.height < self.max_size):
            # Grow the sprite
            self.width = min(self.width + growth_increment, self.max_size)
            self.height = min(self.height + growth_increment, self.max_size)
            self.surf = pygame.Surface((self.width, self.height))
            self.surf.fill(self.color)
            self.surf.set_alpha(self.alpha)
            # I'm not gonna lie this code is questionable
            self.rect = self.surf.get_rect(
                center=(self.rect[0] + self.width/2, self.rect[1] + self.height/2))
            
            # Update parameters
            
            # Update max speeds
            # 50% speed hit at 200
            self.speed_inhibitor = max(.5, 1 - self.width/(2*200))
            self.jerk = self.birth_jerk * self.speed_inhibitor
            self.acc_max = self.birth_acc_max * self.speed_inhibitor
            self.vel_max = self.birth_vel_max * self.speed_inhibitor

            self.avatar = pygame.transform.smoothscale(img_hungry_predator, (self.width, self.height))

            # Update image size
            # if (self.width >= self.max_size) & (self.height >= self.max_size):
            #     self.avatar = pygame.transform.smoothscale(img_happy, (self.width, self.height))
            # elif (self.width >= self.max_size * .75) & (self.height >= self.max_size * .75):
            #     self.avatar = pygame.transform.smoothscale(img_neutral, (self.width, self.height))
            # else:
            #     self.avatar = pygame.transform.smoothscale(self.base_avatar, (self.width, self.height))