import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.FlowLayout;

import javax.swing.BoxLayout;
import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTextArea;
import javax.swing.JTextField;

public class Test extends JFrame {
	
	JPanel p, panh, panm, panb;
	JTextField tfh1, tfh2, tfh3;
	JTextField tfm1, tfm2, tfm3;
	JTextField tfb1, tfb2, tfb3;

	public Test(){
	    super("Test de Drag'n Drop");
	    setSize(800, 660);
	    
	    p = (JPanel) getContentPane();
	    p.setLayout(new BorderLayout());

	    //-------------------------------------------------------------------------------------------------------------------------------------------------
	    //panel du haut
	    
	    p.add(panh = new JPanel(), BorderLayout.NORTH);
	    panh.setLayout(new FlowLayout());
	    
	    //premier textField
	    panh.add(tfh1 = new JTextField("Texte déplaçable !"));
	    tfh1.setDragEnabled(true); //C'est cette instruction qui permet le déplacement de son contenu
	    tfh1.setPreferredSize(new Dimension(200,200));

	    //On crée le second textfield avec contenu déplaçable
	    panh.add(tfh2 = new JTextField());
	    tfh2.setDragEnabled(true);
	    tfh2.setPreferredSize(new Dimension(200,200));
	    
	    //Et le troisième, sans
	    panh.add(tfh3 = new JTextField());
	    tfh3.setDragEnabled(true);
	    tfh3.setPreferredSize(new Dimension(200,200));

	    //-------------------------------------------------------------------------------------------------------------------------------------------------
	    //panel du milieu
	    
	    p.add(panm = new JPanel(), BorderLayout.CENTER);
	    panm.setLayout(new FlowLayout());
	    
	    //premier textField
	    panm.add(tfm1 = new JTextField());
	    tfm1.setDragEnabled(true); //C'est cette instruction qui permet le déplacement de son contenu
	    tfm1.setPreferredSize(new Dimension(200,200));

	    //On crée le second textfield avec contenu déplaçable
	    panm.add(tfm2 = new JTextField());
	    tfm2.setPreferredSize(new Dimension(200,200));
	    tfm2.setDragEnabled(true);
	    
	    //Et le troisième, sans
	    panm.add(tfm3 = new JTextField());
	    tfm3.setPreferredSize(new Dimension(200,200));
	    tfm3.setDragEnabled(true);	
	    
	    //-------------------------------------------------------------------------------------------------------------------------------------------------
	    //panel du bas
	    
	    p.add(panb = new JPanel(), BorderLayout.SOUTH);
	    panb.setLayout(new FlowLayout());
	    
	    //premier textField
	    panb.add(tfb1 = new JTextField());
	    tfb1.setDragEnabled(true); //C'est cette instruction qui permet le déplacement de son contenu
	    tfb1.setPreferredSize(new Dimension(200,200));

	    //On crée le second textfield avec contenu déplaçable
	    panb.add(tfb2 = new JTextField());
	    tfb2.setPreferredSize(new Dimension(200,200));
	    tfb2.setDragEnabled(true);
	    
	    //Et le troisième, sans
	    panb.add(tfb3 = new JTextField());
	    tfb3.setPreferredSize(new Dimension(200,200));
	    tfb3.setDragEnabled(true);	
	    
	    //-------------------------------------------------------------------------------------------------------------------------------------------------
	    setVisible(true);
	    setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
	  }

	  public static void main(String[] args){
	    new Test();
	  }  

}
