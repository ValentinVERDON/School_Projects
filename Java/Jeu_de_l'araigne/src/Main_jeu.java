import java.awt.Color;
import java.awt.Dimension;
import java.awt.FlowLayout;
import java.awt.Font;
import java.awt.GridLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import javax.swing.BorderFactory;
import javax.swing.BoxLayout;
import javax.swing.JButton;
import javax.swing.JColorChooser;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JTable;
import javax.swing.SwingConstants;
import javax.swing.border.LineBorder;

public class Main_jeu extends JFrame{

	public static void main(String[] args) {
		new Main_jeu();

	}
	
	
	JPanel pStart, pButtonStart;
	JTable tableau;
	
	
	Pion h1,h2, h3, m1, m2, m3, b1, b2, b3;
	Pion[][] Pions;
	
	JPanel panJeu,panJeuGrille, panJeuLabel,panParametre,panColor;
	JLabel annonce;
	
	JButton start, bcouleur_j1,bcouleur_j2,parametre;
	JLabel titre;
	
	JPanel pVainqueur, pVainqueurButton, pVainqueurLabel;
	JLabel resultat;
	JButton restart, accueil;
	
	Color couleur_j1;
	Color couleur_j2;
	
	int red1,red2,blue1,blue2,green1,green2;
	int c_red1,c_red2,c_blue1,c_blue2,c_green1,c_green2;
	
	
	public int Joueur;
	public int Total_activated;
	public int mem_i,mem_j;
	public int mem_etat;
	public boolean wantMove = false;
	
	
	public Main_jeu(){
		
		super("Jeu de l'araigné");
		setSize(600,600);
	    setBackground(new Color(191,219,246));
	    
        
        
      //---------- Page Start  -------------
        
        pStart = new JPanel();
        pStart.setBackground(new Color(191,219,246));
	    pStart.setLayout(new GridLayout(2,1));
        
	    //titre
        pStart.add(titre = new JLabel("Jeu de l'araignée", SwingConstants.CENTER));
        titre.setFont(new Font("serif", Font.BOLD, 50));
        
        //bouton start
        pButtonStart = new JPanel();
        pButtonStart.setLayout(new FlowLayout());
        pButtonStart.setBackground(new Color(191,219,246));
        
        pButtonStart.add(start = new JButton("Commencer"));
        start.setPreferredSize(new Dimension(200,50));
        start.setFont(new Font("serif", Font.BOLD, 20));
        
        start.addActionListener(new ActionListener() {
        	public void actionPerformed(ActionEvent e) { 
        		StartGame();
        		pStart.setVisible(false);
        		revalidate();
        		repaint();
        	} 
        });
        
        pButtonStart.add(parametre = new JButton("Paramètres"));
        parametre.setPreferredSize(new Dimension(200,50));
        parametre.setFont(new Font("serif", Font.BOLD, 20));
        
        parametre.addActionListener(new ActionListener() {
        	public void actionPerformed(ActionEvent e) {
        		pStart.setVisible(false);  
        		ChooseColor();
        	}	
        });
        
        pStart.add(pButtonStart);
        
        add(pStart);
        
        //---------- Parametrage  -------------
        
	    setVisible(true);
	    setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
	    
	    couleur_j1=Color.red;
        couleur_j2=Color.blue;
        RecupColor();
        
	}
      
	
	//---------- Page Couleur  -------------
	
	public void RecupColor() {
		
		//récupération des couleurs choisis
		red1 = couleur_j1.getRed();
        green1 = couleur_j1.getGreen();
        blue1 = couleur_j1.getBlue();
        red2 = couleur_j2.getRed();
        green2 = couleur_j2.getGreen();
        blue2 = couleur_j2.getBlue();
	}
	
	
	public void ChooseColor() {
        
		panParametre = new JPanel();
		panParametre.setBackground(new Color(191,219,246));
		panParametre.setLayout(new GridLayout(2,1));
		
		//titre
        panParametre.add(titre = new JLabel("Paramètres", SwingConstants.CENTER));
        titre.setFont(new Font("serif", Font.BOLD, 30));
		
		panColor = new JPanel();
		panColor.setBackground(new Color(191,219,246));
		panColor.setLayout(new FlowLayout());
		
		
        //boutons couleurs
        panColor.add(bcouleur_j1 = new JButton("Couleur Joueur 1"));
        bcouleur_j1.setPreferredSize(new Dimension(200,50));
        bcouleur_j1.setFont(new Font("serif", Font.BOLD, 20));
        
        bcouleur_j1.addActionListener(new ActionListener() {
        	public void actionPerformed(ActionEvent e) {
        		couleur_j1=JColorChooser.showDialog(pStart,"Select a color",couleur_j1);   
        		RecupColor();
        	}	
        });
        
        panColor.add(bcouleur_j2 = new JButton("Couleur Joueur 2"));
        bcouleur_j2.setPreferredSize(new Dimension(200,50));
        bcouleur_j2.setFont(new Font("serif", Font.BOLD, 20));
        
        bcouleur_j2.addActionListener(new ActionListener() {
        	public void actionPerformed(ActionEvent e) {
        		couleur_j2=JColorChooser.showDialog(pStart,"Select a color",couleur_j2); 
        		RecupColor();
        	}	
        });
        
        
        //bouton accueil
      		panColor.add(accueil = new JButton("Accueil"));
      		accueil.setPreferredSize(new Dimension(200,50));
      		accueil.setFont(new Font("serif", Font.BOLD, 20));
      		
      		accueil.addActionListener(new ActionListener() {
      			public void actionPerformed(ActionEvent e) {
      				pStart.setVisible(true);
      				panParametre.setVisible(false);
      				revalidate();
              		repaint();
      			}
      		});
        
        panParametre.add(panColor);
        add(panParametre);
   }


