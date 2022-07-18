import csv
import pandas as pd
import numpy as np

"""
Funções que interagem com os arquivos csv
"""

Player = ''
Fase = 1
Nivel = 1

def set_Player(A):
    global Player
    Player = A

def get_Player():
    global Player
    return Player

def set_Fase(A):
    global Fase
    Fase = A

def get_Fase():
    global Fase
    return Fase

def set_Nivel(A):
    global Nivel
    Nivel = A

def get_Nivel():
    global Nivel
    return Nivel

csv.register_dialect(
    'mydialect',
    delimiter = ',',
    quotechar = '"',
    doublequote = True,
    skipinitialspace = True,
    lineterminator = '\n',
    quoting = csv.QUOTE_MINIMAL)

def CadastrarJogador(Nome, Nasc, Obs):
    #Kartea
    Config = ['Nome', 'Data de Nasc.', 'Observacoes', 'Fase Atual', 'Nivel Atual', 'Tempo de Nivel', 'Carro',
              'Ambiente', 'Paleta', 'Alvo', 'Obstaculo', 'Imagem Feedback Positivo', 'Imagem Feedback Neutro',
              'Imagem Feedback Negativo', 'Som Feedback Positivo', 'Som Feedback Neutro', 'Som Feedback Negativo',
              'HUD', 'Som']
    Dados = [Nome, Nasc, Obs, '1', '1', '120', 'carro.png', 'ambiente.png', '0', 'alvo.png', 'obstaculo.png',
               'feedPos.png', 'feedNeut.png' 'feedNeg.png', 'feedPos.mp3','feedNeut.mp3', 'feedNeg.mp3',
               True, True]
    file = 'Jogadores/' + Nome + '_KarTEA_config.csv'

    with open(file, 'w') as csvfile:
        csvwriter = csv.writer(csvfile, dialect='mydialect')
        csvwriter.writerow(Config)
        csvwriter.writerow(Dados)

    fields = ['Sessao', 'Data da Sessao', 'Hora Inicio', 'Fase Alcancada', 'Nivel Alcancado', 'Pontuacao Geral',
              'Q Movimentos', 'Q Alvos Colididos', 'Q Alvos Desviados', 'Q Obstaculos Colididos',
              'Q Obstaculos Desviados']
    file = 'Jogadores/' + Nome + '_KarTEA_sessao.csv'
    with open(file, 'w') as csvfile:
        csvwriter = csv.writer(csvfile, dialect='mydialect')
        csvwriter.writerow(fields)

    fields = ['ID', 'Sessao', 'Hora do Evento', 'Fase', 'Nivel', 'Posicao jogador', 'Posicao Evento', 'Tipo de Evento']
    file = 'Jogadores/' + Nome + '_KarTEA_detalhado.csv'
    with open(file, 'w') as csvfile:
        csvwriter = csv.writer(csvfile, dialect='mydialect')
        csvwriter.writerow(fields)

    #RepeTEA
    Config = ['Nome', 'Data de Nasc.', 'Observacoes', 'Fase Atual', 'Nivel Atual', 'Tempo de Nivel']
    Dados = [Nome, Nasc, Obs, '1', '1', '120']
    file = 'Jogadores/' + Nome + '_RepeTEA_config.csv'

    with open(file, 'w') as csvfile:
        csvwriter = csv.writer(csvfile, dialect='mydialect')
        csvwriter.writerow(Config)
        csvwriter.writerow(Dados)

    fields = ['Sessao', 'Data da Sessao', 'Hora Inicio', 'Fase Alcancada', 'Nivel Alcancado', 'Pontuacao Geral']
    file = 'Jogadores/' + Nome + '_RepeTEA_sessao.csv'
    with open(file, 'w') as csvfile:
        csvwriter = csv.writer(csvfile, dialect='mydialect')
        csvwriter.writerow(fields)

    fields = ['ID', 'Sessao', 'Hora do Evento', 'Fase', 'Nivel', 'Posicao jogador', 'Posicao Evento', 'Tipo de Evento']
    file = 'Jogadores/' + Nome + '_RepeTEA_detalhado.csv'
    with open(file, 'w') as csvfile:
        csvwriter = csv.writer(csvfile, dialect='mydialect')
        csvwriter.writerow(fields)

