from Rules import *
from Functions import *
import copy
def ai_action(team1, team2, corpses, must_list):
    print("start printing all possible moves")
    move_list = []
    successors = []
    if must_list:
        successors = get_successors(must_list, team1, team2, corpses, True)
    else:
        successors = get_successors(team2.sprites(), team1, team2, corpses, False)
    
    for x in successors:
        print(x[0].info.cord, x[1])
def virtual_move(stone_small, act_list, t1, t2, cp):
    D = [1, -1]
    shift = (act_list[0][0] - stone.cord[0])*(act_list[0][1] - stone.cord[1])
    if shift in D:
        pass
        #normal move:
    else :
        all_stone = t1 + t2 + cp 
        pre = stone.cord
        while(act_list):
            next = act_list.pop()
            cross = [(pre[0]-next[0])/2, (pre[1]-next[1])/2]
            eaten = (x for x in all_stone if x.cord == cross)
            if eaten == None:
                print("Error for remove eaten stone")
            else :
                if eaten.dead :
                    cp.remove(eaten)
                else:
                    if eaten.team = 1:
                        t1.remove(eaten)
                    else
                        t2.remove(eaten)
                    eaten.team = 0
                    cp.append(eaten)
        stone = (x for x in t1 + t2 if stone_small == x)
        stone.cord = act_list[len(act_list) - 1]

def alphabeta(team, t1, t2, cp, depth, alpha, beta, maximizingPlayer):
    state = copy.deepcopy(t1 + t2 + cp)
    if gameover_light(state):
        if turn :
            return float("inf")
        else:
            return -float("inf")
    elif depth == 0 :
        return heuristic(state, team)
    if maximizingPlayer:
        v = float("-inf")
        for move_list in get_successors(team, t1, t2, cp):
            for move_path in move_list[1]:
                t1_next = copy.deepcopy(t1)
                t2_next = copy.deepcopy(t2)
                cp_next = copy.deepcopy(cp)
                virtual_move(move_list[0], move_path, t1_next, t2_next, cp_next)
                v = max(v, alphabeta(3 - team, t1_next, t2_next, cp_next, depth - 1, alpha, beta, False))
                alpha = max(alpha, v)
                if beta <= alpha: # beta cut-off
                    break
        return v
    else:
        v = float("inf")
        #childs = child of state
        for move_list in get_successors(team, t1, t2, cp):
            for move_path in move_list[1]:
                t1_next = copy.deepcopy(t1)
                t2_next = copy.deepcopy(t2)
                cp_next = copy.deepcopy(cp)
                virtual_move(move_list[0], move_path, t1_next, t2_next, cp_next)
                v = min(v, alphabeta(3 - team, t1_next, t2_next, cp_next, depth - 1, alpha, beta, True))
                alpha = min(alpha, v)
                if beta <= alpha: # beta cut-off
                    break
        return v

class AI():
    def __init__(self, strategy = alphabeta, team):
        self.strategy = strategy
        self.team = team
        
    def set_strategy(self, strategy):
        if not stratetegy == None:
            self.strategy = strategy
            
    def move_stone(self, stone, act_list, team1, team2, corpses):
        D = [1, -1]
        shift = (act_list[0][0] - stone.info.cord[0])*(act_list[0][1] - stone.info.cord[1])
        if shift in D:
            stone.move_to(act_list[0])
            #normal move:
        else :
            all_stone = team1.sprites() + team2.sprites() + corpses.sprites() 
            pre = stone.info.cord
            while(act_list):
                next = act_list.pop()
                cross = [(pre[0]-next[0])/2, (pre[1]-next[1])/2]
                eaten = get_stone(cross, all_stone)
                if eaten == None:
                    print("Error for remove eaten stone")
                else :
                    if eaten.dead :
                        eaten.kill()
                    else:
                        eaten.die(corpese)
            stone.move_to(act_list[len(act_list) - 1])    
            #eating move
    
            
    def get_action(self, team1, team2, corpses, depth = 2):
        team = None
        if team_number == 1:
            team = [x.info for x in team1]
        else:
            team = [x.info for x in team2]
        t1 = [x.info for x in team1]
        t2 = [x.info for x in team2]
        cp = [x.info for x in corpses]
        alpha = float("-inf")
        beta = float("inf")
        best_act = None
        for move_list in get_successors(self.team, t1, t2, cp, False):
            for move_path in move_list[1]:
                t1_next = copy.deepcopy(t1)
                t2_next = copy.deepcopy(t2)
                cp_next = copy.deepcopy(cp)
                virtual_move(move_list[0], move_path, t1_next, t2_next, cp_next)
                tmp_max = alphabeta(self.team, depth % 2, t1, t2, cp, depth, alpha, beta, False)
                if tmp_max > alpha :
                    alpha = tmp_max
                    best_act = [move_list[0], move_path]
            
        self.move_stone(best_act[0], best_act[1], team1, team2, corpses)
        # find best path to move
        # move the stone
# Initial call
#alphabeta(origin, depth, float("-inf"), float("inf"), True)