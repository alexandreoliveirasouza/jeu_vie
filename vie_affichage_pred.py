# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 11:15:18 2020

@author: alexo
"""
#READ ME :
# Programme qui permet, aores avoir fait l'apprentissage, de "jouer" au jeu de la vie 
#n,p est le nb de case
#echelle permet d'augmenter le nb de cases affichées dans la fenetre
#la fenetre est de taille réglable

import random
import pickle 
import numpy as np


############################################################

import tensorflow as tf


tf.executing_eagerly()

nb_sequences = 1000 #il faut savoir combien on a mis de séquences dans la liste pour que la fonction marche 
"""Lecture et creation de la liste data"""

def lecture(depickled,nb_sequences):
    data = list()
    for  i in range(nb_sequences):
        data_load = depickled.load()
        data.append(data_load)
    return(data)
        
# Chargement
with open("data_test", 'rb') as file:
    depickler = pickle.Unpickler(file)
    data = lecture(depickler,nb_sequences)

depickler = None    

file.close()




input_test= list()
output_test = list()


for i in range(int(nb_sequences*0.8),nb_sequences):
    input_test.append(tf.reshape(tf.convert_to_tensor(np.asarray(data[i][0])[0:100,0:100]),(100,100,1)))
    output_test.append(tf.reshape(tf.convert_to_tensor(np.asarray(data[i][1])[0:100,0:100]),(100,100,1)))
  

input_test = tf.convert_to_tensor(input_test)
output_test = tf.convert_to_tensor(output_test)

model = tf.keras.models.load_model('model_jeu_vie')

# Re-evaluate the model
###################################



n, p = 100, 100;
tableau = [[0 for j in range(p)] for i in range(n)] 
data = list() 

def voir_tableau(tab):
    """ Affiche un tableau à l'écran
    Entrée : un tableau à deux dimension
    Sortie : rien (affichage à l'écran) """    

    for i in range(n):
        for j in range(p):
            print(tab[i][j], end="")
        print()

    return

##################################################
#alors moi j'avais fait différemment de cette fonction de base mais ça mettait 
#parfois des erreurs sur les ranges etc... donc ça m'a soulé, celle la marche
#tout le temps au moins
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

##################################################
#ça c'est juste une fonction d'évolution genre qui suit les regles de base
def evolution(tab):
    global data
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
    
    data.append(nouv_tab)
    return nouv_tab


def prediction(tab):
    tab = tf.reshape(tf.convert_to_tensor(np.asarray(tab)),(1,100,100,1))
    nouv_tab = model.predict(tab)
    return nouv_tab




#Affichage graphique
#utilisation du module tkinter, ya surement mieux mais j'aime bien ça c'est assez
#intuitif et facile à utiliser
#le truc chiant cest que j'arrive pas a l'importer correctement 
#donc faut mettre tkinter. avant chaque commande (comme np. en gros)

import tkinter

echelle = int(600/n) 
# Fenêtre tkinter
root = tkinter.Tk()

canvas = tkinter.Canvas(root, width=(n*echelle+200), height=p*echelle, background="white")
canvas.pack(side=tkinter.LEFT, padx=5, pady=5)

# Echelle PERMET DE JOUER SUR LE NB DE CASES AFFICHEES SUR L'ECRAN


def afficher_lignes():
    """ Affiche la grille à l'écran """    
    for i in range(n+1):
        canvas.create_line(0,i*echelle,p*echelle,i*echelle)
    for j in range(p+1):
        canvas.create_line(j*echelle,0,j*echelle,n*echelle) 
    for i in range(n):
        canvas.create_text(echelle//3,i*echelle+echelle//2,text=str(i)) 
    for j in range(p):        
        canvas.create_text(j*echelle+echelle//2,echelle//3,text=str(j)) 
    return


##################################################

def afficher_tableau(tab):
#cette fonction en gros elle convertit ton tableau de 1 et 0 en affichage 
#c'est tout, et donc ça sert de base pour toutes les structures après
    for i in range(n):
        for j in range(p):
            if tab[i][j] != 0:
                canvas.create_rectangle(j*echelle,i*echelle,(j+1)*echelle,(i+1)*echelle,fill="black")        
    return


# Mise en place des différents boutons qui permettent de générer des structures direct


def action_bouton_evolution():
    global tableau
    tableau = evolution(tableau)
    canvas.delete("all")
    afficher_lignes()
    afficher_tableau(tableau)
    b = int(c.get())
    b=b+1
    c.set(str(b))
    return



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


def binariser(tab):
    size = np.shape(tab)
    for i in range(size[0]):
        for j in range(size[1]):
            if tab[i][j]>0.5:
                tab[i][j] = 1
            if tab[i][j]<=0.5:
                tab[i][j] = 0
    return(tab)


def action_bouton_prediction():
    global tableau
    tableau = prediction(tableau)
    tableau = tf.make_tensor_proto(tableau)
    tableau = tf.make_ndarray(tableau)
    tableau = tableau.reshape(100,100)
    tableau = list(tableau)
    tableau = binariser(tableau)
    canvas.delete("all")
    afficher_lignes()
    afficher_tableau(tableau)
    b = int(c.get())
    b=b+1
    c.set(str(b))
    return




def action_bouton_aleatoire():
    global tableau
    tableau = [[0 for j in range(0,p)] for i in range(0,n)] 
    remp=remplissage(tableau)
    while remp<0.35:
        for i in range(n):
            tableau[random.randint(1,n-2)][random.randint(1,p-2)]=1
        remp=remplissage(tableau)
    canvas.delete("all")      
    afficher_lignes()                    
    afficher_tableau(tableau)
    return
a = 1
def animation():
    global tableau 
    global a 
    
    """  tableau = evolution(tableau)
    canvas.delete("all")      
    afficher_lignes()                    
    afficher_tableau(tableau)"""
    action_bouton_evolution()
    if a>0:
        root.after(100, animation)
    elif a<0:
        a=1
    return 

def animation_prediction():
    global tableau 
    global a 
    
    """  tableau = evolution(tableau)
    canvas.delete("all")      
    afficher_lignes()                    
    afficher_tableau(tableau)"""
    action_bouton_prediction()
    if a>0:
        root.after(100, animation)
    elif a<0:
        a=1
    return 

def stop(): 
    global a 
    global data
    a = -1
    return 
def clearall():
    global tableau
    tableau = [[0 for j in range(p)] for i in range(n)]
    return

def clignotant():
    global tableau
    tableau = [[0 for j in range(p)] for i in range(n)] 
    tableau[4][7] = 1
    tableau[4][8] = 1
    tableau[4][9] = 1
    canvas.delete("all")   
    afficher_lignes()   
    afficher_tableau(tableau)
    return

def clignotant4():
    global tableau
    tableau = [[0 for j in range(p)] for i in range(n)] 
    tableau[12][20] = 1
    tableau[13][19] = 1
    tableau[13][20] = 1
    tableau[13][21] = 1
    tableau[14][20] = 1
    canvas.delete("all")   
    afficher_lignes()   
    afficher_tableau(tableau)
    return

# Vaisseau
def planeur():
    global tableau
    tableau = [[0 for j in range(p)] for i in range(n)] 
    tableau[3][4] = 1
    tableau[3][5] = 1
    tableau[3][6] = 1
    tableau[2][6] = 1
    tableau[1][5] = 1
    
    afficher_lignes()   
    afficher_tableau(tableau)
    return

def vaisseau():
    global tableau
    """tableau = [[0 for j in range(p)] for i in range(n)] """
    tableau[9][1] = 1
    tableau[9][4] = 1
    tableau[10][5] = 1
    tableau[11][1] = 1
    tableau[11][5] = 1
    tableau[12][2] = 1
    tableau[12][3] = 1
    tableau[12][4] = 1
    tableau[12][5] = 1
    
    afficher_lignes()   
    afficher_tableau(tableau)
    return


# Pentadecathlon
def pentadecathlon():
    global tableau
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
    canvas.delete("all")      
    afficher_lignes()                    
    afficher_tableau(tableau)
    return

# Canon
def canon():
    global tableau
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

    canvas.delete("all")    
    afficher_lignes()   
    afficher_tableau(tableau)
    return

def ruche():
    global tableau
    tableau = [[0 for j in range(p)] for i in range(n)]
    tableau[21][25] = 1
    tableau[21][26] = 1
    tableau[22][24] = 1
    tableau[22][27] = 1    
    tableau[23][25] = 1
    tableau[23][26] = 1
    canvas.delete("all")    
    afficher_lignes()   
    afficher_tableau(tableau)
    return

def bloc():
    global tableau
    tableau = [[0 for j in range(p)] for i in range(n)]
    tableau[20][20] = 1
    tableau[21][20] = 1
    tableau[20][21] = 1
    tableau[21][21] = 1    
    canvas.delete("all")    
    afficher_lignes()   
    afficher_tableau(tableau)
    return

def bateau():
    global tableau
    tableau = [[0 for j in range(p)] for i in range(n)]
    tableau[20][20] = 1
    tableau[21][20] = 1
    tableau[20][21] = 1
    tableau[21][22] = 1
    tableau[22][21] = 1
    canvas.delete("all")    
    afficher_lignes()   
    afficher_tableau(tableau)
    return

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
    canvas.delete("all")    
    afficher_lignes()   
    afficher_tableau(tableau)
    return

def reset():
    global tableau 
    tableau = [[0 for j in range(0,p)] for i in range(0,n)]
    for i in range(1,p-1):
        for j in range(1,n-1):
            tableau[i][j]=0
    canvas.delete("all")
    c.set(0)
    afficher_lignes()
    afficher_tableau(tableau)
    
    return     



# Boutons

c = tkinter.StringVar()
c.set('0')
text = tkinter.Label(root,fg='red', textvariable= c,width=20,font = ('Helvetica',16))
text.pack(side=tkinter.TOP, padx=5, pady=10) 


# Boutons
menu_mobile = tkinter.Menubutton(root,text='Structures Mobiles',width=20, relief=tkinter.RAISED)
menu_mobile.menu = tkinter.Menu(menu_mobile, tearoff=0)
menu_mobile['menu']=menu_mobile.menu
menu_mobile.menu.add_command(label='Planeur',command=planeur)
menu_mobile.menu.add_command(label='Vaisseau',command=vaisseau)
menu_mobile.menu.add_command(label='Canon',command=canon)
menu_mobile.pack(side=tkinter.TOP, padx=5, pady=5)

menu_stable = tkinter.Menubutton(root,text='Structures Stables',width=20, relief=tkinter.RAISED)
menu_stable.menu = tkinter.Menu(menu_stable, tearoff=0)
menu_stable['menu']=menu_stable.menu
menu_stable.menu.add_command(label='Bloc',command=bloc)
menu_stable.menu.add_command(label='Bateau',command=bateau)
menu_stable.menu.add_command(label='Ruche',command=ruche)
menu_stable.pack(side=tkinter.TOP, padx=5, pady=5)

menu_oscillante = tkinter.Menubutton(root,text='Structures Oscillantes',width=20, relief=tkinter.RAISED)
menu_oscillante.menu = tkinter.Menu(menu_oscillante, tearoff=0)
menu_oscillante['menu']=menu_oscillante.menu
menu_oscillante.menu.add_command(label='Clignotant',command=clignotant)
menu_oscillante.menu.add_command(label='Clignotant x4',command=clignotant4)
menu_oscillante.menu.add_command(label='Pentadecathlon',command=pentadecathlon)
menu_oscillante.menu.add_command(label='Galaxie',command=galaxie)
menu_oscillante.pack(side=tkinter.TOP, padx=5, pady=5)


bouton_reset = tkinter.Button(root,text="Reset", width=20, command=reset)
bouton_reset.pack(side=tkinter.BOTTOM, padx=5, pady=5)

bouton_aleatoire = tkinter.Button(root,text="Aleatoire", width=20, command=action_bouton_aleatoire)
bouton_aleatoire.pack(side=tkinter.TOP, padx=5, pady=20)


bouton_evoluer = tkinter.Button(root,text="Évoluer", width=20, command=action_bouton_evolution)
bouton_evoluer.pack(side=tkinter.BOTTOM, padx=5, pady=20)

bouton_pred = tkinter.Button(root,text="Prediction", width=20, command=action_bouton_prediction)
bouton_pred.pack(side=tkinter.BOTTOM, padx=5, pady=20)

bouton_stop = tkinter.Button(root,text="Stop", width=20, command=stop)
bouton_stop.pack(side=tkinter.BOTTOM, padx=5, pady=5)

bouton_animation = tkinter.Button(root,text="Animation", width=20, command=animation)
bouton_animation.pack(side=tkinter.BOTTOM, padx=5, pady=5)



bouton_animation_prediction = tkinter.Button(root,text="Animation_pred", width=20, command=animation_prediction)
bouton_animation_prediction.pack(side=tkinter.BOTTOM, padx=5, pady=5)



#Allumer et éteindre les cellules au clic

def allumer_eteindre(i,j): #soit ça allume soit ça éteint tout betement
    global tableau
    if tableau[i][j] == 0:
        tableau[i][j] = 1
    else: 
        tableau[i][j] = 0
    return


def xy_vers_ij(x,y): #ça c'est chaud c'est pour savoir ou t'as cliqué mais j'ai juste recopier
    i = y // echelle
    j = x // echelle
    return i, j


def action_clic_souris(event):
    canvas.focus_set()
    # print("Clic à", event.x, event.y)
    x = event.x
    y = event.y
    allumer_eteindre(*xy_vers_ij(x,y))
    canvas.delete("all")   
    afficher_lignes()    
    afficher_tableau(tableau)
    return

# Liaison clic de souris/action
canvas.bind("<Button-1>",action_clic_souris)


afficher_lignes() #permet d'afficher le quadrillage, tu peux l'enlever c'est
#purement graphique en fait ça l'affichera après le clic

# afficher_tableau(tableau)
root.mainloop()


