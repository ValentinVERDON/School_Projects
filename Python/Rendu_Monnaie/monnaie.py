# -*- coding: utf-8 -*-
"""
Created on Fri May  6 13:51:14 2022

@author: valen
"""



""" méthode glouttone """

def Monnaie_Gloutonne(S,M,D):
    compteur=len(S)-1
    T=[0 for i in range(len(S))]
    while M!=0:
        trouvé = False
        while not trouvé and compteur >=0:
            if S[compteur]<=M and D[compteur]>0:
                trouvé=True
            compteur-=1
        nb_piece=M//S[compteur+1]
        if D[compteur+1]<nb_piece:
            nb_piece=D[compteur+1]
        D[compteur+1]=D[compteur+1]-nb_piece
        T[compteur+1]= nb_piece
        M=M-nb_piece*S[compteur+1]
        if D==[0 for i in range(len(S))]:
            return "Pas assez de monnaie, il manque: " + str(M)+" centimes"
    return T
    
""" chemin minimal dans un arbre """


def present_arbre(Arbre,Elt):
    for i in range(len(Arbre[0])):
        if Arbre[0][i]==Elt:
            return [True,i]
    return [False,0]

def recherche_indice_elt_liste(L,elt):
    for i in range(len(L)):
        if L[i]==elt:
            return i
    return None

def Monnaie_graphe(S,M):
    File = [M]
    Arbre = [[M],[]] #liste des noeuds, liste des arcs
    M3=1
    while File!=[] and M3!=0:
        M2=File.pop(0)
        cpt=len(S)-1
        while M3!=0 and cpt>-1:
            piece=S[cpt]
            if piece > M2:
                pass
            else:
                [rep,noeud]=present_arbre(Arbre,M2-piece)
                if rep:
                    Arbre[1].append([len(Arbre[0]),noeud,piece])
                else:
                    Arbre[0].append(M2-piece)
                    Arbre[1].append([len(Arbre[0])-1,len(Arbre[0]),piece])
                    File.append(M2-piece)
                    M3=M2-piece
            cpt-=1
                        
    if File==[] and M3!=0:
        return "Le rendu de monnaie est impossible"
    print(Arbre[0])
    print(Arbre[1])
    T=[0 for i in range(len(S))]
    noeud=len(Arbre[0])-2
    compteur = len(Arbre[1])-1
    while noeud!=1:
        [a,b,piece]=Arbre[1][compteur]
        while a!=noeud and b!=noeud:
            compteur-=1
            [a,b,piece]=Arbre[1][compteur]
        if a==noeud:
            noeud=b
            T[recherche_indice_elt_liste(S, piece)]+=1
        if b==noeud:
            noeud=a
            T[recherche_indice_elt_liste(S, piece)]+=1
    return T
            
""" Correction ... pour la génération de l'arbre avec dictionnaire """

def Monnaie_Graphe2(S,M):
    F=[M]
    A={}
    A[M]={}
    M1=M
    while len(F)>0 and M1>0:
        M1=F.pop(0)
        for s in S:
            Mfils=M1-s
            if Mfils>=0:
                if Mfils not in A :
                    A[Mfils]={}
                    F.append(Mfils)
                A[M1][Mfils]=s
    return A          



"""Détermination du plus court chemin"""

def plusCourtChemin(S,M):
    A=Monnaie_Graphe2(S, M)
    if 0 not in A :
        return []
    chemin=[]
    cible=0
    while sum(chemin)!=M:
        for noeud in A :
            if cible in A[noeud]:
                chemin.append(A[noeud][cible])
                cible=noeud
                break
    return chemin

""" Algro Programmation Dynamique """ 

def Monnaie(S,M):
    mat=[[0 for i in range(M+1)] for i in range(len(S)+1)]
    for i in range(len(S)+1):
        for m in range(M+1):
            if m==0:
                mat[i][m]=0
            elif i==0:
                mat[i][m]=float('inf') 
            else:
                aux1,aux2=float('inf') ,float('inf') 
                if m-S[i-1]>=0:
                    aux1=1+mat[i][m-S[i-1]]
                if i>=1:
                    aux2=mat[i-1][m]
                mat[i][m]=min(aux1,aux2)
    return mat[len(S)][M]

