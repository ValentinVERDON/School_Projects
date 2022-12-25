import java.awt.Graphics;

import javax.swing.JFrame;
import javax.swing.JPanel;

public class Line extends JPanel{
	private int x1,x2;
	private int y1,y2;
	
	public Line(int x1, int x2, int y1, int y2) {
		this.x1 = x1;
		this.x2 = x2;
		this.y1 = y1;
		this.y2 = y2;
		
	}
	
	public void paint(Graphics g) {
		g.drawLine(x1,y1,x2,y2);
	}
	
	public static void main(String[] args){
	    JFrame f = new JFrame("Dessiner une ligne");
	    Line l;
	    f.getContentPane().add(l = new Line(20,20,200,200));
	    l.paint(null);
	    f.setSize(250, 250);
	    f.setVisible(true);
	    f.setResizable(false);
	    f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
	  }
}
