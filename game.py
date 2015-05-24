import os, sys, pygame

# initialize pygame
pygame.init()
BLOCK = 90
screen_size = width, height = 720, 720
screen = pygame.display.set_mode(screen_size)
print(screen)

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

# checking if move is legal, return a tuple (int, Stone)
# int   : 1 if move legal, 0 if illegal, -1 if move to origin(no move at all)
# Stone : stone eaten in this move, None if no stone eaten
def check_legal(held, pos, all_stone):
    for stone in all_stone:
        if not held == stone and stone.cord == pos:
            return 0, None
    origin = held.cord
    team = held.team
    king = held.king
    if (pos[0] == (origin[0] + 1)%8 or pos[0] == (origin[0] - 1)%8) and \
        (pos[1] == origin[1] + ((1)if(team == 1)else(-1)) or \
        (king and (pos[1] == origin[1] - ((1)if(team == 1)else(-1))))):
        return 1, None
    elif pos == origin:
        return -1, None
    elif (pos[0] == (origin[0] + 2)%8 or pos[0] == (origin[0] - 2)%8) and \
        (pos[1] == origin[1] + ((2)if(team == 1)else(-2)) or \
        (king and (pos[1] == origin[1] - ((2)if(team == 1)else(-2))))):
        for stone in all_stone:
            if not stone.team == team:
                if (stone.cord == [(origin[0]+1)%8, origin[1]+1] and pos == [(origin[0]+2)%8, origin[1]+2] or \
                    stone.cord == [(origin[0]-1)%8, origin[1]+1] and pos == [(origin[0]-2)%8, origin[1]+2] or \
                    stone.cord == [(origin[0]+1)%8, origin[1]-1] and pos == [(origin[0]+2)%8, origin[1]-2] or \
                    stone.cord == [(origin[0]-1)%8, origin[1]-1] and pos == [(origin[0]-2)%8, origin[1]-2]) and king or \
                   (stone.cord == [(origin[0]+1)%8, origin[1]+1] and pos == [(origin[0]+2)%8, origin[1]+2] or \
                    stone.cord == [(origin[0]-1)%8, origin[1]+1] and pos == [(origin[0]-2)%8, origin[1]+2]) and team == 1 or \
                   (stone.cord == [(origin[0]+1)%8, origin[1]-1] and pos == [(origin[0]+2)%8, origin[1]-2] or \
                    stone.cord == [(origin[0]-1)%8, origin[1]-1] and pos == [(origin[0]-2)%8, origin[1]-2]) and team == 2:
                    return 1, stone
        return 0, None
    else:
        return 0, None
# function for AI, give game state        
def get_state():
    pass
# load images and make objects
# team1, team2 are both Group class in pygame
bg = PureImage("map1.jpg", scale = screen_size)
msg = PureImage("message.png")
msg.move_to_pixel([0, -BLOCK/2])
corpses = pygame.sprite.Group()
team1 = pygame.sprite.Group()
for i in range(12):
    pos = [ ((i%4)*2)if(i>3 and i<8)else((i%4)*2+1) , (0)if(i<4)else((1)if(i<8)else(2))]
    s = Stone("stone1.png", pos, 1, scale = (BLOCK, BLOCK))
    team1.add(s)
team2 = pygame.sprite.Group()
for i in range(12):
    pos = [ ((i%4)*2+1)if(i>3 and i<8)else((i%4)*2) , (5)if(i<4)else((6)if(i<8)else(7))]
    s = Stone("stone2.png", pos, 2, scale = (BLOCK, BLOCK))
    team2.add(s)

# set some flags, entering game loop
stone_selected = False
player_turn = 1
msg_display_frame = 0
_running = True
while _running:
    # check event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            _running = False
        # if a stone is selected, this stone will follow the cursor
        elif event.type == pygame.MOUSEMOTION and stone_selected:
            for stone in team1.sprites()+team2.sprites()+corpses.sprites():
                if stone.selected:
                    stone.move_to_pixel([event.pos[0]-BLOCK/2, event.pos[1]-BLOCK/2])
        elif event.type == pygame.MOUSEBUTTONDOWN:
            selected_sprite = None
            # test which stone mouse click on, store in selected_sprite
            # decide the action to be taken ()
            for stone in team1.sprites()+team2.sprites()+corpses.sprites():
                if not stone_selected:
                    if stone.rect.collidepoint(event.pos):
                        if player_turn == stone.team:
                            stone.selected = True
                            selected_sprite = stone
                else:
                    if stone.selected:
                        selected_sprite = stone
            # mouse is holding a stone => place the stone(or not)
            if selected_sprite and stone_selected:
                pos = [(event.pos[0] - event.pos[0]%BLOCK)/BLOCK, (event.pos[1] - event.pos[1]%BLOCK)/BLOCK]
                legal_move, eaten_stone = check_legal(selected_sprite, pos, team1.sprites()+team2.sprites()+corpses.sprites())
                if legal_move:
                    selected_sprite.move_to([pos[0], pos[1]])
                    selected_sprite.selected = False
                    stone_selected = False
                    if selected_sprite.team == 1 and pos[1] == 7 or selected_sprite.team == 2 and pos[1] == 0:
                        selected_sprite.become_king()
                    if not legal_move == -1:
                        player_turn = (2)if(player_turn == 1)else(1)
                    if eaten_stone:
                        if eaten_stone.dead:
                            eaten_stone.kill()
                        else:
                            eaten_stone.die(corpses)
                # display message for 20 frames if cannot place stone here
                else:
                    msg.move_to_pixel([(width-240)/2, (height-40)/2])
                    msg_display_frame = 20
            # mouse is not holding anything => take the stone
            elif selected_sprite and not stone_selected:
                selected_sprite.selected = True
                stone_selected = True
        else:
            pass
    # check if any player wins
    stones = team1.sprites() + team2.sprites()
    same_team = True
    for stone in stones:
        if not stone.team == stones[0].team:
            same_team = False
            break
    if same_team:
        print("player",stones[0].team,"wins!")
        _running = False
    # draw screen and display
    screen.blit(bg.image, bg.rect)
    layered_draw(team1.sprites()+team2.sprites()+corpses.sprites())
    pygame.display.update()
    # display message(or not) acording to set frame number
    if msg_display_frame > 0:
        pygame.display.update()
        screen.blit(bg.image, bg.rect)
        layered_draw(team1.sprites()+team2.sprites()+corpses.sprites())
        screen.blit(msg.image, msg.rect)
        pygame.display.update()
        msg_display_frame = msg_display_frame - 1
    else:
        msg.move_to_pixel([0, -BLOCK/2])
    pygame.time.delay(30)

pygame.quit()
sys.exit()
