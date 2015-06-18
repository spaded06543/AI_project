import copy

def gameover(all_stone):
    over = True
    basic = None
    for stone in all_stone:
        if stone.info.team != 0:
            basic = stone
            break
    for stone in all_stone:
        if stone.info.team != basic.info.team and stone.info.team != 0:
            over = False
            break
    if over:
        print("player",basic.info.team,"wins!")
    return over

def gameover_light(all_info):
    over = True
    basic = None
    for info in all_info:
        if info.team != 0:
            basic = info
            break
    for info in all_info:
        if info.team != basic.team and info.team != 0:
            over = False
            break
    if over:
        print("player",basic.team,"wins!")
    return over
# check if pos has a stone already
def occupied(pos, all_stone):
    for stone in all_stone:
        if stone.info.cord == pos:
            return True
    return False

def get_stone(pos, all_stone):
    for stone in all_stone:
        if stone.info.cord == pos:
            return stone
    return None
# return a list of position stone can move
def normal_move2(stone_small, all_stone):
    pos_list = []
    all_pos = [x.cord for x in all_stone]
    if stone_small.king :
        D = [[1, 1], [1, -1], [-1, 1], [-1, -1]]
    elif stone_small.team == 1 :
        D = [[1, 1], [-1, 1]]
    else :
        D = [[1, -1], [-1, -1]]
    for d in D :
        next = [(stone_small.cord[0] + d[0])%8, stone_small.cord[1] + d[1]]
        if not (next in all_pos) and next[1] >= 0 and next[1] <= 7:
            pos_list.append(next)
    return pos_list

# a normal move
def normal_move(held, pos):
    cord = held.info.cord
    team = held.info.team
    king = held.info.king
    if king:
        if (pos[0] == (cord[0] + 1)%8 or pos[0] == (cord[0] - 1)%8) and \
           (pos[1] == cord[1] - 1 or pos[1] == cord[1] + 1):
            return True
        else:
            return False
    else:
        if (pos[0] == (cord[0] + 1)%8 or pos[0] == (cord[0] - 1)%8) and \
           pos[1] == cord[1] + ((1)if(team == 1)else(-1)):
            return True
        else:
            return False

# if stone can eat more
def can_eat_more(held, all_stone):
    team = held.info.team
    king = held.info.king
    cord = held.info.cord
    king_pos = [[(cord[0]+2)%8, cord[1]+2], [(cord[0]+2)%8, cord[1]-2],\
                [(cord[0]-2)%8, cord[1]+2], [(cord[0]-2)%8, cord[1]-2]]
    team1_pos = [[(cord[0]+2)%8, cord[1]+2], [(cord[0]-2)%8, cord[1]+2]]
    team2_pos = [[(cord[0]+2)%8, cord[1]-2], [(cord[0]-2)%8, cord[1]-2]]
    tmp = []
    for pos in king_pos:
        if not occupied(pos, all_stone) and \
           not (pos[1] < 0 or pos[1] > 7):
            tmp.append(pos)
    king_pos = tmp
    tmp = []
    for pos in team1_pos:
        if not occupied(pos, all_stone) and \
           not (pos[1] < 0 or pos[1] > 7):
            tmp.append(pos)
    team1_pos = tmp
    tmp = []
    for pos in team2_pos:
        if not occupied(pos, all_stone) and \
           not (pos[1] < 0 or pos[1] > 7):
            tmp.append(pos)
    team2_pos = tmp

    if king:
        for pos in king_pos:
            for stone in all_stone:
                if stone.info.team != team:
                    if stone.info.cord == [(cord[0]+1)%8, cord[1]+1] and pos == [(cord[0]+2)%8, cord[1]+2] or \
                       stone.info.cord == [(cord[0]-1)%8, cord[1]+1] and pos == [(cord[0]-2)%8, cord[1]+2] or \
                       stone.info.cord == [(cord[0]+1)%8, cord[1]-1] and pos == [(cord[0]+2)%8, cord[1]-2] or \
                       stone.info.cord == [(cord[0]-1)%8, cord[1]-1] and pos == [(cord[0]-2)%8, cord[1]-2]:
                        return True
    elif team == 1:
        for pos in team1_pos:
            for stone in all_stone:
                if stone.info.team != team:
                    if stone.info.cord == [(cord[0]+1)%8, cord[1]+1] and pos == [(cord[0]+2)%8, cord[1]+2] or \
                       stone.info.cord == [(cord[0]-1)%8, cord[1]+1] and pos == [(cord[0]-2)%8, cord[1]+2]:
                        print("team1 continue")
                        return True
    else:
        for pos in team2_pos:
            for stone in all_stone:
                if stone.info.team != team:
                    if stone.info.cord == [(cord[0]+1)%8, cord[1]-1] and pos == [(cord[0]+2)%8, cord[1]-2] or \
                       stone.info.cord == [(cord[0]-1)%8, cord[1]-1] and pos == [(cord[0]-2)%8, cord[1]-2]:
                        print("team2 continue")
                        return True
    return False

# a eat move

