# -*- coding: utf-8 -*-
"""
Created on Fri Mar  4 15:58:00 2022

@author: valen
"""

import sqlite3
import matplotlib.pyplot as plt



#Dans cette première requête, on souhaite étuider les pourcentages de participation dans les régions francaises avec la possibilités de mettre des bornes inf et sup à ce pourcentage.
#On classera les résultat par ordre croissant pour lire plus facilement les données

class election:
    def __init__(self,bdd):
        self.__conn = sqlite3.connect(bdd)
    
    def __del__ (self):
        self.__conn.close()
    
    def selection_region(self,pourcentage_minimum_abst,pourcentage_max): 
        curseur = self.__conn.cursor() 
        try:
            curseur.execute('SELECT Libellédelarégion, "%Abs/Ins" FROM Presidentielle WHERE "%Abs/Ins" >='+str(int(pourcentage_minimum_abst))+' AND "%Abs/Ins"<= '+str(int(pourcentage_max))+' ORDER BY "%Abs/Ins";')
        
        #Ici, on rappele que les bornes sont des nombres entre 0 et 100
        
        except ValueError:             
            print("Les pourcentages d'abstentions doivent être des nombres entre 0 et 100")
            return None
        
        return curseur.fetchall()
    
#Dans cette seconde requête, on souhaite connaitre les écarts en poucentages de voies obtenues entre le candidat 1 et 2 en choisisant une/des régions par leur nom
    
    def diffe_voix(self,liste_région):
        curseur = self.__conn.cursor() 
        try:
            res=[]
            for i in liste_région:
                aux=curseur.execute('SELECT Libellédelarégion FROM Presidentielle WHERE Libellédelarégion = "'+i+'" ;')
                aux=curseur.fetchall()
                
                #test pour vérifier si la région existe
                if aux==[]:
                    print(i+" n'est pas une région francaise")
                
                #réalisation de la requête
                else: 
                    aux=curseur.execute('SELECT Libellédelarégion, "%Voix/Ins1" - "%Voix/Ins2" FROM Presidentielle WHERE Libellédelarégion="'+i+'";')
                    res.append(curseur.fetchall())
                    
        #gestion de l'erreur de typage
        except TypeError:             
            print("Les noms de région sont des chaînes de caractères")
        return res
            
    
if __name__ == '__main__':
    
    #on récupère la bdd
    ab=election("election.sqlite3")
    
################ Première requête #############

    #un exemple d'erreur 
    resultat=ab.selection_region(10,"cinquante")
    
    #exemple de résultat 
    mini=10     #à remplire
    maxi=23     #à remplire
    
    resultat=ab.selection_region(mini,maxi)
    print(resultat)
    
    #exploitation du résultat sous la forme d'un diagramme circulaire
    aux=""
    for i in resultat:
        aux+="\n"+i[0]
    labels = ['autres',aux]
    sizes=[(1-len(resultat)/13)*100,(len(resultat)/13)*100]
    colors=['grey','red']
    explode = (0, 0.1)
    plt.pie(sizes,labels=labels,colors=colors,autopct='%1.1f%%', shadow=True, startangle=90,explode=explode)
    plt.axis('equal')
    plt.title("Pourcentage des régions ayant pour taux d'abstention entre "+str(mini)+" et "+str(maxi))
    plt.savefig('Diagramme_abstention.png')
    plt.show()
    plt.close()
###################### Deuxième requète ######################
    
    #exemple d'erreur
    liste=ab.diffe_voix(["Occcid"])
    liste=ab.diffe_voix([1])
    
    #exemple de résultat
    liste=ab.diffe_voix(["Grand Est","Nouvelle-Aquitaine", "Auvergne et Rhône-Alpes","Bourgogne-Franche-Comté","Bretagne","Centre-Val de Loire","Île-de-France","Occitanie","Hauts-de-France","Normandie","Pays de la Loire","Provence-Alpes-Côte d'Azur","Corse","Guadeloupe","Martinique","Guyane","La Réunion","Mayotte"])
    print(liste)
    
    #Tracer de l'histogramme
    
    plt.figure(figsize = (10, 10))

    Ecart=[i[0][1] for i in liste]
    Noms=[i[0][0] for i in liste]
    l=len(Ecart) 
    plt.barh(range(l),Ecart,  edgecolor = ['blue' for i in range(l)],color = ['yellow' for i in range(l)],linestyle ='solid', hatch ='/') 
    plt.yticks(range(l),Noms) 
    plt.title("Ecart en pourcentage de voix entre les deux candidats")
    
    AVG=0
    for i in Ecart:
        AVG+=i
    AVG=AVG/l
        
    plt.plot([AVG,AVG],[0,l],linestyle = 'dashed', linewidth = 2)#ligne verticale correspondant à la moyenne totale des prix 
    plt.text(AVG, -0.3, "Moyenne",horizontalalignment = 'center', verticalalignment = 'center') 
    plt.savefig('Histogramme_écart_candidat.png')
    plt.show()
    plt.close()
    