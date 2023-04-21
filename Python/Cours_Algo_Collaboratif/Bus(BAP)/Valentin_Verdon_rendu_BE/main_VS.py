# Version programmation object de main.py

"""
 Ce code est une traduction en python du pseudo code
 de l'article "Mutiple Ant Colony Systems for the Busstop
 Allocation Problem"  
 
"""

""" ---------- Les imports ------------- """
import numpy as np
import random
import matplotlib.pyplot as plt
from tqdm import tqdm 
import time 
""" ---------- Classe associée à la création d'une Situation ------------- """
class Situation:

    def __init__(self,m,coord,passager,main_stop):
        self.m = m 
        self.coord = coord
        self.n = len(coord)
        self.passager = passager
        self.main_stop = main_stop
    
    def __str__(self):
        return "Situation : \n m : {},\n n : {},\n coord : {},\n passager : {},\n main_stop :{}".format(self.m,self.n,self.coord,self.passager,self.main_stop)
    
    def envoie_situation(self):
        return self.m,self.n,self.coord,self.passager,self.main_stop
""" ----------- Classe pour la crétion d'une Simulation -------------- """
class Simulation:

    def __init__(self,tau_0=1,r=10,beta=0.5,rho=0.1,alpha=0.1,v=1,q0=0.5,t_max=100):
        self.tau_0 = tau_0
        self.r = r
        self.beta = beta
        self.rho = rho
        self.alpha = alpha
        self.v = v
        self.q0 = q0
        self.t_max = t_max
        self.L_best = -1
        self.S_best = []

        self.historique_L_best = [] # pour tracer les courbes de convergences

    def __str__(self):
        return "Simulation({},{},{},{},{},{},{},{})".format(self.tau_0,self.r,self.beta,self.rho,self.alpha,self.v,self.q0,self.t_max,self.L_best,self.S_best)
    
    def affichage_solution(self):
        print("L_best : ",self.L_best)
        print("S_best : ",self.S_best)
    
    def envoie_solution(self):
        return self.L_best , self.S_best
    
    def envoie_historique(self):
        return self.historique_L_best

    def initialisation (self,m,n,coord):

        # Initialisation des phéromones
        tau = np.full((m,n,n),self.tau_0,dtype=float) # on initialise à tau0
        for l in range(m):  # on met à 0 car il n'y a pas de bus qui va de i à i
            for i in range(n):
                tau[l,i,i] = 0

        # Initialisation des visibilites
        eta = np.zeros((m,n,n))
        for l in  range(m):
            for i in range(n):
                for j in range(n):
                    if i != j :
                        eta[l,i,j] = self.v/self.calcul_distance(coord[i][0], coord[i][1], coord[j][0], coord[j][1])

        # Initialisation pheromones des s to bus stop
        tau_s = np.full((m,n),self.tau_0,dtype=float) 

        return tau , eta, tau_s

    def choix_depart(self,m,n,main_stop,tau_s):

        # Initialisation des arret non visite
        J = [list(range(n)) for i in range(self.r)]
        S = [[[] for l in range(m)] for i in range(self.r)]

        ## Etape 2 : choix des j start à partir des s 
        for l in range(m): # on parcours les colonies
            for k in range(self.r): # on parcours les fourmies
            
                distrib = []
                for j in range(n): # on parcours les busstop pour calculer la distribution de proba
                    distrib.append(self.calcul_proba_s(tau_s,k,j,l,J))
                
                #tirage
                j_start = self.tirage(distrib)
                
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
                tau_s[l][j_start] = (1-self.rho)*tau_s[l][j_start] + self.rho*self.tau_0

        return J, S, tau_s
    
    def progression_fourmi(self,m,n,main_stop,tau,eta,J,S):
        # Etape 3 : 
        for compteur in range(n-1): # on realise la boucle jusqu'à avoir fait tt les busstop dans chaque modèle de solution 
            k = 0
            while k < self.r : # on fait avancer une fourmie de chaque modèle
                # si il ne reste qu'un seul arrêt (pour éviter de tourner en rond à cause du main stop)
                if len(J[k]) == 1 and J[k][0] == main_stop :
                    for l in range(m):
                        if main_stop not in S[k][l]:
                            S[k][l].append(main_stop)
                else : 
                    q = random.random() #on choisis un q aléatoire
                    if q <= self.q0 :
                        # on choisis la fourmie à avancer dans la colonie l de la solution d'indice k
                        j , maxi = -1 , 0
                        for l in range(m): #on parcours les lignes de bus 
                            j0 , maxi0 = self.eq1(tau, eta, S[k][l][-1], l, J, k)
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
                                distrib.append(self.calcul_proba(tau,eta,S[k][l][-1],j,k,l,J))
                            #tirage
                            elt = self.tirage(distrib)
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
                    
                    #maj de tau en suivant l'eq 3
                    tau[l][j] = (1-self.rho)*tau[l][j] + self.rho*self.tau_0

                #maj k 
                k += 1

        return J,S,tau
    
    def maj_meilleur_solution(self,S,L,passager,main_stop,m,coord):
        for k in range(self.r):
            # on calcule la performance de la solution k
            L[k] = self.evaluer(S[k],passager,main_stop,m,coord)

            # on met à jour la meilleure solution 
            if L[ k] < self.L_best or self.L_best == -1 : 
                self.L_best = L[k]
                self.S_best = S[k]

        # on enregistre le nouveau L_best
        self.historique_L_best.append(self.L_best)
    
    def maj_pheromones(self,m,n,tau,tau_s):
        for l in range(m):
            for i in range(n):
                for j in range(n):
                    if i != j :
                        if j in self.S_best[l] and i in self.S_best[l] :
                            tau[l][i][j] = (1-self.alpha)*tau[l][i][j] + self.alpha/self.L_best
                        else :
                            tau[l][i][j] = (1-self.alpha)*tau[l][i][j]

        # maj pour les phéromones initiaux :
        for l in range(m):
            for j in range(n):
                if j == self.S_best[l][0] :
                    tau_s[l][j] = (1-self.alpha)*tau_s[l][j] + self.alpha/self.L_best
                else :
                    tau_s[l][j] = (1-self.alpha)*tau_s[l][j]
        return tau, tau_s

    def lancer_simulation(self,Situation):

        # récupération de la situation :
        m,n,coord,passager,main_stop = Situation.envoie_situation()

        # initialisation des paramètres auxiliaires de la simulation :
        L = np.zeros(self.r) # score de chaque solution


        # initialisation des tableau de la simulation :
        tau , eta, tau_s = self.initialisation(m,n,coord) # initialisation des phéromones et visibilités

        # lancement calcul :
        for _ in tqdm(range(self.t_max)):

            # Choix des arrets de départs des fourmis
            J, S, tau_s = self.choix_depart(m,n,main_stop,tau_s)

            # Progression des fourmis
            J,S,tau = self.progression_fourmi(m,n,main_stop,tau,eta,J,S)

            # Calcul des scores des solutions et maj de la meilleur solution
            self.maj_meilleur_solution(S,L,passager,main_stop,m,coord)

            # Maj des phéromones
            tau, tau_s = self.maj_pheromones(m,n,tau,tau_s)

    """ ------------- Fonction auxiliaire ------------ """     
    
    def calcul_distance(self,x1,y1,x2,y2):
        return np.sqrt((x1-x2)**2 + (y1-y2)**2)
    
    def eq1(self,tau,eta,i,l,J,k):
        maxi = 0
        j = -1
        for i_j in range(len(J[k])):
            h = J[k][i_j]
            aux = tau[l,i,h]*eta[l,i,h]**self.beta
            if aux >= maxi :
                maxi = aux 
                j = i_j
        return j , maxi
    
    def calcul_proba(self,tau,eta,i,j,k,l,J):
        aux = 0
        Jk = J[k]
        if len(Jk) == 1 :
            return 1
        elif j in Jk :
            for h in Jk:
                aux += tau[l,i,h]*eta[l,i,h]**self.beta
            return (tau[l,i,j]*eta[l,i,j]**self.beta)/aux
        else :
            return 0
        
    # eta_s est le même pour tt le monde donc negligeable
    def calcul_proba_s(self,tau_s,k,j,l,J):
        aux = 0
        Jk = J[k]
        if j in Jk :
            for h in Jk:
                aux += tau_s[l,h]
            return tau_s[l,j]/aux
        else :
            return 0

    # tirage aléatoire dans un tableau 
    def tirage(self,tab):
        return np.random.choice(len(tab), p=tab)
    
    ''' ------ Fonction évaluation d'une solution ----------'''
    # recherche appartenance busstop / ligne de bus
    def recherche_busstrop_ligne(self,sol,arret,m):
        for l in range(m):
            if arret in sol[l]:
                return l
        return -1

    # calcul temps pour aller d'un busstop à un autre sur la même ligne :
    def calcul_une_ligne(self,sol,ligne,arret1,arret2,coord):
        temps = 0
        i1 = sol[ligne].index(arret1)
        i2 = sol[ligne].index(arret2)
        if i2 > i1 :
            for i in range(i1,i2):
                temps += self.calcul_distance(coord[sol[ligne][i]][0], coord[sol[ligne][i]][1], coord[sol[ligne][i+1]][0], coord[sol[ligne][i+1]][1])/self.v
        else :
            for i in range(i1,i2,-1):
                temps += self.calcul_distance(coord[sol[ligne][i]][0], coord[sol[ligne][i]][1], coord[sol[ligne][i-1]][0], coord[sol[ligne][i-1]][1])/self.v
        return temps

    # calcul temps pour un passager (on suppose qu'il n'y pas d'attente à la main busstop et qu'il va dans la bonne direction)
    def calcul_un_passager(self,sol,pas,main_stop,m,coord):
        temps = 0
        depart,arrive = pas[0],pas[1]
        ligne_depart = self.recherche_busstrop_ligne(sol,depart,m)
        ligne_arrive = self.recherche_busstrop_ligne(sol,arrive,m)

        # cas où les deux arrêts sont sur la même ligne de bus
        if ligne_depart == ligne_arrive :
            temps = self.calcul_une_ligne(sol,ligne_depart,depart,arrive,coord)          
        # cas où les deux arrêts sont sur des lignes différentes
        else :
            temps = self.calcul_une_ligne(sol,ligne_depart,depart,main_stop,coord)
            temps += self.calcul_une_ligne(sol,ligne_arrive,main_stop,arrive,coord)
        return temps
                    
    # évaluation d'un solution
    def evaluer(self,sol,passager,main_stop,m,coord):
        temps_moyen = 0
        for pas in passager :
            temps_moyen += self.calcul_un_passager(sol,pas,main_stop,m,coord)
        return temps_moyen/len(passager)

