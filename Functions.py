import copy
import pygame
from Rules import *

# function for drawing all sprites in a given list
# Note that drawing top_stone last keep it on top layer
def draw_sprite(sprites, screen):
    top_stone = None
    for sprite in sprites:
        if not sprite.selected:
            screen.blit(sprite.image, sprite.rect)
        else:
            top_stone = sprite
    if top_stone:
        screen.blit(top_stone.image, top_stone.rect)

# select game mode(AI or 2P)
def select_gamemode(window, button1, button2, screen, width, height, SCALE):
    game_mode = -1
    window.move_to_pixel([(width-300*SCALE/100)/2, (height-300*SCALE/100)/2])
    button1.move_to_pixel([(width-200*SCALE/100)/2, (height-100*SCALE/100-SCALE)/2])
    button2.move_to_pixel([(width-200*SCALE/100)/2, (height-100*SCALE/100+SCALE)/2])
    screen.blit(window.image, window.rect)
    screen.blit(button1.image, button1.rect)
    screen.blit(button2.image, button2.rect)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button1.rect.collidepoint(event.pos):
                    game_mode = 0
                elif button2.rect.collidepoint(event.pos):
                    game_mode = 1
        if game_mode != -1:
            break
    print(game_mode)
    return game_mode

def heuristic(all_stone, turn):
    heuristic = 0
    x = {1:2, 2:1}
    mapping = {0:7, 1:6, 2:5, 3:4, 4:3, 5:2, 6:1, 7:0}
    #print x[turn]
    if gameover(all_stone):
        
    for stone in all_stone:
        #print stone.team
        if stone.info.team == x[turn]:
            if stone.info.king == True:
                heuristic += 7
            else:
                heuristic += stone.info.cord[1]
            #print "player",stone.team," ",stone.cord[1]

        elif stone.info.team == 0:
            heuristic += 0
        elif stone.info.team != x[turn]:
            if stone.info.king == True:
                heuristic -= 7
            else:
                heuristic -= mapping[stone.info.cord[1]]
            #print "player",stone.team," ",mapping[stone.cord[1]]
    return heuristic

# get all possible moves for team
# return [stone, move]
def get_successors(stones, team1, team2, corpses, must):
    successors = []
    eat_successors = []
    eat_len = []
    stone_pos_pair = []
    shift = [[-1,-1],[-1,1],[1,-1],[1,1],[-2,-2],[-2,2],[2,-2],[2,2]]
    if must:
        for stone in stones:
            stone_pos_pair.append([stone, [[stone.info.cord[0]+x[0], stone.info.cord[1]+x[1]] for x in shift[4:]]])
    else:
        for stone in stones:
            stone_pos_pair.append([stone, [[stone.info.cord[0]+x[0], stone.info.cord[1]+x[1]] for x in shift]])

    for [stone, pos_list] in stone_pos_pair:
        for pos in pos_list:
            if pos[1] < 0 or pos[1] > 7:
                continue
            pos[0] = pos[0]%8
            tmp = can_move(stone, pos, team1, team2, corpses)
            if tmp == 1:
                successors.append([stone,pos])
            elif tmp > 1:
                eat_successors.append([stone,pos])
                eat_len.append(tmp)
    if len(eat_len) != 0:
        max_len = max(eat_len)
        for length, successor in zip(eat_len, eat_successors):
            if length == max_len:
                successors.append(successor)
    return successors
