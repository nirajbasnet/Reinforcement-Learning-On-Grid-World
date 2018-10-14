import World
import threading
import time
import random
import math


class Qlearning:
    def __init__(self):
        self.discount=0.90
        self.epsilon=0.1
        self.alpha = 0.2
        self.actions = World.actions
        self.states = []
        self.Q = {}
        self.bias=1.0
        self.weights=[0.1,0.1]
        for i in range(World.x):
            for j in range(World.y):
                self.states.append((i, j))

        for state in self.states:
            temp = {}
            for action in self.actions:
                temp[action] = 0.1
                World.set_cell_score(state, action, temp[action])
            self.Q[state] = temp

        for (i, j) in World.targets:
            for action in self.actions:
                self.Q[(i, j)][action] = 1                                 #score for reaching the target
                World.set_cell_score((i, j), action, 1)


    def do_action(self,action):
        s = World.player[0]
        r = -World.score
        World.try_move(World.characters[0], action)
        s2 = World.player[0]
        r += World.score
        return s, action, r, s2

    def manhattandistance(self,s2,s):
        delta = (s2[0] - s[0], s2[1] - s[1])
        dis=abs(delta[0])+abs(delta[1])
        if dis==0:
            return 1.0
        else:
            return (1.0/dis)

    def get_qvalue(self,s,a):
        dx, dy = World.map_action_commands(a)
       # print("delta=",dx,dy)
        new_s=(s[0]+dx,s[1]+dy)
       # print("new_state=",new_s)
        dist=self.manhattandistance(World.targets[0],new_s)
       # print("mandis=",dist)
        sum_feature=self.weights[0]*self.bias+self.weights[1]*dist
        return sum_feature


    def max_Q(self,s):
        maxQValue = float('-inf')
        for a in World.actions:
            value=self.get_qvalue(s,a)
           # print("values",a,value)
            if value>maxQValue:
                maxQValue=value
                maxact=a
       # print("maximum value=",maxact,maxQValue)
        return maxact,maxQValue


    def inc_Q(self,s, a, alpha, inc):
        self.Q[s][a] *= 1 - alpha
        self.Q[s][a] += alpha * inc
        World.set_cell_score(s, a, self.Q[s][a])

    def find_best_action(self,state):
        if(random.random()<self.epsilon):
           # print("random action")
            act=random.choice(World.actions)
        else:
           # print("maxq")
            act,val=self.max_Q(state)
        return act


    def run(self):
        time.sleep(1)
        t = 1
        while True:
            # Choosing the best action at current state and executing it
            s = World.player[0]
            World.try_move(World.characters[2], random.choice(World.actions))
            max_act=self.find_best_action(s)
            #print("first stage",max_act)
            (s, a, r, s2) = self.do_action(max_act)

            # Update Q
            max_act, max_val = self.max_Q(s2)
            # self.inc_Q(s, a, alpha, r + self.discount * max_val)

            difference = (r + self.discount * max_val) - self.get_qvalue(s,a)
            self.weights[0] += self.alpha * difference * 1.0       #for bias feature
            self.weights[1] += self.alpha * difference * self.manhattandistance(World.targets[0],s)   #for distance feature

            # Check if the game has restarted
            t += 1.0
            # World.check_target()
            if World.has_restarted():
                World.restart_game()
                time.sleep(0.01)
                t = 0.3

            # Update the learning rate
            #self.alpha = self.alpha*0.98

            time.sleep(0.1)

if __name__== "__main__":
    qlearning = Qlearning()
    t = threading.Thread(target=qlearning.run)
    t.daemon = True
    t.start()
    World.start_game()