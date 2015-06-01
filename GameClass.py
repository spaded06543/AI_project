import os, sys, pygame
BLOCK = 90
screen_size = width, height = 720, 720
# class for pure image (background, messages, etc.)
class PureImage:
    def __init__(self, file, scale = None):
        self.image = pygame.image.load(os.path.join("Resources",file)).convert_alpha()
        if scale:
            self.image = pygame.transform.smoothscale(self.image, scale)
        self.rect = self.image.get_rect()

    def move_to_pixel(self, pixel):
        self.rect = self.image.get_rect()
        self.rect.move_ip(pixel[0], pixel[1])

# class for a stone, inherit from Sprite class in pygame
class Stone(pygame.sprite.Sprite):
    def __init__(self, file, pos, team, scale = None):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join("Resources",file)).convert_alpha()
        if scale:
            self.image = pygame.transform.smoothscale(self.image, scale)
        self.scale = scale
        self.rect = self.image.get_rect()
        self.rect.move_ip(pos[0] * BLOCK, pos[1] * BLOCK)
        self.cord = [pos[0], pos[1]]
        self.team = team
        self.must_eat = False
        self.selected = False
        self.king = False
        self.dead = False

    def die(self, group):
        self.image = pygame.image.load(os.path.join("Resources","corpse.png")).convert_alpha()
        if self.scale:
            self.image = pygame.transform.smoothscale(self.image, self.scale)
        self.kill()
        group.add(self)
        self.team = 0
        self.dead = True

    def become_king(self):
        if self.team == 1:
            self.image = pygame.image.load(os.path.join("Resources","king1.png")).convert_alpha()
            if self.scale:
                self.image = pygame.transform.smoothscale(self.image, self.scale)
        else:
            self.image = pygame.image.load(os.path.join("Resources","king2.png")).convert_alpha()
            if self.scale:
                self.image = pygame.transform.smoothscale(self.image, self.scale)
        self.king = True

    def move(self, shift):
        self.rect.move_ip(shift[0] * BLOCK, shift[1] * BLOCK)
        self.cord = [self.cord[0] + shift[0], self.cord[1] + shift[1]]
        # edge check
        if self.rect.left < 0 or self.rect.right > width or self.rect.top < 0 or self.rect.bottom > height:
            self.rect.move_ip(-shift[0] * BLOCK, -shift[1] * BLOCK)
            self.cord = [self.cord[0] - shift[0], self.cord[1] - shift[1]]

    def move_to(self, pos):
        self.rect = self.image.get_rect()
        self.rect.move_ip(pos[0] * BLOCK, pos[1] * BLOCK)
        self.cord = [pos[0], pos[1]]
        print(self.cord)
    
    def move_to_pixel(self, pixel):
        self.rect = self.image.get_rect()
        self.rect.move_ip(pixel[0], pixel[1])