	public void StartGame() {
		
		// Initialisation
        Joueur =1;
        Total_activated = 0;
		
		panJeu = new JPanel();
		panJeu.setLayout(new BoxLayout(panJeu, BoxLayout.Y_AXIS));
		
		panJeuLabel = new JPanel();
		panJeuLabel.setBackground(new Color(191,219,246));
		panJeuLabel.add(annonce = new JLabel("Phase 1 : Choix des cases du joueur "+String.valueOf(Joueur)));
		annonce.setBorder(BorderFactory.createEmptyBorder(20, 0, 0, 0));
		annonce.setFont(new Font("serif", Font.BOLD, 20));
		
		panJeu.add(panJeuLabel);
		
		panJeuGrille = new JPanel();
	    panJeuGrille.setLayout(new GridLayout(3,3));
	    panJeuGrille.setBackground(new Color(191,219,246));
	    panJeuGrille.setPreferredSize(new Dimension(600,600));
	    panJeuGrille.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
	    
		
		
		
        //Grille
        
        panJeuGrille.add(h1 = new Pion());
        panJeuGrille.add(h2 = new Pion());
        panJeuGrille.add(h3 = new Pion());
        
        panJeuGrille.add(m1 = new Pion());
        panJeuGrille.add(m2 = new Pion());
        panJeuGrille.add(m3 = new Pion());
        
        panJeuGrille.add(b1 = new Pion());
        panJeuGrille.add(b2 = new Pion());
        panJeuGrille.add(b3 = new Pion());
        
        Pions = new Pion[3][3];
        Pions[0][0] = h1;Pions[0][1] = h2;Pions[0][2] = h3;
        Pions[1][0] = m1;Pions[1][1] = m2;Pions[1][2] = m3;
        Pions[2][0] = b1;Pions[2][1] = b2;Pions[2][2] = b3;
        
        panJeu.add(panJeuGrille);
        add(panJeu);
        pack();
		
	}
	
	//Test si le mouvement fait gagner la partie
	public boolean TestVainqueur() {
		
		for (int i=0; i<3; i++) {
			if ((Pions[i][0].etat == Pions[i][1].etat) && (Pions[i][0].etat == Pions[i][2].etat) && (Pions[i][0].etat != 0)) {
				return true;
			}
		}

		for (int j=0; j<3; j++) {
			if ((Pions[0][j].etat == Pions[1][j].etat) && (Pions[0][j].etat == Pions[2][j].etat) && (Pions[0][j].etat != 0)) {
				return true;
			}
				
		}

		if ((Pions[0][0].etat == Pions[1][1].etat) && (Pions[0][0].etat == Pions[2][2].etat) && (Pions[0][0].etat != 0)) {
			return true;
		}
			

		if ((Pions[0][2].etat == Pions[1][1].etat) && (Pions[0][2].etat == Pions[2][0].etat) && (Pions[0][2].etat != 0)) {
			return true;
		}
		
		return false;
		
	}
	
