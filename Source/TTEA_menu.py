import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
import numpy
from PIL import Image, ImageTk
import os
import arquivo
import settings

def center_window_on_screen(width, height):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_cord = int((screen_width/2) - (width/2))
    y_cord = int((screen_height/2) - (height/2))
    root.geometry("{}x{}+{}+{}".format(width, height, x_cord, y_cord))

def show_menu():
    root.title('Menu TTEA')
    arr_Jogadores = ler_nome_jogadores()
    # set combo values
    jogador_cb['values'] = arr_Jogadores

    width, height = 400, 600
    center_window_on_screen(width, height)
    menu_frame.pack()
    cad_frame.forget()


def show_cad():
    root.title('Cadastro TTEA')
    width, height = 300, 150
    center_window_on_screen(width, height)
    cad_frame.pack()
    menu_frame.forget()

root = tk.Tk()

# config the root window
root.resizable(False, False)
root.title('Menu TTEA')
width, height = 400, 600
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
center_window_on_screen(width, height)

# frames
menu_frame = tk.Frame(root)
cad_frame = tk.Frame(root)

# Menu

# Logo
image = Image.open("Assets/TTEA Logo.png")
photo = ImageTk.PhotoImage(image)
imagem = tk.Label(menu_frame, text = "TTEA Logo", image = photo)
imagem.image = photo
imagem.pack()

# label
label = ttk.Label(menu_frame, text="Jogos:")
label.pack(fill=tk.X, padx=100, pady=5)

# create a combobox
selected_game = tk.StringVar()
game_cb = ttk.Combobox(menu_frame, textvariable=selected_game)
game = ''

# set combo values
game_cb['values'] = ['KARTEA', 'REPETEA']

# prevent typing a value
game_cb['state'] = 'readonly'

# place the widget
game_cb.pack(fill=tk.X, padx=100, pady=5)


# bind the selected value changes
def game_changed(event):
    global game
    game = selected_game.get()
    jogador_cb['state'] = 'readonly'

game_cb.bind('<<ComboboxSelected>>', game_changed)



# label
label = ttk.Label(menu_frame, text="Jogador:")
label.pack(fill=tk.X, padx=100, pady=5)

# create a combobox
selected_jogador = tk.StringVar()
jogador_cb = ttk.Combobox(menu_frame, textvariable=selected_jogador)

arr_Jogadores = []

def ler_nome_jogadores():
    # Reading registered players
    path = os.getcwd() + "\Jogadores"
    Jogadores = os.listdir(path)
    #print(Jogadores)

    arr = []
    b = ''

    for a in Jogadores:
        a = a.replace('_KarTEA.csv','')
        a = a.replace('_KarTEA_detalhado.csv','')
        a = a.replace('_RepeTEA.csv','')
        a = a.replace('_RepeTEA_detalhado.csv','')
        if a != b:
            arr.append(a)
        b = a
    return arr

#print(arr_Jogadores)
arr_Jogadores = ler_nome_jogadores()
# set combo values
jogador_cb['values'] = arr_Jogadores

# prevent typing a value
jogador_cb['state'] = 'disabled'

# place the widget
jogador_cb.pack(fill=tk.X, padx=100, pady=5)


# bind the selected value changes
jogador = ''
FASE = 0
NIVEL = 0
def jogador_changed(event):
    global jogador
    jogador = selected_jogador.get()

    PLAYER = "Jogadores/" + jogador
    if game == 'KARTEA':
        PLAYER_ARQ = PLAYER + "_KarTEA.csv"
        PLAYER_ARQ_DET = PLAYER + "_KarTEA_detalhado.csv"
    elif game == 'REPETEA':
        PLAYER_ARQ = PLAYER + "_RepeTEA.csv"
        PLAYER_ARQ_DET = PLAYER + "_RepeTEA_detalhado.csv"

    CONFIGS = []
    CONFIGS = arquivo.lerConfigs(PLAYER_ARQ)

    global FASE, NIVEL
    FASE = CONFIGS[1]
    NIVEL = CONFIGS[3]
    fase_cb['state'] = 'readonly'
    fase_cb.current(int(FASE)-1)
    nivel_cb['state'] = 'readonly'
    nivel_cb.current(int(NIVEL)-1)