#----------------------------------------------------------------------------------------------------------------------#

def gravaDados(filename, Dados):# Dados é um vetor com os dados para gravar no arquivo 'filename'
    with open(filename, 'a+', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, dialect='mydialect')
        csvwriter.writerow(Dados)

def grava_Sessao(jogador, id, data, hora, fase, nivel, pont, mov, alvos_c, alvos_d, obst_c, obst_d):
    file = 'Jogadores/'+jogador+'_KarTEA_sessao.csv'
    fields = [id, data, hora, fase, nivel, pont, mov, alvos_c, alvos_d, obst_c, obst_d]
    with open(file,'a+', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, dialect='mydialect')
        csvwriter.writerow(fields)

def grava_Detalhado(jogador, id, sessao, hora, fase, nivel, pos_jog, pos_ev, tipo):
    file = 'Jogadores/' + jogador + '_KarTEA_detalhado.csv'
    fields = [id, sessao, hora, fase, nivel, pos_jog, pos_ev, tipo]
    with open(file, 'a+', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, dialect='mydialect')
        csvwriter.writerow(fields)


#----------------------------------------------------------------------------------------------------------------------#

def lerConfigs(filename): #Apenas para os arquivos gerais, nos detalhados retorna a primeira linha de dados
    """
    Player_Kartea.csv = ['Sessao', 'Data da Sessao', 'Hora Inicio', 'Fase Alcancada', 'Nivel Alcancado', 'Pontuacao Geral', 
                         'Q Movimentos', 'Q Alvos Colididos', 'Q Alvos Desviados', 'Q Obstaculos Colididos', 
                         'Q Obstaculos Desviados']

    Player_Kartea_config.csv = ['Nome', 'Data de Nasc.', 'Observacoes', 'Fase Atual', 'Nivel Atual', 'Tempo de Nivel', 'Carro',
                                  'Ambiente', 'Paleta', 'Alvo', 'Obstaculo', 'Imagem Feedback Positivo', 'Imagem Feedback Neutro',
                                  'Imagem Feedback Negativo', 'Som Feedback Positivo', 'Som Feedback Neutro', 'Som Feedback Negativo',
                                  'HUD', 'Som']

    Player_Kartea_detalhado = ['ID', 'Sessao', 'Hora do Evento', 'Fase', 'Nivel', 'Posicao jogador', 'Posicao Evento', 'Tipo de Evento']

    Fases = ['', ]

    """
    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile, dialect='mydialect')
        fields = next(csvreader)  # Dados do jogador
        fields = next(csvreader)  # Configuracoes
        return fields

#Le os pontos de calibração realizados antes do jogo
def lerCalibracao():
    pontos_calibracao = np.zeros((4, 2), int)
    df = pd.read_csv('calibracao.csv')

    # getting value/data
    pontos_calibracao[0][0] = df["Ponto 1 x"].values[0]
    pontos_calibracao[0][1] = df["Ponto 1 y"].values[0]
    pontos_calibracao[1][0] = df["Ponto 2 x"].values[0]
    pontos_calibracao[1][1] = df["Ponto 2 y"].values[0]
    pontos_calibracao[2][0] = df["Ponto 3 x"].values[0]
    pontos_calibracao[2][1] = df["Ponto 3 y"].values[0]
    pontos_calibracao[3][0] = df["Ponto 4 x"].values[0]
    pontos_calibracao[3][1] = df["Ponto 4 y"].values[0]

    return pontos_calibracao


#----------------------------------------------------------------------------------------------------------------------#

