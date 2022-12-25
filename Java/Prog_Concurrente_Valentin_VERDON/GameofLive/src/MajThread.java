/**
 * 
 * Cette classe a pour objectif de gérer les actions des Threads.
 * C'est ici qu'on implémente la logique du jeu.
 *
 */


public class MajThread extends Thread{
	
	//Gestion des grilles
	private boolean[][] oldGrid, newGrid;
	private CellGrid cellGrid;
	//Nombre de Threads
	private int Nb_Threads;
	//Indicateur START/STOP
	private boolean toStop= false;
	
	// Constructeur qui récupère la grille
	public MajThread(CellGrid cellGrid){
		this.cellGrid = cellGrid;
	}
	
	//Mesure du temps
	private long temps = 0;
	
	
	@Override
	public void run(){
		//Action à réaliser en permanence
		while(toStop == false){
			
			long deb = System.currentTimeMillis();
			//Récupération + création des grilles de travail
			oldGrid = cellGrid.getGrid();
			newGrid = new boolean[oldGrid.length][oldGrid[0].length];
			
			//Création des SousThread (Thread de travail)
			SousThread[] sousThread = new SousThread[Nb_Threads];
			
			//Caclul de la taille des morceaux de grille
			int blockSize = oldGrid.length / Nb_Threads;
			
			//Création des sousThreads
			for(int i = 0; i < Nb_Threads; i++){
				int iEnd = (i == Nb_Threads - 1) ? oldGrid.length : (i+1) * blockSize;
				sousThread[i] = new SousThread(i * blockSize, iEnd);
				sousThread[i].start();
			}
			
			//On lance les sousThreads
			for(int i = 0; i < sousThread.length; i++){
				try {
					sousThread[i].join();
				} catch (InterruptedException e) {
					e.printStackTrace();
				}
			}
			
			long fin = System.currentTimeMillis();
			
			if ((fin-deb)>temps) temps = fin-deb;
			Main_GAmeOfLife.instance.setTemps(temps);
			//On remplace la grille en évitant les conflits entre les Threads
			synchronized(this){
				if(toStop == false){
					cellGrid.replaceGrid(newGrid);
				}
			}
			
			
			//On repaint la grille
			Main_GAmeOfLife.instance.repaintGrid();
		}
	}
	
	
	
	//Mise sur Stop
	public synchronized void lagStop(){
		toStop = true;
	}
	
	public void setNb_Threads(int value) {
		Nb_Threads = value;
	}
	
	//Classe des SousThreads (Thread de travail)
	private class SousThread extends Thread{
		private int iStart, iEnd;
		
		//Constructeur avec leur zone de travail
		public SousThread(int iStart, int iEnd){
			this.iStart = iStart;
			this.iEnd = iEnd;
		}
		
		@Override
		public void run() {
			//iEnd is excluded
			
			//On parcours le morceau de lignes du Thread
			for(int i = iStart; i < iEnd; i++){
				//On parcours toute la colonne
				for(int j = 0; j < oldGrid[0].length; j++){
					//On compte les voisins vivants
					int count = 0;
					//On parcours le voisinage
					for(int iSub = Math.max(0, i - 1); iSub < Math.min(i + 2, oldGrid.length); iSub++){
						for(int jSub = Math.max(0, j - 1); jSub < Math.min(j + 2, oldGrid[i].length); jSub++){
							if(iSub == i && jSub == j){
								continue;
							}
							if(oldGrid[iSub][jSub]){
								count++;
							}
						}
					}
					// Action en fonction de l'état des voisins
					if(count < 2 || count > 3){
						newGrid[i][j] = false;
					}else if(count == 3){
						newGrid[i][j] = true;
					}else{
						newGrid[i][j] = oldGrid[i][j];
					}
				}
			}
		}
	}
}
