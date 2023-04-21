"""
 Ce code est une traduction en python du pseudo code
 de l'article "Mutiple Ant Colony Systems for the Busstop
 Allocation Problem"  
 
"""

import numpy as np
import random
import matplotlib.pyplot as plt
from tqdm import tqdm 
""" ---------- paramètres ---------------"""
m  = 2      # nombre de ligne de bus
coord = [(0,0),(0,3),(2,1),(3,3),(6,1),(4,2),(3,5)] # coordonnées des arrets (on suppose qu'il  n'y a pas de doublons)
passager = [(0,1),(1,2),(0,3),(4,1)] # liste des couples départ-arrivé des passagers
main_stop = 4
n = len(coord) # nombre d'arret de bus
tau_0 = 1   # quantité de phéromones initiale
r = 10       # nombre de fourmis dans chaque ligne
beta = 0.5  # paramètre visibilté vs importance des phéromones
rho = 0.1   # taux d'évaporation des phéromones
alpha = 0.1 # learning rate
v = 1       # vitesse moyenne 
q0 = 0.5    # importance relative entre exploration et exploitation
L = np.zeros(r) # score de chaque solution
L_best = -1   # score de la meilleur solution 
S_best = []   # meilleur solution
t_max = 100    # nombre de boucle

""" -------- Génération des passager """

def generation_passager(nb_passager):
    passager = []
    for i in range(nb_passager):
        passager.append((random.randint(0,n-1),random.randint(0,n-1)))
    return passager

passager = generation_passager(100)

""" -------- Etude performance ---------- """
liste_L = []

""" ---------- fonctions annexes --------"""
def calcul_proba(tau,eta,beta,i,j,k,l,J):
    aux = 0
    Jk = J[k]
    if len(Jk) == 1 :
        return 1
    elif j in Jk :
        for h in Jk:
            aux += tau[l,i,h]*eta[l,i,h]**beta
        return (tau[l,i,j]*eta[l,i,j]**beta)/aux
    else :
        return 0

# eta_s est le même pour tt le monde donc negligeable
def calcul_proba_s(tau_s,k,j,l,J):
    aux = 0
    Jk = J[k]
    if j in Jk :
        for h in Jk:
            aux += tau_s[l,h]
        return tau_s[l,j]/aux
    else :
        return 0
    
def calcul_distance(x1,y1,x2,y2):
    return np.sqrt((x1-x2)**2 + (y1-y2)**2)

def tirage(tab):
    return np.random.choice(len(tab), p=tab)

def eq1(tau,eta,beta,i,l,J,k):
    maxi = 0
    j = -1
    for i_j in range(len(J[k])):
        h = J[k][i_j]
        aux = tau[l,i,h]*eta[l,i,h]**beta
        if aux >= maxi :
            maxi = aux 
            j = i_j
    return j , maxi

''' ------ Fonction évaluation d'une solution ----------'''
# recherche appartenance busstop / ligne de bus
def recherche_busstrop_ligne(sol,arret):
    for l in range(m):
        if arret in sol[l]:
            return l
    return -1

# calcul temps pour aller d'un busstop à un autre sur la même ligne :
def calcul_une_ligne(sol,ligne,arret1,arret2):
    temps = 0
    i1 = sol[ligne].index(arret1)
    i2 = sol[ligne].index(arret2)
    if i2 > i1 :
        for i in range(i1,i2):
            temps += calcul_distance(coord[sol[ligne][i]][0], coord[sol[ligne][i]][1], coord[sol[ligne][i+1]][0], coord[sol[ligne][i+1]][1])/v
    else :
        for i in range(i1,i2,-1):
            temps += calcul_distance(coord[sol[ligne][i]][0], coord[sol[ligne][i]][1], coord[sol[ligne][i-1]][0], coord[sol[ligne][i-1]][1])/v
    return temps


# calcul temps pour un passager (on suppose qu'il n'y pas d'attente à la main busstop et qu'il va dans la bonne direction)
def calcul_un_passager(sol,pas):
    temps = 0
    depart,arrive = pas[0],pas[1]
    ligne_depart = recherche_busstrop_ligne(sol,depart)
    ligne_arrive = recherche_busstrop_ligne(sol,arrive)

    # cas où les deux arrêts sont sur la même ligne de bus
    if ligne_depart == ligne_arrive :
        temps = calcul_une_ligne(sol,ligne_depart,depart,arrive)          
    # cas où les deux arrêts sont sur des lignes différentes
    else :
        temps = calcul_une_ligne(sol,ligne_depart,depart,main_stop)
        temps += calcul_une_ligne(sol,ligne_arrive,main_stop,arrive)
    return temps
                

# évaluation d'un solution
def evaluer(sol):
    temps_moyen = 0
    for pas in passager :
        temps_moyen += calcul_un_passager(sol,pas)
    return temps_moyen/len(passager)
  
