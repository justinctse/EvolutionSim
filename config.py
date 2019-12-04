import pygame

SCREEN_WIDTH, SCREEN_HEIGHT = 1600, 900
frame_rate = 60 # Base frame rate
num_tomato = 50
num_pumpkin = 10
num_basic_searching_herbivores = 10

# Base Creature parameters for round 1
base_max_size = 100
base_size = 15
base_jerk = .02
base_acc_max = .25
base_vel_max = 2.5
base_search_distance = 150
base_num_offspring_divisor = 20

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

# Loading in assets
img_hungry = pygame.image.load('assets/hungry_256.png')
img_dead = pygame.image.load('assets/dead_256.png')
img_happy = pygame.image.load('assets/happy_256.png')
img_neutral = pygame.image.load('assets/neutral_256.png')
img_tomato = pygame.image.load('assets/tomato_64.png')
img_pumpkin = pygame.image.load('assets/pumpkin_64.png')