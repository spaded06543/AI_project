from Rules import *
from Functions import *
import copy
import threading
from queue import Queue

def virtual_move(stone_small, act_list, t1, t2, cp):
    D = [1, -1, 7, -7]
    shift = ((act_list[0][0] - stone_small.cord[0]) % 8)*(act_list[0][1] - stone_small.cord[1])
    #print("shift {0}, {1}".format((act_list[0][0] - stone_small.cord[0]) % 8,act_list[0][1] - stone_small.cord[1]))
    if shift in D:
        pass
        #normal move:
    else :
        all_stone = t1 + t2 + cp 
        pre = stone_small.cord
        for i in range(0, len(act_list)):
            next = act_list[i]
            cross = [(next[0]+pre[0])/2, (next[1]+pre[1])/2]
            if (next[0] - pre[0]) in [6, -6] :
                cross[0] = (cross[0] + 4) % 8
            get_eaten = [x for x in t1 + t2 + cp if x.cord == cross]
            #print("eaten {0}".format(get_eaten))
            eaten = get_eaten[0]
            if eaten == None:
                print("Error for remove eaten stone")
            else :
                if eaten in cp :
                    cp.remove(eaten)
                else:
                    if eaten.team == 1:
                        t1.remove(eaten)
                    else :
                        t2.remove(eaten)
                    cp.append(eaten)
            pre = next
    stone = [x for x in (t1 + t2) if stone_small.cord == x.cord][0]
    #print("~~~~{0}~~~~".format(stone))
    if stone == None:
        print("==============ERROR==============")
    stone.cord = act_list[len(act_list) - 1]
    if stone.cord[1] + stone.team * 7 == 14:
        stone.king = True

def minimax(team, weight, t1, t2, cp, depth, maximizingPlayer):
    state = copy.deepcopy(t1 + t2 + cp)
    if gameover_light(team, t1, t2, cp):
        if maximizingPlayer:
            return -10000
        else:
            return 10000
    elif depth == 0 :
        sum = weight[0] * heuristic(state, team) + weight[1] * stone_gap(t1, t2) + weight[2] * king_stone_gap(t1, t2)
        su = get_successors(team, t1, t2, cp)
        sum += weight[3] * max_path_len(su) + weight[4] * number_path(su)
        return sum

    if maximizingPlayer:
        bestValue = -10000
        for move_list in get_successors ( 3 - team, t1, t2, cp ) :
            for move_path in move_list[1]:
                t1_next = copy.deepcopy(t1)
                t2_next = copy.deepcopy(t2)
                cp_next = copy.deepcopy(cp)
                virtual_move(move_list[0], move_path, t1_next, t2_next, cp_next)
                val = minimax ( 3 - team, weight, t1_next, t2_next, cp_next, depth - 1, False )
                bestValue = max(bestValue, val)
        return bestValue
    else :
        bestValue = 10000
        for move_list in get_successors ( 3 - team, t1, t2, cp ) :
            for move_path in move_list[1]:
                t1_next = copy.deepcopy(t1)
                t2_next = copy.deepcopy(t2)
                cp_next = copy.deepcopy(cp)
                virtual_move(move_list[0], move_path, t1_next, t2_next, cp_next)
                val = minimax ( 3 - team, weight, t1_next, t2_next, cp_next, depth - 1, True ) 
                bestValue = min(bestValue, val)
        return bestValue  
    
def alphabeta(team, weight, t1, t2, cp, depth, alpha, beta, maximizingPlayer):
    state = copy.deepcopy(t1 + t2 + cp)
    if gameover_light(team, t1, t2, cp):
        if maximizingPlayer:
            return -10000
        else:
            return 10000
    elif depth == 0 :
        sum = weight[0] * heuristic(state, team) + weight[1] * stone_gap(t1, t2) + weight[2] * king_stone_gap(t1, t2)
        su = get_successors(team, t1, t2, cp)
        sum += weight[3] * max_path_len(su) + weight[4] * number_path(su)
        return sum

    if maximizingPlayer:
        v = -10000
        for move_list in get_successors(3 - team, t1, t2, cp):
            for move_path in move_list[1]:
                t1_next = copy.deepcopy(t1)
                t2_next = copy.deepcopy(t2)
                cp_next = copy.deepcopy(cp)
                virtual_move(move_list[0], move_path, t1_next, t2_next, cp_next)
                v = max(v, alphabeta(3 - team, weight, t1_next, t2_next, cp_next, depth - 1, alpha, beta, False))
                #print("max", depth, v)
                alpha = max(alpha, v)
                if beta <= alpha: # beta cut-off
                    break
        #print("max", depth, v, "final")
        return v
    else:
        v = 10000
        #childs = child of state
        for move_list in get_successors(3 - team, t1, t2, cp):
            for move_path in move_list[1]:
                t1_next = copy.deepcopy(t1)
                t2_next = copy.deepcopy(t2)
                cp_next = copy.deepcopy(cp)
                virtual_move(move_list[0], move_path, t1_next, t2_next, cp_next)
                v = min(v, alphabeta(3 - team, weight, t1_next, t2_next, cp_next, depth - 1, alpha, beta, True))
                #print("min", depth, v)
                beta = min(beta, v)
                if beta <= alpha: # beta cut-off
                    break
        #print("min", depth, v, "final")
        return v

