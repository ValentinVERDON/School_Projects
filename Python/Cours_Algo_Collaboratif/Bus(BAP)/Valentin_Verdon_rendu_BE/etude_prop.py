# Ce programme étudie les propriétés associées à l'algorithme du BUS(BAP) 

import main_VS as m
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm 
import random


""" ------- Fonctions pour la visualisation des situations et solutions ---------- """
def calcul_lw(passager,nb_arret):
    # on calcule la taille des traits
    # faire une liste de taille nb_arret * nb_arret
    liste_lw = np.zeros((nb_arret,nb_arret))
    for i in range(len(passager)):
        arret1 = passager[i][0]
        arret2 = passager[i][1]
        liste_lw[arret1][arret2] += 1
    maxi = 0
    for i in range(len(passager)):
        aux  = liste_lw[arret1][arret2]+liste_lw[arret2][arret1]
        if aux > maxi :
            maxi = aux
    return liste_lw , maxi


def affichage_situation_depart(coord,passager,main_stop):
    # on calcule la taille des traits
    liste_lw,maxi = calcul_lw(passager,len(coord))
    # on affiche les coordonnées des arrêts
    for i in range(len(coord)):
        plt.scatter(coord[i][0],coord[i][1],color = "red")
    # on affiche les coordonnées des passagers
    for i in range(len(passager)):
        arret1 = passager[i][0]
        arret2 = passager[i][1]
        x1 = coord[arret1]
        x2 = coord[arret2]
        plt.plot([x1[0],x2[0]],[x1[1],x2[1]],c = "green",lw=(liste_lw[arret1][arret2]+liste_lw[arret2][arret1])/maxi*1)
        # afficher au dessus du segment son épaisseur
        plt.text((x1[0]+x2[0])/2,(x1[1]+x2[1])/2,str(int(liste_lw[arret1][arret2]+liste_lw[arret2][arret1])),fontsize = 5)

    # on affiche les coordonnées de l'arrêt principal
    plt.scatter(coord[main_stop][0],coord[main_stop][1],color = "blue")
    plt.title("Situation de départ")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.show()

def creation_couleur(ligne_bus):
    couleurs = {}
    for i in range(len(ligne_bus)):
        rouge = random.randint(0, 255)
        vert = random.randint(0, 255)
        bleu = random.randint(0, 255)
        couleur = (rouge/255,vert/255,bleu/255)
        couleurs[i] = couleur
    return couleurs

def affichage_situation_finale(coord,main_stop,liste_bus):
    #dictionnaire des couleurs
    couleurs = creation_couleur(liste_bus)
    # on affiche les coordonnées des arrêts
    for i in range(len(coord)):
        plt.scatter(coord[i][0],coord[i][1],color = "red")
    # on affiche les coordonnées de l'arrêt principal
    plt.scatter(coord[main_stop][0],coord[main_stop][1],color = "blue")
    # on affiche les coordonnées des bus
    for l in range(len(liste_bus)) :
        couleur = couleurs[l]
        ligne = liste_bus[l]
        for i in range(len(ligne)-1):
            arret1 = ligne[i]
            arret2 = ligne[i+1]
            x1 = coord[arret1]
            x2 = coord[arret2]
            plt.plot([x1[0],x2[0]],[x1[1],x2[1]],c = couleur)
    plt.title("Situation finale")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.show()


""" -------------- Fonctions pour l'étude de l'algorithme ----------- """

def etude_un_parametre(nom,debut,fin,nb_pts,situation):
    # créer une liste de debut à fin avec nb_pts
    liste = np.linspace(debut,fin,nb_pts)
    # on crée une liste vide pour stocker les résultats
    resultat = []
    for i in tqdm(liste) :
        simulation = m.Simulation(**{nom: i}) # on crée une simulation en gardant les paramètres de bases (sauf pour le paramètre étudié)
        simulation.lancer_simulation(situation) # on lance la simulation
        historique_L_best = simulation.envoie_historique() # on récupère l'historique
        resultat.append(historique_L_best) # on ajoute l'historique à la liste des résultats
    return resultat


