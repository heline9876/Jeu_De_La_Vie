import itertools
import tkinter as Tk
import random


class Jeu:
    def __init__(self, root):
        self.grille = [[False for _ in range(0)]for _ in range(0)]       #Chaque case représenté dans la grille est soit vivante (True) soit morte (False). Par défaut, elles sont mortes.
        self.cases_GUI = [[False for _ in range(0)]for _ in range(0)]       #Cette matrice contient les objets "rectangle" affichés dans le canvas.
        self.canvas = Tk.Canvas(root)        
        self.x = 0
        self.y = 0
        self.hauteur = 0
        self.longueur = 0
        self.taille_case = 0
        self.drapeau_arret = False
        self.root = root


    def afficher_grille(self):
        for x, y in itertools.product(range(self.longueur), range(self.hauteur)):
            if self.grille[x][y] is True:
                self.canvas.itemconfig(self.cases_GUI[x][y], fill='white')
            else:
                self.canvas.itemconfig(self.cases_GUI[x][y], fill='#080808')
    
    
    def activer_cases(self, event):  # sourcery skip: class-extract-method
        x = (event.x - (event.x%self.taille_case)) // self.taille_case
        y = (event.y - (event.y%self.taille_case)) // self.taille_case
        self.canvas.itemconfig(self.cases_GUI[x][y], fill='white')
        self.grille[x][y] = True
        
            
    def desactiver_cases(self, event):
        x = (event.x - (event.x%self.taille_case)) // self.taille_case
        y = (event.y - (event.y%self.taille_case)) // self.taille_case
        self.canvas.itemconfig(self.cases_GUI[x][y], fill='#080808')
        self.grille[x][y] = False


    def stopper_simulation(self):
        self.drapeau_arret = False
        self.canvas.bind("<Button-1>", self.activer_cases)
        self.canvas.bind("<Button-3>", self.desactiver_cases)
    
    
    def lancer_simulation(self):
        if self.drapeau_arret is False:
            self.drapeau_arret = True
            self.canvas.unbind("<Button-1>")
            self.canvas.unbind("<Button-3>")
            self.root.after(20, self.modifier_etat_cases)

    def générer_plateau_aléatoire(self):
        self.grille = [[random.random() < 0.4 for _ in range(self.hauteur)] for _ in range(self.longueur)]
        self.afficher_grille()
                    
                    
    def modifier_etat_cases(self):
        self.grille_temp = [[False for _ in range(self.hauteur)]for _ in range(self.longueur)]
        for x, y in itertools.product(range(self.longueur), range(self.hauteur)):

            nombres_voisines_vivantes = self.nombres_voisines(x, y)

            if nombres_voisines_vivantes == 3 and self.grille[x][y] is False:
                self.grille_temp[x][y] = True

            if nombres_voisines_vivantes < 2 or nombres_voisines_vivantes > 3 and self.grille[x][y] is True:
                self.grille_temp[x][y] = False

            if nombres_voisines_vivantes in [2, 3] and self.grille[x][y] is True:
                self.grille_temp[x][y] = True

        if self.grille == self.grille_temp:
            self.stopper_simulation()
        self.grille = self.grille_temp
        self.afficher_grille()
        if self.drapeau_arret:
            self.root.after(20, self.modifier_etat_cases)


    def nombres_voisines(self, x, y):
        nombre_voisines_vivantes = 0

        nombre_voisines_vivantes += self.grille[x][(y + 1) % self.hauteur]

        nombre_voisines_vivantes += self.grille[x][(y - 1) % self.hauteur]

        nombre_voisines_vivantes += self.grille[(x + 1) % self.longueur][y]
            
        nombre_voisines_vivantes += self.grille[(x - 1) % self.longueur][y]

        nombre_voisines_vivantes += self.grille[(x - 1) % self.longueur][(y + 1) % self.hauteur]

        nombre_voisines_vivantes += self.grille[(x + 1) % self.longueur][(y + 1) % self.hauteur]
            
        nombre_voisines_vivantes += self.grille[(x - 1) % self.longueur][(y - 1) % self.hauteur]

        nombre_voisines_vivantes += self.grille[(x + 1) % self.longueur][(y - 1) % self.hauteur]
        
        return nombre_voisines_vivantes
    
    
    def reinitialiser_le_plateau(self):
        self.grille = [[False for _ in range(self.hauteur)]for _ in range(self.longueur)]
        self.drapeau_arret = False
        self.modifier_etat_cases()
        
                       
    def afficher_fen_jeu(self):
        try:
            self.longueur = int(self.entry_longueur.get())
            self.hauteur = int(self.entry_hauteur.get())
            self.taille_case = int(self.entry_taille_case.get())
            for item in self.root.winfo_children():
                item.destroy()
            self.activer_widget_fen_jeu()
        except Exception:
           Tk.Label(self.root, text="Veuillez entrer un nombre.", fg='red').grid(row=9)


    def activer_widget_fen_jeu(self):
        self.grille = [[False for _ in range(self.hauteur)]for _ in range(self.longueur)]
        self.canvas = Tk.Canvas(self.root, height=self.taille_case*self.hauteur, width=self.taille_case*self.longueur, highlightthickness=0)
        self.cases_GUI = [[False for _ in range(self.hauteur)] for _ in range(self.longueur)]
        for x, y in itertools.product(range(self.longueur), range(self.hauteur)):
            self.cases_GUI[x][y] = self.canvas.create_rectangle(x*self.taille_case, y*self.taille_case, (x+1)*self.taille_case, (y+1)*self.taille_case, width=0)
        self.canvas.bind("<Button-1>", self.activer_cases)
        self.canvas.bind("<Button-3>", self.desactiver_cases)
        self.afficher_grille()
        frame = Tk.Frame()
        self.bouton_lancer_simulation = Tk.Button(frame, text="Lancer la simulation", command=self.lancer_simulation)
        self.bouton_lancer_simulation.grid(column=0, row=0)
        self.bouton_stopper_simulation = Tk.Button(frame, text="Stopper la simulation", command=self.stopper_simulation)
        self.bouton_stopper_simulation.grid(column=1, row=0)
        self.bouton_réinitialiser_simulation = Tk.Button(frame, text="Réinitialiser le plateau", command=self.reinitialiser_le_plateau)
        self.bouton_réinitialiser_simulation.grid(column=2, row=0)
        self.bouton_aléatoire_simulation = Tk.Button(frame, text="Placer des points aléatoirement", command=self.générer_plateau_aléatoire)
        self.bouton_aléatoire_simulation.grid(column=3, row=0)
        self.canvas.pack()
        frame.pack()


    def ecran_choix_nombre_cases(self):
        Tk.Label(self.root, text="Veuillez entrer le nombre de cellules à la verticale : ").grid(row=1)
        self.entry_hauteur = Tk.Entry(self.root, width=4)
        self.entry_hauteur.grid(row=2)
        self.entry_hauteur.insert(0, "25")
        Tk.Label(self.root, text="Veuillez entrer le nombre de cellules à l'horizontale : ").grid(row=3)
        self.entry_longueur = Tk.Entry(self.root, width=4)
        self.entry_longueur.grid(row=5)
        self.entry_longueur.insert(0, "25")
        Tk.Label(self.root, text="Veuillez entrer la taille voulue de chaque cases en pixel : ").grid(row=6)
        self.entry_taille_case = Tk.Entry(self.root, width=4)
        self.entry_taille_case.grid(row=7)
        self.entry_taille_case.insert(0, "20")
        Tk.Button(self.root, text='Lancer la simulation', command=self.afficher_fen_jeu).grid(row=8)
        