jogador_cb.bind('<<ComboboxSelected>>', jogador_changed)



def cadastrarCallback():
    show_cad()


B = tk.Button(menu_frame, text ="Cadastrar Novo Jogador", command = cadastrarCallback)

B.pack(fill=tk.X, padx=100, pady=10)


# label
label = ttk.Label(menu_frame, text="Fase:")
label.pack(fill=tk.X, padx=100, pady=5)

# create a combobox
selected_fase = tk.StringVar()
fase_cb = ttk.Combobox(menu_frame, textvariable=selected_fase)

# set combo values
fase_cb['values'] = ['1', '2', '3']

# prevent typing a value
fase_cb['state'] = 'disabled'

# place the widget
fase_cb.pack(fill=tk.X, padx=100, pady=5)

fase = ''
# bind the selected value changes
def fase_changed(event):
    global fase
    fase = selected_fase.get()

fase_cb.bind('<<ComboboxSelected>>', fase_changed)


# label
label = ttk.Label(menu_frame, text="Nível:")
label.pack(fill=tk.X, padx=100, pady=5)

# create a combobox
selected_nivel = tk.StringVar()
nivel_cb = ttk.Combobox(menu_frame, textvariable=selected_nivel)

# set combo values
nivel_cb['values'] = ['1', '2', '3', '4', '5']

# prevent typing a value
nivel_cb['state'] = 'disabled'

# place the widget
nivel_cb.pack(fill=tk.X, padx=100, pady=5)

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

B = tk.Button(menu_frame, text ="Jogar", command = JogarCallback)

B.pack()

menu_frame.pack()

#Frame Cadastro
arr_Jogadores = ler_nome_jogadores()

NomeString = tk.StringVar(cad_frame)
DataString = tk.StringVar(cad_frame)
ObsString = tk.StringVar(cad_frame)

LNome = tk.Label(cad_frame, text="Nome: ")
LNome.grid(column=0, row=0, sticky=tk.W)
Nome = tk.Entry(cad_frame, width=20, textvariable=NomeString)
Nome.grid(column=1, row=0, padx=10)

LData = tk.Label(cad_frame, text="Data de Nasc.: ")
LData.grid(column=0, row=1, sticky=tk.W)
Data = tk.Entry(cad_frame, width=20, textvariable=DataString)
Data.grid(column=1, row=1, padx=10)

LObs = tk.Label(cad_frame, text="Observação: ")
LObs.grid(column=0, row=2, sticky=tk.W)
Obs = tk.Entry(cad_frame, width=20, textvariable=ObsString)
Obs.grid(column=1, row=2, padx=10)

def cadastrarcallback():
    SNome = NomeString.get()
    SData = DataString.get()
    SObs = ObsString.get()
    #print(SNome, SData, SObs)

    if SNome not in arr_Jogadores:
        arquivo.CadastrarJogador(SNome, SData, SObs)
        arr_Jogadores.append(SNome)
        res = tk.messagebox.askquestion (title='Jogador cadastrado!', message='Jogador cadastrado com sucesso!\nDeseja cadastrar outro jogador?')
        if res == 'no':
            show_menu()
    else:
        tk.messagebox.showerror(title='Erro!', message='Jogador com esse nome já esta cadastrado!')

B = tk.Button(cad_frame, text="Cadastrar Novo Jogador", command=cadastrarcallback)

B.grid(column=0, row=3, padx=10, pady=10, sticky=tk.W)

def cancelarcallback():
    show_menu()

B = tk.Button(cad_frame, text="Cancelar", command=cancelarcallback)

B.grid(column=1, row=3, padx=10, pady=10, sticky=tk.W)

root.mainloop()