""" ----------- Main ----------- """
if __name__ == "__main__":
    # on crée des coord aléatoire
    coord,main_stop = m.generation_coord(20,42)
    # on génère des passagers
    passager = m.generation_passager(100,len(coord),42)
    # on crée une situation
    situation = m.Situation(3,coord,passager,main_stop)

    """ ----- Test pour les fonctions d'affichage -----"""
    
    # on affiche la situation de départ
    affichage_situation_depart(coord,passager,main_stop)
    # on trouve une solution
    simulation = m.Simulation(t_max = 200)
    simulation.lancer_simulation(situation)
    # on affiche la situation finale
    affichage_situation_finale(coord,main_stop,simulation.S_best)

    """ ------- Etude de la convergence ------- """
    # on va étudié la converge de notre solution : 
    #   1) petite simulation : voir qu'il y a convergence vers différentes solutions
    #   2) grande simulation : voir que la solution converge vers une solution optimale (avec le temps !)
    #   Afficher en parrallèle l'évolution des taux de phéromones ? 

    # 1) petite simulation
    """
    liste_L_best = [] 
    nb_simulations = 30
    for i in tqdm(range(nb_simulations)):
        simulation = m.Simulation(t_max = 100)
        simulation.lancer_simulation(situation)
        liste_L_best.append(simulation.L_best)
    plt.hist(liste_L_best,bins = 15)
    plt.title("Histogramme des temps moyens obtenus")
    plt.xlabel("Temps moyen")
    plt.ylabel("Nombre de simulations")
    plt.show()
    """
    # 2) grande simulation
    """
    liste_historique_L_best = []
    nb_simulations = 3
    for i in tqdm(range(nb_simulations)):
        simulation = m.Simulation(t_max = 1000)
        simulation.lancer_simulation(situation)
        liste_historique_L_best.append(simulation.envoie_historique())
    for i in range(len(liste_historique_L_best)):
        plt.plot(liste_historique_L_best[i],label = "Simulation " + str(i))
    plt.legend()
    plt.title("Evolution des temps moyens obtenus")
    plt.xlabel("Iteration")
    plt.ylabel("Temps moyen")
    plt.show()
    """

    """---------- Etude du paramètre beta -------- """
    """parametre = "beta"
    debut = 0
    fin = 6
    nb_pts = 6
    resultat = etude_un_parametre(parametre,debut,fin,nb_pts,situation)
    # on trace les courbes de resultat en mettant comme label la valeur de beta avec un dégradé de couleur
    for i in range(len(resultat)):
        plt.plot(resultat[i],label = parametre + " = " + str(debut + i*(fin-debut)/nb_pts), c = ((1-i/(len(resultat)-1)),0,0))
    plt.legend()
    plt.title("Etude du paramètre beta")
    plt.xlabel("Iteration")
    plt.ylabel("L_best")
    plt.show() """

    """---------- Etude du paramètre rho -------- """
    """parametre = "rho"
    debut = 0
    fin = 1.1
    nb_pts = 5
    resultat = etude_un_parametre(parametre,debut,fin,nb_pts,situation)
    # on trace les courbes de resultat en mettant comme label la valeur de rho avec un dégradé de couleur
    for i in range(len(resultat)):
        plt.plot(resultat[i],label = parametre + " = " + str(debut + i*(fin-debut)/nb_pts), c = ((1-i/(len(resultat)-1)),0,0))
    plt.legend()
    plt.title("Etude du paramètre rho")
    plt.xlabel("Iteration")
    plt.ylabel("L_best")
    plt.show()"""

    """---------- Etude du paramètre alpha -------- """
    """parametre = "alpha"
    debut = 0
    fin = 0.1
    nb_pts = 10
    resultat = etude_un_parametre(parametre,debut,fin,nb_pts,situation)
    # on trace les courbes de resultat en mettant comme label la valeur de alpha avec un dégradé de couleur
    for i in range(len(resultat)):
        plt.plot(resultat[i],label = parametre + " = " + str(debut + i*(fin-debut)/nb_pts), c = ((1-i/(len(resultat)-1)),0,0))
    plt.legend()
    plt.title("Etude du paramètre alpha")
    plt.xlabel("Iteration")
    plt.ylabel("L_best")
    plt.show()"""

    """---------- Etude du paramètre q0 -------- """
    '''parametre = "q0"
    debut = 0
    fin = 0.9
    nb_pts = 10
    resultat = etude_un_parametre(parametre,debut,fin,nb_pts,situation)
    # on trace les courbes de resultat en mettant comme label la valeur de q0 avec un dégradé de couleur
    for i in range(len(resultat)):
        plt.plot(resultat[i],label = parametre + " = " + str(debut + i*(fin-debut)/(nb_pts-1)), c = ((1-i/(len(resultat)-1)),0,0))
    plt.legend()
    plt.title("Etude du paramètre q0")
    plt.xlabel("Iteration")
    plt.ylabel("L_best")
    plt.show()'''







