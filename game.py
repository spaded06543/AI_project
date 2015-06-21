from AI import *
from GameClass import *
import sys, random
class player():
    def __init__(self, id, agent, weight):
        self.id = id
        self.agent = agent
        self.win = 0
        self.weight = weight
    def set_weight(self, weight):
        self.weight = weight
    def reset_win(self):
        self.win = 0
class game():
    def __init__(self, p1, p2):
        p1.agent.set_team(1)
        p1.agent.set_team(2)
        self.player = [p1, p2]
        
        self.stones = [[], [], []]
        for i in range(12):
            pos = [ ((i%4)*2)if(i>3 and i<8)else((i%4)*2+1) , (0)if(i<4)else((1)if(i<8)else(2))]
            s = Stone_light(pos, 1, False)
            #s.become_king()
            self.stones[1].append(s)
        for i in range(12):
            pos = [ ((i%4)*2+1)if(i>3 and i<8)else((i%4)*2) , (5)if(i<4)else((6)if(i<8)else(7))]
            s = Stone_light(pos, 2, False)
            #s.become_king()
            self.stones[2].append(s)
        #print(self.stones[1],self.stones[2])
    def run(self, turn):
        count = 0
        flag = False
        lose = 0
        while count < turn:
            count += 1
            for i in range(2):
                ret = self.player[i].agent.get_action_light(self.player[i].weight, self.stones[1], self.stones[2], self.stones[0])
                if ret == -1:
                    flag = True
                    win_team = 0 if i == 1 else 1
                    self.player[win_team].win += 1
                    print("player {0} win".format(self.player[win_team].id))
                    break
            if flag :
                break
        
        if count == turn:
            t1_stone = len(self.stone[1])
            t2_stone = len(self.stone[2])
            if t1_stone > t2_stone :
                print("player {0} win".format(self.player[0].id))
                self.player[0].win += 1
            elif t1_stone < t2_stone :
                print("player {0} win".format(self.player[1].id))
                self.player[1].win += 1
            
if __name__ == "__main__":
    if len(sys.argv) < 2 :
        print("Usage : game.py [generation] [play_turn]")
        sys.exit()
    play_turn = int(sys.argv[2])
    generation = int(sys.argv[1])
    
    playerList = []
    ai = AI(0)
    playerList.append(player(1, ai, [3, 15, 10, 20, 5]))
    ai = AI(0)
    playerList.append(player(2, ai, [3, 10, 20, 10, 7]))
    ai = AI(0)
    playerList.append(player(3, ai, [10, 3, 7, 5, 2]))
    ai = AI(0)
    playerList.append(player(4, ai, [3, 13, 9, 14, 4]))
    for i in range(6):
        w = []
        for j in range(5):
            w.append(random.randint(1, 30))
        ai = AI(0)
        playerList.append(player(i + 5, ai, w))
    
    for i in range(generation):
        print("generation : {0}".format(i+1))
        for j in range(10):
            playerList[j].win = 0
        for j in range(10):
            for k in range(j+1,10):
                g = game(playerList[j], playerList[k])
                g.run(play_turn)
                
        playerList = sorted(playerList, key = lambda x : -(x.win))
        id = 4
        
        for j in range(10):
            print("player {0} : {1}".format(playerList[j].id, playerList[j].win))
            playerList[i].reset_win()
        for j in range(4):
            for k in range(j+1,4):
                w = [0, 0, 0, 0, 0]
                for l in range(5):
                    w[l] = playerList[j].weight[l] + playerList[k].weight[l] + random.randint(-3,3)
                playerList[id].set_weight(weight)
                id += 1
        
        
    for i in range(4):
        print("AI {0}, weight : {1}".format(i, playerList[i].weight))
        