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

def heuristic(all_stone, team):
    heuristic = 0
    x = {1:2, 2:1}
    mapping = {0:7, 1:6, 2:5, 3:4, 4:3, 5:2, 6:1, 7:0}
    #print x[turn]
    for stone in all_stone:
        #print stone.team
        if stone.team == x[team]:
            if stone.king == True:
                heuristic += 7
            else:
                heuristic += stone.cord[1]
            #print "player",stone.team," ",stone.cord[1]

        elif stone.team == 0:
            heuristic += 0
        elif stone.team != x[team]:
            if stone.king == True:
                heuristic -= 7
            else:
                heuristic -= mapping[stone.cord[1]]
            #print "player",stone.team," ",mapping[stone.cord[1]]
    return heuristic

# get all possible moves for team
# return [stone, path]
def get_successors(team, team1_info, team2_info, corpses_info):
    successors = []
    eat_successors = []
    eat_len = []
    stone_pos_pair = []
    stone_path_pair = []
    shift = [[-1,-1],[-1,1],[1,-1],[1,1]]
    info_list = (team1_info)if(team == 1)else(team2_info)
        
    for info in info_list:
        path = max_eat(info, team1_info, team2_info, corpses_info)
        if path:
            stone_path_pair.append([info, path])
    max_index = []
    max_len = 0
    for i in range(0, len(stone_path_pair)):
        if len(stone_path_pair[i][1][0]) > max_len:
            max_index = [i]
            max_len = len(stone_path_pair[i][1][0])
        elif len(stone_path_pair[i][1][0]) == max_len:
            max_index.append(i)
    for i in max_index:
        successors.append(stone_path_pair[i])
    if successors:
        return successors

    for info in info_list:
        stone_pos_pair.append([info, [[info.cord[0]+x[0], info.cord[1]+x[1]] for x in shift]])
    for [info, pos_list] in stone_pos_pair:
        success_pos = []
        for pos in pos_list:
            if pos[1] < 0 or pos[1] > 7:
                continue
            pos[0] = pos[0]%8
            tmp = can_move_normal(info, pos, team1_info, team2_info, corpses_info)
            if tmp == 1:
                success_pos.append([pos])
            elif tmp > 1:
                print("oops!")
        successors.append([info, success_pos])
    return successors
