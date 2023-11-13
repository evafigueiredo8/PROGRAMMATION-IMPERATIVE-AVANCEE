#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 24 16:11:34 2023

@author: bisgambiglia_p
"""
import numpy as np
import math

class CSP():
    #Définition et initialisation des propriétés de l'application
    #   1 - Pays contient la liste de Pays ['Portugal', 'Espagne', ....] cette liste est obtenue
    #           a partir de la première ligne du fichier
    #   2 - La liste des Contraintes qui est une matrice (21,21) qui sera obtenue en analysant 
    #           toutes les lignes restantes du tableau 
    #   3 - Les domaines de définition de différents pays, c'est à dire les couleurs qu'ils peuvent 
    #           prendre 
    #   4 - Les valeurs ou couleurs qui sont affectés à chaque pays
    def __init__(self, file_name):
        filin = open(file_name,'r')
        self.Pays=filin.readline().split()
        #Initialisation des Contraintes, des Domaines et des Couleurs 
        self.size = len(self.Pays)
        self.Contraintes = np.zeros( (self.size,self.size), dtype=int)
        self.Domaines = []
        self.Couleurs = [""]*self.size
        #Lecture de toutes les lignes restantes du fichier
        lines = filin.readlines() ; filin.close()
        for line in lines:
            #Pour chaque ligne on se doit de définir le pays d'origine (le premier) et tous ses voisins
            #   Exemple : Andorre Espagne France => Andorre partage une frontière avec la France et l'Espagne.
            pays=line.split() 
            #On l'indice du premier pays
            indX = self.Pays.index(pays[0])
            for y in pays[1:]:
                #Puis pour tous les pays avec lequels indX partage une frontière on récupère son
                #   index et l'on met à pour les contraintes
                indY = self.Pays.index(y)
                self.Contraintes[indX, indY]=1
            self.Domaines.append(['Rouge', 'Vert', 'Bleu', 'Jaune'])
                
    #La méthode MRV recherche quel pays doit être sélectionné en premier. Le choix se porte
    #   dans un premier temps les pays qui ont le plus petit domaine et ensuite sur ceux qui 
    #   partagent le plus de contraintes avec des pays non encore coloriés.
    def MRV(self):
        #On recherche ici les indices des pays qui ne sont pas encore coloriés.
        #Cette instruction est une verison condensée de :
        #   nonAffect = []
        #   for i in range(self.size) :
        #       if self.Couleurs[i]==""
        #           nonAffect.append(i)
        nonAffect = [s for s in range(self.size) if self.Couleurs[s]==""]
        #Si tous les pays sont coloriés on retourne une liste vide qui servira à arreter le récursivité
        if len(nonAffect)==0 : return []
        #On chercher quel est la taille du plus petit domaine des pays non encore affectés 
        #Cette instruction est une verison condensée de :
        #   minMRV = math.inf
        #   for i in nonAffect :
        #       if (len(self.Domaines[i])<minMRV) : minMRV = self.Domaines[i]
        minMRV = min( len(self.Domaines[s]) for s in nonAffect)
        #On peut maintenant ne retenir de nonAffect que les sommets qui ont une taille de leur 
        #   domaine de définition égal à la valeur minMRV
        MRVs = [s for s in nonAffect if len(self.Domaines[s])==minMRV]
        #Si un seul pays est retenu on peut le retourner car le choix est fait
        if len(MRVs)==1 : return MRVs
        #Si plusieurs pays on le même MRV on cherche combiens ils ont de voisins non encore coloriés 
        Degree=[]
        for s in MRVs:
            #Pour chaque pays on doit donc compter le nombre de voisins (de 1) sans prendre en compte
            #   les voisins déjà coloriés
            #Cette instruction est une verison condensée de :
            #   compte=0
            #   for x in range(self.size):
            #      if self.Contraintes[s][x]==1 and self.Couleurs[x]==""
            #                  compte +=1
            #   Degree.append(compte)
            Degree.append(sum(self.Contraintes[s][x] for x in range(self.size) if self.Couleurs[x]==""))
        #Degree contient maintenant le nombre de contraintes pour chaque pays de MRVs
        #On peut donc sélectionner dans MRVs uniquement les pays qui ont le degree max
        DHs = [ MRVs[s] for s in range(len(MRVs)) if Degree[s]==max(Degree) ]
        return DHs
    
    #Cette fonction classe l'ordre dans lequel doivent être choisi les valeurs pour un pays donné (indS)
    #On va choisir en priorité de prendre une coleur qui invalide le moins de valeurs sur ses voisins non encore assignés
    def nextValue(self, indS):
        #On recherche tous les pays qui ont une frontière avec indS et qui ne sont pas encore coloriés
        nonAffect = [s for s in range(self.size) if self.Contraintes[indS][s]!=0 and self.Couleurs[s]==""]
        #Si tous les pays liés à indS sont déjà coloriés on peut choisir n'importe quelle couleur pour indS
        if len(nonAffect)==0 : return self.Domaines[indS]
        #On va chercher pour toutes les couleurs que l'on peut mettre dans indS quelle impact elle aura
        #   sur les pays voisins.
        impact = []
        for color in self.Domaines[indS] : 
            compte = sum(color in self.Domaines[s] for s in nonAffect)
            impact.append(compte)
        #impact va contenir pour chaque couleur le nombre de domaine impacter 
        #Le zip permet de regrouper deux listes ici le nombre de domaines impacté 'impact' par les couleurs de indS
        #La fonction sorted va donc trier ces deux liste par impact (sur les chiffres) puis par domaines (sur les caractères)
        #   On obtient ensuite dans y,x les indices et les couleurs classées de la plus grande à la plus petite (-1)
        #   puis on ne retient que les couleurs (x) qui correspondent à des valeurs positives
        #Exemple si impact=[1,3,-1,2] pour Domaines[indS]=['Rouge', 'Vert', 'Bleu', 'Jaune']
        #   le Sorted va rendre y=[-1,1,2,3] et X=['Bleu','Rouge','Jaune','Vert']
        #   le y!=-1 supprimera de la liste le bleu il restera donc ['Vert','Jaune','Rouge'] à prendre dans cet ordre
        valeursTries = [x for y, x in sorted(zip(impact,self.Domaines[indS]), reverse=True)]
        return valeursTries 

europe=CSP('Europe.txt')
Termine = False

def backtracking_search():
    global europe, Termine
    #On recherche quel pays choisir en premier en fonction du MRV puis du degré
    listeVariables = europe.MRV()
    #S'il n'y a plus de variables à sélectionner on a terminé l'algorithme
    if len(listeVariables)==0 : Termine=True ; return 
    #On choisi un pays au hasard, le premier fait l'affaire 
    S = listeVariables[0]
    #On classe les valeurs à mettre dans S dans l'ordre de l'impact minimum qu'elles peuvent avoir 
    listeValeurs = europe.nextValue(S)
    for V in listeValeurs:
        #On met à jour la couleur de S à la valeur V choisie dans la liste
        europe.Couleurs[S]=V
        #On recherche tous les pays qui seront modifiés par cette affectation, donc tous les voisins
        #   de S qui ont la couleur V dans leur domaine de définition
        #   Pour cela on parcours tous les pays : for x in range(europe.size)
        #       et l'on ne retient que les pays qui sont des voisins de S : europe.Contraintes[S,x]!=0 
        #       qui n'ont pas déjà une couleur : europe.Couleurs[x]==""
        #       et qui on V dans leur domaine : V in europe.Domaines[x]
        domainesModifies = [x for x in range(europe.size) if europe.Contraintes[S,x]!=0 and europe.Couleurs[x]=="" and V in europe.Domaines[x]]
        #On modifie donc les domaines en suppriment la couleur V
        for indS in domainesModifies:
            europe.Domaines[indS].remove(V)
        #Appel résursif
        backtracking_search()
        if (Termine==True) : return
        #Backtrackig : on remet la couleur V dans tous les domaines modifiés
        for indS in domainesModifies:
            europe.Domaines[indS].append(V)
        #On enléve la couleur affectée précédement
        europe.Couleurs[S]=""

backtracking_search()
