"""
Programme Snake version 1

"""
from tkinter import *
from random import randint 
tk = Tk()

def right(event):
    global direction
    direction = 'right'
    print(direction)
def left(event):
    global direction
    direction = 'left'
    print(direction)
def up(event):
    global direction
    direction = 'up'
    print(direction)
def down(event):
    global direction
    direction = 'down'
    print(direction)

def computeNextFrame(numFrame,coordonnee):
    global direction
    numFrame = numFrame + 1
    can.delete('all')
    
    for n in range (len(coordonnee)-1,0,-1):
        coordonnee[n][0] = coordonnee[n-1][0]
        coordonnee[n][1] = coordonnee[n-1][1]
         
    if direction == 'right':
        coordonnee[0][0] += 20
        if coordonnee[0][0] > 500:
            coordonnee[0][0] = 0
    if direction == 'left':
        coordonnee[0][0] += -20
        if coordonnee[0][0] < 0:
            coordonnee[0][0] = 480
    if direction == 'up':
        coordonnee[0][1] += -20
        if coordonnee[0][1] < 0:
            coordonnee[0][1] = 480
    if direction == 'down':
        coordonnee[0][1] += 20
        if coordonnee[0][1] > 500:
            coordonnee[0][1] = 0

    can.create_rectangle(coordonnee[0][0], coordonnee[0][1], coordonnee[0][0] + 20, 
                         coordonnee[0][1] + 20, outline='purple', fill='yellow')
    
    for n in range (len(coordonnee)-1,0,-1):
        if n%2 == 0: 
            ligne = 'blue'
            couleur = 'green'
        else:
            ligne = 'green'
            couleur = 'blue'
        can.create_rectangle(coordonnee[n][0], coordonnee[n][1], coordonnee[n][0] + 20, 
                        coordonnee[n][1] + 20, outline='red', fill='green')
    
    for p in range(len(objet)):
        can.create_oval(objet[p][0], objet[p][1], objet[p][0] + 20, 
                         objet[p][1] + 20, outline= 'red', fill= 'green')
    
    for p in range(len(objet)):
        if coordonnee[0][0]== objet [0][0] and coordonnee[p][1] == objet [p][1]:
            objet [0][0] = randint(1,24)*20
            objet [0][1] = randint(1,24)*20
            coordonnee.append([-20,-20])
    
    game_over = False     
    
    for n in range(1,len(coordonnee)): 
        if coordonnee[0][0] == coordonnee [n][0] and coordonnee[p][1] == coordonnee [n][1]:
            game_over = True 
            
    if game_over : 
        
        TEXTE = "GAME OVER"
        normal_font = tkfont.Font(family="Helvetica", size=12, weight="bold")
        can.create_text(100,200,text = TEXTE, fill='red',  font=normal_font)
    else:
        
        tk.after(100, lambda:computeNextFrame(numFrame,coordonnee, objet))


    tk.after(100, lambda:computeNextFrame(numFrame,coordonnee))

if __name__=="__main__":
    can = Canvas(tk, width=500, height=500, bg='black')
    can.pack()
    direction='up'
    coordonnee = [ [200,200],[200,220],[200,240],[220,240] ]
    objet = []
    x = randint(1,24)
    y = randint(1,24)
    objet.append([x*20,y*20,0])
    computeNextFrame(0,[[200,200]])
    tk.bind('<d>', right)
    tk.bind('<q>', left)
    tk.bind('<z>', up)
    tk.bind('<s>', down)
    tk.mainloop() 




             



