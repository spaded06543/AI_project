from Rules import *
from Functions import *

def ai_action(team1, team2, corpses, must_list):
    print("start printing all possible moves")
    if must_list:
        for stone in must_list:
            successors = get_successors(stone, team1, team2, corpses)
            print("stone ",stone.info.cord,", possible move ",successors)
    else:
        for stone in team2.sprites():
            successors = get_successors(stone, team1, team2, corpses)
            print("stone ",stone.info.cord,", possible move ",successors)