""" -------------------------------- PSEUDO CODE -----------------------------------------"""
def calcul():

    #pour tracer les courbes d'apprentissage
    Liste_L_best = []

    L_best = -1
    ## Etape 1 : initialisation des phéromones
    t = 0   
    tau = np.full((m,n,n),tau_0,dtype=float) # on initialise à tau0
    for l in range(m):  # on met à 0 car il n'y a pas de bus qui va de i à i
        for i in range(n):
            tau[l,i,i] = 0

    """ ------------ Initialisation des tableaux ---------- """

    # Initialisation des visibilites
    eta = np.zeros((m,n,n))
    for l in  range(m):
        for i in range(n):
            for j in range(n):
                if i != j :
                    eta[l,i,j] = v/calcul_distance(coord[i][0], coord[i][1], coord[j][0], coord[j][1])

    tau_s = np.full((m,n),tau_0,dtype=float) #pheromone des s to bus stop
    """ ---------------------------------- SUITE PSEUDO CODE ------------------------------------- """
    while t < t_max :

        # Initialisation des arret non visite
        J = [list(range(n)) for i in range(r)]
        S = [[[] for l in range(m)] for i in range(r)]
        ## Etape 2 : choix des j start à partir des s 

        for l in range(m): # on parcours les colonies
            for k in range(r): # on parcours les fourmies
            
                distrib = []
                for j in range(n): # on parcours les busstop pour calculer la distribution de proba
                    distrib.append(calcul_proba_s(tau_s,k,j,l,J))
                
                #tirage
                j_start = tirage(distrib)
                
                #maj de S
                S[k][l].append(j_start)

                #maj de J
                # si j est le main_stop on regarde vérifie qu'il soit déjà présent dans toutes les sous listes de S[k]
                present = True
                if j_start == main_stop :
                    for ll in range(m):
                        if main_stop not in S[k][ll]:
                            present = False
                            break
                if present :  
                    J[k].remove(j_start)

                #maj de tau_s en suivant l'eq 3
                tau_s[l][j_start] = (1-rho)*tau_s[l][j_start] + rho*tau_0

        # Etape 3 : 
        for w in range(n-1): # on realise la boucle jusqu'à avoir fait tt les busstop dans chaque modèle de solution 
            k = 0

            while k < r : # on fait avancer une fourmie de chaque modèle

                # si il ne reste qu'un seul arrêt 
                if len(J[k]) == 1 and J[k][0] == main_stop :
                    for l in range(m):
                        if main_stop not in S[k][l]:
                            S[k][l].append(main_stop)

                else : 
                    q = random.random() #on choisis un q aléatoire
                    
                    if q <= q0 :
                        
                        # on choisis la fourmie à avancer dans la colonie l de la solution d'indice k
                        j , maxi = -1 , 0
                        for l in range(m): #on parcours les lignes de bus 
                            j0 , maxi0 = eq1(tau, eta, beta, S[k][l][-1], l, J, k)
                            
                            if maxi < maxi0 :
                                maxi = maxi0
                                j = j0
                    else :
                        
                        # on va choisir le busstop selon la distrib de proba
                        stock = []
                        ligne_associe = []
                        for l in range(m):
                            distrib = [] 
                            for j in J[k]: # on parcours les busstop pour calculer la distribution de proba
                                distrib.append(calcul_proba(tau,eta,beta,S[k][l][-1],j,k,l,J))
                            #tirage
                            elt = tirage(distrib)
                            stock.append(elt)
                            ligne_associe.append(stock.index(elt))
                            
                        # tirage final    
                        j = random.choice(stock)
                        # prendre l'élement du même indice que j dans stock dans la liste ligne_associe
                        l = ligne_associe[stock.index(j)]

                    # si la fourmie k est déjà passé par J[k][j] on recommence
                    if J[k][j] in S[k][l] :
                        continue

                    #maj de S
                    S[k][l].append(J[k][j])

                    #maj de Jk
                    #on enlève J[k][j] uniquement si ce n'est pas le main_stop et sinon il faut que tt les lignes l'ai déjà vu 
                    if J[k][j] != main_stop :
                        J[k].remove(J[k][j])
                    else :
                        # on regarde si J[k][j] est présent dans toutes les listes de S[k]
                        if all(J[k][j] in S[k][l] for l in range(m)) :
                            J[k].remove(J[k][j])
                    
                    
                    #maj de tau_s en suivant l'eq 3
                    tau[l][j] = (1-rho)*tau[l][j] + rho*tau_0

                #maj k 
                k += 1

        # Etape 4 : calcul des performances des solutions et maj de la meilleur solution
        for k in range(r):
            # on calcule la performance de la solution k
            L[k] = evaluer(S[k])

            # on met à jour la meilleure solution 
            if L[k] < L_best or L_best == -1 : 
                L_best = L[k]
                S_best = S[k]

        # Etape 5 : maj des phéromones
        for l in range(m):
            for i in range(n):
                for j in range(n):
                    if i != j :
                        if j in S_best[l] and i in S_best[l] :
                            tau[l][i][j] = (1-alpha)*tau[l][i][j] + alpha/L_best
                        else :
                            tau[l][i][j] = (1-alpha)*tau[l][i][j]

        # maj pour les phéromones initiaux :
        for l in range(m):
            for j in range(n):
                if j == S_best[l][0] :
                    tau_s[l][j] = (1-alpha)*tau_s[l][j] + alpha/L_best
                else :
                    tau_s[l][j] = (1-alpha)*tau_s[l][j]

        # On recommence jusqu'à t_max
        t += 1

        Liste_L_best.append(L_best)

    return L_best , Liste_L_best

""" ---------------------------------- FIN PSEUDO CODE ------------------------------------- """

L_best , List = calcul()
plt.plot(List)
plt.show()
''' Tracer Hist des solutions
for i in tqdm(range(30)):
    L_best = calcul()
    liste_L.append(L_best)

plt.hist(liste_L)
plt.show()
print("success") '''
# remarque : ne converge pas toujours vers la même solution ! 

""" --------- A faire ----------"""

# calculer la complexité de l'algo
# tracer kes courbes d'apprentissage (pour voir la convergence en fonction du learning rate)
# faire testes avec différentes situation (juste pour voir la diff entre résultat pas étude complète)
# faire varier les paramètres :r , beta , rho , q0