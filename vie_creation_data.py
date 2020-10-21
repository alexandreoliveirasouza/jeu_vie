# -*- coding: utf-8 -*-
"""
Created on Sun Oct  4 15:32:12 2020

@author: alexo
"""

#Ce script crée un fichier appelé data_test, si vous voulez le changer complétement il faut le supprimer 
#sinon on va juste ecrire à la suite 
#Il faut paramettrer n et p comme souhaité 

import random
import pickle 
import numpy as np 


"""Param"""

n, p = 100, 100;


""" Fonction d'évolution du jeu de la vie """


def nb_voisins(i,j,tab):
    """ Calcule le nb de voisins de la cellule(i,j)
    Entrée : une cellule dans un tableau à deux dimension
    Sortie : le nb de cellules voisines """ 

    nb = 0
    # Voisin en haut à gauche
    if (i>0) and (j>0) and (tab[i-1][j-1] != 0):
        nb += 1
    # Voisin juste au-dessus
    if (i>0) and (tab[i-1][j] != 0):
        nb += 1
    # Voisin en haut à droite
    if (i>0) and (j<p-1) and (tab[i-1][j+1] != 0):
        nb += 1
    # Voisin juste à gauche
    if (j>0) and (tab[i][j-1] != 0):
        nb += 1
    # Voisin juste à droite
    if (j<p-1) and (tab[i][j+1] != 0):
        nb += 1
   # Voisin en bas à gauche
    if (i<n-1) and (j>0) and (tab[i+1][j-1] != 0):
        nb += 1
    # Voisin juste en-dessous
    if (i<n-1) and (tab[i+1][j] != 0):
        nb += 1
    # Voisin en bas à droite
    if (i<n-1) and (j<p-1) and (tab[i+1][j+1] != 0):
        nb += 1

    return nb


def evolution(tab):
    nouv_tab = [[0 for j in range(p)] for i in range(n)]

    for j in range(p):
        for i in range(n):
            # Cellule vivante ou pas ?
            if tab[i][j] != 0:
                cellule_vivante = True
            else:
                cellule_vivante = False

            # Nombres de voisins
            nb = nb_voisins(i,j,tab)

            # Règle du jeu 
            if cellule_vivante == True and (nb == 2 or nb == 3):
                nouv_tab[i][j] = 1
            if cellule_vivante == False and nb == 3:
                nouv_tab[i][j] = 1
    
    return nouv_tab

""" Tableau initiaux aleatoires ou avec des schemas connus """

def remplissage(tableau):
    a = len(tableau)
    b = len(tableau[0])
    taux = 0 
    nb_noir = 0
    nb_tot = (a-2)*(b-2)
    for i in range(1,a-1):
        for j in range(1,b-1):
            if tableau[i][j]==1:
                nb_noir+=1 
    taux = nb_noir/nb_tot 
    return taux



def aleatoire():
    #crée des cellules aleatoires au centre du tableau pour permettre la propagation 
    tableau = [[0 for j in range(0,p)] for i in range(0,n)] 
    while remplissage(tableau)<0.4:
        for i in range(n):
            tableau[random.randint(2,n-3)][random.randint(2,p-3)]=1
    return(tableau)


def clignotant():
    tableau = [[0 for j in range(p)] for i in range(n)] 
    tableau[4][7] = 1
    tableau[4][8] = 1
    tableau[4][9] = 1
    return(tableau)

# Vaisseau
def vaisseau():
    tableau = [[0 for j in range(p)] for i in range(n)] 
    tableau[3][4] = 1
    tableau[3][5] = 1
    tableau[3][6] = 1
    tableau[2][6] = 1
    tableau[1][5] = 1
    return(tableau)


# Pentadecathlon
def pentadecathlon():
    tableau = [[0 for j in range(p)] for i in range(n)] 
    tableau[6][4] = 1
    tableau[6][5] = 1
    tableau[6][7] = 1
    tableau[6][8] = 1    
    tableau[6][9] = 1
    tableau[6][10] = 1
    tableau[6][12] = 1
    tableau[6][13] = 1  
    tableau[5][6] = 1
    tableau[7][6] = 1
    tableau[5][11] = 1
    tableau[7][11] = 1 
    return(tableau)


