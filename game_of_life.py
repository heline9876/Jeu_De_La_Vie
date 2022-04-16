import tkinter as Tk


class Jeu:
    def __init__(self):
        self.grille = [[False for _ in range(9)]for _ in range(9)]       #Chaque case représenté dans la grille est soit vivante (True) soit morte (False). Par défaut, elles sont mortes.
        self.cases = [[False for _ in range(9)]for _ in range(9)]
        self.canvas = Tk.Canvas(root)        
        self.x = 0
        self.y = 0
        self.hauteur = 0
        self.longueur = 0
        self.taille_case = 0
        self.drapeau_arret = False


    def afficher_grille(self):
        for y in range(self.hauteur):
            for x in range(self.longueur):
                if self.grille[y][x] is True:
                    self.canvas.itemconfig(self.cases[y][x], fill='grey')
                else:
                    self.canvas.itemconfig(self.cases[y][x], fill='white')
    
    
    def activer_cases(self, event):
        x = (event.x - (event.x%self.taille_case)) // self.taille_case
        y = (event.y - (event.y%self.taille_case)) // self.taille_case
        self.canvas.itemconfig(self.cases[y][x], fill='grey')
        self.grille[y][x] = True
        
            
    def desactiver_cases(self, event):
        x = (event.x - (event.x%self.taille_case)) // self.taille_case
        y = (event.y - (event.y%self.taille_case)) // self.taille_case
        self.canvas.itemconfig(self.cases[y][x], fill='white')
        self.grille[y][x] = False


    def stopper_simulation(self):
        self.drapeau_arret = False
        self.canvas.bind("<Button-1>", self.activer_cases)
        self.canvas.bind("<Button-3>", self.desactiver_cases)
        self.canvas.bind("<space>", self.lancer_simulation)
    
    
    def lancer_simulation(self):
        if self.drapeau_arret is False:
            self.drapeau_arret = True
            self.canvas.unbind("<Button-1>")
            self.canvas.unbind("<Button-3>")
            self.canvas.bind("<space>", self.stopper_simulation)
            root.after(50, self.modifier_etat_cases)


    def modifier_etat_cases(self):
        self.grille_temp = [[False for _ in range(self.hauteur * self.taille_case)]for _ in range(self.longueur * self.taille_case)]
        for i in range(self.hauteur):
            for j in range(self.longueur):
                nombres_voisines_vivantes = self.nombres_voisines(i, j)

                if nombres_voisines_vivantes == 3 and self.grille[i][j] is False:
                    self.grille_temp[i][j] = True

                if nombres_voisines_vivantes < 2 or nombres_voisines_vivantes > 3 and self.grille[i][j] is True:
                    self.grille_temp[i][j] = False

                if nombres_voisines_vivantes in [2, 3] and self.grille[i][j] is True:
                    self.grille_temp[i][j] = True

        if self.grille == self.grille_temp:                 # Si toutes les cellules de self.grille sont stables, alors on arrête la simulation
            self.stopper_simulation()
        self.grille = self.grille_temp
        self.afficher_grille()
        if self.drapeau_arret is True:
            root.after(50, self.modifier_etat_cases)
        
        
    def nombres_voisines(self, x, y):
        nombre_voisines_vivantes = 0
        
        if self.grille[x][(y + 1) % self.hauteur] is True:
            nombre_voisines_vivantes += 1
            
        if self.grille[x][(y - 1) % self.hauteur] is True:
            nombre_voisines_vivantes += 1

        if self.grille[(x + 1) % self.longueur][y] is True:
            nombre_voisines_vivantes += 1
            
        if self.grille[(x - 1) % self.longueur][y] is True:
            nombre_voisines_vivantes += 1

        if self.grille[(x - 1) % self.longueur][(y + 1) % self.hauteur] is True:
            nombre_voisines_vivantes += 1

        if self.grille[(x + 1) % self.longueur][(y + 1) % self.hauteur] is True:
            nombre_voisines_vivantes += 1
            
        if self.grille[(x - 1) % self.longueur][(y - 1) % self.hauteur] is True:
            nombre_voisines_vivantes += 1

        if self.grille[(x + 1) % self.longueur][(y - 1) % self.hauteur] is True:
            nombre_voisines_vivantes += 1
        
        return nombre_voisines_vivantes
    
    
    def reinitialiser_le_plateau(self):
        #if self.drapeau_arret is False:
            self.grille = [[False for _ in range(self.hauteur * self.taille_case)]for _ in range(self.longueur * self.taille_case)]
            self.modifier_etat_cases()
        
                       
    def afficher_fen_jeu(self):
        try:
            self.hauteur = int(self.entry_hauteur.get())
            self.longueur = int(self.entry_longueur.get())
            self.taille_case = int(self.entry_taille_case.get())
            for item in root.winfo_children():
                item.destroy()
            self.activer_widget_fen_jeu()
        except Exception:
            Tk.Label(root, text="Veuillez entrer un nombre.", bg='light yellow', fg='red').grid(row=9)


    def activer_widget_fen_jeu(self):
        self.grille = [[False for _ in range(self.hauteur * self.taille_case)]for _ in range(self.longueur * self.taille_case)]
        self.canvas = Tk.Canvas(root, width=self.taille_case*self.longueur, height=self.taille_case*self.hauteur, highlightthickness=0)
        self.cases = [[False for _ in range(self.hauteur * self.taille_case)]for _ in range(self.longueur * self.taille_case)]
        for y in range(self.longueur * self.taille_case):
            for x in range(self.hauteur * self.taille_case):
                self.cases[y][x] = self.canvas.create_rectangle(x*self.taille_case, y*self.taille_case, (x+1)*self.taille_case, (y+1)*self.taille_case)
        self.canvas.bind("<Button-1>", self.activer_cases)
        self.canvas.bind("<Button-3>", self.desactiver_cases)
        self.canvas.bind("<space>", lambda : self.lancer_simulation())
        self.afficher_grille()
        frame = Tk.Frame(bg="light yellow")
        self.bouton_lancer_simulation = Tk.Button(frame, text="Lancer la simulation", command=self.lancer_simulation)
        self.bouton_lancer_simulation.grid(column=0, row=0)
        self.bouton_stopper_simulation = Tk.Button(frame, text="Réinitialiser le plateau", command=self.reinitialiser_le_plateau)
        self.bouton_stopper_simulation.grid(column=1, row=0)
        self.bouton_stopper_simulation = Tk.Button(frame, text="Stopper la simulation", command=self.stopper_simulation)
        self.bouton_stopper_simulation.grid(column=2, row=0)
        self.canvas.pack()
        frame.pack()


    def ecran_choix_nombre_cases(self):
        Tk.Label(root, text="Veuillez entrer le nombre de cellules à la verticale : ", bg='light yellow').grid(row=1)
        self.entry_hauteur = Tk.Entry(root, width=4)
        self.entry_hauteur.grid(row=2)
        Tk.Label(root, text="Veuillez entrer le nombre de cellules à l'horizontale : ", bg='light yellow').grid(row=3)
        self.entry_longueur = Tk.Entry(root, width=4)
        self.entry_longueur.grid(row=5)
        Tk.Label(root, text="Veuillez entrer la taille voulue de chaque cases en pixel : ", bg='light yellow').grid(row=6)
        self.entry_taille_case = Tk.Entry(root, width=4)
        self.entry_taille_case.grid(row=7)
        Tk.Button(root, text='Lancer la simulation', command=self.afficher_fen_jeu).grid(row=8)


root = Tk.Tk()
root.resizable(False, False)
root.title("Le Super Jeu De La Vie")
root.configure(bg='light yellow')

jeu = Jeu()
jeu.ecran_choix_nombre_cases()

root.mainloop()
