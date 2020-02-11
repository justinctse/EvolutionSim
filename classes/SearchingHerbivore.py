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
        fear = 50
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
        self.type = 'searcher'
        self.search_distance = search_distance
        self.fear = fear
    
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

    def get_closest_predator(self, predators):
        if len(predators) == 0:
            return None
        closest_point = None
        min_distance = 99999
        for predator in predators:
            # If predator is full then we don't worry about him
            if predator.width >= predator.max_size:
                continue
            # if predator can't kill you then don't worry about him
            if (predator.width + predator.attack) < (self.width + self.defense):
                continue
            coordinates = (predator.rect[0], predator.rect[1])
            distance = get_distance((self.rect[0], self.rect[1]), coordinates)
            if distance < min_distance:
                closest_point = coordinates
                min_distance = distance
        return closest_point

    def update_position(self, foods, predators):
        closest_point_food = self.get_closest_food(foods)
        closest_point_predator = self.get_closest_predator(predators)

        closest_distance_food = get_distance((self.rect[0], self.rect[1]), closest_point_food)
        try:
            closest_distance_predator = get_distance((self.rect[0], self.rect[1]), closest_point_predator)
        except:
            closest_distance_predator = 99999
        # Running from predators takes precedence over food
        if closest_point_food is None:
            self.acc_vert = 0
            self.acc_hor = 0
            self.vel_vert = 0
            self.vel_hor = 0
        elif closest_distance_predator < self.fear:
            # move away from the predator
            self.acc_vert = self.acc_vert - self.jerk * np.sign(closest_point_predator[1] - self.rect[1])
            self.acc_hor = self.acc_hor - self.jerk * np.sign(closest_point_predator[0] - self.rect[0])
            self.vel_vert = self.vel_vert - self.acc_vert
            self.vel_hor = self.vel_hor - self.acc_hor
        elif closest_distance_food < self.search_distance:
            # get right direction
            self.acc_vert = self.acc_vert + self.jerk * np.sign(closest_point_food[1] - self.rect[1])
            self.acc_hor = self.acc_hor + self.jerk * np.sign(closest_point_food[0] - self.rect[0])
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
        self.move(self.vel_hor, self.vel_vert)
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
    # search distance is updated (Note i dont update search distance anymore)
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

            # Update image size
            if (self.width >= self.max_size) & (self.height >= self.max_size):
                self.avatar = pygame.transform.smoothscale(img_happy, (self.width, self.height))
            elif (self.width >= self.max_size * .75) & (self.height >= self.max_size * .75):
                self.avatar = pygame.transform.smoothscale(img_neutral, (self.width, self.height))
            else:
                self.avatar = pygame.transform.smoothscale(self.base_avatar, (self.width, self.height))