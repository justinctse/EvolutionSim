import random 
import pygame 
from config import *
from classes.Creature import Creature
# Herbivore that moves completely randomly
class BasicHerbivore(Creature):
    def __init__(
        self,
        name,
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
        generation=None,
        lineage=[]
    ):
        Creature.__init__(
            self,
            name,
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
            generation=generation,
            lineage=lineage
        )
        self.type = 'basic'

    def update_position(self):
        self.acc_vert = self.acc_vert + random.uniform(-1 * self.jerk, self.jerk)
        self.acc_hor = self.acc_hor + random.uniform(-1 * self.jerk, self.jerk)
        self.vel_vert = self.vel_vert + self.acc_vert
        self.vel_hor = self.vel_hor + self.acc_hor

        # handling max acceleration or velocity
        self.acc_vert = self.handle_max_speed(self.acc_vert, self.acc_max, abs(self.jerk))
        self.acc_hor = self.handle_max_speed(self.acc_hor, self.acc_max, abs(self.jerk))
        self.vel_vert = self.handle_max_speed(self.vel_vert, self.vel_max, abs(self.acc_vert))
        self.vel_hor = self.handle_max_speed(self.vel_hor, self.vel_max, abs(self.acc_hor))

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