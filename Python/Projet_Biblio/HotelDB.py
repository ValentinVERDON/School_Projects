# -*- coding: utf-8 -*-
"""
Created on Fri Mar  4 13:47:43 2022

@author: valen
"""

import sqlite3

class HotelDB:
    def __init__(self,bdd):
        self.__conn = sqlite3.connect(bdd)
    
        
    def __del__ (self):
        self.__conn.close()

#l'objectif de cette requête est d'avoir la liste des noms des hotels ayant le nombre d'étoile demandé
    def get_name_hotel_etoile(self,nbetoiles):
        curseur = self.__conn.cursor()
        liste=[]
        try:
            #vérification de la valeur insérée
            if nbetoiles<=0:
                raise ValueError("Le nombre d'étoile doit être strictement positif")
                
            #commande sql exécutée dans la bdd
            curseur.execute("SELECT nom FROM hotel WHERE Etoiles = " + str(nbEtoiles) +";")
            
        #erreurs renvoyées en cas de non conformité
        except TypeError as typerr:
            print('TypeError:',str(typerr))
        except ValueError as valerr:
            print('ValueError:',str(valerr))
        else:
            liste=curseur.fetchall()
        return liste
    


    def ajout(self,nom,prenom):
        curseur=self.__conn.cursor()
        # on vérifie si le client n'existe pas déjà
        try:
            curseur.execute('SELECT numclient FROM client WHERE nom="'+nom+'" AND prenom="'+prenom+'";')
        except TypeError:
            print ("Les noms et prénoms sont des chaînes de caractères")
            return None
        liste=curseur.fetchall()
        if len(liste) !=0:
            print('Le client existe déjà')
            return liste[0][0]
        # on ajoute le client
        try:
            curseur.execute("INSERT INTO client(nom,prenom) VALUES ('{}','{}');".format(nom,prenom))
            self.__conn.commit()
        except TypeError:
            print ("Les noms et prénoms sont des chaînes de caractères")
            return None
        return curseur.lastrowid
    
if __name__ == '__main__':
    #on récupère la bdd 
    aHotelDB = HotelDB('hotellerie.db')
    
######## récuperer hotels étoilés #########

    #exemple d'erreur 
    nbEtoiles="a" 
    resultat = aHotelDB.get_name_hotel_etoile(nbEtoiles) 
    nbEtoiles=-1 
    resultat = aHotelDB.get_name_hotel_etoile(nbEtoiles) 
    
    #test avec une bonne valeur 
    nbEtoiles = 2 
    resultat = aHotelDB.get_name_hotel_etoile(nbEtoiles) 
    print("Liste des noms d'hotel", nbEtoiles, "étoiles : ", resultat) 
    


####### Ajout d'un client ############
    
    #exemple d'erreur
    res=aHotelDB.ajout(1,"bernard")
    
    #test avec doublons de noms et prénoms
    res=aHotelDB.ajout("Dupont","Marcel")
    
    #ajout d'un client 
    res=aHotelDB.ajout("Tintin","Milou") 
    print(res)