""" ------- Fonction supplémentaire pour l'étude de la solution -----------"""

# Génération de passager aléatoire :
def generation_passager(n,nb_station,random_state=42):
    np.random.seed(random_state)
    passager = []
    for _ in range(n):
        depart = np.random.randint(nb_station)
        arrive = np.random.randint(nb_station)
        while arrive == depart :
            arrive = np.random.randint(nb_station)
        passager.append((depart,arrive))
    return passager

# Génération de coordonnées aléatoire :
def generation_coord(nb_station,random_state=42,x_min=0,x_max=100,y_min=0,y_max=100):
    np.random.seed(random_state)
    coord = []
    for _ in range(nb_station):
        x = np.random.randint(x_min,x_max)
        y = np.random.randint(y_min,y_max)
        while (x,y) in coord :
            x = np.random.randint(x_min,x_max)
            y = np.random.randint(y_min,y_max)
        coord.append((x,y))
    main_stop = np.random.randint(nb_station)
    return coord,main_stop


""" ----------- Main ----------- """

if __name__ == "__main__":

    """ ---- Test pour une situation précise ---- """
    # on génère 100 passager pour 8 station en mettant un random_state = 42
    ##passager = generation_passager(100,8,42)

    # on crée une situation
    ##situation = Situation(2,[(0,0),(2,4),(2,8),(4,2),(6,6),(6,0),(10,4),(14,6)],passager,4)
    # on affiche la situation
    ##print(situation)

    # on crée une simulation
    ##simulation = Simulation()
    # on affiche la simulation
    ##print(simulation)
    # on lance la simulation
    ##simulation.lancer_simulation(situation)
    # on affiche la solution
    ##simulation.affichage_solution()

    """ ---- Test mesure temps moyen d'éxécution ---- """
    """ # on crée des coord aléatoire
    coord,main_stop = generation_coord(20,42)
    # on génère des passagers
    passager = generation_passager(100,len(coord),42)
    # on crée une situation
    situation = Situation(3,coord,passager,main_stop)

    # on créer des simulations, on les fait tourner et on mesure le temps total d'exécution
    nb_simulation = 100
    temps_total = 0
    Liste_resultat = []
    for _ in tqdm(range(nb_simulation)):
        simulation = Simulation()
        debut = time.time()
        simulation.lancer_simulation(situation)
        fin = time.time()
        temps_total += fin-debut
        L_best , S_best = simulation.envoie_solution()
        Liste_resultat.append((L_best,S_best))

    # on affiche le temps total d'exécution
    print("Temps total d'exécution : ",temps_total)
    print("Temps moyen : ",temps_total/nb_simulation) """


    """ ---- Test convergence ---- """

    # on crée des coord aléatoire
    coord,main_stop = generation_coord(20,42)
    # on génère des passagers
    passager = generation_passager(100,len(coord),42)
    # on crée une situation
    situation = Situation(3,coord,passager,main_stop)
    # on lance la simulation
    simulation = Simulation()
    simulation.lancer_simulation(situation)
    # on affiche la solution
    historique_L_best = simulation.envoie_historique()
    plt.title("Evolution de L_best")
    plt.xlabel("Itération")
    plt.ylabel("L_best")
    plt.plot(historique_L_best)
    plt.show()






    
