import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo


root = tk.Tk()

# config the root window
root.geometry('400x600')
root.resizable(False, False)
root.title('TTEA')

# label
label = ttk.Label(text="Jogos:")
label.pack(fill=tk.X, padx=100, pady=5)

# create a combobox
selected_game = tk.StringVar()
game_cb = ttk.Combobox(root, textvariable=selected_game)
game = ''

# set combo values
game_cb['values'] = ['KARTEA', 'REPETEA']

# prevent typing a value
game_cb['state'] = 'readonly'

# place the widget
game_cb.pack(fill=tk.X, padx=100, pady=1)


# bind the selected value changes
def game_changed(event):
    global game
    game = selected_game.get()

game_cb.bind('<<ComboboxSelected>>', game_changed)



# label
label = ttk.Label(text="Jogador:")
label.pack(fill=tk.X, padx=100, pady=5)

# create a combobox
selected_jogador = tk.StringVar()
jogador_cb = ttk.Combobox(root, textvariable=selected_jogador)


# Reading registered players
import os
path = os.getcwd() + "\Jogadores"
Jogadores = os.listdir(path)
#print(Jogadores)

arr_Jogadores = []
b = ''

for a in Jogadores:
    a = a.replace('_KarTEA.csv','')
    a = a.replace('_KarTEA_detalhado.csv','')
    a = a.replace('_RepeTEA.csv','')
    a = a.replace('_RepeTEA_detalhado.csv','')
    if a != b:
        arr_Jogadores.append(a)
    b = a

#print(arr_Jogadores)

# set combo values
jogador_cb['values'] = arr_Jogadores

# prevent typing a value
jogador_cb['state'] = 'readonly'

# place the widget
jogador_cb.pack(fill=tk.X, padx=100, pady=1)


# bind the selected value changes
jogador = ''
def jogador_changed(event):
    global jogador
    jogador = selected_jogador.get()


jogador_cb.bind('<<ComboboxSelected>>', jogador_changed)



def cadastrarCallback():
   import TTEA_cadastro

B = tk.Button(root, text ="Cadastrar Novo Jogador", command = cadastrarCallback)

B.pack()


# label
label = ttk.Label(text="Fase:")
label.pack(fill=tk.X, padx=100, pady=5)

# create a combobox
selected_fase = tk.StringVar()
fase_cb = ttk.Combobox(root, textvariable=selected_fase)

# set combo values
fase_cb['values'] = ['1', '2', '3']

# prevent typing a value
fase_cb['state'] = 'readonly'

# place the widget
fase_cb.pack(fill=tk.X, padx=100, pady=1)

fase = ''
# bind the selected value changes
def fase_changed(event):
    global fase
    fase = selected_fase.get()

fase_cb.bind('<<ComboboxSelected>>', fase_changed)


# label
label = ttk.Label(text="Nível:")
label.pack(fill=tk.X, padx=100, pady=5)

# create a combobox
selected_nivel = tk.StringVar()
nivel_cb = ttk.Combobox(root, textvariable=selected_nivel)

# set combo values
nivel_cb['values'] = ['1', '2', '3', '4', '5']

# prevent typing a value
nivel_cb['state'] = 'readonly'

# place the widget
nivel_cb.pack(fill=tk.X, padx=100, pady=1)

nivel = ''
# bind the selected value changes
def nivel_changed(event):
    global nivel
    nivel = selected_nivel.get()

nivel_cb.bind('<<ComboboxSelected>>', nivel_changed)



def JogarCallback():
    if game == 'KARTEA':
        import KarTEA
        KarTEA.main()
    else:
        print('REPETEA')

B = tk.Button(root, text ="Jogar", command = JogarCallback)

B.pack()





root.mainloop()