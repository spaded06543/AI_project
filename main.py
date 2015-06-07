import os, sys, pygame
from GameClass import *
from Rules import *
from Functions import *

# initialize pygame
pygame.init()
screen = pygame.display.set_mode(screen_size)
print(screen)

# load images and make objects
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

# set flags, entering game loop
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
                    if not selected_sprite.must_eat:
                        selected_sprite.selected = False
                        stone_selected = False
                    if selected_sprite.team == 1 and pos[1] == 7 or selected_sprite.team == 2 and pos[1] == 0:
                        selected_sprite.become_king()
                    if not (legal_move == -1 or selected_sprite.must_eat):
                        player_turn = (2)if(player_turn == 1)else(1)
                    team1_must = []
                    team2_must = []
                    for stone in team1.sprites():
                        if can_eat_more(stone, team1.sprites()+team2.sprites()+corpses.sprites()):
                            team1_must.append(stone)
                            stone.must_eat = True
                        elif stone.must_eat:
                            stone.must_eat = False
                    for stone in team2.sprites():
                        if can_eat_more(stone, team1.sprites()+team2.sprites()+corpses.sprites()):
                            team2_must.append(stone)
                            stone.must_eat = True
                            print(team2_must)
                        elif stone.must_eat:
                            stone.must_eat = False
                # display message for 20 frames if cannot place stone here
                else:
                    msg1.move_to_pixel([(width-240)/2, (height-40)/2])
                    msg_display_frame = 20
            # mouse is not holding anything => take the stone
            elif selected_sprite and not stone_selected:
                print(selected_sprite.must_eat)
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
    draw_sprite(team1.sprites()+team2.sprites()+corpses.sprites(), screen)
    # display message(or not) acording to set frame number
    if msg_display_frame > 0:
        screen.blit(bg.image, bg.rect)
        draw_sprite(team1.sprites()+team2.sprites()+corpses.sprites(), screen)
        screen.blit(msg1.image, msg1.rect)
        screen.blit(msg2.image, msg2.rect)
        msg_display_frame = msg_display_frame - 1
    else:
    pygame.display.update()
        msg1.move_to_pixel([0, -BLOCK/2])
        msg2.move_to_pixel([0, -BLOCK/2])
    pygame.time.delay(30)

pygame.quit()
sys.exit()
