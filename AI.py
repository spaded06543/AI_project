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
    """
    for [stone, successor] in move_list:
        print("stone ",stone.info.cord,", possible move ",successor)
    """
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
        
# Initial call
#alphabeta(origin, depth, float("-inf"), float("inf"), True)