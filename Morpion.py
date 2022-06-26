import tkinter as tk
from tkinter import messagebox
import random
import numpy as np

###############################################################################
# création de la fenetre principale  - ne pas toucher

LARG = 300
HAUT = 300
colorGrille = "blue"
Score = [0,0]


# etat = 0 : en jeu ; etat = 1 : partie terminée ; etats = 2 = attente nouvelle partie
Etats = 0


Window = tk.Tk()
Window.geometry(str(LARG)+"x"+str(HAUT))   # taille de la fenetre
Window.title("ESIEE - Morpion")


# création de la frame principale stockant toutes les pages

F = tk.Frame(Window)
F.pack(side="top", fill="both", expand=True)
F.grid_rowconfigure(0, weight=1)
F.grid_columnconfigure(0, weight=1)

# gestion des différentes pages

ListePages  = {}
PageActive = 0

def CreerUnePage(id):
    Frame = tk.Frame(F)
    ListePages[id] = Frame
    Frame.grid(row=0, column=0, sticky="nsew")
    return Frame

def AfficherPage(id):
    global PageActive
    PageActive = id
    ListePages[id].tkraise()
    
Frame0 = CreerUnePage(0)

canvas = tk.Canvas(Frame0,width = LARG, height = HAUT, bg ="black" )
canvas.place(x=0,y=0)


#################################################################################
#
#  Parametres du jeu

Grille = [ [0,0,0], 
           [0,0,0], 
           [0,0,0] ]  # attention les lignes représentent les colonnes de la grille
           
Grille = np.array(Grille)
Grille = Grille.transpose()  # pour avoir x,y
           
  

###############################################################################
#
# gestion du joueur humain et de l'IA
# VOTRE CODE ICI 
def SimuleHumain():
    if TestFinSimulation() != 0:
        return (0,TestFinSimulation())
    L = PositionPossible()
    resultats = []
    for coup in L:
        Grille[coup[0]][coup[1]] = 1
        R = SimuleIa()[1]
        resultats.append( (coup,R) )
        Grille[coup[0]][coup[1]] = 0
    
    mini = resultats[0][1]
    for i in resultats :
        if i[1] < mini : mini = i[1]
    for j in resultats :
        if j[1] == mini : return j
    return
    


def SimuleIa():
    if TestFinSimulation() != 0:
        return (0,TestFinSimulation())
    L = PositionPossible()
    resultats = []
    for coup in L:
        Grille[coup[0]][coup[1]] = 2
        R = SimuleHumain()[1]
        resultats.append( (coup,R) )
        Grille[coup[0]][coup[1]] = 0

    
    maxi = resultats[0][1]
    for i in resultats :
        if i[1] > maxi : maxi = i[1]
    for j in resultats :
        if j[1] == maxi : return j
    return




def TestFinSimulation() :
    for P in [1,2]:
            for x in range(3):
                if(Grille[x][0] == Grille[x][1] == Grille[x][2] == P):
                    return P
                if(Grille[0][x] == Grille[1][x] == Grille[2][x] == P): 
                    return P
            if(Grille[0][0] == Grille[1][1] == Grille[2][2] == P): 
                return P
            if(Grille[2][0] == Grille[1][1] == Grille[0][2] == P): 
                return P
    if len( PositionPossible() ) == 0 :
        return 1.5
    return 0            # = 0 si partie pas fini / = 1.5 si match null / = 1 si joueur 1 gagnant / = 2 si joueur 2 gagant

def PositionPossible():
    possitions = []
    for x in range (3):
        for y in range (3):
            if Grille[x][y] == 0 : possitions.append((x,y))
    return possitions 

def TestFinPartie() :
    fin = False
    for P in [1,2]:
            for x in range(3):
                if(Grille[x][0] == Grille[x][1] == Grille[x][2] == P):
                    FinPartie(P)
                    fin = True
                if(Grille[0][x] == Grille[1][x] == Grille[2][x] == P): 
                    FinPartie(P)
                    fin = True
            if(Grille[0][0] == Grille[1][1] == Grille[2][2] == P): 
                FinPartie(P)
                fin = True
            if(Grille[2][0] == Grille[1][1] == Grille[0][2] == P): 
                FinPartie(P)
                fin = True
    if Etats == 0 and np.sum(Grille == 0) == 0 :
        fin = True
        FinPartie(0)
    return fin

def NouvellePartie():
    global Grille, colorGrille, FinPartie
    Grille =np.array ([  [0,0,0], 
                         [0,0,0], 
                         [0,0,0] ]).transpose()
    colorGrille = "blue"

def FinPartie(winner):
    global Score, colorGrille, Etats
    Etats = 1
    if winner == 0 :
        colorGrille = "white"
        print("Egalité")
        return

    Score[0] += (winner==1)*1
    Score[1] += (winner==2)*1
    if(winner==1):      colorGrille = "red"
    else:               colorGrille = "Yellow"
    print("Gagnant : Joueur n°{} avec {} points | Perdant : Joueur n°{} avec {} points".format((winner), Score[winner-1], (winner != 2)*1 +1,Score[(winner != 2)*1] ))


def Play(x,y):   
    global Etats
    if Grille[x][y] == 0 :          
        Grille[x][y] = 1
    else :return
    if (TestFinPartie()) : return
    resultat = SimuleIa()[0]
    Grille[resultat[0]][resultat[1]] = 2 
    TestFinPartie()
    




   
          
    
    
################################################################################
#    
# Dessine la grille de jeu

def Dessine(PartieGagnee = False):
        ## DOC canvas : http://tkinter.fdex.eu/doc/caw.html
        canvas.delete("all")
        
        for i in range(4):
            canvas.create_line(i*100,0,i*100,300,fill=colorGrille, width="4" )
            canvas.create_line(0,i*100,300,i*100,fill=colorGrille, width="4" )
            
        for x in range(3):
            for y in range(3):
                xc = x * 100 
                yc = y * 100 
                if ( Grille[x][y] == 1):
                    canvas.create_line(xc+10,yc+10,xc+90,yc+90,fill="red", width="4" )
                    canvas.create_line(xc+90,yc+10,xc+10,yc+90,fill="red", width="4" )
                if ( Grille[x][y] == 2):
                    canvas.create_oval(xc+10,yc+10,xc+90,yc+90,outline="yellow", width="4" )
        
       
        
  
####################################################################################
#
#  fnt appelée par un clic souris sur la zone de dessin

def MouseClick(event):
    global Etats

    if Etats == 0 :
        Window.focus_set()
        x = event.x // 100  # convertit une coordonée pixel écran en coord grille de jeu
        y = event.y // 100
        if ( (x<0) or (x>2) or (y<0) or (y>2) ) : return
        Play(x,y)  # gestion du joueur humain et de l'IA

    elif Etats == 1 : 
        NouvellePartie()
        Etats = 0

    Dessine()
    
canvas.bind('<ButtonPress-1>',    MouseClick)

#####################################################################################
#
#  Mise en place de l'interface - ne pas toucher

AfficherPage(0)
Dessine()
Window.mainloop()


  


    
        

      
 

