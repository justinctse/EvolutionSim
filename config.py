import pygame

SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 800
frame_rate = 60
basic_food_amount = 75
super_food_amount = 25
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