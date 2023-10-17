import numpy as np
import copy

data = np.loadtwt('sac a dos.txt', dtype=int)

data = np.delete(data, (0), axis=1)

def dynamique(Weight):
    Cpre = [0]*(Weight+1)
    SacPre = [[]]*(Weight+1)
    for i in range(len(data)):
        C = [0]*(Weight+1)
        Sac = []
        for w in range(Weight+1):
            if poids>w or Cpre[w] > Cpre[w-poids]+cout:
                C[w] = Cpre[w]
                Sac.append(list(SacPre[w]))
            else:
                C[w]=Cpre[w-poids]+cout
                Sac.append(list(SacPre[w-poids]))
                Sac[-1].append(i)
        Cpre = copy.deepcopy(C)
        SacPre = copy.deepcopy(Sac)
    return Sac, C

Sac, C = dynamique(15)