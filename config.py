import pygame

multiplier = 1 #temp

SCREEN_WIDTH, SCREEN_HEIGHT = 1600, 900
frame_rate = 60 # Base frame rate
num_tomato = 45 * multiplier
num_pumpkin = 20 * multiplier
num_grape = 25 * multiplier
num_basic_searching_herbivores = 25 * multiplier
num_predator = 5 * multiplier

predators_can_eat_each_other = False

# Base Creature parameters for round 1
base_max_size = 110
base_size = 15
base_defense = 10
base_attack = 15
base_jerk = .012 
base_acc_max = .15 
base_vel_max = 2.0 
base_search_distance = 300
base_num_offspring_divisor = 15
base_fear = 500

base_predator_max_size = 80
base_predator_size = 15
base_predator_defense = 10
base_predator_attack = 15
base_predator_jerk = .015
base_predator_acc_max = .2
base_predator_vel_max = 2.2
base_predator_search_distance = 400
base_predator_num_offspring_divisor = 25

# The lower bound of mutation when passing traits
round_trait_decrease_percent = .85
# The upper bound of mutation when passing traits
round_trait_increase_percent = 1.15


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

img_hungry_predator = pygame.image.load('assets/hungry_predator_256.png')
img_sleepy_predator = pygame.image.load('assets/sleepy_predator_256.png')
img_dead_predator = pygame.image.load('assets/dead_predator_256.png')


img_tomato = pygame.image.load('assets/tomato_64.png')
img_pumpkin = pygame.image.load('assets/pumpkin_64.png')
img_grape = pygame.image.load('assets/grape_64.png')