#Manipulação de dados das Configs
def get_K_NOME(filename):
    # reading the csv file
    df = pd.read_csv(filename)

    # getting value/data
    ret = df["Nome"].values[0]
    return ret

def set_K_NOME(filename, a):
    # reading the csv file
    df = pd.read_csv(filename)

    # updating the column value/data
    df.loc[0, 'Nome'] = a

    # writing into the file
    df.to_csv(filename, index=False)
    # print(df)


def get_K_NASC(filename):
    # reading the csv file
    df = pd.read_csv(filename)

    # getting value/data
    ret = df["Data de Nasc."].values[0]
    return ret

def set_K_NASC(filename, a):
    # reading the csv file
    df = pd.read_csv(filename)

    # updating the column value/data
    df.loc[0, 'Data de Nasc.'] = a

    # writing into the file
    df.to_csv(filename, index=False)
    # print(df)


def get_K_OBS(filename):
    # reading the csv file
    df = pd.read_csv(filename)

    # getting value/data
    ret = df["Observacoes"].values[0]
    return ret

def set_K_OBS(filename, a):
    # reading the csv file
    df = pd.read_csv(filename)

    # updating the column value/data
    df.loc[0, 'Observacoes'] = a

    # writing into the file
    df.to_csv(filename, index=False)
    # print(df)


def get_K_FASE(filename):
    # reading the csv file
    df = pd.read_csv(filename)
    
    # getting value/data
    ret = df["Fase Atual"].values[0]
    return ret

def set_K_FASE(filename, a):
    # reading the csv file
    df = pd.read_csv(filename)
    
    # updating the column value/data
    df.loc[0, 'Fase Atual'] = a
    
    # writing into the file
    df.to_csv(filename, index=False)
    #print(df)


def get_K_NIVEL(filename):
    # reading the csv file
    df = pd.read_csv(filename)

    # getting value/data
    ret = df["Nivel Atual"].values[0]
    return ret

def set_K_NIVEL(filename, a):
    # reading the csv file
    df = pd.read_csv(filename)

    # updating the column value/data
    df.loc[0, 'Nivel Atual'] = a

    # writing into the file
    df.to_csv(filename, index=False)
    # print(df)


def get_K_TEMPO_NIVEL(filename):
    # reading the csv file
    df = pd.read_csv(filename)

    # getting value/data
    ret = df["Tempo de Nivel"].values[0]
    return ret    

def set_K_TEMPO_NIVEL(filename, a):
    # reading the csv file
    df = pd.read_csv(filename)

    # updating the column value/data
    df.loc[0, 'Tempo de Nivel'] = a

    # writing into the file
    df.to_csv(filename, index=False)
    # print(df)


def get_K_CARRO(filename):
    # reading the csv file
    df = pd.read_csv(filename)

    # getting value/data
    ret = df["Carro"].values[0]
    return ret    

def set_K_CARRO(filename, a):
    # reading the csv file
    df = pd.read_csv(filename)

    # updating the column value/data
    df.loc[0, 'Carro'] = a

    # writing into the file
    df.to_csv(filename, index=False)
    # print(df)


def get_K_AMBIENTE(filename):
    # reading the csv file
    df = pd.read_csv(filename)

    # getting value/data
    ret = df["Ambiente"].values[0]
    return ret    

def set_K_AMBIENTE(filename, a):
    # reading the csv file
    df = pd.read_csv(filename)

    # updating the column value/data
    df.loc[0, 'Ambiente'] = a

    # writing into the file
    df.to_csv(filename, index=False)
    # print(df)


def get_K_PALETA(filename):
    # reading the csv file
    df = pd.read_csv(filename)

    # getting value/data
    ret = df["Paleta"].values[0]
    return ret    

def set_K_PALETA(filename, a):
    # reading the csv file
    df = pd.read_csv(filename)

    # updating the column value/data
    df.loc[0, 'Paleta'] = a

    # writing into the file
    df.to_csv(filename, index=False)
    # print(df)