def canon():
    tableau = [[0 for j in range(p)] for i in range(n)] 
    tableau[7][1] = 1
    tableau[7][2] = 1
    tableau[8][1] = 1
    tableau[8][2] = 1
    tableau[3][25] = 1
    tableau[4][23] = 1
    tableau[4][25] = 1
    tableau[5][13] = 1
    tableau[5][14] = 1
    tableau[5][21] = 1
    tableau[5][22] = 1
    tableau[5][35] = 1
    tableau[5][36] = 1
    tableau[5][13] = 1
    tableau[6][12] = 1
    tableau[6][16] = 1
    tableau[6][21] = 1
    tableau[6][22] = 1
    tableau[6][35] = 1
    tableau[6][36] = 1
    tableau[7][11] = 1
    tableau[7][17] = 1
    tableau[7][21] = 1
    tableau[7][22] = 1
    tableau[8][11] = 1
    tableau[8][15] = 1
    tableau[8][17] = 1
    tableau[8][18] = 1
    tableau[8][23] = 1
    tableau[8][25] = 1
    tableau[9][11] = 1
    tableau[9][17] = 1
    tableau[9][25] = 1
    tableau[10][12] = 1
    tableau[10][16] = 1
    tableau[11][13] = 1
    tableau[11][14] = 1
    return(tableau)

def ruche():
    global tableau
    tableau = [[0 for j in range(p)] for i in range(n)]
    tableau[21][25] = 1
    tableau[21][26] = 1
    tableau[22][24] = 1
    tableau[22][27] = 1    
    tableau[23][25] = 1
    tableau[23][26] = 1
    return(tableau)

def bloc():
    global tableau
    tableau = [[0 for j in range(p)] for i in range(n)]
    tableau[20][20] = 1
    tableau[21][20] = 1
    tableau[20][21] = 1
    tableau[21][21] = 1
    return(tableau)

def bateau():
    global tableau
    tableau = [[0 for j in range(p)] for i in range(n)]
    tableau[20][20] = 1
    tableau[21][20] = 1
    tableau[20][21] = 1
    tableau[21][22] = 1
    tableau[22][21] = 1
    return(tableau)

def galaxie():
    global tableau
    tableau = [[0 for j in range(p)] for i in range(n)]
    tableau[12][20] = 1
    tableau[12][21] = 1
    tableau[12][22] = 1
    tableau[12][23] = 1
    tableau[12][24] = 1
    tableau[12][25] = 1
    tableau[12][27] = 1
    tableau[12][28] = 1
    tableau[13][20] = 1
    tableau[13][21] = 1
    tableau[13][22] = 1
    tableau[13][23] = 1
    tableau[13][24] = 1
    tableau[13][25] = 1
    tableau[13][27] = 1
    tableau[13][28] = 1
    tableau[14][27] = 1
    tableau[14][28] = 1
    tableau[15][20] = 1
    tableau[15][21] = 1
    tableau[15][27] = 1
    tableau[15][28] = 1
    tableau[16][20] = 1
    tableau[16][21] = 1
    tableau[16][27] = 1
    tableau[16][28] = 1
    tableau[17][20] = 1
    tableau[17][21] = 1
    tableau[17][27] = 1
    tableau[17][28] = 1
    tableau[18][20] = 1
    tableau[18][21] = 1
    tableau[19][20] = 1
    tableau[19][21] = 1
    tableau[19][23] = 1
    tableau[19][24] = 1
    tableau[19][25] = 1
    tableau[19][26] = 1
    tableau[19][27] = 1
    tableau[19][28] = 1
    tableau[20][20] = 1
    tableau[20][21] = 1
    tableau[20][23] = 1
    tableau[20][24] = 1
    tableau[20][25] = 1
    tableau[20][26] = 1
    tableau[20][27] = 1
    tableau[20][28] = 1
    return(tableau)

""" fonction qui permettent la creation du jeu de données """

def sequence(tableau,nb_tours):
    #fonction qui appelle nb_tours fois l'evolution d'un tableau puis 
    #donne en sortie une liste contenant toutes les evolution du tableau
    seq = list()
    for i in range(0,nb_tours):
        seq.append(tableau)
        tableau = evolution(tableau)
    return(seq)

def creation_data(nb_sequences,nb_tours):
    # fonction qui va appeler sequence nb_sequences fois et remplir le fichier de data à chaque fois 
    # nb_tours est le nombre de tours dans les séquences
    with open("data_test", 'ab') as file:
        for i in range(nb_sequences):
            fonct = random.randint(8,10)
            if fonct == 0:
                seq = sequence(clignotant(),nb_tours)
            if fonct == 1:
                seq = sequence(vaisseau(),nb_tours)
            if fonct == 2 and n>40 :
                seq = sequence(canon(),nb_tours)
            if fonct == 3 and n>40 :
                seq = sequence(pentadecathlon(),nb_tours)
            if fonct == 4 and n>40 :
                seq = sequence(ruche(),nb_tours)
            if fonct == 5 and n>40 :
                seq = sequence(bloc(),nb_tours)
            if fonct == 6 and n>40 :
                seq = sequence(bateau(),nb_tours)
            if fonct == 7 and n>40 :
                seq = sequence(galaxie(),nb_tours)
            else: 
                seq = sequence(aleatoire(),nb_tours)
            pickle.dump(seq, file)

"""Main """


nb_sequence = 1000
nb_tours = 2
creation_data(nb_sequence,nb_tours)



















