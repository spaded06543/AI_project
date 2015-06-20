import os, sys, pygame
from GameClass import *
from Rules import *
from Functions import *
from AI import *

if __name__ == "__main__" :
    # initialize pygame
    pygame.init()
    screen = pygame.display.set_mode(screen_size)
    print(screen)

    # load images and make objects
    SCALE = 90
    bg = PureImage("map1.png", scale = SCALE)
    select_window = PureImage("select_bg.png",scale = SCALE)
    button1 = PureImage("button1.png",scale = SCALE)
    button2 = PureImage("button2.png",scale = SCALE)
    msg1 = PureImage("message1.png", scale = SCALE)
    msg2 = PureImage("message2.png", scale = SCALE)
    select_window.move_to_pixel([0, height])
    button1.move_to_pixel([0, height])
    button2.move_to_pixel([0, height])
    msg1.move_to_pixel([0, height])
    msg2.move_to_pixel([0, height])
    corpses = pygame.sprite.Group()
    team1 = pygame.sprite.Group()
    for i in range(12):
        pos = [ ((i%4)*2)if(i>3 and i<8)else((i%4)*2+1) , (0)if(i<4)else((1)if(i<8)else(2))]
        s = Stone("stone1.png", pos, 1, scale = SCALE)
        #s.become_king()
        team1.add(s)
    team2 = pygame.sprite.Group()
    for i in range(12):
        pos = [ ((i%4)*2+1)if(i>3 and i<8)else((i%4)*2) , (5)if(i<4)else((6)if(i<8)else(7))]
        s = Stone("stone2.png", pos, 2, scale = SCALE)
        #s.become_king()
        team2.add(s)

    # select game mode(AI or 2P)
    # gamemode 0 = AI; gamemode 1 = 2P
    gamemode = select_gamemode(select_window, button1, button2, screen, width, height, SCALE)
    if gamemode == 0:
        ai = AI(2, screen)
    # set flags, entering game loop
    stone_selected = False
    player_turn = 1
    msg_display_frame = 0
    _running = True
    flag = 0
    while _running:
        if gamemode == 0 and player_turn == 2:
            #ai_action(team1, team2, corpses)
            for i in ai.get_action(team1, team2, corpses):
                pygame.time.delay(1200)
                screen.blit(bg.image, bg.rect)
                draw_sprite(team1.sprites()+team2.sprites()+corpses.sprites(), screen)
                pygame.display.update()
            #if must continue: continue
            player_turn = 1
        if flag == 1:
            #print (heuristic(stones,player_turn))
            flag = 0
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
                print()
                selected_sprite = None
                # test which stone mouse click on, store in selected_sprite
                for stone in team1.sprites()+team2.sprites()+corpses.sprites():
                    if not stone_selected:
                        if stone.rect.collidepoint(event.pos):
                            if player_turn == stone.info.team:
                                stone.selected = True
                                selected_sprite = stone
                    else:
                        if stone.selected:
                            selected_sprite = stone
                if not selected_sprite:
                    continue
                # check if player can take stone
                pos = [(event.pos[0] - event.pos[0]%BLOCK)/BLOCK, (event.pos[1] - event.pos[1]%BLOCK)/BLOCK]
                info = copy.copy(selected_sprite.info)
                team1_info = [x.info for x in team1.sprites()]
                team2_info = [x.info for x in team2.sprites()]
                corpses_info = [x.info for x in corpses.sprites()]
                successors = get_successors(player_turn, team1_info, team2_info, corpses_info)
                if not selected_sprite.info.cord in [x[0].cord for x in successors]:
                    msg2.move_to_pixel([(width-240*SCALE/100)/2, (height-40*SCALE/100)/2])
                    msg_display_frame = 20
                    selected_sprite.selected = False
                    continue
                # mark that "player is holding a stone"
                if not stone_selected:
                    stone_selected = True
                    continue
                # stone_selected, selected_sprite, selected_sprite.selected all True
                # player try to place a stone
                can_move = False
                for [stone_light, path] in successors:
                    print(stone_light.cord, path)
                    if info.cord == stone_light.cord:
                        first_moves = [x[0] for x in path]
                        if pos in first_moves or (pos == info.cord and not selected_sprite.eating):
                            can_move = True
                
                if not can_move:
                    msg2.move_to_pixel([(width-240*SCALE/100)/2, (height-40*SCALE/100)/2])
                    msg_display_frame = 20
                    continue
                else:
                    selected_sprite.move_to(pos)
                    if pos[0] - info.cord[0] == 2 or pos[0] - info.cord[0] == -2 or\
                       pos[0] - info.cord[0] == 6 or pos[0] - info.cord[0] == -6:
                        eaten = []
                        if pos[0]-info.cord[0] == -2 or pos[0]-info.cord[0] == 6:
                            eaten = [(info.cord[0]-1)%8, (info.cord[1]+pos[1])/2]
                        else:
                            eaten = [(info.cord[0]+1)%8, (info.cord[1]+pos[1])/2]

                        for stone in team1.sprites()+team2.sprites()+corpses.sprites():
                            if stone.info.cord == eaten:
                                if stone.dead:
                                    stone.kill()
                                    break
                                else:
                                    stone.die(corpses)
                                    break
                        team1_info = [x.info for x in team1.sprites()]
                        team2_info = [x.info for x in team2.sprites()]
                        corpses_info = [x.info for x in corpses.sprites()]
                        tmp = Stone_light(selected_sprite.info.cord, selected_sprite.info.team, info.king)
                        if can_eat_more(tmp, team1_info + team2_info + corpses_info):
                            selected_sprite.must_eat = True
                            selected_sprite.eating = True
                        else:
                            selected_sprite.must_eat = False
                            selected_sprite.eating = False
                    if not selected_sprite.eating:
                        selected_sprite.selected = False
                        stone_selected = False
                    if not selected_sprite.info.cord == info.cord and selected_sprite.eating == False:
                        player_turn = (2)if(player_turn == 1)else(1)
                        flag = 1
            else:
                pass
        # check if any player wins
        stones = team1.sprites() + team2.sprites()
        same_team = True
        for stone in stones:
            if not stone.info.team == stones[0].info.team:
                same_team = False
                break
        if same_team:
            print("player",stones[0].info.team,"wins!")
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
            msg1.move_to_pixel([0, height])
            msg2.move_to_pixel([0, height])
        pygame.display.update()
        pygame.time.delay(30)

    pygame.quit()
    sys.exit()
