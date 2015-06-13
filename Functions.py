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
        if not game_mode == -1:
            break
    print(game_mode)
    return game_mode

def heuristic(all_stone,turn):
    heuristic = 0
    x = {1:2,2:1}
    mapping = {0:7,1:6,2:5,3:4,4:3,5:2,6:1,7:0}
    #print x[turn]
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

# get possible moves
def get_successors(stone, team1, team2, corpses):
    cord = stone.info.cord
    team = stone.info.team
    king = stone.info.king
    successors = []
    if team == 1:
        for stone in team1.sprites():
            pos_list = []
            #set pos_list (all possible positions)
            for pos in pos_list:
                if #stone can move to pos:
                    successors.append(pos)
    elif team == 2:
        for stone in team2.sprites():
            pos_list = []
            #set pos_list (all possible positions)
            for pos in pos_list:
                if #stone can move to pos:
                    successors.append(pos)
    return successors
