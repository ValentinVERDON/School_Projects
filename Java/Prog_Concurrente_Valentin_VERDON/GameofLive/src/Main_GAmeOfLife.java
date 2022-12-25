import java.awt.BorderLayout;
import java.awt.EventQueue;
import java.awt.FlowLayout;
import java.awt.Graphics;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.border.EmptyBorder;

/** Principe du Game Of Life 
 * 
 * on met une configuration dans une grille 2*2 qui s'étant à l'infinie
 * 
 * Celle-ci évolue selon les règles suivantes:
 * - moins de 2 voisins: je meurs
 * - plus de 3 voisins: je meurs
 * - si je suis mort et que il y a exactement 3 voisins vivants: je vie
 *
 *
 *2 états possibles: vivant et mort
 *
 *Parralélisation:
 *	On segmente la grille en autant de partie que de threads
 */


public class Main_GAmeOfLife extends JFrame {


	private static final long serialVersionUID = 1L;

	//Nom de l'instance en cours
	static Main_GAmeOfLife instance;
	
	//Element de la fenêtre
	private JLabel Jtemps,JThreads,JTaille;
	private JPanel mainPanel,contentPanel;
	private JButton runPauseButton,restartButton;
	private int cellSize = 5; //taille des cellules
	
	//Grille
	private CellGrid cellGrid;
	
	//Variable associée au fonctionnement de la fenêtre
	private boolean isRunning = false;
	
	//Gestion du nombre de Threads
	private int Nb_Threads=10;
	
	//Thread Principale
	private MajThread majThread;
	
	//Crée le main en exécutant le programme
	public static void main(String[] var) {
		EventQueue.invokeLater(new Runnable() {
			public void run() {
				try {
					
					Main_GAmeOfLife main_GAmeOfLife = new Main_GAmeOfLife();
					main_GAmeOfLife.setVisible(true);
				} catch (Exception e) {
					e.printStackTrace();
				}
			}
		});
	}
	
	public Main_GAmeOfLife() {
		
		//On associe l'instance
		instance = this;
		
		// Paramètre de base de la fenêtre
		setTitle("Game Of Life");
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		setBounds(100, 100, 650, 650);
		mainPanel = new JPanel();
		mainPanel.setBorder(new EmptyBorder(5, 5, 5, 5));
		mainPanel.setLayout(new BorderLayout(0, 0));
		setContentPane(mainPanel);
		
		//On crée notre grille
		cellGrid = new CellGrid("random");
		
		//On crée une barre d'action en dessous la grille
		JPanel buttomPanel = new JPanel();
		FlowLayout flowLayout = (FlowLayout) buttomPanel.getLayout();
		flowLayout.setAlignment(FlowLayout.LEFT);
		mainPanel.add(buttomPanel, BorderLayout.SOUTH);
		
		
		//on crée un bouton STOP/START
		runPauseButton = new JButton("Start");
		runPauseButton.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) {
				if(isRunning){
					stopUpdate();
				}else{
					startUpdate();
				}
			}
		});
		buttomPanel.add(runPauseButton);
		
		
		//On crée un bouton RESTART
		restartButton = new JButton("Restart");
		restartButton.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) {
				if(isRunning){
					stopUpdate();
				}
				cellGrid = new CellGrid("random");
				repaintGrid();
			}
		});
		buttomPanel.add(restartButton);
		
		//On crée un text qui affiche le temps par étape
		Jtemps = new JLabel("Max temps par étape: |");
		buttomPanel.add(Jtemps);
		
		//Label nombre de Threads
		JThreads = new JLabel("Nombre de Threads: " + String.valueOf(Nb_Threads));
		buttomPanel.add(JThreads);
		
		//Label Taille de la grille
		int taille = cellGrid.getTaille();
		JTaille = new JLabel("| Taille de la grille: " + String.valueOf(taille));
		buttomPanel.add(JTaille);
		
		
		//Panel qui affiche la grille (prend toute la place dispo)
		contentPanel = new ContentPanel();
		mainPanel.add(contentPanel, BorderLayout.CENTER);
		
	}
	
	
	//Démarrage/Redémarrage du jeu
	private void startUpdate(){
		isRunning = true;
		runPauseButton.setText("Pause");
		majThread = new MajThread(cellGrid);
		majThread.setNb_Threads(Nb_Threads);
		majThread.start();
	}
	
	//Mise en pause
	private void stopUpdate(){
		isRunning = false;
		runPauseButton.setText("Start");
		majThread.lagStop();
	}
	
	//Repeindre la grille
	public void repaintGrid(){
		//On utilise invokeLater pour éviter de figer l'interface graphique
		EventQueue.invokeLater(new Runnable(){ 
			@Override
			public void run() {
				contentPanel.repaint();
			}
		});
	}
	
	//Mettre à jour le temps
	public void setTemps(long temps) {
		Jtemps.setText("Max temps par étape: " + String.valueOf(temps) +" ms |");
	}
	
	//Class du dessin de la grille
	private class ContentPanel extends JPanel{


		private static final long serialVersionUID = 1L;
		
		int taille = cellGrid.getTaille();

		@Override
		protected void paintComponent(Graphics g) {
			super.paintComponent(g);

			// PARAMETRE POUR ETRE VISIBLE
			boolean[][] partialGrid = cellGrid.getPartialGrid(0, 0, taille-1,taille-1);
			for(int x = 0, j = 0; j < partialGrid.length; x += cellSize, j++){
				for(int y = 0, i = 0; i < partialGrid.length; y += cellSize, i++){
					g.drawRect(x, y, cellSize, cellSize);
					if(partialGrid[i][j] == true){
						g.fillRect(x, y, cellSize, cellSize);
					}
				}
			}
		}
		
		
	}
}
