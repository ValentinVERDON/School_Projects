# importer le fichier python main_VS.py
import main_VS
from tkinter import *

# Création de la classe de la fenêtre principale
class MainWindow(Tk):

    def __init__(self):
        Tk.__init__(self)
        self.title("Algo géntique BUS")
        self.geometry("600x600")
        self.resizable(width=False, height=False)
        self.config(background='#41B77F')

        # créer le panel de gauche qui contiendra les paramètres :
        self.left_panel = Frame(self, width=200, height=600, bg='#ECF0F1')
        
        #scider le panel en 2 partie : la première avec le titre "Paramètre de la Situation" et le second "Paramètre de la Simulation"
        self.left_panel_top = Frame(self.left_panel, width=200, height=300, bg='#D0D3D4')
        self.left_panel_bottom = Frame(self.left_panel, width=200, height=300, bg='#D0D3D4')

        # créer le titre "Paramètre de la Situation"
        self.left_panel_top_title = Label(self.left_panel_top, text="Paramètre de la Situation", font=("Courrier", 14), bg='#ECF0F1')
        self.left_panel_top_title.pack()

        # créer le titre "Paramètre de la Simulation"
        self.left_panel_bottom_title = Label(self.left_panel_bottom, text="Paramètre de la Simulation", font=("Courrier", 14), bg='#ECF0F1')
        self.left_panel_bottom_title.pack()

        # mettre dans chacun de ces deux panel une grille qui acceuillera les labels à gauche et à droite des entré (type spinbox par exemple)
        self.left_panel_top_grid = Frame(self.left_panel_top, width=200, height=300, bg='#D0D3D4')
        self.left_panel_bottom_grid = Frame(self.left_panel_bottom, width=200, height=300, bg='#D0D3D4')

        # créer les labels à gauche des entrées
        self.left_panel_top_grid_label1 = Label(self.left_panel_top_grid, text="Nombre de bus", font=("Courrier", 12), bg='#ECF0F1')
        self.left_panel_top_grid_label2 = Label(self.left_panel_top_grid, text="Nombre de station", font=("Courrier", 12), bg='#ECF0F1')

        # créer les entrées
        self.left_panel_top_grid_entry1 = Spinbox(self.left_panel_top_grid, from_=0, to=100, width=5)
        self.left_panel_top_grid_entry2 = Spinbox(self.left_panel_top_grid, from_=0, to=100, width=5)

        # mettre les labels (centré à gauche) et les entrées (centré à droite) dans la grille 
        self.left_panel_top_grid_label1.grid(row=0, column=0, sticky=W)
        self.left_panel_top_grid_entry1.grid(row=0, column=1, sticky=E)
        self.left_panel_top_grid_label2.grid(row=1, column=0, sticky=W)
        self.left_panel_top_grid_entry2.grid(row=1, column=1, sticky=E)


        # occupons nous du panel simulation en mettant les labels : tau,r,beta,rho,alpha,v,q0,t_max avec pour r et t_max un spinbox et pour les autres une entrée numérique avec potentiellement des décimales (mais toujours positif)
        self.left_panel_bottom_grid_label1 = Label(self.left_panel_bottom_grid, text="Tau", font=("Courrier", 12), bg='#ECF0F1')
        self.left_panel_bottom_grid_label2 = Label(self.left_panel_bottom_grid, text="R", font=("Courrier", 12), bg='#ECF0F1')
        self.left_panel_bottom_grid_label3 = Label(self.left_panel_bottom_grid, text="Beta", font=("Courrier", 12), bg='#ECF0F1')
        self.left_panel_bottom_grid_label4 = Label(self.left_panel_bottom_grid, text="Rho", font=("Courrier", 12), bg='#ECF0F1')
        self.left_panel_bottom_grid_label5 = Label(self.left_panel_bottom_grid, text="Alpha", font=("Courrier", 12), bg='#ECF0F1')
        self.left_panel_bottom_grid_label6 = Label(self.left_panel_bottom_grid, text="V", font=("Courrier", 12), bg='#ECF0F1')
        self.left_panel_bottom_grid_label7 = Label(self.left_panel_bottom_grid, text="Q0", font=("Courrier", 12), bg='#ECF0F1')
        self.left_panel_bottom_grid_label8 = Label(self.left_panel_bottom_grid, text="T_max", font=("Courrier", 12), bg='#ECF0F1')


        # créer les entrées

        self.left_panel_bottom_grid_entry1 = Entry(self.left_panel_bottom_grid, width=5,)
        self.left_panel_bottom_grid_entry2 = Spinbox(self.left_panel_bottom_grid, from_=1, to=100, width=5)
        self.left_panel_bottom_grid_entry3 = Entry(self.left_panel_bottom_grid, width=5)
        self.left_panel_bottom_grid_entry4 = Entry(self.left_panel_bottom_grid, width=5)
        self.left_panel_bottom_grid_entry5 = Entry(self.left_panel_bottom_grid, width=5)
        self.left_panel_bottom_grid_entry6 = Entry(self.left_panel_bottom_grid, width=5)
        self.left_panel_bottom_grid_entry7 = Entry(self.left_panel_bottom_grid, width=5)
        self.left_panel_bottom_grid_entry8 = Spinbox(self.left_panel_bottom_grid, from_=1, to=100, width=5)

        # on met les valeurs d'origine dans les Entry :
        self.left_panel_bottom_grid_entry1.insert(0, 0.5)
        self.left_panel_bottom_grid_entry3.insert(0, 0.5)
        self.left_panel_bottom_grid_entry4.insert(0, 0.5)
        self.left_panel_bottom_grid_entry5.insert(0, 0.5)
        self.left_panel_bottom_grid_entry6.insert(0, 1)
        self.left_panel_bottom_grid_entry7.insert(0, 0.5)


        # mettre les labels (centré à gauche) et les entrées (centré à droite) dans la grille

        self.left_panel_bottom_grid_label1.grid(row=0, column=0, sticky=W)
        self.left_panel_bottom_grid_entry1.grid(row=0, column=1, sticky=E)
        self.left_panel_bottom_grid_label2.grid(row=1, column=0, sticky=W)
        self.left_panel_bottom_grid_entry2.grid(row=1, column=1, sticky=E)
        self.left_panel_bottom_grid_label3.grid(row=2, column=0, sticky=W)
        self.left_panel_bottom_grid_entry3.grid(row=2, column=1, sticky=E)
        self.left_panel_bottom_grid_label4.grid(row=3, column=0, sticky=W)
        self.left_panel_bottom_grid_entry4.grid(row=3, column=1, sticky=E)
        self.left_panel_bottom_grid_label5.grid(row=4, column=0, sticky=W)
        self.left_panel_bottom_grid_entry5.grid(row=4, column=1, sticky=E)
        self.left_panel_bottom_grid_label6.grid(row=5, column=0, sticky=W)
        self.left_panel_bottom_grid_entry6.grid(row=5, column=1, sticky=E)
        self.left_panel_bottom_grid_label7.grid(row=6, column=0, sticky=W)
        self.left_panel_bottom_grid_entry7.grid(row=6, column=1, sticky=E)
        self.left_panel_bottom_grid_label8.grid(row=7, column=0, sticky=W)
        self.left_panel_bottom_grid_entry8.grid(row=7, column=1, sticky=E)

        # mettre en dessous des panel top et bottom un bouton : lancer
        self.left_panel_button = Button(self.left_panel, text="Lancer", font=("Courrier", 12), bg='#ECF0F1')

        # affiche des panels
        self.left_panel.pack(side=LEFT, padx=10, pady=10)
        self.left_panel_top.pack(side=TOP, padx=10, pady=10)
        self.left_panel_button.pack(side=BOTTOM, padx=10, pady=10)
        self.left_panel_bottom.pack(side=BOTTOM, padx=10, pady=10)
        self.left_panel_top_grid.pack(side=TOP, padx=10, pady=10)
        self.left_panel_bottom_grid.pack(side=BOTTOM, padx=10, pady=10)

        
        





# Programme principale
if __name__ == "__main__":
    window = MainWindow()
    window.mainloop()