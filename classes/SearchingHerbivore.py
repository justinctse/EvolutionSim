import pygame
import math
import numpy as np 
import random
from classes.Creature import Creature
# This is a creature that can detect and track food
class SearchingHerbivore(Creature):
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT):
        Creature.__init__(self, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.type = 'searcher'
        self.search_distance = math.sqrt(math.pow(self.width, 2) + math.pow(self.height, 2)) * 10  # size of the diagona * a multiplier
    
    # Get distance to the set of coordinates
    def get_distance(self, coordinates):
        x, y = coordinates[0], coordinates[1]
        self_x, self_y = self.rect[0], self.rect[1]
        return math.sqrt(math.pow(x-self_x, 2) + math.pow(y-self_y, 2))
    
    # Get the closest set of coordinates
    def get_closest_food(self, all_coordinates):
        closest_point = None
        min_distance = 99999
        for coordinates in all_coordinates:
            distance = self.get_distance(coordinates)
            if distance < min_distance:
                closest_point = coordinates
                min_distance = distance
        return closest_point

    def update_position(self, all_coordinates):
        closest_point = self.get_closest_food(all_coordinates)
        if closest_point is None:
            self.acc_vert = 0
            self.acc_hor = 0
            self.vel_vert = 0
            self.vel_hor = 0
        elif self.get_distance(closest_point) < self.search_distance:
            # get right direction
            self.acc_vert = self.acc_vert + random.uniform(0, self.acc_increment) * np.sign(closest_point[1] - self.rect[1])
            self.acc_hor = self.acc_hor + random.uniform(0, self.acc_increment) * np.sign(closest_point[0] - self.rect[0])
            self.vel_vert = self.vel_vert + self.acc_vert
            self.vel_hor = self.vel_hor + self.acc_hor
        else:
            # random movement
            self.acc_vert = self.acc_vert + random.uniform(-1 * self.acc_increment, self.acc_increment)
            self.acc_hor = self.acc_hor + random.uniform(-1 * self.acc_increment, self.acc_increment)
            self.vel_vert = self.vel_vert + self.acc_vert
            self.vel_hor = self.vel_hor + self.acc_hor

        # handling max acceleration or velocity
        self.vel_vert = self.handle_max_speed(self.vel_vert, self.vel_max, abs(self.acc_vert))
        self.vel_hor = self.handle_max_speed(self.vel_hor, self.vel_max, abs(self.acc_hor))
        self.acc_vert = self.handle_max_speed(self.acc_vert, self.acc_max, abs(self.acc_increment))
        self.acc_hor = self.handle_max_speed(self.acc_hor, self.acc_max, abs(self.acc_increment))

        # hor, vert
        self.rect.move_ip(int(self.vel_hor), int(self.vel_vert))
        # Keep creature on the screen
        if self.rect.left < 0:
            self.rect.left = 0
            self.acc_hor = self.acc_hor * -1
            self.vel_hor = 1
        if self.rect.right > self.SCREEN_WIDTH:
            self.rect.right = self.SCREEN_WIDTH
            self.acc_hor = self.acc_hor * -1
            self.vel_hor = -1
        if self.rect.top <= 0:
            self.rect.top = 0
            self.acc_vert = self.acc_vert * -1
            self.vel_vert = 1
        if self.rect.bottom >= self.SCREEN_HEIGHT:
            self.rect.bottom = self.SCREEN_HEIGHT
            self.acc_vert = self.acc_vert * -1
            self.vel_vert = -1