def eat_move(held, pos, team1, team2, corpses):
    cord = held.info.cord
    team = held.info.team
    king = held.info.king
    all_stone = team1.sprites() + team2.sprites() + corpses.sprites()
    if king:
        if (pos[0] == (cord[0] + 2)%8 or pos[0] == (cord[0] - 2)%8) and \
            (pos[1] == cord[1] + 2 or pos[1] == cord[1] - 2):
            for stone in all_stone:
                if stone.info.team != team:
                    if stone.info.cord == [(cord[0]+1)%8, cord[1]+1] and pos == [(cord[0]+2)%8, cord[1]+2] or \
                       stone.info.cord == [(cord[0]-1)%8, cord[1]+1] and pos == [(cord[0]-2)%8, cord[1]+2] or \
                       stone.info.cord == [(cord[0]+1)%8, cord[1]-1] and pos == [(cord[0]+2)%8, cord[1]-2] or \
                       stone.info.cord == [(cord[0]-1)%8, cord[1]-1] and pos == [(cord[0]-2)%8, cord[1]-2]:
                        held.eating = True
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
                            held.eating = False
                        return True
        else:
            return False
    else:
        if (pos[0] == (cord[0] + 2)%8 or pos[0] == (cord[0] - 2)%8) and \
            pos[1] == cord[1] + ((2)if(team == 1)else(-2)):
            for stone in all_stone:
                if stone.info.team != team:
                    if team == 1 and \
                       (stone.info.cord == [(cord[0]+1)%8, cord[1]+1] and pos == [(cord[0]+2)%8, cord[1]+2] or \
                       stone.info.cord == [(cord[0]-1)%8, cord[1]+1] and pos == [(cord[0]-2)%8, cord[1]+2]) or \
                       team == 2 and \
                       (stone.info.cord == [(cord[0]+1)%8, cord[1]-1] and pos == [(cord[0]+2)%8, cord[1]-2] or \
                       stone.info.cord == [(cord[0]-1)%8, cord[1]-1] and pos == [(cord[0]-2)%8, cord[1]-2]):
                        held.eating = True
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
                            held.eating = False
                        return True
        else:
            return False

# return a max eat path of main_stone
def max_eat(main_stone, team1, team2, corpses):
    l = 0
    tmp_path = [];
    t1_p = [x.cord for x in team1]
    t2_p = [x.cord for x in team2]
    cp_p = [x.cord for x in corpses]
    total_p = [cp_p, t1_p, t2_p]
    total_p[main_stone.team].remove(main_stone)
    stack = [(main_stone.cord, [], total_p)]
    #stack = [(main_stone.info.cord, [], team1, team2, corpses)];
    #print("=======MAX_EAT : {0}=======".format(main_stone.info.cord))
    D = None
    if main_stone.king :
        D = [[2, 2], [2, -2], [-2, 2], [-2, -2]] #direction
    elif main_stone.team == 1 :
        D = [[2, 2], [-2, 2]]
    else :
        D = [[2, -2], [-2, -2]]
    a = None
    while(len(stack) > 0):
        a = stack.pop()
        #print("get :{0}".format(a[0]))
        for d in D:
            next_step = [(d[0] + a[0][0]) % 8, d[1] + a[0][1]]
            #print("try go {0}".format(next_step))
            #t1, t2, cp = copy.deepcopy(a[2]), copy.deepcopy(a[3]), copy.deepcopy(a[4])
            t1, t2, cp = copy.deepcopy(a[2][1]), copy.deepcopy(a[2][2]), copy.deepcopy(a[2][0])
            stones = t1 + t2 + cp
            if next_step not in stones and next_step[1] >= 0 and next_step[1] <= 7:
                #print("\t next_step OK.")
                eaten= [(int(d[0]/2) + a[0][0]) % 8, int(d[1] / 2) + a[0][1]]
                #eaten = get_stone(cross, stones)
                #print("eat ?{0}".format(eaten))
                if eaten in stones and eaten not in a[2][main_stone.team] :
                    #print("\t~eat ok~")
                    if eaten in t1:
                        t1.remove(eaten)
                        cp.append(eaten)
                    elif eaten in t2:
                        t2.remove(eaten)
                        cp.append(eaten)
                    else:
                        cp.remove(eaten)
                    #print("corpses : {0}".format(cp))
                    tmp_path.append(a[1] + [next_step])
                    l = max(l, len(a[1]) + 1)
                    stack.append((next_step, a[1] + [next_step], [cp,t1,t2]))
    #print(len(tmp_path))
    if len(tmp_path) == 0 :
        return []
    tmp_path = sorted(tmp_path, key = lambda x : -len(x))
    path = []
    for i in range(0, len(tmp_path)):
        #print("len path {0} : {1}".format(i, len(tmp_path[i])))
        if len(tmp_path[i]) == l :
            path.append(tmp_path[i])
        else :
            break
    return path

# check if move is legal
# return [num, path], path is [] if move illegal
# num is 1 if normal move, pathlen+1 if eat move
def can_move_normal(stone_info, pos, team1_info, team2_info, corpses_info):
    all_info = team1_info + team2_info + corpses_info
    normal_list = normal_move2(stone_info, all_info)
    occupied = False
    
    for info in all_info:
        if info.cord == pos:
            occupied = True

    if occupied:
        return 0
    elif pos in normal_list:
        return 1
    else:
        return 0

# check if move is legal(move if legal), return a int
# return    : 1 if move legal, 0 if illegal, -1 if move to origin(no move at all)
def move_if_legal(held, pos, team1, team2, corpses):
    all_stone = team1.sprites() + team2.sprites() + corpses.sprites()
    if not held.eating and pos == held.info.cord:
        held.move_to([pos[0], pos[1]])
        return -1
    elif occupied(pos, all_stone):
        return 0
    elif not held.must_eat and normal_move(held, pos):
        held.move_to([pos[0], pos[1]])
        return 1
    elif eat_move(held, pos, team1, team2, corpses):
        return 1
    else:
        return 0
