from Rules import *
from Functions import *

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
    
def alphabeta(team1, team2, corpses, depth, alpha, beta, maximizingPlayer):
    state = copy.deepcopy(team1.sprites() + team2.sprites() + corpses.sprites())
    if depth == 0 or gameover(state):
        return heuristic(state, turn)
    if maximizingPlayer:
        v = float("-inf")
        #childs = child of state
        childs = []
        for child in childs:
            v = max(v, alphabeta(child, depth - 1, alpha, beta, False))
            alpha = max(alpha, v)
            if beta <= alpha: # beta cut-off
                break
        return v
    else:
        v = float("inf")
        #childs = child of state
        childs = []
        for child in childs:
            v = min(v, alphabeta(child, depth - 1, alpha, beta, True))
            beta = min(beta, v)
            if beta <= alpha: # alpha cut-off
                break
        return v

class AI():
    def __init__(self, strategy = alphabeta):
        self.strategy = strategy
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
    def get_action(self, team1, team2, corpses, myteam):
        pass
        # find best path to move
        # move the stone
# Initial call
#alphabeta(origin, depth, float("-inf"), float("inf"), True)