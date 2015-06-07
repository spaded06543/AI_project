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
