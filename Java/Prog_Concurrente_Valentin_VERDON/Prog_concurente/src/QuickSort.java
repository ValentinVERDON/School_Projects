/**Principe:
-mettre un nombre fixe de threads
- on sépare notre tableau en autant de thread donné
- chacun d'entre eux fait un quick sort
- on utilise un thread final pour tout regrouper (cette action fait perdre beaucoup de temps ...)
**/

import java.util.Random;



public class QuickSort {
	static int Nb_threads = 8;
	 
	// ----------- Trie Rapide -----------------
	
	//initialisation du tri avec en entrée uniquement le tableau
    public static void triRapide(double tableau[]){
    int longueur=tableau.length;
    triRapide(tableau,0,longueur-1);
    }
    
	private static void triRapide(double tableau[],int deb,int fin){
	    if(deb<fin){
	        int positionPivot=partition(tableau,deb,fin);
	        triRapide(tableau,deb,positionPivot-1);
	        triRapide(tableau,positionPivot+1,fin);
	        }
	    }
    
    //On déplace les éléments du tableau pour avoir un tableau trié en fonction du pivot
	private static int partition(double tableau[],int deb,int fin){
	    int compt=deb;
	    double pivot=tableau[deb];
	    
	    for(int i=deb+1;i<=fin;i++){
	        if (tableau[i]<pivot){
	            compt++;//définie la place du pivot pour la fin de la boucle
	            //On met l'élément tableau[i] à sa place (peut importe la place du pivot à ce moment)
	            echanger(tableau,compt,i);
	            }
	        }
	    //On met le pivot au bon endroit
	    echanger(tableau,deb,compt);
	    return(compt);
	    }
	
	// Fonction pour échanger deux éléments du tableau
	public static void echanger(double[] tableau, int compt, int i ) {
		double aux = tableau[compt];
		tableau[compt]=tableau[i];
		tableau[i]=aux;
	}
	
	// --------------- Parralélisation -------------------
	private static class Calcul implements Runnable{
		int deb;
		int fin;
		double[] tab;
		
		//Contructeur pour passer les indices du Threads
		public Calcul(double[] tab,int deb, int fin) {
			this.deb=deb;
			this.fin=fin;
			this.tab=tab;
		}
		
		public void run() {
			triRapide(this.tab,this.deb,this.fin);
		}
	}
	
	//Regrouper les différents sous tableaux de la parralélisation
	public static double [] concatenation(double[] tab, int[] indice) {
		double [] result = new double[tab.length];
		for (int i=0;i<tab.length;i++) {
			
			//On choisis le premier indice encore valable
			int aux_indice = 0;
			while (indice[aux_indice]>indice[aux_indice+1]) {
				aux_indice+=2;
				
			}
			
			//On place le plus petit élément au début du tableau de travail
			double aux_valeur = tab[indice[aux_indice]];
			for (int j=0;j<indice.length;j+=2) {
				if ((aux_valeur>tab[indice[j]])&&(indice[j]<=indice[j+1])) {
					aux_indice= j;
					aux_valeur= tab[indice[j]];
				}	
			}
			result[i]=aux_valeur;
			indice[aux_indice]+=1;
		}
		return result;
	}
	
	// ----------------- Main ----------------------
	public static void main(String[] arges) {
		
		// ------------- Préparation des programmes ----------------- 
		//Variables pour calculer le temps du programme
        long startTime;
		long endTime;
		long auxTime;
		
		// Création de mon tableau
		double[]monTableau = new double[1000000];
		Random randomNumbers = new Random(); // random number generator
        for(int i=0; i < monTableau.length; i++)  
            monTableau[i]= randomNumbers.nextInt(100000);
        
        //Création du 2nd tableau
        double[]monTableau2 = new double[1000000];
        for(int i=0; i < monTableau.length; i++)  
            monTableau2[i]= randomNumbers.nextInt(100000);
        
        // ----------- Programme sans parralélisme -------------------
		startTime = System.currentTimeMillis(); 
        triRapide(monTableau);
        endTime = System.currentTimeMillis();
        System.out.println(endTime-startTime);
        
      //---------------- Avec parralélisme: --------------------------- 
        startTime = System.currentTimeMillis();
		
        //Calcul des indices + initialisation des Threads
        int l = monTableau2.length;
        int pas = (int)l/Nb_threads;
        int deb; int fin;
        
        int[] indice = new int[Nb_threads*2];
		Thread Ids[] = new Thread[Nb_threads]; //tableau des threads
		for (int i=0; i< Nb_threads; i++){// création et paramétrage des threads
			if (i< Nb_threads-1) {
				deb = i*pas;
				fin = (i+1)*pas-1;
				indice[i*2]=deb;
				indice[i*2+1]=fin;
			}
			else {
				deb = (Nb_threads-1)*pas;
				fin = l-1;
				indice[2*i]=deb;
				indice[2*i+1]=fin;
			}
			Ids[i]= new Thread(new Calcul(monTableau2,deb,fin));
			Ids[i].start();
		}
		
        //Lancement du calcul
		for (int i=0; i < Nb_threads; i++) {
			try {
				Ids[i].join();
			}
			catch (InterruptedException ie)
			{// Ne devrait pas arriver car on n’appelle pas interrupt()
			}
		}
		auxTime=System.currentTimeMillis();
		monTableau2 =concatenation(monTableau2,indice);
		endTime = System.currentTimeMillis();
		System.out.println(auxTime-startTime);
        System.out.println(endTime-startTime);
	}//Fin main
}//Fin class
