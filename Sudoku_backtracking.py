import numpy as np
import math

class CSP():
    def __init__(self, file_name):
        self.grille = np.loadtxt(file_name)
        self.toFill = []
        self.domaines = []
        self.size = len(self.grille)

    def constrains(self, x, y):
        libres = []
        occupees = []
        #Parcours de la ligne
        for l in range(len(self.size)):
            if l == x : continue
            if self.grille[x,l]==0: libres.append((x,l))
            else : occupees.append((x,l))
        #Parcours des colonnes
        for c in range(len(self.size)):
            if c == x : continue
            if self.grille[c,y]==0 : libres.append((c,y))
            else : occupees.append((c,y))
        #Parcours des blocs
        for l in range(3*(x//3), 3*(x//3)+3):
            for c in range(3*(y//3), 3*(y//3)+3):
                if (l == x) or (c == x) : continue
                if self.grille[l,c]!=0 : libres.append(self.grille[l,c])
                else : occupees.append((l,c))
        return libres, occupees

    def accepte(self):
        domaine = []
        for s in self.toFill:
            lirbes, occupees, = self.constrains(s[0],s[1])
            values = []
            for x in occupees :
                values.append(self.grille[x[0],x[1]])
            domaine.append([x for x in range(1, self.size + 1) if x not in values])
        return domaine

    def MRV(self):
        cases = np.where(sudoku==0)
        self.toFill = [(x,y) for x,y in zip(cases[0],cases[1])]
        return cases
    
sudoku = CSP('Sudoku.txt')
domaine = sudoku.MRV()