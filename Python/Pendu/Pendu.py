# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 13:40:25 2022

@author: valen
"""

from tkinter import *
import tkinter.messagebox
from random import randint
from formes import *
from tkinter.colorchooser import askcolor
import numpy as np

class ZoneAffichage(Canvas):
    def __init__(self, parent, largeur, hauteur):
        Canvas.__init__(self, parent, width=largeur, height=hauteur)

        #création du pendu (graphique)
        self.__listeShape=[]
        # Base, Poteau, Traverse, Corde
        self.__listeShape.append(Rectangle(self, 50,  270, 200,  26, "brown"))
        self.__listeShape.append(Rectangle(self, 87,   83,  26, 200, "brown"))
        self.__listeShape.append(Rectangle(self, 87,   70, 150,  26, "brown"))
        self.__listeShape.append(Rectangle(self, 183,  67,  10,  40, "brown"))
        # Tete, Tronc
        self.__listeShape.append(Rectangle(self, 188, 120,  20,  20, "black"))
        self.__listeShape.append(Rectangle(self, 175, 143,  26,  60, "black"))
        # Bras gauche et droit
        self.__listeShape.append(Rectangle(self, 133, 150,  40,  10, "black"))
        self.__listeShape.append(Rectangle(self, 203, 150,  40,  10, "black"))
        # Jambes gauche et droite
        self.__listeShape.append(Rectangle(self, 175, 205,  10,  40, "black"))
        self.__listeShape.append(Rectangle(self, 191, 205,  10,  40, "black"))
    
    #fonction pour cacher le pendu
    def cachePendu(self):
        for i in range(len(self.__listeShape)):
            self.__listeShape[i].setState("hidden")
    
    #fonction pour dessiner le pendu
    def dessinePiecePendu(self,i):
        if i<=len(self.__listeShape):
            self.__listeShape[i-1].setState("normal")
            
    #fonction pour cacher une pièce du pendu:
    def cacherpiece(self,i):
        if i<=len(self.__listeShape):
            self.__listeShape[i-1].setState("hidden")
        
#classe pour récupérer la lettre du clavier
class MonBoutonLettre(Button):
    def __init__(self,parent,grandparent,t):
        Button.__init__(self, parent,text=t,state=DISABLED)
        self.__lettre=t
        self.__fenetre= grandparent
        
    def cliquer(self):
        self.config(state=DISABLED)
        self.__fenetre.traitement(self.__lettre)


class FenPrincipale(Tk):
    
    
    def __init__(self):
        Tk.__init__(self)
        self.__nbManques=0
        self.title('Jeu du pendu')
        self.geometry("800x600+200+200")
        self.couleur_ZoneAffichage = "green"
        self.couleur_clavier='white'
        self.couleur_background='white'
        self.configure(background=self.couleur_background)
        self.__liste_event=[]
        
        #menu_partie_quitter
        barreOutils=Frame(self)
        boutonQuitter=Button(barreOutils,text="X",width=5,bg="red")
        boutonNouvellePartie=Button(barreOutils,text="Nouvelle Partie",width=20,bg="green")
        

        
        #figure-pendu
        self.__canevas=ZoneAffichage(self,300,300)
        
        
        #affichage mot
        self.__texte_mot=StringVar()
        self.__texte_mot.set("Mot : ")
        mot=Label(self,textvariable=self.__texte_mot)
        
        
        #clavier
        clavier=Frame(self)
        self.__L=[]
        for i in range(26):
            l=chr(ord('A')+i)
            lettre=Button(clavier,text=l,padx=2,pady=2,state=DISABLED,bg=self.couleur_clavier)
            lettre=MonBoutonLettre(clavier,self, l)
            self.__L.append(lettre)
        
                
            
            
        #placement des éléments
        barreOutils.pack(side=TOP)
        boutonQuitter.pack(side=LEFT,padx=5,pady=5,ipady=7,ipadx=7)
        boutonNouvellePartie.pack(side=LEFT,padx=13,pady=5,ipady=7,ipadx=15)
        
        
        self.__canevas.pack(side=TOP)
        mot.pack(side=TOP)
        
        clavier.pack(side=TOP)
        for i in range(3):
            for j in range(7):
                self.__L[i*7+j].grid(row=i,column=j,ipady=10,ipadx=20)
        for j in range(5):
            self.__L[21+j].grid(row=3,column=j+1,ipady=7,ipadx=15)
        
    

        
         
        
        ############# travail personnel #############
    
        #création de l'interface pour changer les couleurs de l'interface 
        boutonCouleur=Menubutton(barreOutils,text='Choisir une couleur | ✒️ ',bg='white')
        boutonCouleur.pack(side=RIGHT, padx=5, pady=5)
        menuDeroulantCouleur=Menu(boutonCouleur, tearoff = 0)
        menuDeroulantCouleur.add_command(label="Couleur de la zone d'affichage", command=self.changer_couleur_ZoneAffichage)
        menuDeroulantCouleur.add_command(label='Couleur du clavier', command=self.changer_couleur_clavier)
        menuDeroulantCouleur.add_command(label="Couleur de l'arrière plan", command=self.changer_couleur_background)
        
        
        #bouton retour en arrière
        boutonUndo=Button(barreOutils,text=' ↩️ ',bg='blue',width=3)
        boutonUndo.pack(side=RIGHT, padx=5, pady=5,ipady=7,ipadx=7)
        
        ############################################
        
        #Commandes associées aux bouttons
        boutonQuitter.config(command=self.destroy)
        boutonNouvellePartie.config(command=self.lancement)
        for i in range(26):
            self.__L[i].config(command=self.__L[i].cliquer)
        boutonCouleur.configure(menu=menuDeroulantCouleur)
        boutonUndo.config(command=self.undo)
        if len(self.__liste_event)!=0: #si aucun événements a été enregistré, on ne peut pas cliquer sur retour en arrière
            boutonUndo.config(state=NORMAL)
        #chargement du fichier de mot
        self.chargeMots()
     
    #fonction pour gérer la couleur des éléments    
    def set_couleur_ZoneAffichage(self,couleur):
        self.couleur_ZoneAffichage  = couleur
        self.__canevas.config(bg=self.couleur_ZoneAffichage)

    def set_couleur_clavier(self,couleur):
        self.couleur_clavier =couleur
        for i in self.__L:
            i.config(bg=self.couleur_clavier)

    def set_couleur_background(self,couleur):
        self.couleur_background =couleur
        self.configure(bg=self.couleur_background)        
     
        
    #Menu pour changer la couleur des formes du pendu
    def changer_couleur_ZoneAffichage(self): #change la couleur des formes qui vont être affichées à l'avenir
        C = askcolor(title="Choisis ta couleur")
        self.set_couleur_ZoneAffichage(C[1])

    def changer_couleur_clavier(self): #change la couleur d'arrière plan du clavier
        C = askcolor(title="Choisis ta couleur")
        self.set_couleur_clavier(C[1])

    def changer_couleur_background(self): #change la couleur d'arrière plan du clavier
        C = askcolor(title="Choisis ta couleur")
        self.set_couleur_background(C[1])
    
    #fonction pour charger le fichier mots    
    def chargeMots(self):
        f=open('mots.txt', 'r')
        s=f.read()
        self.__mots=s.split('\n')
        f.close()
         
    #création d'une nouvelle partie
    def lancement(self):
        for i in range(26):
            self.__L[i].config(state=NORMAL)
        
        #nouveau mot à deviner
        self.__mot=self.__mots[randint(0,len(self.__mots)-1)]
        self.__motAffiche=len(self.__mot)*"*"
        self.__texte_mot.set("Mot : " + self.__motAffiche)
        self.__nbManques=0
        
        #graphique
        self.__canevas.cachePendu()
     
    #action à réaliser lorsqu'on clique sur une lettre    
    def traitement(self,lettre):
        cpt=0
        lettres=list(self.__motAffiche)
        for i in range(len(self.__mot)):
            if self.__mot[i]==lettre:
                cpt+=1
                lettres[i]=lettre
        
        self.__motAffiche=''.join(lettres)
        
        if cpt==0:
            self.__nbManques += 1
            self.__liste_event.append([lettre,False])
            if self.__nbManques >=10:
                self.finPartie(False)
                
            self.__canevas.dessinePiecePendu(self.__nbManques)
            
        else:
            self.__texte_mot.set("Mot : " + self.__motAffiche)
            self.__liste_event.append([lettre,True])
            if self.__mot == self.__motAffiche:
                self.finPartie(True)
    
    #résultat à afficher en fin de partie
    def finPartie(self,gagne):
        for b in self.__L:
            b.config(state=DISABLED)
        if gagne:
            self.__texte_mot.set(self.__mot+' - Bravo vous avez gagné')
        else:
            self.__texte_mot.set(self.__mot+' - Dommage vous avez perdu')

    #fonction pour avoir l'historique des coups
    def undo(self):
        try :
            num_bouton=ord(self.__liste_event[-1][0])-ord('A')
            self.__L[num_bouton].config(state=NORMAL) #changer l'état de la lettre
            if self.__liste_event[-1][1]==False: #on a raté le dernier coup
                self.__canevas.cacherpiece(self.__nbManques) #retirer la forme du coup manque
                self.__nbManques-=1 #reset des coups manqués
    
            else: #on a trouver une lettre au dernier coup
                newmotcache=''
                for i in range(len(self.__mot)):
                    T=np.array(self.__liste_event) #convertion
                    if self.__mot[i] in list(T[:-1,0]):#si c'est la bonne lettre (on vérifie dans les anciens coups)
                        newmotcache+=self.__mot[i]
                    else:
                        newmotcache+='*'
                self.__motAffiche = newmotcache
            self.__texte_mot.set('Mot : '+self.__motAffiche+'\n'+"Vous avez annulé le coup précédent")
            self.__liste_event.pop() #on retire le dernier coup de la liste
        
        #cas où le premier coup n'a pas encore été joué
        except IndexError:
            tkinter.messagebox.showwarning ( title = "Erreur" , message = "Attention, tu dois jouer ton premier coup!" )

if __name__ == '__main__':
    
	fen = FenPrincipale()
	fen.mainloop()
