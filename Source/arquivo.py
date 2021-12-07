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

Nome = 'Gabriel'
Nasc = '20/01/1997'
Obs = ''

CadastrarJogador(Nome, Nasc, Obs)

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
print(lerConfigs('Jogadores/Gabriel_Kartea.csv'))
print(lerConfigs('Jogadores/Gabriel_RepeTEA.csv'))

# reading csv file
with open(filename, 'r') as csvfile:
    csvreader = csv.reader(csvfile, dialect='mydialect')
    fields = next(csvreader)#Dados do jogador
    fields = next(csvreader)#Configuracoes
    fields = next(csvreader)#Campos de Dados
  
    # extracting each data row one by one
    for row in csvreader:
        rows.append(row)
  
    # get total number of rows
    print("Total no. of data rows: %d"%(csvreader.line_num-3))

# printing the field names
print('Field names are:' + ', '.join(field for field in fields))
  
#  printing first 5 rows
print('\nFirst 5 rows are:\n')
for row in rows[:5]:
    # parsing each column of a row
    for col in row:
        print("%10s "%col)
    print('\n')
"""