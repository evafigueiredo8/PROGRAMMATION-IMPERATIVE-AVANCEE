import numpy as np

import math
import copy

sudoku = np.loadtxt('Sudoku.txt')
cases = np.where(sudoku==0)
trouve = False

def ligne(Mat, l):
    return [x for x in sudoku[l,:] if x>0]

def colonne(Mat, c):
    return [x for x in sudoku[:,c] if x>0]

def bloc(Mat, l, c):
    L = []
    for x in range(3*(l//3), 3*(l//3)+3):
        for y in range(3*(c//3), 3*(c//3)+3):
            if Mat[x,y]!=0:
                L.append(Mat[x,y])
    return L

def conflits(Mat, l, c):
    return set([x for x in sudoku[l,:] if x>0] + colonne(Mat, c) + bloc(Mat,l,c))

def fill_sudoku(num):
    global sudoku, cases, trouve
    if num==len(cases[0]):
        trouve = True
        return
    conf = conflits(sudoku, cases[0][num], cases[1][num])
    for e in range(1,10):
        if e not in conf:
            sudoku[cases[0][num], cases[1][num]]=e
            fill_sudoku(num+1)
            if trouve:
                return
            sudoku[cases[0][num], cases[1][num]]=0

fill_sudoku(0)
def fichier_sudoku(fichier):
    np.savetxt(fichier, sudoku, fmt='%d', delimiter=' ')

if trouve:
    fichier_sudoku("solution_sudoku.txt")