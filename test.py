import math
def manhattandistance(s2, s):
    temp = (s2[0]-s[0],s2[1]-s[1])
    dis = abs(temp[0]) + abs(temp[1])
    if dis == 0:
        return 1
    else:
        return (1 / dis)

s2=(3,3)
s=(1,5)
dist=manhattandistance(s2,s)
print(dist)