import pygame

SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 800
SCREEN_WIDTH, SCREEN_HEIGHT = 1600, 900
frame_rate = 60
basic_food_amount = 50
super_food_amount = 10
num_basic_searching_herbivores = 5
num_fast_searching_herbivores = 0

# Fields to skip when doing a stats dump
skip_fields = [
    '_Sprite__g', 
    'surf', 
    'rect',
    'acc_hor',
    'acc_vert',
    'vel_hor',
    'vel_vert'
]

img_hungry = pygame.image.load('assets/hungry_256.png')
img_dead = pygame.image.load('assets/dead_256.png')
img_basic_food = pygame.image.load('assets/tomato_64.png')
img_super_food = pygame.image.load('assets/pumpkin_64.png')