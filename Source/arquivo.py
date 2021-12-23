import csv

"""
Funções que interagem com os arquivos csv
"""

csv.register_dialect(
    'mydialect',
    delimiter = ',',
    quotechar = '"',
    doublequote = True,
    skipinitialspace = True,
    lineterminator = '\n',
    quoting = csv.QUOTE_MINIMAL)

def CadastrarJogador(Nome, Nasc, Obs):
    Dados = ['Nome', Nome, 'Data de Nasc.', Nasc, 'Observacoes', Obs]
    Configs = ['Fase Atual', '1', 'Nivel Atual', '1', 'Tempo de Nivel', '120', 'Carro', 'carro.png', 'Ambiente', 'ambiente.png', 'Paleta', '0', 'Alvo', 'alvo.png', 'Obstaculo', 'obstaculo.png', 'Imagem Feedback Positivo', 'feedPos.png', 'Imagem Feedback Neutro', 'feedNeut.png', 'Imagem Feedback Negativo', 'feedNeg.png', 'Som Feedback Positivo', 'feedPos.mp3', 'Som Feedback Neutro', 'feedNeut.mp3', 'Som Feedback Negativo', 'feedNeg.mp3', 'HUD', True, 'Som', True]
    fields = ['Sessao', 'Data da Sessao', 'Hora Inicio', 'Fase Alcancada', 'Nivel Alcancado', 'Pontuacao Geral', 'Q Movimentos', 'Q Alvos Colididos', 'Q Alvos Desviados', 'Q Obstaculos Colididos', 'Q Obstaculos Desviados']
    file = 'Jogadores/' + Nome + '_KarTEA.csv'
    with open(file, 'w') as csvfile:
        csvwriter = csv.writer(csvfile, dialect='mydialect')
        csvwriter.writerow(Dados)
        csvwriter.writerow(Configs)
        csvwriter.writerow(fields)

    Configs = ['Fase Atual', '1', 'Nivel Atual', '1', 'Tempo de Nivel', '120', 'Tempo de Ajuda', '60']
    fields = ['Sessao', 'Data da Sessao', 'Hora Inicio', 'Fase Atual', 'Nivel Atual', 'Pontuacao Geral', 'Quant. Movimentos', 'Quant. Alvos Colididos', 'Quant. Alvos Desviados', 'Quant. Obstaculos Colididos', 'Quant. Obstaculos Desviados']
    file = 'Jogadores/' + Nome + '_RepeTEA.csv'
    with open(file, 'w') as csvfile:
        csvwriter = csv.writer(csvfile, dialect='mydialect')
        csvwriter.writerow(Dados)
        csvwriter.writerow(Configs)
        csvwriter.writerow(fields)

    fields = ['ID', 'Sessao', 'Hora do Evento', 'Fase', 'Nivel', 'Posicao jogador', 'Posicao Evento', 'Tipo de Evento']
    file = 'Jogadores/' + Nome + '_KarTEA_detalhado.csv'
    with open(file, 'w') as csvfile:
        csvwriter = csv.writer(csvfile, dialect='mydialect')
        csvwriter.writerow(fields)

    fields = ['ID', 'Sessao', 'Hora do Evento', 'Fase', 'Nivel', 'Posicao jogador', 'Posicao Evento', 'Tipo de Evento']
    file = 'Jogadores/' + Nome + '_RepeTEA_detalhado.csv'
    with open(file, 'w') as csvfile:
        csvwriter = csv.writer(csvfile, dialect='mydialect')
        csvwriter.writerow(fields)

"""
Nome = 'Gabriel'
Nasc = '20/01/1997'
Obs = ''

CadastrarJogador(Nome, Nasc, Obs)
"""

def gravaDados(filename, Dados):# Dados é um vetor com os dados para gravar no arquivo 'filename'
    with open(filename, 'a') as csvfile:
        csvwriter = csv.writer(csvfile, dialect='mydialect')
        csvwriter.writerow(Dados)

"""
Exemplo de uso 
Dados = ['1', '01/07/2021', '15:05:21', '1', '1', '0', '0', '0', '0', '0', '0']
gravaDados('Gabriel_Kartea.csv', Dados)
"""

def lerConfigs(filename): #Apenas para os arquivos gerais, nos detalhados retorna a primeira linha de dados
    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile, dialect='mydialect')
        fields = next(csvreader)  # Dados do jogador
        fields = next(csvreader)  # Configuracoes
        return fields

"""
#Array de Configs do KARTEA
print(lerConfigs('Jogadores/Gabriel_KarTEA.csv'))
CONFIGS = arquivo.lerConfigs(PLAYER_ARQ)

K_FASE = CONFIGS[1]
K_NIVEL = CONFIGS[3]
K_TEMPO_NIVEL = CONFIGS[5]
K_CARRO = CONFIGS[7]
K_AMBIENTE = CONFIGS[9]
K_PALETA = CONFIGS[11]
K_ALVO = CONFIGS[13]
K_OBSTACULO = CONFIGS[15]
K_IMG_FEED_POS = CONFIGS[17]
K_IMG_FEED_NEU = CONFIGS[19]
K_IMG_FEED_NEG = CONFIGS[21]
K_SOM_FEED_POS = CONFIGS[23]
K_SOM_FEED_NEU = CONFIGS[25]
K_SOM_FEED_NEG = CONFIGS[27]

#Array de Configs do REPETEA
print(lerConfigs('Jogadores/Gabriel_RepeTEA.csv'))
CONFIGS = arquivo.lerConfigs(PLAYER_ARQ)

R_FASE = CONFIGS[1]
R_NIVEL = CONFIGS[3]
R_TEMPO_NIVEL = CONFIGS[5]
"""