class AI():
    def __init__(self, team, strategy = alphabeta ):
        self.strategy = strategy
        self.team = team
    
    def set_team(self, team):
        self.team = team
        
    def set_strategy(self, strategy):
        if not stratetegy == None:
            self.strategy = strategy
            
    def move_stone(self, stone, act_list, team1, team2, corpses):
        D = [1, -1, 7, -7]
        shift = ((act_list[0][0] - stone.info.cord[0]) % 8)*(act_list[0][1] - stone.info.cord[1])
        true_stone = [x for x in team1.sprites() + team2.sprites() if x.info.cord == stone.info.cord][0]
        if shift in D:
            stone.move_to(act_list[0])
            true_stone.move_to(act_list[0])    
            yield
            #normal move:
        else :
            all_stone = team1.sprites() + team2.sprites() + corpses.sprites() 
            pre = stone.info.cord
            for i in range(0, len(act_list)):
                next = act_list[i]
                true_stone.move_to(next) # move stone
                cross = [(next[0]+pre[0])/2, (next[1]+pre[1])/2]
                if (next[0] - pre[0]) in [6, -6] :
                    cross[0] = (cross[0] + 4) % 8
                eaten = get_stone(cross, all_stone)
                if eaten == None:
                    print("Error for remove eaten stone")
                else :
                    if eaten in corpses :
                        eaten.kill()
                    else:
                        eaten.die(corpses)
                pre = next
                yield
            #eating move
    
   
    def get_action(self, weight, team1, team2, corpses, depth = 4):
        team = None
        if self.team == 1:
            team = [x.info for x in team1]
        else:
            team = [x.info for x in team2]
        t1 = [x.info for x in team1]
        t2 = [x.info for x in team2]
        cp = [x.info for x in corpses]
        alpha = float("-inf")
        beta = float("inf")
        best_act = None
        for move_list in get_successors(self.team, t1, t2, cp):
            for move_path in move_list[1]:
                t1_next = copy.deepcopy(t1)
                t2_next = copy.deepcopy(t2)
                cp_next = copy.deepcopy(cp)
                #print("move list {0}, {1}".format(move_list[0].cord, move_path))
                virtual_move(move_list[0], move_path, t1_next, t2_next, cp_next)
                #tmp_max = self.strategy(3 - self.team, weight, t1_next, t2_next, cp_next, depth, False)
                # ^^^ this is minimax ^^^
                tmp_max = self.strategy(3 - self.team, weight, t1_next, t2_next, cp_next, depth, alpha, beta, False)
                if tmp_max > alpha :
                    alpha = tmp_max
                    best_act = [move_list[0], move_path]
        print("choose", alpha)
        stone_list = [corpses, team1, team2]
        act_stone = [x for x in stone_list[self.team] if x.info == best_act[0]][0]
        for i in self.move_stone(act_stone, best_act[1], team1, team2, corpses) :
            yield
    def get_action_light(self, weight, t1, t2, cp, depth = 4):
        team = None
        if self.team == 1:
            team = t1
        else:
            team = t2
        alpha = float("-inf")
        beta = float("inf")
        #print("==team {0}==".format(self.team))
        best_act = None
        for move_list in get_successors(self.team, t1, t2, cp):
            for move_path in move_list[1]:
                #print(move_list[0].cord, move_path)
                t1_next = copy.deepcopy(t1)
                t2_next = copy.deepcopy(t2)
                cp_next = copy.deepcopy(cp)
                #print("move list {0}, {1}".format(move_list[0].cord, move_path))
                virtual_move(move_list[0], move_path, t1_next, t2_next, cp_next)
                tmp_max = self.strategy(3-self.team, weight, t1_next, t2_next, cp_next, depth, alpha, beta, False)
                #print("act evaluation : {0}".format(tmp_max))
                if tmp_max > alpha :
                    alpha = tmp_max
                    best_act = [move_list[0], move_path]
        #print("choose", alpha)
        if best_act == None :
            return -1
        virtual_move(best_act[0], best_act[1], t1, t2, cp)
        #if best_act[0].cord[0] - best_act[1].cord[0] > 1 :
        #    print("---eat---")
        return 1
        # find best path to move
        # move the stone
# Initial call
#alphabeta(origin, depth, float("-inf"), float("inf"), True)