########## TODO : multiple captures(forced) ###########
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

#############################
######### ALL RULES #########
#############################
# check if pos has a stone already
def occupied(held, pos, all_stone):
    for stone in all_stone:
        if not held == stone and stone.cord == pos:
            return True
    return False
# a normal move
def normal_move(held, pos):
    cord = held.cord
    team = held.team
    king = held.king
    if king:
        if (pos[0] == (cord[0] + 1)%8 or pos[0] == (cord[0] - 1)%8) and \
           (pos[1] == cord[1] - 1 or pos[1] == cord[1] + 1):
            held.move_to([pos[0], pos[1]])
            return True
        else:
            return False
    else:
        if (pos[0] == (cord[0] + 1)%8 or pos[0] == (cord[0] - 1)%8) and \
           pos[1] == cord[1] + ((1)if(team == 1)else(-1)):
            held.move_to([pos[0], pos[1]])
            return True
        else:
            return False
# if stone can eat more
def can_eat_more(held, all_stone):
    team = held.team
    king = held.king
    cord = held.cord
    king_pos = [[(cord[0]+2)%8, cord[1]+2], [(cord[0]+2)%8, cord[1]-2],\
                [(cord[0]-2)%8, cord[1]+2], [(cord[0]-2)%8, cord[1]-2]]
    team1_pos = [[(cord[0]+2)%8, cord[1]+2], [(cord[0]-2)%8, cord[1]+2]]
    team2_pos = [[(cord[0]+2)%8, cord[1]-2], [(cord[0]-2)%8, cord[1]-2]]
    tmp = []
    for pos in king_pos:
        if not occupied(held, pos, all_stone) and \
           not (pos[1] < 0 or pos[1] > 7):
            tmp.append(pos)
    king_pos = tmp
    tmp = []
    for pos in team1_pos:
        if not occupied(held, pos, all_stone) and \
           not (pos[1] < 0 or pos[1] > 7):
            tmp.append(pos)
    team1_pos = tmp
    tmp = []
    for pos in team2_pos:
        if not occupied(held, pos, all_stone) and \
           not (pos[1] < 0 or pos[1] > 7):
            tmp.append(pos)
    team2_pos = tmp

    if king:
        for pos in king_pos:
            for stone in all_stone:
                if not stone.team == team:
                    if stone.cord == [(cord[0]+1)%8, cord[1]+1] and pos == [(cord[0]+2)%8, cord[1]+2] or \
                       stone.cord == [(cord[0]-1)%8, cord[1]+1] and pos == [(cord[0]-2)%8, cord[1]+2] or \
                       stone.cord == [(cord[0]+1)%8, cord[1]-1] and pos == [(cord[0]+2)%8, cord[1]-2] or \
                       stone.cord == [(cord[0]-1)%8, cord[1]-1] and pos == [(cord[0]-2)%8, cord[1]-2]:
                        return True
    elif team == 1:
        for pos in team1_pos:
            for stone in all_stone:
                if not stone.team == team:
                    if stone.cord == [(cord[0]+1)%8, cord[1]+1] and pos == [(cord[0]+2)%8, cord[1]+2] or \
                       stone.cord == [(cord[0]-1)%8, cord[1]+1] and pos == [(cord[0]-2)%8, cord[1]+2]:
                        print("team1 continue")
                        return True
    else:
        for pos in team2_pos:
            for stone in all_stone:
                if not stone.team == team:
                    if stone.cord == [(cord[0]+1)%8, cord[1]-1] and pos == [(cord[0]+2)%8, cord[1]-2] or \
                       stone.cord == [(cord[0]-1)%8, cord[1]-1] and pos == [(cord[0]-2)%8, cord[1]-2]:
                        print("team2 continue")
                        return True
    return False
