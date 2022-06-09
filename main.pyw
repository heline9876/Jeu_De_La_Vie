import tkinter as Tk
from Classe_Jeu import Jeu

root = Tk.Tk()
root.resizable(False, False)
root.title("Le Super Jeu De La Vie")

jeu = Jeu(root)
jeu.ecran_choix_nombre_cases()

root.mainloop()
