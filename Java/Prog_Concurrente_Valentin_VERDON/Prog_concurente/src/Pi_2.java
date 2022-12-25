
public class Pi_2 {
	static int Nb_threads =20;
	static int Nb_total = 60000000;
	static int Nb_iterations = Nb_total/Nb_threads; //itérations par threads
	static double resultat_local[] = new double[Nb_threads];
	static double max = 10;
	static double pas=max/(Nb_iterations*Nb_threads);
	
	public static double f(double x) {
		return Math.exp(-x*x/2);
	}
	
	private static class Calcul implements Runnable {
		int myNum; 
		
		// pour passer le numéro du Threads en paramètre 
		public Calcul(int num) {
			myNum = num;
		}
		
		public void run(){
			double stockage = 0;
			for (int i=this.myNum*Nb_iterations; i<(this.myNum+1)*Nb_iterations; i++) {// calcul du morceau d'intégrale
				stockage+=pas*(f(pas*i)+f(pas*(i+1)))/2;
			}
			resultat_local[myNum]=stockage; //stockage du morceau d'intégrale
		}
		
		public static void main(String[] arges) {
			double valeur_pi=0;
			
			// pour calculer le temps du programme
			long startTime = System.currentTimeMillis();
			long endTime = System.currentTimeMillis();
			
			startTime = System.currentTimeMillis();
			
			Thread Ids[] = new Thread[Nb_threads]; //tableau des threads
			for (int i=0; i< Nb_threads; i++){// création et paramétrage des threads
				Ids[i]= new Thread(new Calcul(i));
				Ids[i].start();
			}
			
			//Lancement du calcul
			System.out.println("C'est parti");
			
			for (int i=0; i < Nb_threads; i++) {
				try {
					Ids[i].join();
					valeur_pi+= resultat_local[i];
				}
				catch (InterruptedException ie)
				{// Ne devrait pas arriver car on n’appelle pas interrupt()
				}
			}
			//maj valeur pi
			valeur_pi =valeur_pi*valeur_pi*2;
			
			
			//affichage du résultat
			endTime = System.currentTimeMillis();
			System.out.println(valeur_pi);
			System.out.println(endTime-startTime);

		}
	}
}
