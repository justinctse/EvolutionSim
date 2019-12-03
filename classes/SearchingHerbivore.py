import pygame
import math
import numpy as np 
import random
from config import *
from classes.Creature import Creature
from helper_functions.class_functions import get_distance
# This is a creature that can detect and track food
class SearchingHerbivore(Creature):
    def __init__(
        self,
        name,
        color = (0,0,0),
        max_size=100,
        width=25,
        height=25,
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
        search_distance_multiplier = 2
    ):
        Creature.__init__(
            self,
            name,
            color=color,
            max_size=max_size,
            width=width,
            height=height,
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
        self.type = 'searcher'
        self.search_distance_multiplier = search_distance_multiplier
        self.search_distance = math.sqrt(math.pow(self.width, 2) + math.pow(self.height, 2)) * self.search_distance_multiplier  # size of the diagonal * a multiplier
    
    # Get the closest food given an iterable of foods
    def get_closest_food(self, foods):
        if len(foods) == 0:
            return None
        closest_point = None
        min_distance = 99999
        for food in foods:
            coordinates = (food.rect[0], food.rect[1])
            distance = get_distance((self.rect[0], self.rect[1]), coordinates)
            if distance < min_distance:
                closest_point = coordinates
                min_distance = distance
        return closest_point

    # TODO: Create a better death function

    def update_position(self, foods):
        closest_point = self.get_closest_food(foods)
        if closest_point is None:
            self.acc_vert = 0
            self.acc_hor = 0
            self.vel_vert = 0
            self.vel_hor = 0
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

    # Overriding the original function, I need to do this so that
    # search distance is updated
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
            self.search_distance = math.sqrt(math.pow(self.width, 2) + math.pow(self.height, 2)) * self.search_distance_multiplier
            # Update max speeds
            # 50% speed hit at 200
            self.speed_inhibitor = max(.5, 1 - self.width/(2*200))
            self.jerk = self.birth_jerk * self.speed_inhibitor
            self.acc_max = self.birth_acc_max * self.speed_inhibitor
            self.vel_max = self.birth_vel_max * self.speed_inhibitor

            # Update image size
            if (self.width >= self.max_size) & (self.height >= self.max_size):
                self.avatar = pygame.transform.smoothscale(img_happy, (self.width, self.height))
            else:
                self.avatar = pygame.transform.smoothscale(self.base_avatar, (self.width, self.height))