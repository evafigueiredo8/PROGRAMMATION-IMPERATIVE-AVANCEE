import numpy as np
import math
import copy

Labyrinthe = np.loadtxt('Laby.txt')
Direction = [(0,1), (1,0), (0,-1),(-1,0)]
a = (Labyrinthe.shape[0]-1, Labyrinthe.shape[1]-1)
trouve = False

e = (0,0)
Labyrinthe[e[0], e[1]] = 1

def acceptable(e, d):
    px = e[0] + d[0]
    py = e[1] + d[1]
    if px >= Labyrinthe.shape[0] or py >= Labyrinthe.shape[1] or px < 0 or py <0 :
        return False
    if Labyrinthe[px, py] == -1 or Labyrinthe[px, py] == 1 :
        return False
    return True

def chercher(a, e) :
    global trouve
    if a[0]==e[0] and a[1]==e[1] :
        trouve = True; return
    for d in Direction :
        if acceptable(e, d) :
            ne = (e[0]+d[0], e[1]+d[1])
            Labyrinthe[ne[0], ne[1]] = 1
            chercher(a, ne)
            if trouve :
                return
            Labyrinthe[ne[0], ne[1]] = 0

nbESolution = math.inf
LabyrintheSolution = copy.deepcopy(Labyrinthe)

def chercherSolution(a, e, nbE) :
    global nbESolution, LabyrintheSolution
    if a[0]==e[0] and a[1]==e[1] :
        if nbE < nbESolution :
            nbESolution = nbE ; LabyrintheSolution = copy.deepcopy(Labyrinthe)
            return
    for d in Direction :
        if acceptable(e, d) :
            ne = (e[0]+d[0], e[1]+d[1])
            Labyrinthe[ne[0], ne[1]] = 1
            chercherSolution(a, ne, nbE+1)
            Labyrinthe[ne[0], ne[1]] = 0


chercherSolution(a,e, 1)