	//affichage du résultat de la partie
	public void AfficheVainqueur(int e) {
		
		//fenetre principale
		pVainqueur = new JPanel();
		pVainqueur.setSize(300,300);
		pVainqueur.setLayout(new GridLayout(2,1));
		pVainqueur.setBackground(new Color(191,219,246));
		
		//label resultat
		pVainqueur.add(resultat = new JLabel("",SwingConstants.CENTER));
		resultat.setFont(new Font("serif", Font.BOLD, 40));
		
		//bouton restart
		pVainqueurButton = new JPanel();
		pVainqueurButton.setLayout(new FlowLayout());
		pVainqueurButton.setBackground(new Color(191,219,246));
		
		pVainqueurButton.add(restart = new JButton("Recommencer"));
		restart.setPreferredSize(new Dimension(200,50));
		restart.setFont(new Font("serif", Font.BOLD, 20));
		
		restart.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				StartGame();
				pVainqueur.setVisible(false);
				revalidate();
        		repaint();
			}
		});
		
		pVainqueur.add(pVainqueurButton);
		
		//bouton accueil
		pVainqueurButton.add(accueil = new JButton("Accueil"));
		accueil.setPreferredSize(new Dimension(200,50));
		accueil.setFont(new Font("serif", Font.BOLD, 20));
		
		accueil.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				pStart.setVisible(true);
				pVainqueur.setVisible(false);
				revalidate();
        		repaint();
			}
		});
		
		// CHangement du texte selon le vainqueur
		if (e == 1) {
			resultat.setText("Le joueur 1 a gagné");
			resultat.setForeground(couleur_j1);
		}
		
		else {
			resultat.setText("Le joueur 2 a gagné");
			resultat.setForeground(couleur_j2);
		}
		
		
		//Changement de panel
		remove(panJeu);
		add(pVainqueur);
		revalidate();
		repaint();
	
	}
	
	public int[] indice(Pion p) {
		for(int i=0;i<3;i++) {
			for(int j=0;j<3;j++) {
				if (Pions[i][j] == p)
					return new int[] {i,j};
			}
		}
		
		return null;
	}
	
	
	public class Pion extends JButton implements ActionListener{
		
		
		public int etat;
		public int placement;
		public int ligne,colonne;
		
		public Pion() {
			super();
			setBorder(new LineBorder(Color.BLACK));
			setBackground(Color.white);
			setOpaque(true);
			setFocusPainted(false);

			addActionListener(this);
			
			etat = 0;

		}
		
		public void coloration() {
			if (Joueur == 1) {
				setBackground(couleur_j1);
				this.etat = 1;
				Joueur = 2;
			}
			else{
				setBackground(couleur_j2);
				this.etat = 2;
				Joueur = 1;
				}
		}
		
		public void decoloration() {
			setBackground(Color.white);
			etat = 0;
		}
		
		
		@Override
		public void actionPerformed(ActionEvent e) {
			
			
			// choix des pions (phase 1)
			if ((Total_activated < 6) && (etat == 0) ) {
				coloration();
				Total_activated ++;
				annonce.setText("Phase 1 : Choix des cases du joueur "+String.valueOf(Joueur));
				if (TestVainqueur() == true) {
					AfficheVainqueur(etat);
				}
			}
			
			else {
				
				// selection de la case à deplacer
				if(etat == Joueur) {
					if(etat == 1) {
						setBackground(new Color((int) (red1*0.6),(int) (green1*0.6),(int) (blue1*0.6)));
						if((wantMove ==true)&&((mem_i!=indice(this)[0])||(mem_j!=indice(this)[1]))) Pions[mem_i][mem_j].setBackground(couleur_j1); //on remet la couleur de base à la case précedemment sélectionnée
					}
					else {
						setBackground(new Color((int) (red2*0.6),(int) (green2*0.6),(int) (blue2*0.6)));
						if((wantMove ==true)&&((mem_i!=indice(this)[0])||(mem_j!=indice(this)[1]))) Pions[mem_i][mem_j].setBackground(couleur_j2); 
					}
					
					mem_i = indice(this)[0];
					mem_j = indice(this)[1];
					mem_etat = etat;
					wantMove = true;
					
					for (int i=0; i<3;i++) {
						for (int j=0; j<3;j++) {
							if(Pions[i][j].etat == 0) {
								if ((Math.abs(i-indice(this)[0])<2)&&(Math.abs(j-indice(this)[1])<2)) {
									if(etat == 1) {
										Pions[i][j].setBackground(new Color(220,220,220)); //on indique au joueur les possibilté de mouvement
									}
									else {
										
										Pions[i][j].setBackground(new Color(220,220,220)); 
									}
								}
								else {
									Pions[i][j].setBackground(Color.white);
								}
							}
						}
					}
					
				}
				
				// selection de la destination et deplacement
				if((wantMove == true) && (etat == 0)) {
					if ((Math.abs(mem_i-indice(this)[0])<2)&&(Math.abs(mem_j-indice(this)[1])<2)) {
						coloration();
						Pions[mem_i][mem_j].decoloration();
						wantMove = false;
						
						for (int i=0; i<3;i++) {
							for (int j=0; j<3;j++) {
								if(Pions[i][j].etat == 0) {
									Pions[i][j].setBackground(Color.white);
								}
							}
						}
						
						if (TestVainqueur() == true) {
							AfficheVainqueur(etat);
						}
					}
				}
				
			}
			
			if (Total_activated == 6) {
				annonce.setText("Phase 2 : déplacement du joueur " + String.valueOf(Joueur));
			}
			
			
		}
	}
}