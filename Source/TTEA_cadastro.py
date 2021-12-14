from tkinter import *
import tkinter as tk
from tkinter import messagebox

import  arquivo

import os

path = os.getcwd() + "\Jogadores"
Jogadores = os.listdir(path)
# print(Jogadores)

arr_Jogadores = []
b = ''

for a in Jogadores:
    a = a.replace('_KarTEA.csv', '')
    a = a.replace('_KarTEA_detalhado.csv', '')
    a = a.replace('_RepeTEA.csv', '')
    a = a.replace('_RepeTEA_detalhado.csv', '')
    if a != b:
        arr_Jogadores.append(a)
    b = a

root = tk.Tk()
root.geometry('300x150')

NomeString = tk.StringVar(root)
DataString = tk.StringVar(root)
ObsString = tk.StringVar(root)

LNome = tk.Label(root, text="Nome: ")
LNome.grid(column=0, row=0, sticky=tk.W)
Nome = tk.Entry(root, width=20, textvariable=NomeString)
Nome.grid(column=1, row=0, padx=10)

LData = tk.Label(root, text="Data de Nasc.: ")
LData.grid(column=0, row=1, sticky=tk.W)
Data = tk.Entry(root, width=20, textvariable=DataString)
Data.grid(column=1, row=1, padx=10)

LObs = tk.Label(root, text="Observação: ")
LObs.grid(column=0, row=2, sticky=tk.W)
Obs = tk.Entry(root, width=20, textvariable=ObsString)
Obs.grid(column=1, row=2, padx=10)

def cadastrarcallback():
    SNome = NomeString.get()
    SData = DataString.get()
    SObs = ObsString.get()
    #print(SNome, SData, SObs)

    if SNome not in arr_Jogadores:
        arquivo.CadastrarJogador(SNome, SData, SObs)
        arr_Jogadores.append(SNome)
        tk.messagebox.askquestion (title='Jogador cadastrado!', message='Jogador cadastrado com sucesso!\nDeseja cadastrar outro?')
    else:
        tk.messagebox.showerror(title='Erro!', message='Jogador com esse nome já esta cadastrado!')

B = tk.Button(root, text="Cadastrar Novo Jogador", command=cadastrarcallback)

B.grid(column=0, row=3, pady=10, sticky=tk.W)

root.mainloop()