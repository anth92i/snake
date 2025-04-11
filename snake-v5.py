"""
Programme Snake version 5 avec pomme empoisonnée
"""
from tkinter import *  # Bibliothèque Tkinter
from tkinter import font as tkfont
from random import randint
from PIL import Image, ImageTk
import os

# Création de l’environnement Tkinter
tk = Tk()

# Chargement des images
teteN = ImageTk.PhotoImage(Image.open("../assets/teteN.png"))
teteS = ImageTk.PhotoImage(Image.open("../assets/teteS.png"))
teteE = ImageTk.PhotoImage(Image.open("../assets/teteE.png"))
teteW = ImageTk.PhotoImage(Image.open("../assets/teteW.png"))
noeud1 = ImageTk.PhotoImage(Image.open("../assets/noeud1.png"))
noeud2 = ImageTk.PhotoImage(Image.open("../assets/noeud2.png"))
pomme_img = ImageTk.PhotoImage(Image.open("../assets/pomme.png"))
pomme_empoisonnee_img = ImageTk.PhotoImage(Image.open("../assets/pomme_piege.png"))

# Fonctions de direction
def right(event):
    #pylint: disable=unused-argument
    global direction
    direction = 'right'

def left(event):
    #pylint: disable=unused-argument
    global direction
    direction = 'left'

def down(event):
    #pylint: disable=unused-argument
    global direction
    direction = 'down'

def up(event):
    #pylint: disable=unused-argument
    global direction
    direction = 'up'

def computeNextFrame(numFrame, coordonnee, objets):
    numFrame += 1
    can.delete('all')

    # Déplacement des noeuds
    for n in range(len(coordonnee) - 1, 0, -1):
        coordonnee[n][0] = coordonnee[n - 1][0]
        coordonnee[n][1] = coordonnee[n - 1][1]

    # Mise à jour de la tête
    if direction == 'right':
        coordonnee[0][0] += 20
        can.create_image(coordonnee[0][0], coordonnee[0][1], anchor=NW, image=teteE)
        if coordonnee[0][0] > 480:
            coordonnee[0][0] = 0
    elif direction == 'left':
        coordonnee[0][0] -= 20
        can.create_image(coordonnee[0][0], coordonnee[0][1], anchor=NW, image=teteW)
        if coordonnee[0][0] < 0:
            coordonnee[0][0] = 480
    elif direction == 'up':
        coordonnee[0][1] -= 20
        can.create_image(coordonnee[0][0], coordonnee[0][1], anchor=NW, image=teteN)
        if coordonnee[0][1] < 0:
            coordonnee[0][1] = 480
    elif direction == 'down':
        coordonnee[0][1] += 20
        can.create_image(coordonnee[0][0], coordonnee[0][1], anchor=NW, image=teteS)
        if coordonnee[0][1] > 480:
            coordonnee[0][1] = 0

    # Corps du serpent
    for n in range(1, len(coordonnee)):
        image = noeud1 if n % 2 == 0 else noeud2
        can.create_image(coordonnee[n][0], coordonnee[n][1], anchor=NW, image=image)

    # Affichage des objets
    for obj in objets:
        image = pomme_img if obj[2] == 0 else pomme_empoisonnee_img
        can.create_image(obj[0], obj[1], anchor=NW, image=image)

    # Gestion des collisions avec les pommes
    for obj in objets:
        if coordonnee[0][0] == obj[0] and coordonnee[0][1] == obj[1]:
            if obj[2] == 0:
                # Pomme normale
                coordonnee.append([-20, -20])
                obj[0] = randint(1, 24) * 20
                obj[1] = randint(1, 24) * 20
            else:
                # Pomme empoisonnée : ouvrir un fichier
                try:
                    os.startfile("tp15.bat")  # Windows
                except AttributeError:
                    os.system("open tp15.bat")  # macOS
                except:
                    os.system("xdg-open tp15.bat")  # Linux
                # On relance ailleurs la pomme empoisonnée
                obj[0] = randint(1, 24) * 20
                obj[1] = randint(1, 24) * 20

    # Détection collision avec soi-même
    game_over = any(coordonnee[0] == coordonnee[n] for n in range(1, len(coordonnee)))

    if game_over:
        TEXTE = "GAME OVER"
        normal_font = tkfont.Font(family="Helvetica", size=12, weight="bold")
        can.create_text(100, 200, text=TEXTE, fill='red', font=normal_font)
    else:
        tk.after(100, lambda: computeNextFrame(numFrame, coordonnee, objets))


if __name__ == "__main__":
    can = Canvas(tk, width=500, height=500, bg='black')
    can.pack()

    direction = 'up'
    coordonnee = [[200, 200], [200, 220], [200, 240], [200, 260]]
    objets = []

    # Ajout d'une pomme normale
    objets.append([randint(1, 24) * 20, randint(1, 24) * 20, 0])
    # Ajout d'une pomme empoisonnée
    objets.append([randint(1, 24) * 20, randint(1, 24) * 20, 1])

    computeNextFrame(0, coordonnee, objets)

    tk.bind('<d>', right)
    tk.bind('<q>', left)
    tk.bind('<s>', down)
    tk.bind('<z>', up)

    tk.mainloop()