def get_K_ALVO(filename):
    # reading the csv file
    df = pd.read_csv(filename)

    # getting value/data
    ret = df["Alvo"].values[0]
    return ret    

def set_K_ALVO(filename, a):
    # reading the csv file
    df = pd.read_csv(filename)

    # updating the column value/data
    df.loc[0, 'Alvo'] = a

    # writing into the file
    df.to_csv(filename, index=False)
    # print(df)


def get_K_OBSTACULO(filename):
    # reading the csv file
    df = pd.read_csv(filename)

    # getting value/data
    ret = df["Obstaculo"].values[0]
    return ret    

def set_K_OBSTACULO(filename, a):
    # reading the csv file
    df = pd.read_csv(filename)

    # updating the column value/data
    df.loc[0, 'Obstaculo'] = a

    # writing into the file
    df.to_csv(filename, index=False)
    # print(df)


def get_K_IMG_FEED_POS(filename):
    # reading the csv file
    df = pd.read_csv(filename)

    # getting value/data
    ret = df["Imagem Feedback Positivo"].values[0]
    return ret    

def set_K_IMG_FEED_POS(filename, a):
    # reading the csv file
    df = pd.read_csv(filename)

    # updating the column value/data
    df.loc[0, 'Imagem Feedback Positivo'] = a

    # writing into the file
    df.to_csv(filename, index=False)
    # print(df)


def get_K_IMG_FEED_NEU(filename):
    # reading the csv file
    df = pd.read_csv(filename)

    # getting value/data
    ret = df["Imagem Feedback Neutro"].values[0]
    return ret    

def set_K_IMG_FEED_NEU(filename, a):
    # reading the csv file
    df = pd.read_csv(filename)

    # updating the column value/data
    df.loc[0, 'Imagem Feedback Neutro'] = a

    # writing into the file
    df.to_csv(filename, index=False)
    # print(df)


def get_K_IMG_FEED_NEG(filename):
    # reading the csv file
    df = pd.read_csv(filename)

    # getting value/data
    ret = df["Imagem Feedback Negativo"].values[0]
    return ret    

def set_K_IMG_FEED_NEG(filename, a):
    # reading the csv file
    df = pd.read_csv(filename)

    # updating the column value/data
    df.loc[0, 'Imagem Feedback Negativo'] = a

    # writing into the file
    df.to_csv(filename, index=False)
    # print(df)


def get_K_SOM_FEED_POS(filename):
    # reading the csv file
    df = pd.read_csv(filename)

    # getting value/data
    ret = df["Som Feedback Positivo"].values[0]
    return ret    

def set_K_SOM_FEED_POS(filename, a):
    # reading the csv file
    df = pd.read_csv(filename)

    # updating the column value/data
    df.loc[0, 'Som Feedback Positivo'] = a

    # writing into the file
    df.to_csv(filename, index=False)
    # print(df)


def get_K_SOM_FEED_NEU(filename):
    # reading the csv file
    df = pd.read_csv(filename)

    # getting value/data
    ret = df["Som Feedback Neutro"].values[0]
    return ret    

def set_K_SOM_FEED_NEU(filename, a):
    # reading the csv file
    df = pd.read_csv(filename)

    # updating the column value/data
    df.loc[0, 'Som Feedback Neutro'] = a

    # writing into the file
    df.to_csv(filename, index=False)
    # print(df)


def get_K_SOM_FEED_NEG(filename):
    # reading the csv file
    df = pd.read_csv(filename)

    # getting value/data
    ret = df["Som Feedback Negativo"].values[0]
    return ret    

def set_K_SOM_FEED_NEG(filename, a):
    # reading the csv file
    df = pd.read_csv(filename)

    # updating the column value/data
    df.loc[0, 'Som Feedback Negativo'] = a

    # writing into the file
    df.to_csv(filename, index=False)
    # print(df)