"""Idem avec nombre de pièce """

def recherche_elt(L,elt):
    for i in range(len(L)):
        if L[i]==elt:
            return i
    return None
        

def Monnaie_D(S,M,D):
    mat=[[[0,[],D] for i in range(M+1)] for i in range(len(S)+1)]
    for i in range(len(S)+1):
        for m in range(M+1):
            if m==0:
                mat[i][m]=[0,[],D]
            elif i==0:
                mat[i][m]=[float('inf'),[],D]
            else:
                aux1,aux2=[float('inf'),[],D] ,[float('inf'),[],D] 
                if m-S[i-1]>=0 and mat[i][m-S[i-1]][2][i-1]>0:
                    aux1=[1+mat[i][m-S[i-1]][0],mat[i][m-S[i-1]][1].copy(),mat[i][m-S[i-1]][2].copy()]
                    aux1[1].append(S[i-1])
                    aux1[2][i-1]-=1
                if i>=1:
                    aux2=mat[i-1][m]
                if aux1[0]>aux2[0]:
                    mat[i][m]=aux2
                else:
                    mat[i][m]=aux1
    if mat[len(S)][M][0]==float('inf'):
        return "On ne peut pas rendre la monnaie"
    return mat[len(S)][M]


""" minimisation poids """

def Monnaie_Poids(S,P,M):
    mat=[[[0,0] for i in range(M+1)] for i in range(len(S)+1)] #on construit le tableau avec (reste,poids)
    for i in range(len(P)+1):
        for m in range(M+1):
            if m==0:
                mat[i][m]=[0,0]
            elif i==0:
                mat[i][m]=[float('inf'),float('inf')]
            else:
                aux1,aux2=[float('inf'),float('inf')] ,[float('inf'),float('inf')]
                if m-S[i-1]>=0:
                    aux1=[1+mat[i][m-S[i-1]][0],mat[i][m-S[i-1]][1]+P[i-1]]
                if i>=1:
                    aux2=mat[i-1][m]
                if aux1[1]>aux2[1]:
                    mat[i][m]=aux2
                else:
                    mat[i][m]=aux1
    return mat[len(S)][M]
            
"""Poids Gloutonne"""

def Poids_Gloutonne(S,P,M):
    L=[(P[i]/S[i],S[i],P[i]) for i in range(len(S))]
    for i in range(len(L)):
        aux=L[i][0]
        indice=i
        for j in range(i+1,len(L)):
            if aux>L[j][0]:
                aux=L[j][0]
                indice=j
        L[indice],L[i]=L[i],L[indice]
    M1=M
    res=0 
    while M1!=0:
        indice=0
        while indice < len(L) and M1<L[indice][1]:
            indice+=1
        r,s,p=L[indice]
        res =res + p*(M1//s)
        M1=M1%s
    return res
        


if __name__ == "__main__":
    
    S=[1,2,5,10,20,50,100,200,500,1000,2000,5000,10000]
    D=[0,0,0,0,0,100,10,0,0,0,0,0,0]


    S=[1,7,23]
    D=[5,2,100]
    M=28
    #print(plusCourtChemin(S, M))
    #print(Monnaie_D(S,M,D))
    
    S=[1,3,4,7]
    P=[10,27,32,55]
    #print(Monnaie_Poids(S, M, P))
    
    S=[1,3,4]
    D=[10,0,2]
    M=7
    print(Monnaie_D(S, M, D))
   
    
   
    S=[1,3,4,7]
    P=[10,27,32,55]
    compteur=1
    a=Poids_Gloutonne(S,P,compteur)
    b=Monnaie_Poids(S,P,compteur)[1]
    while a==b and compteur<=20:
        compteur +=1
        a=Poids_Gloutonne(S, P, compteur)
        b=Monnaie_Poids(S,P,compteur)[1]
    print(a,b,compteur)
    
    
    
    
        
        