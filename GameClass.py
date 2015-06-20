import os, sys, pygame
BLOCK = 90
screen_size = width, height = BLOCK*8, BLOCK*8

# class for pure image (background, messages, etc.)
class PureImage:
    def __init__(self, file, scale = None):
        self.image = pygame.image.load(os.path.join("Resources",file)).convert_alpha()
        if scale:
            img_w = self.image.get_width()
            img_h = self.image.get_height()
            self.image = pygame.transform.smoothscale(self.image, (int(img_w*(scale/100)), int(img_h*(scale/100))))
        self.scale = scale
        self.rect = self.image.get_rect()

    def move_to_pixel(self, pixel):
        self.rect = self.image.get_rect()
        self.rect.move_ip(pixel[0], pixel[1])

# class holds important info for stone
class Stone_light:
    def __init__(self, pos, team):
        self.cord = pos 
        self.team = team
        self.king = False

# class for a stone, inherit from Sprite class in pygame
class Stone(pygame.sprite.Sprite):
    def __init__(self, file, pos, team, scale = None):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join("Resources",file)).convert_alpha()
        if scale:
            img_w = self.image.get_width()
            img_h = self.image.get_height()
            self.image = pygame.transform.smoothscale(self.image, (int(img_w*(scale/100)), int(img_h*(scale/100))))
        self.scale = scale
        self.rect = self.image.get_rect()
        self.rect.move_ip(pos[0] * BLOCK, pos[1] * BLOCK)
        self.must_eat = False
        self.eating = False
        self.selected = False
        self.dead = False
        self.info = Stone_light(pos, team)

    def die(self, group):
        self.image = pygame.image.load(os.path.join("Resources","corpse.png")).convert_alpha()
        if self.scale:
            img_w = self.image.get_width()
            img_h = self.image.get_height()
            self.image = pygame.transform.smoothscale(self.image, (int(img_w*(self.scale/100)), int(img_h*(self.scale/100))))
        self.kill()
        group.add(self)
        self.info.team = 0
        self.dead = True

    def become_king(self):
        if self.info.team == 1:
            self.image = pygame.image.load(os.path.join("Resources","king1.png")).convert_alpha()
            if self.scale:
                img_w = self.image.get_width()
                img_h = self.image.get_height()
                self.image = pygame.transform.smoothscale(self.image, (int(img_w*(self.scale/100)), int(img_h*(self.scale/100))))
        else:
            self.image = pygame.image.load(os.path.join("Resources","king2.png")).convert_alpha()
            if self.scale:
                img_w = self.image.get_width()
                img_h = self.image.get_height()
                self.image = pygame.transform.smoothscale(self.image, (int(img_w*(self.scale/100)), int(img_h*(self.scale/100))))
        self.info.king = True

    def move_to(self, pos):
        self.rect = self.image.get_rect()
        self.rect.move_ip(pos[0] * BLOCK, pos[1] * BLOCK)
        self.info.cord = [pos[0], pos[1]]
        if self.info.team == 1 and self.info.cord[1] == 7 or \
           self.info.team == 2 and self.info.cord[1] == 0:
            self.become_king()
        print(self.info.cord)
    
    def move_to_pixel(self, pixel):
        self.rect = self.image.get_rect()
        self.rect.move_ip(pixel[0], pixel[1])
