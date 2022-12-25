/**
 * Cette classe permet de créer les grilles du jeu
 * On peut créer des grilles vierges ou aléatoire (pas encore personalisé)
 * 
 */
//Classe des gilles (taille 2000*2000)
public class CellGrid {

	//La grille est un tableau 2d de booléen
	private boolean [][] grid;
	private int taille = 1000;
	
	
	//Constructeur de CellGrid
	public CellGrid(String etat) {
		//Pour effacer la grille
		if (etat=="vide") grid= new boolean[taille][taille];
		//Pour générer une grille aléatoire
		else if (etat=="random") {
			grid= new boolean[taille][taille];
			for(int i = 0; i < taille; i++){
				for(int j = 0; j < taille; j++){
					if(Math.random() > 0.6) grid[i][j] = true;
					
				}
			}
		}//end etat="random"
	}//End CellGrid constructeur
	
	//Pour remplacer la grille
	public synchronized void replaceGrid(boolean[][] newGrid){
		grid = newGrid;
	}
	
	//Getteur
	public boolean[][]getGrid(){
		return grid;
	}
	
	public int getTaille() {
		return taille;
	}
	
	//On utilise synchronized pour bloquer les autres threads qui voudrait accéder à cette valeur
	public synchronized boolean getValue(int i,int j) {
		return grid[i][j];
	}
	
	//Idem pour un morceau de grille
	public synchronized boolean[][] getPartialGrid(int iTop, int jLeft, int iBottom, int jRight){
		//iBottom et jRight sont inclues
		boolean[][] partialGrid = new boolean[iBottom - iTop + 1][jRight - jLeft + 1]; //on crée la nouvelle grille
		for(int iOut = 0, iGrid = iTop; iGrid <= iBottom; iOut++, iGrid++){
			System.arraycopy(grid[iGrid], jLeft, partialGrid[iOut], 0, partialGrid[iOut].length); //on copie les valeur avec la méthode arraycopie
		}
		return partialGrid;
	}
}//End CellGrid Class
