import sys, pygame

# initialize pygame 
pygame.init()
screen_size = width, height = 640, 640
BLOCK = 80
screen = pygame.display.set_mode(screen_size)
print(screen)
_running = True

class PureImage:
    def __init__(self, file, scale = None):
        self.image = pygame.image.load(file).convert_alpha()
        if scale:
            self.image = pygame.transform.smoothscale(self.image, scale)
        self.rect = self.image.get_rect()

    def move_to_pixel(self, pixel):
        self.rect = self.image.get_rect()
        self.rect.move_ip(pixel[0], pixel[1])

class Stone(pygame.sprite.Sprite):
    def __init__(self, file, pos, team, scale = None):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(file).convert_alpha()
        if scale:
            self.image = pygame.transform.smoothscale(self.image, scale)
        self.rect = self.image.get_rect()
        self.rect.move_ip(pos[0] * BLOCK, pos[1] * BLOCK)
        self.team = team
        self.selected = False

    def move(self, shift):
        self.rect.move_ip(shift[0] * BLOCK, shift[1] * BLOCK)
        # edge check
        if self.rect.left < 0 or self.rect.right > width\
            or self.rect.top < 0 or self.rect.bottom > height:
            self.rect.move_ip(-shift[0] * BLOCK, -shift[1] * BLOCK)

    def move_to(self, pos):
        self.rect = self.image.get_rect()
        self.rect.move_ip(pos[0] * BLOCK, pos[1] * BLOCK)
    
    def move_to_pixel(self, pixel):
        self.rect = self.image.get_rect()
        self.rect.move_ip(pixel[0], pixel[1])

# function for drawing all sprites in a given list
# Note that drawing top_stone last keep it on top layer
def layered_draw(sprites):
    top_stone = None
    for sprite in sprites:
        if sprite.selected == False:
            screen.blit(sprite.image, sprite.rect)
        else:
            top_stone = sprite
    if top_stone:
        screen.blit(top_stone.image, top_stone.rect)

# load all images in and make objects
bg = PureImage("map1.jpg", scale = (640, 640))
msg = PureImage("message.png")
msg.move_to_pixel([0, -BLOCK/2])
team1 = pygame.sprite.Group()
for i in range(12):
    pos = [ ((i%4)*2)if(i>3 and i<8)else((i%4)*2+1) , (0)if(i<4)else((1)if(i<8)else(2))]
    s = Stone("stone1.png", pos, 1, scale = (80, 80))
    team1.add(s)
team2 = pygame.sprite.Group()
for i in range(12):
    pos = [ ((i%4)*2+1)if(i>3 and i<8)else((i%4)*2) , (5)if(i<4)else((6)if(i<8)else(7))]
    s = Stone("stone2.png", pos, 1, scale = (80, 80))
    team2.add(s)

# set flag, start main loop
stone_selected = False
msg_display_frame = 0
while _running:
    # check event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            _running = False
        if event.type == pygame.MOUSEMOTION and stone_selected:
            for sprite in team1.sprites() + team2.sprites():
                if sprite.selected:
                    sprite.move_to_pixel([event.pos[0]-BLOCK/2, event.pos[1]-BLOCK/2])
        if event.type == pygame.MOUSEBUTTONDOWN:
            can_place = True
            selected_sprite = None
            for sprite in team1.sprites() + team2.sprites():
                if stone_selected:
                    if sprite.selected:
                        selected_sprite = sprite
                    elif sprite.rect.collidepoint(event.pos):
                        can_place = False
                else:
                    if sprite.rect.collidepoint(event.pos):
                        sprite.selected = True
                        selected_sprite = sprite
            if selected_sprite and stone_selected: # mouse is holding a stone
                if can_place:
                    pos = [event.pos[0] - event.pos[0]%BLOCK, event.pos[1] - event.pos[1]%BLOCK]
                    selected_sprite.move_to_pixel([pos[0], pos[1]])
                    selected_sprite.selected = False
                    stone_selected = False
                else:
                    msg.move_to_pixel([(width-240)/2, (height-40)/2])
                    msg_display_frame = 20
            elif selected_sprite and not stone_selected: # mouse select a stone
                selected_sprite.selected = True
                stone_selected = True
        else:
            pass
    # draw screen and display
    screen.blit(bg.image, bg.rect)
    layered_draw(team1.sprites()+team2.sprites())
    pygame.display.update()
    # display other message
    if msg_display_frame > 0:
        pygame.display.update()
        screen.blit(bg.image, bg.rect)
        layered_draw(team1.sprites()+team2.sprites())
        screen.blit(msg.image, msg.rect)
        pygame.display.update()
        msg_display_frame = msg_display_frame - 1
    else:
        msg.move_to_pixel([0, -BLOCK/2])
    pygame.time.delay(30)

pygame.quit()
sys.exit()
