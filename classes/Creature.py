import pygame 
class Creature(pygame.sprite.Sprite):
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT):
        super(Creature, self).__init__()
        self.SCREEN_WIDTH = SCREEN_WIDTH 
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.max_size = 100
        self.width = 25
        self.height = 25
        self.surf = pygame.Surface((self.width, self.height))
        self.surf.fill((0, 0, 0))
        self.rect = self.surf.get_rect(
                center=((SCREEN_WIDTH-self.surf.get_width())/2, (SCREEN_HEIGHT-self.surf.get_height())/2))

        self.acc_increment = .33
        self.acc_max = 1.0
        self.vel_max = 5.0

        self.acc_vert = 0
        self.acc_hor = 0
        self.vel_vert = 0
        self.vel_hor = 0
    
    # returns new speed, 
    def handle_max_speed(self, metric, max, increment):
        to_return = metric
        if abs(metric) > max:
            if metric > 0:
                to_return = to_return - increment
            else:
                to_return = to_return + increment
        return to_return

    def grow(self, growth_increment = 5):
        if (self.width < self.max_size) & (self.height < self.max_size):
            self.width = min(self.width + growth_increment, self.max_size)
            self.height = min(self.height + growth_increment, self.max_size)
            self.surf = pygame.Surface((self.width, self.height))
            self.surf.fill((0,0,0))
            # I'm not gonna lie this code is questionable
            self.rect = self.surf.get_rect(
                center=(self.rect[0] + self.width/2, self.rect[1] + self.height/2))