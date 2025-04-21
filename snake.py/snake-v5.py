from tkinter import *
from tkinter import font as tkfont
from random import randint
from PIL import Image, ImageTk, ImageOps
import subprocess

# Constantes
TAILLE = 40
LARGEUR = 500
HAUTEUR = 500

# Fenêtre principale
tk = Tk()
tk.title("Snake Deluxe")

# Chargement des images
def load_image(name):
    return ImageTk.PhotoImage(Image.open(f"../assets/{name}.png").resize((TAILLE, TAILLE)))

apple_image = Image.open("../assets/apple.png").resize((TAILLE, TAILLE))
inverse_apple_image = ImageOps.mirror(apple_image)

images = {
    "head_up": load_image("head_up"),
    "head_down": load_image("head_down"),
    "head_left": load_image("head_left"),
    "head_right": load_image("head_right"),
    "tail_up": load_image("tail_up"),
    "tail_down": load_image("tail_down"),
    "tail_left": load_image("tail_left"),
    "tail_right": load_image("tail_right"),
    "body_vertical": load_image("body_vertical"),
    "body_horizontal": load_image("body_horizontal"),
    "body_topleft": load_image("body_topleft"),
    "body_topright": load_image("body_topright"),
    "body_bottomleft": load_image("body_bottomleft"),
    "body_bottomright": load_image("body_bottomright"),
    "apple": ImageTk.PhotoImage(apple_image),
    "inverse_apple": ImageTk.PhotoImage(inverse_apple_image),
    "bat_apple": load_image("bat_apple")
}

# Variables globales
direction = 'up'
inverser_controles = False

def right(event): global direction; direction = 'left' if inverser_controles else 'right'
def left(event): global direction; direction = 'right' if inverser_controles else 'left'
def down(event): global direction; direction = 'up' if inverser_controles else 'down'
def up(event): global direction; direction = 'down' if inverser_controles else 'up'

# Calcule direction entre deux points avec gestion des bords
def get_direction(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    dx = (x2 - x1) % LARGEUR
    dy = (y2 - y1) % HAUTEUR

    if dx == TAILLE: return 'right'
    if dx == (LARGEUR - TAILLE): return 'left'
    if dy == TAILLE: return 'down'
    if dy == (HAUTEUR - TAILLE): return 'up'
    return None

# Génération pomme
def nouvelle_pomme():
    while True:
        pos = [randint(0, (LARGEUR - TAILLE) // TAILLE) * TAILLE,
               randint(0, (HAUTEUR - TAILLE) // TAILLE) * TAILLE]
        if pos not in [s for s in snake]:
            return pos

# Affichage du serpent
def afficher_serpent():
    for i in range(len(snake)):
        x, y = snake[i]
        if i == 0:
            can.create_image(x, y, anchor=NW, image=images[f"head_{direction}"])
        elif i == len(snake) - 1:
            dir_queue = get_direction(snake[i - 1], snake[i])
            can.create_image(x, y, anchor=NW, image=images[f"tail_{dir_queue}"])
        else:
            prev = snake[i - 1]
            curr = snake[i]
            next_ = snake[i + 1]

            dir_prev = get_direction(curr, prev)
            dir_next = get_direction(curr, next_)

            if (dir_prev in ['up', 'down'] and dir_next in ['up', 'down']):
                can.create_image(x, y, anchor=NW, image=images["body_vertical"])
            elif (dir_prev in ['left', 'right'] and dir_next in ['left', 'right']):
                can.create_image(x, y, anchor=NW, image=images["body_horizontal"])
            else:
                turns = {
                    ('up', 'left'): "body_topleft",
                    ('left', 'up'): "body_topleft",
                    ('up', 'right'): "body_topright",
                    ('right', 'up'): "body_topright",
                    ('down', 'left'): "body_bottomleft",
                    ('left', 'down'): "body_bottomleft",
                    ('down', 'right'): "body_bottomright",
                    ('right', 'down'): "body_bottomright"
                }
                segment = turns.get((dir_prev, dir_next)) or turns.get((dir_next, dir_prev))
                can.create_image(x, y, anchor=NW, image=images[segment])

# Frame suivante
def next_frame():
    global inverser_controles, pomme, inverse_pomme, bat_pomme

    can.delete("all")
    head_x, head_y = snake[0]

    if direction == 'right': head_x += TAILLE
    elif direction == 'left': head_x -= TAILLE
    elif direction == 'up': head_y -= TAILLE
    elif direction == 'down': head_y += TAILLE

    head_x %= LARGEUR
    head_y %= HAUTEUR
    new_head = [head_x, head_y]

    if new_head in snake[1:]:
        can.create_text(LARGEUR // 2, HAUTEUR // 2, text="GAME OVER", fill='red',
                        font=tkfont.Font(size=30, weight="bold"))
        return

    snake.insert(0, new_head)

    if snake[0] == pomme:
        pomme = nouvelle_pomme()
    elif snake[0] == inverse_pomme:
        inverse_pomme = nouvelle_pomme()
        inverser_controles = not inverser_controles
    elif snake[0] == bat_pomme:
        bat_pomme = nouvelle_pomme()
        subprocess.Popen(["start", "danger.bat"], shell=True)
    else:
        snake.pop()

    afficher_serpent()
    can.create_image(pomme[0], pomme[1], anchor=NW, image=images["apple"])
    can.create_image(inverse_pomme[0], inverse_pomme[1], anchor=NW, image=images["inverse_apple"])
    can.create_image(bat_pomme[0], bat_pomme[1], anchor=NW, image=images["bat_apple"])

    tk.after(100, next_frame)

# Initialisation
can = Canvas(tk, width=LARGEUR, height=HAUTEUR, bg='black')
can.pack()

snake = [[200, 200], [200, 240], [200, 280]]
pomme = nouvelle_pomme()
inverse_pomme = nouvelle_pomme()
bat_pomme = nouvelle_pomme()

tk.bind('<z>', up)
tk.bind('<s>', down)
tk.bind('<q>', left)
tk.bind('<d>', right)

next_frame()
tk.mainloop()
