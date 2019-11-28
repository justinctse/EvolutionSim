import random 
import pygame 
from classes.Creature import Creature
# Herbivore that moves completely randomly
class BasicHerbivore(Creature):
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT):
        Creature.__init__(self, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.type = 'basic'

    def update_position(self):
        self.acc_vert = self.acc_vert + random.uniform(-1 * self.acc_increment, self.acc_increment)
        self.acc_hor = self.acc_hor + random.uniform(-1 * self.acc_increment, self.acc_increment)
        self.vel_vert = self.vel_vert + self.acc_vert
        self.vel_hor = self.vel_hor + self.acc_hor

        # handling max acceleration or velocity
        self.acc_vert = self.handle_max_speed(self.acc_vert, self.acc_max, abs(self.acc_increment))
        self.acc_hor = self.handle_max_speed(self.acc_hor, self.acc_max, abs(self.acc_increment))
        self.vel_vert = self.handle_max_speed(self.vel_vert, self.vel_max, abs(self.acc_vert))
        self.vel_hor = self.handle_max_speed(self.vel_hor, self.vel_max, abs(self.acc_hor))

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