# a eat move
def eat_move(held, pos, team1, team2, corpses):
    cord = held.cord
    team = held.team
    king = held.king
    all_stone = team1.sprites() + team2.sprites() + corpses.sprites()
    if king:
        if (pos[0] == (cord[0] + 2)%8 or pos[0] == (cord[0] - 2)%8) and \
            (pos[1] == cord[1] + 2 or pos[1] == cord[1] - 2):
            for stone in all_stone:
                if not stone.team == team:
                    if stone.cord == [(cord[0]+1)%8, cord[1]+1] and pos == [(cord[0]+2)%8, cord[1]+2] or \
                       stone.cord == [(cord[0]-1)%8, cord[1]+1] and pos == [(cord[0]-2)%8, cord[1]+2] or \
                       stone.cord == [(cord[0]+1)%8, cord[1]-1] and pos == [(cord[0]+2)%8, cord[1]-2] or \
                       stone.cord == [(cord[0]-1)%8, cord[1]-1] and pos == [(cord[0]-2)%8, cord[1]-2]:
                        held.move_to([pos[0], pos[1]])
                        if stone.dead:
                            stone.kill()
                        else:
                            stone.die(corpses)
                        all_stone = team1.sprites() + team2.sprites() + corpses.sprites()
                        if can_eat_more(held, all_stone):
                            held.must_eat = True
                        else:
                            held.must_eat = False
                        return True
        else:
            return False
    else:
        if (pos[0] == (cord[0] + 2)%8 or pos[0] == (cord[0] - 2)%8) and \
            pos[1] == cord[1] + ((2)if(team == 1)else(-2)):
            for stone in all_stone:
                if not stone.team == team:
                    if team == 1 and \
                       (stone.cord == [(cord[0]+1)%8, cord[1]+1] and pos == [(cord[0]+2)%8, cord[1]+2] or \
                       stone.cord == [(cord[0]-1)%8, cord[1]+1] and pos == [(cord[0]-2)%8, cord[1]+2]) or \
                       team == 2 and \
                       (stone.cord == [(cord[0]+1)%8, cord[1]-1] and pos == [(cord[0]+2)%8, cord[1]-2] or \
                       stone.cord == [(cord[0]-1)%8, cord[1]-1] and pos == [(cord[0]-2)%8, cord[1]-2]):
                        held.move_to([pos[0], pos[1]])
                        if stone.dead:
                            stone.kill()
                        else:
                            stone.die(corpses)
                        all_stone = team1.sprites() + team2.sprites() + corpses.sprites()
                        if can_eat_more(held, all_stone):
                            held.must_eat = True
                        else:
                            held.must_eat = False
                        return True
        else:
            return False
# checking if move is legal, return a int
# return    : 1 if move legal, 0 if illegal, -1 if move to origin(no move at all)
def move_if_legal(held, pos, team1, team2, corpses):
    all_stone = team1.sprites() + team2.sprites() + corpses.sprites()
    if occupied(held, pos, all_stone):
        return 0
    elif not held.must_eat and pos == held.cord:
        held.move_to([pos[0], pos[1]])
        return -1
    elif not held.must_eat and normal_move(held, pos):
        return 1
    elif eat_move(held, pos, team1, team2, corpses):
        return 1
    else:
        return 0
# function for AI, give game state        
def get_state():
    pass
# load images and make objects
# team1, team2 , corpses are all Group class in pygame
bg = PureImage("map1.jpg", scale = screen_size)
msg1 = PureImage("message1.png")
msg2 = PureImage("message2.png")
msg1.move_to_pixel([0, -BLOCK/2])
msg2.move_to_pixel([0, -BLOCK/2])
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
team1_must = []
team2_must = []
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
            # decide the action to be taken
            for stone in team1.sprites()+team2.sprites()+corpses.sprites():
                if not stone_selected:
                    if stone.rect.collidepoint(event.pos):
                        if player_turn == stone.team:
                            stone.selected = True
                            selected_sprite = stone
                else:
                    if stone.selected:
                        selected_sprite = stone
            # check
            if selected_sprite and selected_sprite.team == 1 and \
               len(team1_must) and not selected_sprite in team1_must:
                selected_sprite.selected = False
                msg2.move_to_pixel([(width-240)/2, (height-40)/2])
                msg_display_frame = 20
            elif selected_sprite and selected_sprite.team == 2 and \
               len(team2_must) and not selected_sprite in team2_must:
                selected_sprite.selected = False
                msg2.move_to_pixel([(width-240)/2, (height-40)/2])
                msg_display_frame = 20
            # mouse is holding a stone => place the stone(or not)
            elif selected_sprite and stone_selected:
                pos = [(event.pos[0] - event.pos[0]%BLOCK)/BLOCK, (event.pos[1] - event.pos[1]%BLOCK)/BLOCK]
                legal_move = move_if_legal(selected_sprite, pos, team1, team2, corpses)
                if legal_move:
                    team1_must = []
                    team2_must = []
                    for stone in team1.sprites():
                        if can_eat_more(stone, team1.sprites()+team2.sprites()+corpses.sprites()):
                            team1_must.append(stone)
                    for stone in team2.sprites():
                        if can_eat_more(stone, team1.sprites()+team2.sprites()+corpses.sprites()):
                            team2_must.append(stone)

                    if not selected_sprite.must_eat:
                        selected_sprite.selected = False
                        stone_selected = False
                    if selected_sprite.team == 1 and pos[1] == 7 or selected_sprite.team == 2 and pos[1] == 0:
                        selected_sprite.become_king()
                    if not (legal_move == -1 or selected_sprite.must_eat):
                        player_turn = (2)if(player_turn == 1)else(1)
                # display message for 20 frames if cannot place stone here
                else:
                    msg1.move_to_pixel([(width-240)/2, (height-40)/2])
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
        screen.blit(msg1.image, msg1.rect)
        screen.blit(msg2.image, msg2.rect)
        pygame.display.update()
        msg_display_frame = msg_display_frame - 1
    else:
        msg1.move_to_pixel([0, -BLOCK/2])
        msg2.move_to_pixel([0, -BLOCK/2])
    pygame.time.delay(30)

pygame.quit()
sys.exit()
