#################################################################################
######################### SOFTWARE BASE - PROJETO T-TEA #########################
#################################################################################
################################# VERSÃO 1.0 ####################################
#################################################################################
import csv
import cv2
import mediapipe as mp
import numpy as np
import pygame
import time
import random
from pygame import mixer
import datetime
import arquivo

pygame.init()
#################################################################################
################################## Hora de Inicio ###############################
#################################################################################
inicio_da_sessao=False
if inicio_da_sessao==False:
    inicio_da_sessao_t0 = int(time.time())
    hora_inicio = datetime.datetime.now().time()
    inicio_da_sessao=True

#################################################################################
################################## CORES & FONTES ###############################
#################################################################################
azul = 0, 0, 255
verde = 0, 255, 0
vermelho = 255, 0, 0
amarelo = 255, 255, 0
branco = 255, 255, 255
preto = 0, 0, 0
fonte = cv2.FONT_HERSHEY_SIMPLEX
font = pygame.font.SysFont('Sans', 25)
#################################################################################
############################# VARIÁVEIS DE PROGRAMA #############################
#################################################################################
mp_drawing = mp.solutions.drawing_utils  # Configuração do MediaPipe. Ver https://google.github.io/mediapipe/solutions/pose.html para maiores detalhes.
mp_pose = mp.solutions.pose  # Configuração do MediaPipe. Ver https://google.github.io/mediapipe/solutions/pose.html para maiores detalhes.
pontos_calibracao = np.zeros((4, 2), int)  # Matriz para os pontos de calibração de perspectiva - 4 linhas/ 2 colunas
contador = 4  # Contador utilizado nos 4 pontos de calibração - Mas agora não tem uso, pois a calibração ocorre no menu
game_start=False # Coloca na tela iniciar
gameExit=False # Sai do completamente do jogo
figura_selecionada=False # Usada para evitar que o usuário apenas selecione uma vez a figura e não ficar piscando
lista_sorteio=[] #São as figuras sorteadas pelo computador e colocadas nesta lista, para depois fazer a comparação com as escolhas do usuário
pontuacao=0 # Pontos conseguidos em durante a rodada
atencao_memorizar=False
hud_switch=True
som_switch=True
pausa_switch=False
tempo_ajuda_switch=False
tentativa=1
q_acertos=0
q_acertos_com_ajuda=0
q_ajudas=0
q_erros=0
q_omissao=0

csv.register_dialect(
    'mydialect',
    delimiter = ',',
    quotechar = '"',
    doublequote = True,
    skipinitialspace = True,
    lineterminator = '\n',
    quoting = csv.QUOTE_MINIMAL)

#################################################################################
######################## ARQUIVO DO JOGADOR SELECIONADO #########################
#################################################################################
jogador_selecionado = 'Jogadores/' + arquivo.get_Player() +'_RepeTEA.csv'
jogador_selecionado_config = 'Jogadores/' + arquivo.get_Player() +'_RepeTEA_config.csv'
jogador_selecionado_detalhado = 'Jogadores/' + arquivo.get_Player() +'_RepeTEA_detalhado.csv'
print(jogador_selecionado)
hud_switch=arquivo.get_R_HUD(jogador_selecionado_config)
som_switch=arquivo.get_R_SOM(jogador_selecionado_config)

pontos_calibracao_repetea = arquivo.lerCalibracao()
print("Pontos de Calibracao do RepeTEA: ", pontos_calibracao_repetea)

########################################################################################
############################ LEITURA DO ARQUIVO CONFIG.CSV #############################
########################################################################################
with open(jogador_selecionado_config, 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    linha_1_csv = next(csv_reader)
    linha_2_csv = next(csv_reader)
    sessao = int(linha_2_csv[0])+1
    nome_no_hud = linha_2_csv[1]
    fase_no_hud = linha_2_csv[4]
    nivel_no_hud = linha_2_csv[5]
    tempo_ajuda= int(linha_2_csv[6])
    tempo_total=int(linha_2_csv[7])
    t_exposicao=float(linha_2_csv[8])
    t_vez_do_jogador = float(linha_2_csv[9])
    camera=int(linha_2_csv[12])
    largura_projetor=int(linha_2_csv[13])
    altura_projetor=int(linha_2_csv[14])
    largura_tela_controle=int(linha_2_csv[15])
    altura_tela_controle = int(linha_2_csv[16])
    paleta_de_cores = str(linha_2_csv[17])
    paleta_de_sons = str(linha_2_csv[18])

relacao_largura = (largura_projetor / largura_tela_controle)  # Esta relação é usada na correção de perspectiva.
relacao_altura = (altura_projetor / altura_tela_controle)  # Esta relação é usada na correção de perspectiva.
tela_de_calibracao = np.zeros((altura_projetor, largura_projetor, 3),np.uint8)  # Tela que será usada para o projetar o jogo.
tela_de_controle = np.zeros((altura_tela_controle, largura_tela_controle, 3),np.uint8)  # Tela que será usada para o projetar o jogo.

camera = cv2.VideoCapture(camera,cv2.CAP_DSHOW)  # O valor entre parênteses indica qual câmera será utilizada. 0=default; 1,2,3...= câmeras externas.

tamanho_sequencia = int (fase_no_hud)
tamanho_sequencia_atual = int (fase_no_hud)
nivel_sequencia = int (nivel_no_hud)
nivel_sequencia_atual = int (nivel_no_hud)

#############################################################################################
############################### SPRITES COM PALETA DE CORES #################################
#############################################################################################

icone_fig=pygame.image.load('Assets/Repetea_Figuras/'+paleta_de_cores+'/icone.png')
atencao_perto_fig=pygame.image.load('Assets/Repetea_Figuras/'+paleta_de_cores+'/atencao_perto.png')
atencao_longe_fig=pygame.image.load('Assets/Repetea_Figuras/'+paleta_de_cores+'/atencao_longe.png')
trofeu_fig=pygame.image.load('Assets/Repetea_Figuras/'+paleta_de_cores+'/trofeu.png')
trofeu_25_fig=pygame.image.load('Assets/Repetea_Figuras/'+paleta_de_cores+'/trofeu_25.png')
trofeu_50_fig=pygame.image.load('Assets/Repetea_Figuras/'+paleta_de_cores+'/trofeu_50.png')
trofeu_75_fig=pygame.image.load('Assets/Repetea_Figuras/'+paleta_de_cores+'/trofeu_75.png')
triste_fig=pygame.image.load('Assets/Repetea_Figuras/'+paleta_de_cores+'/triste.png')
feliz_fig=pygame.image.load('Assets/Repetea_Figuras/'+paleta_de_cores+'/feliz.png')
vez_do_jogador_verde_1_fig=pygame.image.load('Assets/Repetea_Figuras/'+paleta_de_cores+'/vez_do_jogador_verde_1.png')
vez_do_jogador_verde_2_fig=pygame.image.load('Assets/Repetea_Figuras/'+paleta_de_cores+'/vez_do_jogador_verde_2.png')
base_com_pe_fig=pygame.image.load('Assets/Repetea_Figuras/'+paleta_de_cores+'/base_com_pe.png')
base_com_pe_verde_fig=pygame.image.load('Assets/Repetea_Figuras/'+paleta_de_cores+'/base_com_pe_verde.png')
base_com_pe_vermelho_fig=pygame.image.load('Assets/Repetea_Figuras/'+paleta_de_cores+'/base_com_pe_vermelho.png')
base_sem_pe_fig=pygame.image.load('Assets/Repetea_Figuras/'+paleta_de_cores+'/base_sem_pe.png')
avisos_fig=pygame.image.load('Assets/Repetea_Figuras/'+paleta_de_cores+'/avisos.png')
ajuda_f1_fig=pygame.image.load('Assets/Repetea_Figuras/'+paleta_de_cores+'/ajuda_F1.png')
instrucao_calibrar_fig=pygame.image.load('Assets/Repetea_Figuras/'+paleta_de_cores+'/calibrar.png')
repetea_iniciar_fig=pygame.image.load('Assets/Repetea_Figuras/'+paleta_de_cores+'/base_com_iniciar.png')
pausa_fig=pygame.image.load('Assets/Repetea_Figuras/'+paleta_de_cores+'/pause.png')
sem_sinal_fig=pygame.image.load('Assets/Repetea_Figuras/'+paleta_de_cores+'/sem_sinal.png')
tempo_fig=pygame.image.load('Assets/Repetea_Figuras/'+paleta_de_cores+'/tempo.png')
som_ligado_fig=pygame.image.load('Assets/Repetea_Figuras/'+paleta_de_cores+'/som_ligado.png')
som_desligado_fig=pygame.image.load('Assets/Repetea_Figuras/'+paleta_de_cores+'/som_desligado.png')
hud_on_fig=pygame.image.load('Assets/Repetea_Figuras/'+paleta_de_cores+'/hud_on.png')
hud_off_fig=pygame.image.load('Assets/Repetea_Figuras/'+paleta_de_cores+'/hud_off.png')
posicionamento_fig=pygame.image.load('Assets/Repetea_Figuras/'+paleta_de_cores+'/posicionamento.png')
fase_abaixo_fig=pygame.image.load('Assets/Repetea_Figuras/'+paleta_de_cores+'/fase_abaixo.png')
fase_acima_fig=pygame.image.load('Assets/Repetea_Figuras/'+paleta_de_cores+'/fase_acima.png')
silhueta_perto_fig=pygame.image.load('Assets/Repetea_Figuras/'+paleta_de_cores+'/silhueta_perto.png')
silhueta_longe_fig=pygame.image.load('Assets/Repetea_Figuras/'+paleta_de_cores+'/silhueta_longe.png')
triagulo_longe_selecionado_fig=pygame.image.load('Assets/Repetea_Figuras/'+paleta_de_cores+'/triangulo_selecionado_longe.png')
triagulo_longe_selecionado_ajuda_fig=pygame.image.load('Assets/Repetea_Figuras/'+paleta_de_cores+'/triangulo_selecionado_longe_ajuda.png')
retangulo_longe_selecionado_fig=pygame.image.load('Assets/Repetea_Figuras/'+paleta_de_cores+'/retangulo_selecionado_longe.png')
retangulo_longe_selecionado_ajuda_fig=pygame.image.load('Assets/Repetea_Figuras/'+paleta_de_cores+'/retangulo_selecionado_longe_ajuda.png')
circulo_longe_selecionado_fig=pygame.image.load('Assets/Repetea_Figuras/'+paleta_de_cores+'/circulo_selecionado_longe.png')
circulo_longe_selecionado_ajuda_fig=pygame.image.load('Assets/Repetea_Figuras/'+paleta_de_cores+'/circulo_selecionado_longe_ajuda.png')
quadrado_longe_selecionado_fig=pygame.image.load('Assets/Repetea_Figuras/'+paleta_de_cores+'/quadrado_selecionado_longe.png')
quadrado_longe_selecionado_ajuda_fig=pygame.image.load('Assets/Repetea_Figuras/'+paleta_de_cores+'/quadrado_selecionado_longe_ajuda.png')
triagulo_perto_selecionado_fig=pygame.image.load('Assets/Repetea_Figuras/'+paleta_de_cores+'/triangulo_selecionado_perto.png')
triagulo_perto_selecionado_ajuda_fig=pygame.image.load('Assets/Repetea_Figuras/'+paleta_de_cores+'/triangulo_selecionado_perto_ajuda.png')
retangulo_perto_selecionado_fig=pygame.image.load('Assets/Repetea_Figuras/'+paleta_de_cores+'/retangulo_selecionado_perto.png')
retangulo_perto_selecionado_ajuda_fig=pygame.image.load('Assets/Repetea_Figuras/'+paleta_de_cores+'/retangulo_selecionado_perto_ajuda.png')
circulo_perto_selecionado_fig=pygame.image.load('Assets/Repetea_Figuras/'+paleta_de_cores+'/circulo_selecionado_perto.png')
circulo_perto_selecionado_ajuda_fig=pygame.image.load('Assets/Repetea_Figuras/'+paleta_de_cores+'/circulo_selecionado_perto_ajuda.png')
quadrado_perto_selecionado_fig=pygame.image.load('Assets/Repetea_Figuras/'+paleta_de_cores+'/quadrado_selecionado_perto.png')
quadrado_perto_selecionado_ajuda_fig=pygame.image.load('Assets/Repetea_Figuras/'+paleta_de_cores+'/quadrado_selecionado_perto_ajuda.png')

#################################################################################
################################# PALETA DE SONS ################################
#################################################################################
som_triangulo_wav = mixer.Sound('Assets/Repetea_Sons/'+paleta_de_sons+'/1_triangulo.wav')
som_retangulo_wav = mixer.Sound('Assets/Repetea_Sons/'+paleta_de_sons+'/2_retangulo.wav')
som_circulo_wav = mixer.Sound('Assets/Repetea_Sons/'+paleta_de_sons+'/3_circulo.wav')
som_quadrado_wav = mixer.Sound('Assets/Repetea_Sons/'+paleta_de_sons+'/4_quadrado.wav')
som_feliz_wav = mixer.Sound('Assets/Repetea_Sons/'+paleta_de_sons+'/5_feliz.wav')
som_triste_wav = mixer.Sound('Assets/Repetea_Sons/'+paleta_de_sons+'/6_triste.wav')
som_iniciar_wav = mixer.Sound('Assets/Repetea_Sons/'+paleta_de_sons+'/7_iniciar.wav')
som_trofeu_wav = mixer.Sound('Assets/Repetea_Sons/'+paleta_de_sons+'/8_trofeu.wav')
som_background_wav = mixer.Sound('Assets/Repetea_Sons/'+paleta_de_sons+'/9_background.wav')
som_vez_do_jogador_1_wav = mixer.Sound('Assets/Repetea_Sons/'+paleta_de_sons+'/10_vez_do_jogador_1.wav')
som_vez_do_jogador_2_wav = mixer.Sound('Assets/Repetea_Sons/'+paleta_de_sons+'/10_vez_do_jogador_2.wav')
som_ajuda_wav = mixer.Sound('Assets/Repetea_Sons/'+paleta_de_sons+'/11_ajuda.wav')

#################################################################################
################################### FUNÇÕES #####################################
#################################################################################
def evento():
    data= datetime.date.today()
    hora= datetime.datetime.now().time()


def avisos(): #Tela inicial com os avisos do equipamento
    gameDisplay.blit(avisos_fig,(0, 0))

def atencao_perto(): #Para o jogador prestar atencao
    gameDisplay.blit(atencao_perto_fig,(0, 0))

def atencao_longe(): #Para o jogador prestar atencao
    gameDisplay.blit(atencao_longe_fig,(0, 0))

def ajuda_f1(): #Tela com as teclas de atalho
    gameDisplay.blit(ajuda_f1_fig, (0, 0))

def trofeu(): #Trofeu sem emoji (Não usado)
    gameDisplay.blit(trofeu_fig,(0, 0))

def trofeu_25(): #Trofeu quando usuário atinge até 25% do total
    gameDisplay.blit(trofeu_25_fig, (0, 0))

def trofeu_50(): #Trofeu quando usuário atinge de 25% a 75% do total
    gameDisplay.blit(trofeu_50_fig, (0, 0))

def trofeu_75(): #Trofeu quando usuário atinge acima de 75% do total
    gameDisplay.blit(trofeu_75_fig, (0, 0))

def vez_do_jogador_perto_1():
    gameDisplay.blit(vez_do_jogador_verde_1_fig, (0, 0))

def vez_do_jogador_perto_2():
    gameDisplay.blit(vez_do_jogador_verde_2_fig, (0, 0))

def vez_do_jogador_perto(): #Indica quando inicia a resposta do jogador
    base_com_pe_verde()
    silhueta_perto()
    if hud_switch == True:
        hud_info()
    tela_update()
    delay()
    vez_do_jogador_perto_2()
    som_vez_do_jogador_1()
    silhueta_perto()
    if hud_switch == True:
        hud_info()
    tela_update()
    delay()
    vez_do_jogador_perto_1()
    som_vez_do_jogador_2()
    silhueta_perto()
    if hud_switch == True:
        hud_info()
    tela_update()
    delay()
    tempo_de_vez_do_jogador() #Este tempo libera os circulos verder para controle inibitório da Dr. do Rio

def vez_do_jogador_longe(): #Indica quando inicia a resposta do jogador
    base_com_pe_verde()
    silhueta_longe()
    if hud_switch == True:
        hud_info()
    tela_update()
    delay()
    vez_do_jogador_perto_2()
    som_vez_do_jogador_1()
    silhueta_longe()
    if hud_switch == True:
        hud_info()
    tela_update()
    delay()
    vez_do_jogador_perto_1()
    som_vez_do_jogador_2()
    silhueta_longe()
    if hud_switch == True:
        hud_info()
    tela_update()
    delay()
    tempo_de_vez_do_jogador()  # Este tempo libera os circulos verder para controle inibitório da Dr. do Rio

def pausa():
    gameDisplay.blit(pausa_fig, (0, 0))

def som_ligado():
    gameDisplay.blit(som_ligado_fig, (0, 0))

def som_desligado():
    gameDisplay.blit(som_desligado_fig, (0, 0))

def hud_on():
    gameDisplay.blit(hud_on_fig, (0, 0))

def hud_off():
    gameDisplay.blit(hud_off_fig, (0, 0))

def posicionamento():
    gameDisplay.blit(posicionamento_fig, (0, 0))

def fase_abaixo():
    gameDisplay.blit(fase_abaixo_fig, (0, 0))

def fase_acima():
    gameDisplay.blit(fase_acima_fig, (0, 0))

def sem_sinal():
    gameDisplay.blit(sem_sinal_fig, (0, 0))

def tempo_max():
    gameDisplay.blit(tempo_fig, (0, 0))

def feliz():
    gameDisplay.blit(feliz_fig,(0, 0))

def triste():
    gameDisplay.blit(triste_fig,(0, 0))

def base_sem_pe():
    gameDisplay.blit(base_sem_pe_fig,(0, 0))

def base_com_pe(): #base com pé branco
    gameDisplay.blit(base_com_pe_fig,(0, 0))

def base_com_pe_verde():
    gameDisplay.blit(base_com_pe_verde_fig,(0, 0))

def base_com_pe_vermelho():
    gameDisplay.blit(base_com_pe_vermelho_fig,(0, 0))

def silhueta_longe():
    gameDisplay.blit(silhueta_longe_fig,(0, 0))

def triangulo_longe_selecionado():
    gameDisplay.blit(triagulo_longe_selecionado_fig, (0, 0))

def triangulo_longe_selecionado_ajuda():
    gameDisplay.blit(triagulo_longe_selecionado_ajuda_fig, (0, 0))

def retangulo_longe_selecionado():
    gameDisplay.blit(retangulo_longe_selecionado_fig, (0, 0))

def retangulo_longe_selecionado_ajuda():
    gameDisplay.blit(retangulo_longe_selecionado_ajuda_fig, (0, 0))

def circulo_longe_selecionado():
    gameDisplay.blit(circulo_longe_selecionado_fig, (0, 0))

def circulo_longe_selecionado_ajuda():
    gameDisplay.blit(circulo_longe_selecionado_ajuda_fig, (0, 0))

def quadrado_longe_selecionado():
    gameDisplay.blit(quadrado_longe_selecionado_fig, (0, 0))

def quadrado_longe_selecionado_ajuda():
    gameDisplay.blit(quadrado_longe_selecionado_ajuda_fig, (0, 0))

def silhueta_perto():
    gameDisplay.blit(silhueta_perto_fig,(0, 0))

def triangulo_perto_selecionado():
    gameDisplay.blit(triagulo_perto_selecionado_fig, (0, 0))

def triangulo_perto_selecionado_ajuda():
    gameDisplay.blit(triagulo_perto_selecionado_ajuda_fig, (0, 0))

def retangulo_perto_selecionado():
    gameDisplay.blit(retangulo_perto_selecionado_fig, (0, 0))

def retangulo_perto_selecionado_ajuda():
    gameDisplay.blit(retangulo_perto_selecionado_ajuda_fig, (0, 0))

def circulo_perto_selecionado():
    gameDisplay.blit(circulo_perto_selecionado_fig, (0, 0))

def circulo_perto_selecionado_ajuda():
    gameDisplay.blit(circulo_perto_selecionado_ajuda_fig, (0, 0))

def quadrado_perto_selecionado():
    gameDisplay.blit(quadrado_perto_selecionado_fig, (0, 0))

def quadrado_perto_selecionado_ajuda():
    gameDisplay.blit(quadrado_perto_selecionado_ajuda_fig, (0, 0))

def instrucao_calibrar():
    gameDisplay.blit(instrucao_calibrar_fig, (0, 0))

def repetea_iniciar():
    gameDisplay.blit(repetea_iniciar_fig, (0, 0))

def fill_preto():
    gameDisplay.fill(preto)

def som_triangulo():
    if som_switch==True:
        som_triangulo_wav.play()

def som_retangulo():
    if som_switch == True:
        som_retangulo_wav.play()

def som_circulo():
    if som_switch == True:
        som_circulo_wav.play()

def som_quadrado():
    if som_switch == True:
        som_quadrado_wav.play()

def som_feliz():
    if som_switch == True:
        som_feliz_wav.play()

def som_triste():
    if som_switch == True:
        som_triste_wav.play()

def som_iniciar():
    if som_switch == True:
        som_iniciar_wav.play()

def som_vez_do_jogador_1():
    if som_switch == True:
        som_vez_do_jogador_1_wav.play()

def som_vez_do_jogador_2():
    if som_switch==True:
        som_vez_do_jogador_2_wav.play()

def som_ajuda():
    if som_switch == True:
        som_ajuda_wav.play()

def som_trofeu():
    if som_switch == True:
        som_trofeu_wav.play()

def hud_info():
    fase_hud = str(tamanho_sequencia_atual)
    tentativa_hud = str(tentativa)
    nivel_hud = nivel_sequencia_atual

    if nivel_hud==1:
        nivel_hud='Perto'
    if nivel_hud==2:
        nivel_hud='Longe'

    nivel_hud = str(nivel_hud)
    inicio_da_sessao_t1 = int(time.time())
    tempo_int = int((inicio_da_sessao_t1 - inicio_da_sessao_t0)/60)
    tempo_hud = str(tempo_int)


    texto_jogador = font.render('Jogador:', True, branco)
    gameDisplay.blit(texto_jogador, [(0.05 * largura_projetor), (0.8 * altura_projetor)])
    texto_nome_partida = font.render(nome_no_hud, True, branco)
    gameDisplay.blit(texto_nome_partida, [(0.15 * largura_projetor), (0.8 * altura_projetor)])

    texto_tempo = font.render('Minutos:', True, branco)
    gameDisplay.blit(texto_tempo, [(0.05 * largura_projetor), (0.85 * altura_projetor)])
    texto_tempo_partida = font.render(tempo_hud, True, branco)
    gameDisplay.blit(texto_tempo_partida, [(0.15 * largura_projetor), (0.85 * altura_projetor)])

    texto_fase = font.render('Fase:', True, branco)
    gameDisplay.blit(texto_fase, [(0.7 * largura_projetor), (0.8 * altura_projetor)])
    texto_fase_partida = font.render(fase_hud, True, branco)
    gameDisplay.blit(texto_fase_partida, [(0.76 * largura_projetor), (0.8 * altura_projetor)])

    texto_tentativa = font.render('Tentativa:', True, branco)
    gameDisplay.blit(texto_tentativa, [(0.83 * largura_projetor), (0.8 * altura_projetor)])
    texto_tentativa_partida = font.render(tentativa_hud, True, branco)
    gameDisplay.blit(texto_tentativa_partida, [(0.94 * largura_projetor), (0.8 * altura_projetor)])

    texto_nivel = font.render('Nível:', True, branco)
    gameDisplay.blit(texto_nivel, [(0.7 * largura_projetor), (0.85 * altura_projetor)])
    texto_nivel_partida = font.render(nivel_hud, True, branco)
    gameDisplay.blit(texto_nivel_partida, [(0.77 * largura_projetor), (0.85 * altura_projetor)])



def mousePoints(event, x, y, flags, params):
    # Função para capturar cliques do Mouse:
    global contador
    if event == cv2.EVENT_LBUTTONDOWN:
        pontos_calibracao[contador] = x, y
        contador = contador + 1



def posicao():
    # Função para determinar a posição do jogador na área de projeçao:
    # Transformação de Perspectiva:
    pts1 = np.float32([pontos_calibracao_repetea[0], pontos_calibracao_repetea[1], pontos_calibracao_repetea[2], pontos_calibracao_repetea[3]])
    pts2 = np.float32(
        [[0, 0], [largura_tela_controle, 0], [0, altura_tela_controle], [largura_tela_controle, altura_tela_controle]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    perspectiva = cv2.warpPerspective(tela_de_controle, matrix, (largura_tela_controle, altura_tela_controle))

    # Posição do jogador:
    p = (int(x_pose * largura_tela_controle), int(y_pose * altura_tela_controle))
    position_x = (matrix[0][0] * p[0] + matrix[0][1] * p[1] + matrix[0][2]) / (
    (matrix[2][0] * p[0] + matrix[2][1] * p[1] + matrix[2][2]))
    position_y = (matrix[1][0] * p[0] + matrix[1][1] * p[1] + matrix[1][2]) / (
    (matrix[2][0] * p[0] + matrix[2][1] * p[1] + matrix[2][2]))
    p_after = (int((position_x) * (relacao_largura)), int((position_y) * (relacao_altura)))

    return p_after

def rand():
    #Função para sortear a figura
    rand_figura = round(random.randrange(0, 4))
    return rand_figura

def delay():
    time.sleep(0.5)

def tempo_de_vez_do_jogador():
    time.sleep(t_vez_do_jogador)

def tempo_de_exposição():
    time.sleep(t_exposicao)

def tela_update():
    pygame.display.update()


def sorteio_longe():
    figura_longe = rand()
    lista_sorteio.append(figura_longe)
    print(lista_sorteio)
    #fill_preto()
    if hud_switch == True:
        hud_info()
    #atencao_longe()
    #base_com_pe_verde()
    #tela_update()
    tempo_de_exposição()

    #fill_preto()
    if hud_switch == True:
        hud_info()
    silhueta_longe()
    base_com_pe_verde()
    tela_update()
    tempo_de_exposição()

    if figura_longe == 0:
        triangulo_longe_selecionado()
        som_triangulo()
        # base_com_pe_vermelho()
        base_com_pe_verde()
        tela_update()
        tempo_de_exposição()

    elif figura_longe == 1:
        retangulo_longe_selecionado()
        som_retangulo()
        # base_com_pe_vermelho()
        base_com_pe_verde()
        tela_update()
        tempo_de_exposição()

    elif figura_longe == 2:
        circulo_longe_selecionado()
        som_circulo()
        # base_com_pe_vermelho()
        base_com_pe_verde()
        tela_update()
        tempo_de_exposição()

    else:
        quadrado_longe_selecionado()
        som_quadrado()
        # base_com_pe_vermelho()
        base_com_pe_verde()
        tela_update()
        tempo_de_exposição()


def sorteio_perto():
    figura_perto = rand()
    lista_sorteio.append(figura_perto)
    print(lista_sorteio)
    #fill_preto()
    if hud_switch == True:
        hud_info()
    #atencao_perto()
    #base_com_pe_verde()
    #tela_update()
    tempo_de_exposição()


    #fill_preto()
    if hud_switch == True:
        hud_info()
    silhueta_perto()
    base_com_pe_verde()
    tela_update()
    tempo_de_exposição()

    if figura_perto == 0:
        triangulo_perto_selecionado()
        som_triangulo()
        #base_com_pe_vermelho()
        base_com_pe_verde()
        tela_update()
        tempo_de_exposição()

    elif figura_perto == 1:
        retangulo_perto_selecionado()
        som_retangulo()
        #base_com_pe_vermelho()
        base_com_pe_verde()
        tela_update()
        tempo_de_exposição()

    elif figura_perto == 2:
        circulo_perto_selecionado()
        som_circulo()
        #base_com_pe_vermelho()
        base_com_pe_verde()
        tela_update()
        tempo_de_exposição()

    else:
        quadrado_perto_selecionado()
        som_quadrado()
        #base_com_pe_vermelho()
        base_com_pe_verde()
        tela_update()
        tempo_de_exposição()


gameWarning = pygame.display.set_mode((largura_projetor, altura_projetor))
pygame.display.set_caption('RepeTEA')
pygame.display.set_icon(icone_fig)
gameWarning.blit(avisos_fig,(0, 0))
pygame.display.update()
gameWarning=False

while not gameWarning:
    for event in pygame.event.get():
        # SAIR ou CONCORDO
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                gameDisplay = pygame.display.set_mode((largura_projetor, altura_projetor))
                pygame.display.set_caption('RepeTEA')
                pygame.display.set_icon(icone_fig)
                #instrucao_calibrar()
                pygame.display.update()
                gameWarning=True
            if event.key == pygame.K_q:
                gameExit = True
                cv2.destroyWindow('tela_de_controle')
                pygame.quit()
                camera.release()
                exit()


#################################################################################
#################### Inicialização do MediaPipe e Calibração ####################
#################################################################################
while not gameExit:

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while camera.isOpened():
            ret, frame = camera.read()

            # Tela de Controle para RGB.
            tela_de_controle = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            tela_de_controle.flags.writeable = False

            # Detecção.
            results = pose.process(tela_de_controle)

            # Tela de Controle para BGR.
            tela_de_controle.flags.writeable = True
            tela_de_controle = cv2.cvtColor(tela_de_controle, cv2.COLOR_RGB2BGR)

            # Extração de coordenadas de pontos de referência.
            try:
                landmarks = results.pose_landmarks.landmark
                #x_pose = (landmarks[mp_pose.PoseLandmark.RIGHT_EAR.value].x + landmarks[mp_pose.PoseLandmark.LEFT_EAR.value].x)/2 # 33 Pontos de referência do MediaPipe. Ex: RIGHT_FOOT_INDEX; NOSE; RIGHT_INDEX; RIGHT_EAR, RIGHT_HEEL
                #y_pose = (landmarks[mp_pose.PoseLandmark.RIGHT_EAR.value].y + landmarks[mp_pose.PoseLandmark.LEFT_EAR.value].y)/2# 33 Pontos de referência do MediaPipe. Ex: RIGHT_FOOT_INDEX; NOSE; RIGHT_INDEX; RIGHT_EAR
                x_pose = (landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value].x + landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value].x)/2
                y_pose = (landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value].y + landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value].y)/2

                # Desenho dos pontos de referência
                mp_drawing.draw_landmarks(tela_de_controle, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                          mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                                          mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2)
                                          )
                # Antes da Calibração.
                if contador <= 3:
                    calibracao()

                # Depois da Calibração.
                elif contador == 4:
                    cv2.line(tela_de_controle, (pontos_calibracao_repetea[0]), (pontos_calibracao_repetea[1]), (verde), 2)
                    cv2.line(tela_de_controle, (pontos_calibracao_repetea[1]), (pontos_calibracao_repetea[3]), (verde), 2)
                    cv2.line(tela_de_controle, (pontos_calibracao_repetea[2]), (pontos_calibracao_repetea[0]), (verde), 2)
                    cv2.line(tela_de_controle, (pontos_calibracao_repetea[2]), (pontos_calibracao_repetea[3]), (verde), 2)

                    cv2.circle(tela_de_controle, (pontos_calibracao_repetea[0]), 5, azul, 3)
                    cv2.circle(tela_de_controle, (pontos_calibracao_repetea[1]), 5, azul, 3)
                    cv2.circle(tela_de_controle, (pontos_calibracao_repetea[2]), 5, azul, 3)
                    cv2.circle(tela_de_controle, (pontos_calibracao_repetea[3]), 5, azul, 3)
                    cv2.destroyWindow("TELA DE CALIBRACAO")
                    gameDisplay = pygame.display.set_mode((largura_projetor, altura_projetor))
                    pygame.display.set_caption('RepeTEA')
                    pygame.display.set_icon(icone_fig)
                    jogador=posicao()

                    if jogador[0] > 350 and jogador[0] < 450 and jogador[1] > 400 and game_start==False:
                        game_start=True
                        som_iniciar()


                    if game_start==True:
                        #print(tamanho_sequencia)
                        #print(tamanho_sequencia_atual)

                        if pausa_switch == True:
                            fill_preto()
                            pausa()
                            pygame.display.update()

                    #################################################################################
                    #################################################################################
                    ##################### Jogador posicionado e inicio de sequencia# ################
                    #################################################################################
                    ###################################### PERTO ####################################
                    #################################################################################
                    #################################################################################


                        if nivel_sequencia==1 and pausa_switch==False: # NIVEL PERTO
                            ##########################
                            ####SORTEIO DA JOGADA#####
                            ##########################
                            if tamanho_sequencia>0:
                                sorteio_perto()
                                tamanho_sequencia=tamanho_sequencia-1
                                if tamanho_sequencia<=0:
                                    sinal_de_vez=True

                            ###########################
                            #######VEZ DO JOGADOR######
                            ###########################

                            else:

                                if sinal_de_vez==True:
                                    vez_do_jogador_perto()
                                    sinal_de_vez=False
                                    disparo_relogio = False
                                    item_da_lista=0
                                base_sem_pe()

                                if figura_selecionada==True:
                                    base_com_pe_verde()

                                if tempo_ajuda_switch==False:
                                    silhueta_perto()

                                if tempo_ajuda_switch==True:
                                    if lista_sorteio[item_da_lista]==0:
                                        triangulo_perto_selecionado_ajuda()

                                    if lista_sorteio[item_da_lista]==1:
                                        retangulo_perto_selecionado_ajuda()

                                    if lista_sorteio[item_da_lista]==2:
                                        circulo_perto_selecionado_ajuda()

                                    if lista_sorteio[item_da_lista]==3:
                                        quadrado_perto_selecionado_ajuda()

                                if hud_switch==True:
                                    hud_info()
                                    #tela_update()

                                pygame.draw.circle(gameDisplay, (amarelo), jogador, 15)
                                tela_update()

                            ###############################
                            ##############TEMPO############
                            ###############################

                                if disparo_relogio==False:
                                    t0=int(time.time())
                                    disparo_relogio=True
                                t1=int(time.time())
                                tempo = int(t1-t0)
                                #print(tempo)

                            ##########################################################################
                            ##############SELEÇÃO DAS FIGURAS PELO JOGADOR DENTRO DO TEMPO############
                            ##########################################################################
                                if tempo<=tempo_ajuda:
                                    #print(lista_sorteio[item_da_lista])
                                    tempo_ajuda_switch=False
                                    jogador = posicao()


                                    if (jogador[0] > 0 and jogador[0] < 175) and (
                                            jogador[1] > 300 and jogador[1] < 400) and figura_selecionada==False:
                                        #print('triângulo')
                                        triangulo_perto_selecionado()
                                        som_triangulo()
                                        tela_update()
                                        delay()
                                        figura_selecionada=True

                                        if lista_sorteio[item_da_lista]==0:
                                            pontuacao=pontuacao+10
                                            feliz()
                                            som_feliz()
                                            tela_update()
                                            q_acertos=q_acertos+1
                                            delay()

                                        if lista_sorteio[item_da_lista]!=0:
                                            triste()
                                            som_triste()
                                            tela_update()
                                            q_erros=q_erros+1
                                            delay()

                                        item_da_lista=item_da_lista+1
                                        print('tentativa')
                                        print(tentativa)

                                        if item_da_lista == tamanho_sequencia_atual and tentativa == 1:
                                            lista_sorteio = []
                                            item_da_lista = 0
                                            tamanho_sequencia = tamanho_sequencia_atual
                                            disparo_relogio=False
                                            tentativa = 2

                                        if item_da_lista == tamanho_sequencia_atual and tentativa == 2:
                                            lista_sorteio = []
                                            item_da_lista = 0
                                            tamanho_sequencia = tamanho_sequencia_atual
                                            disparo_relogio = False
                                            tentativa = 3

                                        if item_da_lista==tamanho_sequencia_atual and tentativa==3:
                                            pontuacao_final = int((pontuacao / (tamanho_sequencia_atual * 30)) * 100)
                                            lista_sorteio = []
                                            item_da_lista = 0
                                            pontuacao=0
                                            tentativa=1

                                            print('pontuacao_final')
                                            print(pontuacao_final)


                                            if pontuacao_final>= 75:
                                                #tamanho_sequencia_atual=tamanho_sequencia_atual+1
                                                tamanho_sequencia=tamanho_sequencia_atual
                                                nivel_sequencia_atual=2
                                                nivel_sequencia=2
                                                fill_preto()
                                                trofeu_75()
                                                som_trofeu()
                                                tela_update()
                                                delay()
                                                delay()
                                                delay()
                                                delay()


                                            if pontuacao_final>=25 and pontuacao_final<75:
                                                tamanho_sequencia=tamanho_sequencia_atual
                                                fill_preto()
                                                trofeu_50()
                                                som_trofeu()
                                                tela_update()
                                                delay()
                                                delay()
                                                delay()
                                                delay()

                                            if pontuacao_final<25:
                                                if tamanho_sequencia_atual==1:
                                                    tamanho_sequencia=tamanho_sequencia_atual
                                                    fill_preto()
                                                    trofeu_25()
                                                    som_trofeu()
                                                    tela_update()
                                                    delay()
                                                    delay()
                                                    delay()
                                                    delay()

                                                if tamanho_sequencia_atual > 1:
                                                    tamanho_sequencia_atual=tamanho_sequencia_atual-1
                                                    tamanho_sequencia=tamanho_sequencia_atual
                                                    fill_preto()
                                                    trofeu_25()
                                                    som_trofeu()
                                                    tela_update()
                                                    delay()
                                                    delay()
                                                    delay()
                                                    delay()



                                            game_start=False
                                            figura_selecionada=False





                                    elif (jogador[0] > 175 and jogador[0] < 400) and (
                                            jogador[1] > 180 and jogador[1] < 300) and figura_selecionada==False:
                                        #print('retângulo')
                                        retangulo_perto_selecionado()
                                        som_retangulo()
                                        tela_update()
                                        delay()
                                        figura_selecionada = True
                                        if lista_sorteio[item_da_lista]==1:
                                            pontuacao=pontuacao+10
                                            feliz()
                                            som_feliz()
                                            tela_update()
                                            q_acertos = q_acertos + 1
                                            delay()

                                        if lista_sorteio[item_da_lista]!=1:
                                            triste()
                                            som_triste()
                                            tela_update()
                                            q_erros = q_erros + 1
                                            delay()

                                        item_da_lista=item_da_lista+1

                                        print('tentativa')
                                        print(tentativa)

                                        if item_da_lista == tamanho_sequencia_atual and tentativa == 1:
                                            lista_sorteio = []
                                            item_da_lista = 0
                                            tamanho_sequencia = tamanho_sequencia_atual
                                            disparo_relogio = False
                                            tentativa=2

                                        if item_da_lista == tamanho_sequencia_atual and tentativa == 2:
                                            lista_sorteio = []
                                            item_da_lista = 0
                                            tamanho_sequencia = tamanho_sequencia_atual
                                            disparo_relogio = False
                                            tentativa=3

                                        if item_da_lista==tamanho_sequencia_atual and tentativa==3:
                                            pontuacao_final = int((pontuacao / (tamanho_sequencia_atual * 30)) * 100)
                                            lista_sorteio = []
                                            item_da_lista = 0
                                            pontuacao=0
                                            tentativa=1

                                            print('pontuacao_final')
                                            print(pontuacao_final)


                                            if pontuacao_final>= 75:
                                                #tamanho_sequencia_atual=tamanho_sequencia_atual+1
                                                tamanho_sequencia=tamanho_sequencia_atual
                                                nivel_sequencia_atual=2
                                                nivel_sequencia=2
                                                fill_preto()
                                                trofeu_75()
                                                som_trofeu()
                                                tela_update()
                                                delay()
                                                delay()
                                                delay()
                                                delay()


                                            if pontuacao_final>=25 and pontuacao_final<75:
                                                tamanho_sequencia=tamanho_sequencia_atual
                                                fill_preto()
                                                trofeu_50()
                                                som_trofeu()
                                                tela_update()
                                                delay()
                                                delay()
                                                delay()
                                                delay()

                                            if pontuacao_final<25:
                                                if tamanho_sequencia_atual==1:
                                                    tamanho_sequencia=tamanho_sequencia_atual
                                                    fill_preto()
                                                    trofeu_25()
                                                    som_trofeu()
                                                    tela_update()
                                                    delay()
                                                    delay()
                                                    delay()
                                                    delay()

                                                if tamanho_sequencia_atual > 1:
                                                    tamanho_sequencia_atual=tamanho_sequencia_atual-1
                                                    tamanho_sequencia=tamanho_sequencia_atual
                                                    fill_preto()
                                                    trofeu_25()
                                                    som_trofeu()
                                                    tela_update()
                                                    delay()
                                                    delay()
                                                    delay()
                                                    delay()



                                            game_start=False
                                            figura_selecionada=False




                                    elif (jogador[0] > 400 and jogador[0] < 625) and (
                                            jogador[1] > 180 and jogador[1] < 300) and figura_selecionada==False:
                                        #print('círculo')
                                        circulo_perto_selecionado()
                                        som_circulo()
                                        tela_update()
                                        delay()
                                        figura_selecionada = True

                                        if lista_sorteio[item_da_lista]==2:
                                            pontuacao=pontuacao+10
                                            feliz()
                                            som_feliz()
                                            tela_update()
                                            q_acertos = q_acertos + 1
                                            delay()

                                        if lista_sorteio[item_da_lista]!=2:
                                            triste()
                                            som_triste()
                                            tela_update()
                                            q_erros = q_erros + 1
                                            delay()

                                        item_da_lista=item_da_lista+1

                                        print('tentativa')
                                        print(tentativa)

                                        if item_da_lista == tamanho_sequencia_atual and tentativa == 1:
                                            lista_sorteio = []
                                            item_da_lista = 0
                                            tamanho_sequencia = tamanho_sequencia_atual
                                            disparo_relogio = False
                                            tentativa=2

                                        if item_da_lista == tamanho_sequencia_atual and tentativa == 2:
                                            lista_sorteio = []
                                            item_da_lista = 0
                                            tamanho_sequencia = tamanho_sequencia_atual
                                            disparo_relogio = False
                                            tentativa=3

                                        if item_da_lista==tamanho_sequencia_atual and tentativa==3:
                                            pontuacao_final = int((pontuacao / (tamanho_sequencia_atual * 30)) * 100)
                                            lista_sorteio = []
                                            item_da_lista = 0
                                            pontuacao=0
                                            tentativa=1

                                            print('pontuacao_final')
                                            print(pontuacao_final)


                                            if pontuacao_final>= 75:
                                                #tamanho_sequencia_atual=tamanho_sequencia_atual+1
                                                tamanho_sequencia=tamanho_sequencia_atual
                                                nivel_sequencia_atual=2
                                                nivel_sequencia = 2
                                                fill_preto()
                                                trofeu_75()
                                                som_trofeu()
                                                tela_update()
                                                delay()
                                                delay()
                                                delay()
                                                delay()


                                            if pontuacao_final>=25 and pontuacao_final<75:
                                                tamanho_sequencia=tamanho_sequencia_atual
                                                fill_preto()
                                                trofeu_50()
                                                som_trofeu()
                                                tela_update()
                                                delay()
                                                delay()
                                                delay()
                                                delay()

                                            if pontuacao_final<25:
                                                if tamanho_sequencia_atual==1:
                                                    tamanho_sequencia=tamanho_sequencia_atual
                                                    fill_preto()
                                                    trofeu_25()
                                                    som_trofeu()
                                                    tela_update()
                                                    delay()
                                                    delay()
                                                    delay()
                                                    delay()

                                                if tamanho_sequencia_atual > 1:
                                                    tamanho_sequencia_atual=tamanho_sequencia_atual-1
                                                    tamanho_sequencia=tamanho_sequencia_atual
                                                    fill_preto()
                                                    trofeu_25()
                                                    som_trofeu()
                                                    tela_update()
                                                    delay()
                                                    delay()
                                                    delay()
                                                    delay()



                                            game_start=False
                                            figura_selecionada=False




                                    elif (jogador[0] > 625 and jogador[0] < 800) and (
                                            jogador[1] > 300 and jogador[1] < 400) and figura_selecionada==False:
                                        #print('quadrado')
                                        quadrado_perto_selecionado()
                                        som_quadrado()
                                        tela_update()
                                        delay()
                                        figura_selecionada = True

                                        if lista_sorteio[item_da_lista]==3:
                                            pontuacao=pontuacao+10
                                            feliz()
                                            som_feliz()
                                            tela_update()
                                            q_acertos = q_acertos + 1
                                            delay()

                                        if lista_sorteio[item_da_lista]!=3:
                                            triste()
                                            som_triste()
                                            tela_update()
                                            q_erros = q_erros + 1
                                            delay()

                                        item_da_lista=item_da_lista+1

                                        print('tentativa')
                                        print(tentativa)

                                        if item_da_lista==tamanho_sequencia_atual and tentativa==1:
                                            lista_sorteio =[]
                                            item_da_lista=0
                                            tamanho_sequencia = tamanho_sequencia_atual
                                            disparo_relogio = False
                                            tentativa = 2

                                        if item_da_lista==tamanho_sequencia_atual and tentativa==2:
                                            lista_sorteio = []
                                            item_da_lista = 0
                                            tamanho_sequencia = tamanho_sequencia_atual
                                            disparo_relogio = False
                                            tentativa = 3

                                        if item_da_lista==tamanho_sequencia_atual and tentativa==3:
                                            pontuacao_final = int((pontuacao / (tamanho_sequencia_atual * 30)) * 100)
                                            lista_sorteio = []
                                            item_da_lista = 0
                                            pontuacao=0
                                            tentativa=1

                                            print('pontuacao_final')
                                            print(pontuacao_final)


                                            if pontuacao_final>= 75:
                                                #tamanho_sequencia_atual=tamanho_sequencia_atual+1
                                                tamanho_sequencia=tamanho_sequencia_atual
                                                nivel_sequencia_atual=2
                                                nivel_sequencia = 2
                                                fill_preto()
                                                trofeu_75()
                                                som_trofeu()
                                                tela_update()
                                                delay()
                                                delay()
                                                delay()
                                                delay()


                                            if pontuacao_final>=25 and pontuacao_final<75:
                                                tamanho_sequencia=tamanho_sequencia_atual
                                                fill_preto()
                                                trofeu_50()
                                                som_trofeu()
                                                tela_update()
                                                delay()
                                                delay()
                                                delay()
                                                delay()

                                            if pontuacao_final<25:
                                                if tamanho_sequencia_atual==1:
                                                    tamanho_sequencia=tamanho_sequencia_atual
                                                    fill_preto()
                                                    trofeu_25()
                                                    som_trofeu()
                                                    tela_update()
                                                    delay()
                                                    delay()
                                                    delay()
                                                    delay()

                                                if tamanho_sequencia_atual > 1:
                                                    tamanho_sequencia_atual=tamanho_sequencia_atual-1
                                                    tamanho_sequencia=tamanho_sequencia_atual
                                                    fill_preto()
                                                    trofeu_25()
                                                    som_trofeu()
                                                    tela_update()
                                                    delay()
                                                    delay()
                                                    delay()
                                                    delay()



                                            game_start=False
                                            figura_selecionada=False



                                    elif (jogador[0] > 300 and jogador[0] < 500) and (
                                            jogador[1] > 400 and jogador[1] < 600):
                                        #print('base')
                                        #base_com_pe_verde()
                                        #tela_update()

                                        if figura_selecionada==True:
                                            disparo_relogio = False
                                            figura_selecionada = False


                                    else:
                                        print(tempo)
                                ##########################################################################
                                ##############SELEÇÃO DAS FIGURAS PELO JOGADOR DENTRO DA AJUDA ###########
                                ##########################################################################
                                if tempo> tempo_ajuda and tempo<=tempo_total:
                                    if tempo_ajuda_switch == False:
                                        som_ajuda()
                                        q_ajudas=q_ajudas+1
                                    tempo_ajuda_switch=True
                                    jogador = posicao()

                                    if (jogador[0] > 0 and jogador[0] < 175) and (
                                            jogador[1] > 300 and jogador[1] < 400) and figura_selecionada == False:
                                        # print('triângulo')
                                        triangulo_perto_selecionado()
                                        som_triangulo()
                                        tela_update()
                                        delay()
                                        figura_selecionada = True
                                        disparo_relogio=False
                                        tempo_ajuda_switch = False

                                        if lista_sorteio[item_da_lista] == 0:
                                            pontuacao = pontuacao + 5
                                            feliz()
                                            som_feliz()
                                            tela_update()
                                            q_acertos_com_ajuda = q_acertos_com_ajuda + 1
                                            delay()

                                        if lista_sorteio[item_da_lista] != 0:
                                            triste()
                                            som_triste()
                                            tela_update()
                                            q_erros = q_erros + 1
                                            delay()

                                        item_da_lista = item_da_lista + 1
                                        print('tentativa')
                                        print(tentativa)

                                        if item_da_lista==tamanho_sequencia_atual and tentativa==1:
                                            lista_sorteio =[]
                                            item_da_lista=0
                                            tamanho_sequencia = tamanho_sequencia_atual
                                            disparo_relogio = False
                                            tentativa = 2

                                        if item_da_lista==tamanho_sequencia_atual and tentativa==2:
                                            lista_sorteio = []
                                            item_da_lista = 0
                                            tamanho_sequencia = tamanho_sequencia_atual
                                            disparo_relogio = False
                                            tentativa = 3

                                        if item_da_lista == tamanho_sequencia_atual and tentativa==3:
                                            pontuacao_final = int(
                                                (pontuacao / (tamanho_sequencia_atual * 30)) * 100)
                                            lista_sorteio = []
                                            item_da_lista = 0
                                            pontuacao = 0
                                            tentativa = 1

                                            print('pontuacao_final')
                                            print(pontuacao_final)

                                            if pontuacao_final >= 75:
                                                #tamanho_sequencia_atual = tamanho_sequencia_atual + 1
                                                tamanho_sequencia = tamanho_sequencia_atual
                                                nivel_sequencia_atual=2
                                                nivel_sequencia = 2
                                                fill_preto()
                                                trofeu_75()
                                                som_trofeu()
                                                tela_update()
                                                delay()
                                                delay()
                                                delay()
                                                delay()
                                                nivel_sequencia = 2

                                            if pontuacao_final >= 25 and pontuacao_final < 75:
                                                tamanho_sequencia = tamanho_sequencia_atual
                                                fill_preto()
                                                trofeu_50()
                                                som_trofeu()
                                                tela_update()
                                                delay()
                                                delay()
                                                delay()
                                                delay()

                                            if pontuacao_final < 25:
                                                if tamanho_sequencia_atual == 1:
                                                    tamanho_sequencia = tamanho_sequencia_atual
                                                    fill_preto()
                                                    trofeu_25()
                                                    som_trofeu()
                                                    tela_update()
                                                    delay()
                                                    delay()
                                                    delay()
                                                    delay()

                                                if tamanho_sequencia_atual > 1:
                                                    tamanho_sequencia_atual = tamanho_sequencia_atual - 1
                                                    tamanho_sequencia = tamanho_sequencia_atual
                                                    fill_preto()
                                                    trofeu_25()
                                                    som_trofeu()
                                                    tela_update()
                                                    delay()
                                                    delay()
                                                    delay()
                                                    delay()

                                            game_start = False
                                            figura_selecionada = False





                                    elif (jogador[0] > 175 and jogador[0] < 400) and (
                                            jogador[1] > 180 and jogador[1] < 300) and figura_selecionada == False:
                                        # print('retângulo')
                                        retangulo_perto_selecionado()
                                        som_retangulo()
                                        tela_update()
                                        delay()
                                        figura_selecionada = True
                                        disparo_relogio = False
                                        tempo_ajuda_switch = False

                                        if lista_sorteio[item_da_lista] == 1:
                                            pontuacao = pontuacao + 5
                                            feliz()
                                            som_feliz()
                                            tela_update()
                                            q_acertos_com_ajuda = q_acertos_com_ajuda + 1
                                            delay()

                                        if lista_sorteio[item_da_lista] != 1:
                                            triste()
                                            som_triste()
                                            tela_update()
                                            q_erros = q_erros + 1
                                            delay()

                                        item_da_lista = item_da_lista + 1
                                        print('tentativa')
                                        print(tentativa)

                                        if item_da_lista==tamanho_sequencia_atual and tentativa==1:
                                            lista_sorteio =[]
                                            item_da_lista=0
                                            tamanho_sequencia = tamanho_sequencia_atual
                                            disparo_relogio = False
                                            tentativa = 2

                                        if item_da_lista==tamanho_sequencia_atual and tentativa==2:
                                            lista_sorteio = []
                                            item_da_lista = 0
                                            tamanho_sequencia = tamanho_sequencia_atual
                                            disparo_relogio = False
                                            tentativa = 3

                                        if item_da_lista == tamanho_sequencia_atual and tentativa==3:
                                            pontuacao_final = int(
                                                (pontuacao / (tamanho_sequencia_atual * 30)) * 100)
                                            lista_sorteio = []
                                            item_da_lista = 0
                                            pontuacao = 0
                                            tentativa = 1

                                            print('pontuacao_final')
                                            print(pontuacao_final)

                                            if pontuacao_final >= 75:
                                                #tamanho_sequencia_atual = tamanho_sequencia_atual + 1
                                                tamanho_sequencia = tamanho_sequencia_atual
                                                nivel_sequencia_atual = 2
                                                nivel_sequencia = 2
                                                fill_preto()
                                                trofeu_75()
                                                som_trofeu()
                                                tela_update()
                                                delay()
                                                delay()
                                                delay()
                                                delay()
                                                nivel_sequencia = 2

                                            if pontuacao_final >= 25 and pontuacao_final < 75:
                                                tamanho_sequencia = tamanho_sequencia_atual
                                                fill_preto()
                                                trofeu_50()
                                                som_trofeu()
                                                tela_update()
                                                delay()
                                                delay()
                                                delay()
                                                delay()

                                            if pontuacao_final < 25:
                                                if tamanho_sequencia_atual == 1:
                                                    tamanho_sequencia = tamanho_sequencia_atual
                                                    fill_preto()
                                                    trofeu_25()
                                                    som_trofeu()
                                                    tela_update()
                                                    delay()
                                                    delay()
                                                    delay()
                                                    delay()

                                                if tamanho_sequencia_atual > 1:
                                                    tamanho_sequencia_atual = tamanho_sequencia_atual - 1
                                                    tamanho_sequencia = tamanho_sequencia_atual
                                                    fill_preto()
                                                    trofeu_25()
                                                    som_trofeu()
                                                    tela_update()
                                                    delay()
                                                    delay()
                                                    delay()
                                                    delay()

                                            game_start = False
                                            figura_selecionada = False




                                    elif (jogador[0] > 400 and jogador[0] < 625) and (
                                            jogador[1] > 180 and jogador[1] < 300) and figura_selecionada == False:
                                        # print('círculo')
                                        circulo_perto_selecionado()
                                        som_circulo()
                                        tela_update()
                                        delay()
                                        figura_selecionada = True
                                        disparo_relogio = False
                                        tempo_ajuda_switch = False

                                        if lista_sorteio[item_da_lista] == 2:
                                            pontuacao = pontuacao + 5
                                            feliz()
                                            som_feliz()
                                            tela_update()
                                            q_acertos_com_ajuda = q_acertos_com_ajuda + 1
                                            delay()

                                        if lista_sorteio[item_da_lista] != 2:
                                            triste()
                                            som_triste()
                                            tela_update()
                                            q_erros = q_erros + 1
                                            delay()

                                        item_da_lista = item_da_lista + 1
                                        print('tentativa')
                                        print(tentativa)

                                        if item_da_lista==tamanho_sequencia_atual and tentativa==1:
                                            lista_sorteio =[]
                                            item_da_lista=0
                                            tamanho_sequencia = tamanho_sequencia_atual
                                            disparo_relogio = False
                                            tentativa = 2

                                        if item_da_lista==tamanho_sequencia_atual and tentativa==2:
                                            lista_sorteio = []
                                            item_da_lista = 0
                                            tamanho_sequencia = tamanho_sequencia_atual
                                            disparo_relogio = False
                                            tentativa = 3

                                        if item_da_lista == tamanho_sequencia_atual and tentativa==3:
                                            pontuacao_final = int(
                                                (pontuacao / (tamanho_sequencia_atual * 30)) * 100)
                                            lista_sorteio = []
                                            item_da_lista = 0
                                            pontuacao = 0
                                            tentativa = 1

                                            print('pontuacao_final')
                                            print(pontuacao_final)

                                            if pontuacao_final >= 75:
                                                #tamanho_sequencia_atual = tamanho_sequencia_atual + 1
                                                tamanho_sequencia = tamanho_sequencia_atual
                                                nivel_sequencia_atual = 2
                                                nivel_sequencia = 2
                                                fill_preto()
                                                trofeu_75()
                                                som_trofeu()
                                                tela_update()
                                                delay()
                                                delay()
                                                delay()
                                                delay()
                                                nivel_sequencia = 2

                                            if pontuacao_final >= 25 and pontuacao_final < 75:
                                                tamanho_sequencia = tamanho_sequencia_atual
                                                fill_preto()
                                                trofeu_50()
                                                som_trofeu()
                                                tela_update()
                                                delay()
                                                delay()
                                                delay()
                                                delay()

                                            if pontuacao_final < 25:
                                                if tamanho_sequencia_atual == 1:
                                                    tamanho_sequencia = tamanho_sequencia_atual
                                                    fill_preto()
                                                    trofeu_25()
                                                    som_trofeu()
                                                    tela_update()
                                                    delay()
                                                    delay()
                                                    delay()
                                                    delay()

                                                if tamanho_sequencia_atual > 1:
                                                    tamanho_sequencia_atual = tamanho_sequencia_atual - 1
                                                    tamanho_sequencia = tamanho_sequencia_atual
                                                    fill_preto()
                                                    trofeu_25()
                                                    som_trofeu()
                                                    tela_update()
                                                    delay()
                                                    delay()
                                                    delay()
                                                    delay()

                                            game_start = False
                                            figura_selecionada = False




                                    elif (jogador[0] > 625 and jogador[0] < 800) and (
                                            jogador[1] > 300 and jogador[1] < 400) and figura_selecionada == False:
                                        # print('quadrado')
                                        quadrado_perto_selecionado()
                                        som_quadrado()
                                        tela_update()
                                        delay()
                                        figura_selecionada = True
                                        disparo_relogio = False
                                        tempo_ajuda_switch = False

                                        if lista_sorteio[item_da_lista] == 3:
                                            pontuacao = pontuacao + 5
                                            feliz()
                                            som_feliz()
                                            tela_update()
                                            q_acertos_com_ajuda = q_acertos_com_ajuda + 1
                                            delay()

                                        if lista_sorteio[item_da_lista] != 3:
                                            triste()
                                            som_triste()
                                            tela_update()
                                            q_erros = q_erros + 1
                                            delay()

                                        item_da_lista = item_da_lista + 1
                                        print('tentativa')
                                        print(tentativa)

                                        if item_da_lista==tamanho_sequencia_atual and tentativa==1:
                                            lista_sorteio =[]
                                            item_da_lista=0
                                            tamanho_sequencia = tamanho_sequencia_atual
                                            disparo_relogio = False
                                            tentativa = 2

                                        if item_da_lista==tamanho_sequencia_atual and tentativa==2:
                                            lista_sorteio = []
                                            item_da_lista = 0
                                            tamanho_sequencia = tamanho_sequencia_atual
                                            disparo_relogio = False
                                            tentativa = 3

                                        if item_da_lista == tamanho_sequencia_atual and tentativa==3:
                                            pontuacao_final = int(
                                                (pontuacao / (tamanho_sequencia_atual * 30)) * 100)
                                            lista_sorteio = []
                                            item_da_lista = 0
                                            pontuacao = 0
                                            tentativa = 1

                                            print('pontuacao_final')
                                            print(pontuacao_final)

                                            if pontuacao_final >= 75:
                                                #tamanho_sequencia_atual = tamanho_sequencia_atual + 1
                                                tamanho_sequencia = tamanho_sequencia_atual
                                                nivel_sequencia_atual = 2
                                                nivel_sequencia = 2
                                                fill_preto()
                                                trofeu_75()
                                                som_trofeu()
                                                tela_update()
                                                delay()
                                                delay()
                                                delay()
                                                delay()
                                                nivel_sequencia = 2

                                            if pontuacao_final >= 25 and pontuacao_final < 75:
                                                tamanho_sequencia = tamanho_sequencia_atual
                                                fill_preto()
                                                trofeu_50()
                                                som_trofeu()
                                                tela_update()
                                                delay()
                                                delay()
                                                delay()
                                                delay()

                                            if pontuacao_final < 25:
                                                if tamanho_sequencia_atual == 1:
                                                    tamanho_sequencia = tamanho_sequencia_atual
                                                    nivel_sequencia_atual=1
                                                    nivel_sequencia=1
                                                    fill_preto()
                                                    trofeu_25()
                                                    som_trofeu()
                                                    tela_update()
                                                    delay()
                                                    delay()
                                                    delay()
                                                    delay()

                                                if tamanho_sequencia_atual > 1:
                                                    tamanho_sequencia_atual = tamanho_sequencia_atual - 1
                                                    tamanho_sequencia = tamanho_sequencia_atual
                                                    nivel_sequencia_atual = 1
                                                    nivel_sequencia = 1
                                                    fill_preto()
                                                    trofeu_25()
                                                    som_trofeu()
                                                    tela_update()
                                                    delay()
                                                    delay()
                                                    delay()
                                                    delay()

                                            game_start = False
                                            figura_selecionada = False



                                    elif (jogador[0] > 300 and jogador[0] < 500) and (
                                            jogador[1] > 400 and jogador[1] < 600):
                                        # print('base')
                                        # base_com_pe_verde()
                                        # tela_update()

                                        if figura_selecionada == True:
                                            disparo_relogio = False
                                            figura_selecionada = False


                                    else:
                                        print(tempo)
                                        #tela_update()



                                    #disparo_relogio=False
                                ##########################################################################
                                ########################### OMISSÃO PELO JOGADOR #########################
                                ##########################################################################

                                if tempo>tempo_total:
                                    fill_preto()
                                    tempo_max()
                                    som_triste()
                                    tela_update()
                                    delay()
                                    delay()
                                    delay()
                                    delay()
                                    delay()
                                    tamanho_sequencia=tamanho_sequencia_atual
                                    nivel_sequencia_atual=1
                                    nivel_sequencia=1
                                    lista_sorteio=[]
                                    item_da_lista=0
                                    tentativa=1
                                    q_omissao=q_omissao+1
                                    disparo_relogio=False
                                    tempo_ajuda_switch = False
                                    game_start=False

                        #################################################################################
                        #################################################################################
                        ##################### Jogador posicionado e inicio de sequencia# ################
                        #################################################################################
                        ###################################### LONGE ####################################
                        #################################################################################
                        #################################################################################

                        elif nivel_sequencia==2 and pausa_switch==False: # NIVEL LONGE:

                            ##########################
                            ####SORTEIO DA JOGADA#####
                            ##########################
                            if tamanho_sequencia > 0:
                                sorteio_longe()
                                tamanho_sequencia = tamanho_sequencia - 1
                                if tamanho_sequencia <= 0:
                                    sinal_de_vez = True

                            ###########################
                            #######VEZ DO JOGADOR######
                            ###########################
                            else:

                                if sinal_de_vez==True:
                                    vez_do_jogador_longe()
                                    sinal_de_vez=False
                                    disparo_relogio = False
                                    item_da_lista=0
                                base_sem_pe()

                                if figura_selecionada == True:
                                    base_com_pe_verde()

                                if tempo_ajuda_switch == False:
                                    silhueta_longe()

                                if tempo_ajuda_switch == True:
                                    if lista_sorteio[item_da_lista] == 0:
                                        triangulo_longe_selecionado_ajuda()

                                    if lista_sorteio[item_da_lista] == 1:
                                        retangulo_longe_selecionado_ajuda()

                                    if lista_sorteio[item_da_lista] == 2:
                                        circulo_longe_selecionado_ajuda()

                                    if lista_sorteio[item_da_lista] == 3:
                                        quadrado_longe_selecionado_ajuda()

                                if hud_switch == True:
                                    hud_info()
                                    #tela_update()

                                pygame.draw.circle(gameDisplay, (amarelo), jogador, 15)
                                tela_update()

                            ###############################
                            ##############TEMPO############
                            ###############################

                                if disparo_relogio==False:
                                    t0=int(time.time())
                                    disparo_relogio=True
                                t1=int(time.time())
                                tempo = int(t1-t0)
                                #print(tempo)

                            ##########################################################################
                            ##############SELEÇÃO DAS FIGURAS PELO JOGADOR DENTRO DO TEMPO############
                            ##########################################################################
                                if tempo <= tempo_ajuda:
                                    # print(lista_sorteio[item_da_lista])
                                    tempo_ajuda_switch = False
                                    jogador = posicao()

                                    if (jogador[0] > 0 and jogador[0] < 175) and (
                                            jogador[1] > 125 and jogador[1] < 240) and figura_selecionada == False:
                                        # print('triângulo')
                                        triangulo_longe_selecionado()
                                        som_triangulo()
                                        tela_update()
                                        delay()
                                        figura_selecionada = True

                                        if lista_sorteio[item_da_lista] == 0:
                                            pontuacao = pontuacao + 10
                                            feliz()
                                            som_feliz()
                                            tela_update()
                                            q_acertos = q_acertos + 1
                                            delay()

                                        if lista_sorteio[item_da_lista] != 0:
                                            triste()
                                            som_triste()
                                            tela_update()
                                            q_erros = q_erros + 1
                                            delay()

                                        item_da_lista = item_da_lista + 1
                                        print('tentativa')
                                        print(tentativa)

                                        if item_da_lista == tamanho_sequencia_atual and tentativa == 1:
                                            lista_sorteio = []
                                            item_da_lista = 0
                                            tamanho_sequencia = tamanho_sequencia_atual
                                            disparo_relogio = False
                                            tentativa = 2

                                        if item_da_lista == tamanho_sequencia_atual and tentativa == 2:
                                            lista_sorteio = []
                                            item_da_lista = 0
                                            tamanho_sequencia = tamanho_sequencia_atual
                                            disparo_relogio = False
                                            tentativa = 3

                                        if item_da_lista == tamanho_sequencia_atual and tentativa == 3:
                                            pontuacao_final = int((pontuacao / (tamanho_sequencia_atual * 30)) * 100)
                                            lista_sorteio = []
                                            item_da_lista = 0
                                            pontuacao = 0
                                            tentativa = 1

                                            print('pontuacao_final')
                                            print(pontuacao_final)

                                            if pontuacao_final >= 75:
                                                tamanho_sequencia_atual=tamanho_sequencia_atual+1
                                                tamanho_sequencia = tamanho_sequencia_atual
                                                nivel_sequencia_atual = 1
                                                nivel_sequencia = 1
                                                fill_preto()
                                                trofeu_75()
                                                som_trofeu()
                                                tela_update()
                                                delay()
                                                delay()
                                                delay()
                                                delay()


                                            if pontuacao_final >= 25 and pontuacao_final < 75:
                                                tamanho_sequencia = tamanho_sequencia_atual
                                                nivel_sequencia = 2
                                                fill_preto()
                                                trofeu_50()
                                                som_trofeu()
                                                tela_update()
                                                delay()
                                                delay()
                                                delay()
                                                delay()

                                            if pontuacao_final < 25:
                                                if tamanho_sequencia_atual == 1:
                                                    tamanho_sequencia = tamanho_sequencia_atual
                                                    nivel_sequencia_atual = 1
                                                    nivel_sequencia = 1
                                                    fill_preto()
                                                    trofeu_25()
                                                    som_trofeu()
                                                    tela_update()
                                                    delay()
                                                    delay()
                                                    delay()
                                                    delay()

                                                if tamanho_sequencia_atual > 1:
                                                    tamanho_sequencia_atual = tamanho_sequencia_atual - 1
                                                    tamanho_sequencia = tamanho_sequencia_atual
                                                    nivel_sequencia_atual = 2
                                                    nivel_sequencia = 2
                                                    fill_preto()
                                                    trofeu_25()
                                                    som_trofeu()
                                                    tela_update()
                                                    delay()
                                                    delay()
                                                    delay()
                                                    delay()

                                            game_start = False
                                            figura_selecionada = False





                                    elif (jogador[0] > 175 and jogador[0] < 400) and (
                                            jogador[1] > 0 and jogador[1] < 125) and figura_selecionada == False:
                                        # print('retângulo')
                                        retangulo_longe_selecionado()
                                        som_retangulo()
                                        tela_update()
                                        delay()
                                        figura_selecionada = True
                                        if lista_sorteio[item_da_lista] == 1:
                                            pontuacao = pontuacao + 10
                                            feliz()
                                            som_feliz()
                                            tela_update()
                                            q_acertos = q_acertos + 1
                                            delay()

                                        if lista_sorteio[item_da_lista] != 1:
                                            triste()
                                            som_triste()
                                            tela_update()
                                            q_erros = q_erros + 1
                                            delay()

                                        item_da_lista = item_da_lista + 1

                                        print('tentativa')
                                        print(tentativa)

                                        if item_da_lista == tamanho_sequencia_atual and tentativa == 1:
                                            lista_sorteio = []
                                            item_da_lista = 0
                                            tamanho_sequencia = tamanho_sequencia_atual
                                            disparo_relogio = False
                                            tentativa = 2

                                        if item_da_lista == tamanho_sequencia_atual and tentativa == 2:
                                            lista_sorteio = []
                                            item_da_lista = 0
                                            tamanho_sequencia = tamanho_sequencia_atual
                                            disparo_relogio = False
                                            tentativa = 3

                                        if item_da_lista == tamanho_sequencia_atual and tentativa == 3:
                                            pontuacao_final = int((pontuacao / (tamanho_sequencia_atual * 30)) * 100)
                                            lista_sorteio = []
                                            item_da_lista = 0
                                            pontuacao = 0
                                            tentativa = 1

                                            print('pontuacao_final')
                                            print(pontuacao_final)

                                            if pontuacao_final >= 75:
                                                tamanho_sequencia_atual=tamanho_sequencia_atual+1
                                                tamanho_sequencia = tamanho_sequencia_atual
                                                nivel_sequencia_atual = 1
                                                nivel_sequencia = 1
                                                fill_preto()
                                                trofeu_75()
                                                som_trofeu()
                                                tela_update()
                                                delay()
                                                delay()
                                                delay()
                                                delay()


                                            if pontuacao_final >= 25 and pontuacao_final < 75:
                                                tamanho_sequencia = tamanho_sequencia_atual
                                                nivel_sequencia_atual=2
                                                nivel_sequencia=2
                                                fill_preto()
                                                trofeu_50()
                                                som_trofeu()
                                                tela_update()
                                                delay()
                                                delay()
                                                delay()
                                                delay()

                                            if pontuacao_final < 25:
                                                if tamanho_sequencia_atual == 1:
                                                    tamanho_sequencia = tamanho_sequencia_atual
                                                    nivel_sequencia_atual=1
                                                    nivel_sequencia=1
                                                    fill_preto()
                                                    trofeu_25()
                                                    som_trofeu()
                                                    tela_update()
                                                    delay()
                                                    delay()
                                                    delay()
                                                    delay()

                                                if tamanho_sequencia_atual > 1:
                                                    tamanho_sequencia_atual = tamanho_sequencia_atual
                                                    tamanho_sequencia = tamanho_sequencia_atual
                                                    nivel_sequencia_atual=2
                                                    nivel_sequencia=2
                                                    fill_preto()
                                                    trofeu_25()
                                                    som_trofeu()
                                                    tela_update()
                                                    delay()
                                                    delay()
                                                    delay()
                                                    delay()

                                            game_start = False
                                            figura_selecionada = False




                                    elif (jogador[0] > 400 and jogador[0] < 625) and (
                                            jogador[1] > 0 and jogador[1] < 150) and figura_selecionada == False:
                                        # print('círculo')
                                        circulo_longe_selecionado()
                                        som_circulo()
                                        tela_update()
                                        delay()
                                        figura_selecionada = True

                                        if lista_sorteio[item_da_lista] == 2:
                                            pontuacao = pontuacao + 10
                                            feliz()
                                            som_feliz()
                                            tela_update()
                                            q_acertos = q_acertos + 1
                                            delay()

                                        if lista_sorteio[item_da_lista] != 2:
                                            triste()
                                            som_triste()
                                            tela_update()
                                            q_erros = q_erros + 1
                                            delay()

                                        item_da_lista = item_da_lista + 1

                                        print('tentativa')
                                        print(tentativa)

                                        if item_da_lista == tamanho_sequencia_atual and tentativa == 1:
                                            lista_sorteio = []
                                            item_da_lista = 0
                                            tamanho_sequencia = tamanho_sequencia_atual
                                            disparo_relogio = False
                                            tentativa = 2

                                        if item_da_lista == tamanho_sequencia_atual and tentativa == 2:
                                            lista_sorteio = []
                                            item_da_lista = 0
                                            tamanho_sequencia = tamanho_sequencia_atual
                                            disparo_relogio = False
                                            tentativa = 3

                                        if item_da_lista == tamanho_sequencia_atual and tentativa == 3:
                                            pontuacao_final = int((pontuacao / (tamanho_sequencia_atual * 30)) * 100)
                                            lista_sorteio = []
                                            item_da_lista = 0
                                            pontuacao = 0
                                            tentativa = 1

                                            print('pontuacao_final')
                                            print(pontuacao_final)

                                            if pontuacao_final >= 75:
                                                tamanho_sequencia_atual=tamanho_sequencia_atual+1
                                                tamanho_sequencia = tamanho_sequencia_atual
                                                nivel_sequencia_atual = 1
                                                nivel_sequencia = 1
                                                fill_preto()
                                                trofeu_75()
                                                som_trofeu()
                                                tela_update()
                                                delay()
                                                delay()
                                                delay()
                                                delay()


                                            if pontuacao_final >= 25 and pontuacao_final < 75:
                                                tamanho_sequencia = tamanho_sequencia_atual
                                                nivel_sequencia_atual=2
                                                nivel_sequencia=2
                                                fill_preto()
                                                trofeu_50()
                                                som_trofeu()
                                                tela_update()
                                                delay()
                                                delay()
                                                delay()
                                                delay()

                                            if pontuacao_final < 25:
                                                if tamanho_sequencia_atual == 1:
                                                    tamanho_sequencia = tamanho_sequencia_atual
                                                    nivel_sequencia_atual=1
                                                    nivel_sequencia=1
                                                    fill_preto()
                                                    trofeu_25()
                                                    som_trofeu()
                                                    tela_update()
                                                    delay()
                                                    delay()
                                                    delay()
                                                    delay()

                                                if tamanho_sequencia_atual > 1:
                                                    tamanho_sequencia_atual = tamanho_sequencia_atual - 1
                                                    tamanho_sequencia = tamanho_sequencia_atual
                                                    nivel_sequencia_atual=2
                                                    nivel_sequencia=2
                                                    fill_preto()
                                                    trofeu_25()
                                                    som_trofeu()
                                                    tela_update()
                                                    delay()
                                                    delay()
                                                    delay()
                                                    delay()

                                            game_start = False
                                            figura_selecionada = False




                                    elif (jogador[0] > 625 and jogador[0] < 800) and (
                                            jogador[1] > 125 and jogador[1] < 240) and figura_selecionada == False:
                                        # print('quadrado')
                                        quadrado_longe_selecionado()
                                        som_quadrado()
                                        tela_update()
                                        delay()
                                        figura_selecionada = True

                                        if lista_sorteio[item_da_lista] == 3:
                                            pontuacao = pontuacao + 10
                                            feliz()
                                            som_feliz()
                                            tela_update()
                                            q_acertos = q_acertos + 1
                                            delay()

                                        if lista_sorteio[item_da_lista] != 3:
                                            triste()
                                            som_triste()
                                            tela_update()
                                            q_erros = q_erros + 1
                                            delay()

                                        item_da_lista = item_da_lista + 1

                                        print('tentativa')
                                        print(tentativa)

                                        if item_da_lista == tamanho_sequencia_atual and tentativa == 1:
                                            lista_sorteio = []
                                            item_da_lista = 0
                                            tamanho_sequencia = tamanho_sequencia_atual
                                            disparo_relogio = False
                                            tentativa = 2

                                        if item_da_lista == tamanho_sequencia_atual and tentativa == 2:
                                            lista_sorteio = []
                                            item_da_lista = 0
                                            tamanho_sequencia = tamanho_sequencia_atual
                                            disparo_relogio = False
                                            tentativa = 3

                                        if item_da_lista == tamanho_sequencia_atual and tentativa == 3:
                                            pontuacao_final = int((pontuacao / (tamanho_sequencia_atual * 30)) * 100)
                                            lista_sorteio = []
                                            item_da_lista = 0
                                            pontuacao = 0
                                            tentativa = 1

                                            print('pontuacao_final')
                                            print(pontuacao_final)

                                            if pontuacao_final >= 75:
                                                tamanho_sequencia_atual=tamanho_sequencia_atual+1
                                                tamanho_sequencia = tamanho_sequencia_atual
                                                nivel_sequencia_atual = 1
                                                nivel_sequencia = 1
                                                fill_preto()
                                                trofeu_75()
                                                som_trofeu()
                                                tela_update()
                                                delay()
                                                delay()
                                                delay()
                                                delay()


                                            if pontuacao_final >= 25 and pontuacao_final < 75:
                                                tamanho_sequencia = tamanho_sequencia_atual
                                                nivel_sequencia_atual=2
                                                nivel_sequencia=2
                                                fill_preto()
                                                trofeu_50()
                                                som_trofeu()
                                                tela_update()
                                                delay()
                                                delay()
                                                delay()
                                                delay()

                                            if pontuacao_final < 25:
                                                if tamanho_sequencia_atual == 1:
                                                    tamanho_sequencia = tamanho_sequencia_atual
                                                    nivel_sequencia_atual=1
                                                    nivel_sequencia=1
                                                    fill_preto()
                                                    trofeu_25()
                                                    som_trofeu()
                                                    tela_update()
                                                    delay()
                                                    delay()
                                                    delay()
                                                    delay()

                                                if tamanho_sequencia_atual > 1:
                                                    tamanho_sequencia_atual = tamanho_sequencia_atual - 1
                                                    tamanho_sequencia = tamanho_sequencia_atual
                                                    nivel_sequencia_atual=2
                                                    nivel_sequencia=2
                                                    fill_preto()
                                                    trofeu_25()
                                                    som_trofeu()
                                                    tela_update()
                                                    delay()
                                                    delay()
                                                    delay()
                                                    delay()

                                            game_start = False
                                            figura_selecionada = False



                                    elif (jogador[0] > 300 and jogador[0] < 500) and (
                                            jogador[1] > 400 and jogador[1] < 600):
                                        # print('base')
                                        # base_com_pe_verde()
                                        # tela_update()

                                        if figura_selecionada == True:
                                            disparo_relogio = False
                                            figura_selecionada = False


                                    else:
                                        print(tempo)
                                ##########################################################################
                                ##############SELEÇÃO DAS FIGURAS PELO JOGADOR DENTRO DA AJUDA ###########
                                ##########################################################################
                                if tempo > tempo_ajuda and tempo <= tempo_total:
                                    if tempo_ajuda_switch==False:
                                        som_ajuda()
                                        q_ajudas = q_ajudas + 1
                                    tempo_ajuda_switch = True
                                    jogador = posicao()

                                    if (jogador[0] > 0 and jogador[0] < 175) and (
                                            jogador[1] > 125 and jogador[1] < 240) and figura_selecionada == False:
                                        # print('triângulo')
                                        triangulo_longe_selecionado()
                                        som_triangulo()
                                        tela_update()
                                        delay()
                                        figura_selecionada = True
                                        disparo_relogio = False
                                        tempo_ajuda_switch = False

                                        if lista_sorteio[item_da_lista] == 0:
                                            pontuacao = pontuacao + 5
                                            feliz()
                                            som_feliz()
                                            tela_update()
                                            q_acertos_com_ajuda = q_acertos_com_ajuda + 1
                                            delay()

                                        if lista_sorteio[item_da_lista] != 0:
                                            triste()
                                            som_triste()
                                            tela_update()
                                            q_erros = q_erros + 1
                                            delay()

                                        item_da_lista = item_da_lista + 1
                                        print('tentativa')
                                        print(tentativa)

                                        if item_da_lista == tamanho_sequencia_atual and tentativa == 1:
                                            lista_sorteio = []
                                            item_da_lista = 0
                                            tamanho_sequencia = tamanho_sequencia_atual
                                            disparo_relogio = False
                                            tentativa = 2

                                        if item_da_lista == tamanho_sequencia_atual and tentativa == 2:
                                            lista_sorteio = []
                                            item_da_lista = 0
                                            tamanho_sequencia = tamanho_sequencia_atual
                                            disparo_relogio = False
                                            tentativa = 3

                                        if item_da_lista == tamanho_sequencia_atual and tentativa == 3:
                                            pontuacao_final = int(
                                                (pontuacao / (tamanho_sequencia_atual * 30)) * 100)
                                            lista_sorteio = []
                                            item_da_lista = 0
                                            pontuacao = 0
                                            tentativa = 1

                                            print('pontuacao_final')
                                            print(pontuacao_final)

                                            if pontuacao_final >= 75:
                                                tamanho_sequencia_atual = tamanho_sequencia_atual + 1
                                                tamanho_sequencia = tamanho_sequencia_atual
                                                nivel_sequencia_atual=1
                                                nivel_sequencia=1
                                                fill_preto()
                                                trofeu_75()
                                                som_trofeu()
                                                tela_update()
                                                delay()
                                                delay()
                                                delay()
                                                delay()


                                            if pontuacao_final >= 25 and pontuacao_final < 75:
                                                tamanho_sequencia = tamanho_sequencia_atual
                                                nivel_sequencia_atual=2
                                                nivel_sequencia=2
                                                fill_preto()
                                                trofeu_50()
                                                som_trofeu()
                                                tela_update()
                                                delay()
                                                delay()
                                                delay()
                                                delay()

                                            if pontuacao_final < 25:
                                                if tamanho_sequencia_atual == 1:
                                                    tamanho_sequencia = tamanho_sequencia_atual
                                                    nivel_sequencia_atual=1
                                                    nivel_sequencia=1
                                                    fill_preto()
                                                    trofeu_25()
                                                    som_trofeu()
                                                    tela_update()
                                                    delay()
                                                    delay()
                                                    delay()
                                                    delay()

                                                if tamanho_sequencia_atual > 1:
                                                    tamanho_sequencia_atual = tamanho_sequencia_atual - 1
                                                    tamanho_sequencia = tamanho_sequencia_atual
                                                    nivel_sequencia_atual=2
                                                    nivel_sequencia=2
                                                    fill_preto()
                                                    trofeu_25()
                                                    som_trofeu()
                                                    tela_update()
                                                    delay()
                                                    delay()
                                                    delay()
                                                    delay()

                                            game_start = False
                                            figura_selecionada = False





                                    elif (jogador[0] > 175 and jogador[0] < 400) and (
                                            jogador[1] > 0 and jogador[1] < 125) and figura_selecionada == False:
                                        # print('retângulo')
                                        retangulo_longe_selecionado()
                                        som_retangulo()
                                        tela_update()
                                        delay()
                                        figura_selecionada = True
                                        disparo_relogio = False
                                        tempo_ajuda_switch = False

                                        if lista_sorteio[item_da_lista] == 1:
                                            pontuacao = pontuacao + 5
                                            feliz()
                                            som_feliz()
                                            tela_update()
                                            q_acertos_com_ajuda = q_acertos_com_ajuda + 1
                                            delay()

                                        if lista_sorteio[item_da_lista] != 1:
                                            triste()
                                            som_triste()
                                            tela_update()
                                            q_erros = q_erros + 1
                                            delay()

                                        item_da_lista = item_da_lista + 1
                                        print('tentativa')
                                        print(tentativa)

                                        if item_da_lista == tamanho_sequencia_atual and tentativa == 1:
                                            lista_sorteio = []
                                            item_da_lista = 0
                                            tamanho_sequencia = tamanho_sequencia_atual
                                            disparo_relogio = False
                                            tentativa = 2

                                        if item_da_lista == tamanho_sequencia_atual and tentativa == 2:
                                            lista_sorteio = []
                                            item_da_lista = 0
                                            tamanho_sequencia = tamanho_sequencia_atual
                                            disparo_relogio = False
                                            tentativa = 3

                                        if item_da_lista == tamanho_sequencia_atual and tentativa == 3:
                                            pontuacao_final = int(
                                                (pontuacao / (tamanho_sequencia_atual * 30)) * 100)
                                            lista_sorteio = []
                                            item_da_lista = 0
                                            pontuacao = 0
                                            tentativa = 1

                                            print('pontuacao_final')
                                            print(pontuacao_final)

                                            if pontuacao_final >= 75:
                                                tamanho_sequencia_atual = tamanho_sequencia_atual + 1
                                                tamanho_sequencia = tamanho_sequencia_atual
                                                nivel_sequencia_atual=1
                                                nivel_sequencia=1
                                                fill_preto()
                                                trofeu_75()
                                                som_trofeu()
                                                tela_update()
                                                delay()
                                                delay()
                                                delay()
                                                delay()


                                            if pontuacao_final >= 25 and pontuacao_final < 75:
                                                tamanho_sequencia = tamanho_sequencia_atual
                                                nivel_sequencia_atual=2
                                                nivel_sequencia=2
                                                fill_preto()
                                                trofeu_50()
                                                som_trofeu()
                                                tela_update()
                                                delay()
                                                delay()
                                                delay()
                                                delay()

                                            if pontuacao_final < 25:
                                                if tamanho_sequencia_atual == 1:
                                                    tamanho_sequencia = tamanho_sequencia_atual
                                                    nivel_sequencia_atual=1
                                                    nivel_sequencia=1
                                                    fill_preto()
                                                    trofeu_25()
                                                    som_trofeu()
                                                    tela_update()
                                                    delay()
                                                    delay()
                                                    delay()
                                                    delay()

                                                if tamanho_sequencia_atual > 1:
                                                    tamanho_sequencia_atual = tamanho_sequencia_atual - 1
                                                    tamanho_sequencia = tamanho_sequencia_atual
                                                    nivel_sequencia_atual=2
                                                    nivel_sequencia=2
                                                    fill_preto()
                                                    trofeu_25()
                                                    som_trofeu()
                                                    tela_update()
                                                    delay()
                                                    delay()
                                                    delay()
                                                    delay()

                                            game_start = False
                                            figura_selecionada = False




                                    elif (jogador[0] > 400 and jogador[0] < 625) and (
                                            jogador[1] > 0 and jogador[1] < 150) and figura_selecionada == False:
                                        # print('círculo')
                                        circulo_longe_selecionado()
                                        som_circulo()
                                        tela_update()
                                        delay()
                                        figura_selecionada = True
                                        disparo_relogio = False
                                        tempo_ajuda_switch = False

                                        if lista_sorteio[item_da_lista] == 2:
                                            pontuacao = pontuacao + 5
                                            feliz()
                                            som_feliz()
                                            tela_update()
                                            q_acertos_com_ajuda = q_acertos_com_ajuda + 1
                                            delay()

                                        if lista_sorteio[item_da_lista] != 2:
                                            triste()
                                            som_triste()
                                            tela_update()
                                            q_erros = q_erros + 1
                                            delay()

                                        item_da_lista = item_da_lista + 1
                                        print('tentativa')
                                        print(tentativa)

                                        if item_da_lista == tamanho_sequencia_atual and tentativa == 1:
                                            lista_sorteio = []
                                            item_da_lista = 0
                                            tamanho_sequencia = tamanho_sequencia_atual
                                            disparo_relogio = False
                                            tentativa = 2

                                        if item_da_lista == tamanho_sequencia_atual and tentativa == 2:
                                            lista_sorteio = []
                                            item_da_lista = 0
                                            tamanho_sequencia = tamanho_sequencia_atual
                                            disparo_relogio = False
                                            tentativa = 3

                                        if item_da_lista == tamanho_sequencia_atual and tentativa == 3:
                                            pontuacao_final = int(
                                                (pontuacao / (tamanho_sequencia_atual * 30)) * 100)
                                            lista_sorteio = []
                                            item_da_lista = 0
                                            pontuacao = 0
                                            tentativa = 1

                                            print('pontuacao_final')
                                            print(pontuacao_final)

                                            if pontuacao_final >= 75:
                                                tamanho_sequencia_atual = tamanho_sequencia_atual + 1
                                                tamanho_sequencia = tamanho_sequencia_atual
                                                nivel_sequencia_atual=1
                                                nivel_sequencia=1
                                                fill_preto()
                                                trofeu_75()
                                                som_trofeu()
                                                tela_update()
                                                delay()
                                                delay()
                                                delay()
                                                delay()


                                            if pontuacao_final >= 25 and pontuacao_final < 75:
                                                tamanho_sequencia = tamanho_sequencia_atual
                                                nivel_sequencia_atual=2
                                                nivel_sequencia=2
                                                fill_preto()
                                                trofeu_50()
                                                som_trofeu()
                                                tela_update()
                                                delay()
                                                delay()
                                                delay()
                                                delay()

                                            if pontuacao_final < 25:
                                                if tamanho_sequencia_atual == 1:
                                                    tamanho_sequencia = tamanho_sequencia_atual
                                                    nivel_sequencia_atual=1
                                                    nivel_sequencia=1
                                                    fill_preto()
                                                    trofeu_25()
                                                    som_trofeu()
                                                    tela_update()
                                                    delay()
                                                    delay()
                                                    delay()
                                                    delay()

                                                if tamanho_sequencia_atual > 1:
                                                    tamanho_sequencia_atual = tamanho_sequencia_atual - 1
                                                    tamanho_sequencia = tamanho_sequencia_atual
                                                    nivel_sequencia_atual=2
                                                    nivel_sequencia=2
                                                    fill_preto()
                                                    trofeu_25()
                                                    som_trofeu()
                                                    tela_update()
                                                    delay()
                                                    delay()
                                                    delay()
                                                    delay()

                                            game_start = False
                                            figura_selecionada = False




                                    elif (jogador[0] > 625 and jogador[0] < 800) and (
                                            jogador[1] > 125 and jogador[1] < 240) and figura_selecionada == False:
                                        # print('quadrado')
                                        quadrado_longe_selecionado()
                                        som_quadrado()
                                        tela_update()
                                        delay()
                                        figura_selecionada = True
                                        disparo_relogio = False
                                        tempo_ajuda_switch = False

                                        if lista_sorteio[item_da_lista] == 3:
                                            pontuacao = pontuacao + 5
                                            feliz()
                                            som_feliz()
                                            tela_update()
                                            q_acertos_com_ajuda = q_acertos_com_ajuda + 1
                                            delay()

                                        if lista_sorteio[item_da_lista] != 3:
                                            triste()
                                            som_triste()
                                            tela_update()
                                            q_erros = q_erros + 1
                                            delay()

                                        item_da_lista = item_da_lista + 1
                                        print('tentativa')
                                        print(tentativa)

                                        if item_da_lista == tamanho_sequencia_atual and tentativa == 1:
                                            lista_sorteio = []
                                            item_da_lista = 0
                                            tamanho_sequencia = tamanho_sequencia_atual
                                            disparo_relogio = False
                                            tentativa = 2

                                        if item_da_lista == tamanho_sequencia_atual and tentativa == 2:
                                            lista_sorteio = []
                                            item_da_lista = 0
                                            tamanho_sequencia = tamanho_sequencia_atual
                                            disparo_relogio = False
                                            tentativa = 3

                                        if item_da_lista == tamanho_sequencia_atual and tentativa == 3:
                                            pontuacao_final = int(
                                                (pontuacao / (tamanho_sequencia_atual * 30)) * 100)
                                            lista_sorteio = []
                                            item_da_lista = 0
                                            pontuacao = 0
                                            tentativa = 1

                                            print('pontuacao_final')
                                            print(pontuacao_final)

                                            if pontuacao_final >= 75:
                                                tamanho_sequencia_atual = tamanho_sequencia_atual + 1
                                                tamanho_sequencia = tamanho_sequencia_atual
                                                nivel_sequencia_atual=1
                                                nivel_sequencia=1
                                                fill_preto()
                                                trofeu_75()
                                                som_trofeu()
                                                tela_update()
                                                delay()
                                                delay()
                                                delay()
                                                delay()
                                                nivel_sequencia = 1

                                            if pontuacao_final >= 25 and pontuacao_final < 75:
                                                tamanho_sequencia = tamanho_sequencia_atual
                                                nivel_sequencia_atual=2
                                                nivel_sequencia=2
                                                fill_preto()
                                                trofeu_50()
                                                som_trofeu()
                                                tela_update()
                                                delay()
                                                delay()
                                                delay()
                                                delay()

                                            if pontuacao_final < 25:
                                                if tamanho_sequencia_atual == 1:
                                                    tamanho_sequencia = tamanho_sequencia_atual
                                                    nivel_sequencia_atual=1
                                                    nivel_sequencia=1
                                                    fill_preto()
                                                    trofeu_25()
                                                    som_trofeu()
                                                    tela_update()
                                                    delay()
                                                    delay()
                                                    delay()
                                                    delay()

                                                if tamanho_sequencia_atual > 1:
                                                    tamanho_sequencia_atual = tamanho_sequencia_atual - 1
                                                    tamanho_sequencia = tamanho_sequencia_atual
                                                    nivel_sequencia_atual=2
                                                    nivel_sequencia=2
                                                    fill_preto()
                                                    trofeu_25()
                                                    som_trofeu()
                                                    tela_update()
                                                    delay()
                                                    delay()
                                                    delay()
                                                    delay()

                                            game_start = False
                                            figura_selecionada = False



                                    elif (jogador[0] > 300 and jogador[0] < 500) and (
                                            jogador[1] > 400 and jogador[1] < 600):
                                        # print('base')
                                        # base_com_pe_verde()
                                        # tela_update()

                                        if figura_selecionada == True:
                                            disparo_relogio = False
                                            figura_selecionada = False


                                    else:
                                        print(tempo)
                                        # tela_update()

                                    # disparo_relogio=False
                                ##########################################################################
                                ########################### OMISSÃO PELO JOGADOR #########################
                                ##########################################################################
                                if tempo > tempo_total:
                                    fill_preto()
                                    tempo_max()
                                    som_triste()
                                    tela_update()
                                    delay()
                                    delay()
                                    delay()
                                    delay()
                                    delay()
                                    tamanho_sequencia = tamanho_sequencia_atual
                                    nivel_sequencia_atual=2
                                    nivel_sequencia=2
                                    lista_sorteio = []
                                    item_da_lista = 0
                                    tentativa = 1
                                    q_omissao = q_omissao + 1
                                    disparo_relogio = False
                                    tempo_ajuda_switch = False
                                    game_start = False

                            #################################################################################
                            #################################################################################



                        else:
                            nivel_sequencia=1



                    else:
                        repetea_iniciar()
                        pygame.draw.circle(gameDisplay, (amarelo), jogador, 15)
                        pygame.display.update()


            except:
                if contador <= 3:
                    pass
                if contador>3:
                    print('SEM SINAL')
                    sem_sinal()
                    tela_update()
                    cv2.putText(tela_de_controle, 'SEM SINAL',
                                (int(largura_projetor / 10), (int(altura_projetor / 2))), fonte, 3,
                                verde, 5, cv2.LINE_AA)

                    #data = datetime.date.today()
                    #hora_sem_sinal = datetime.datetime.now().time()
                    #arquivo.gravaDados(jogador_selecionado_detalhado,[sessao, data, hora_sem_sinal, tamanho_sequencia_atual, nivel_sequencia_atual,posicao(), 'Sem Sinal'])
                    pass


            # Atualização das telas
            cv2.imshow("TELA DE CONTROLE", tela_de_controle)
            cv2.setMouseCallback("TELA DE CONTROLE", mousePoints)


            #################################################################################
            ###################################### ATALHOS ##################################
            #################################################################################

            # Teclas de Atalho
            for event in pygame.event.get():
                # SAIR
                if event.type == pygame.QUIT:
                    arquivo.set_R_FASE(jogador_selecionado, tamanho_sequencia_atual)
                    arquivo.set_R_NIVEL(jogador_selecionado, nivel_sequencia_atual)
                    arquivo.set_R_HUD(jogador_selecionado, hud_switch)
                    arquivo.set_R_SOM(jogador_selecionado, som_switch)

                    gameExit=True
                    print('QUIT')
                    cv2.destroyWindow('tela_de_controle')
                    pygame.quit()
                    camera.release()
                    exit()
                # AJUDA F1
                if event.type == pygame.KEYDOWN:
                    if event.key==pygame.K_F1:
                        fill_preto()
                        ajuda_f1()
                        pygame.display.update()
                        delay()
                        delay()
                        delay()
                        delay()
                        delay()
                        t0 = int(time.time())

                # POSIÇÃO DAS FIGURAS (P ou 1)
                    if event.key==pygame.K_p or event.key==pygame.K_1:
                        fill_preto()
                        posicionamento()
                        pygame.display.update()
                        delay()
                        delay()
                        delay()

                # HUD ON/OFF (H ou 2)
                    if event.key==pygame.K_h or event.key==pygame.K_2:

                        if hud_switch==False:
                            fill_preto()
                            hud_on()
                            pygame.display.update()
                            data = datetime.date.today()
                            hora_hud_ligado = datetime.datetime.now().time()
                            arquivo.gravaDados(jogador_selecionado_detalhado,[sessao, data, hora_hud_ligado, tamanho_sequencia_atual,nivel_sequencia_atual, posicao(), 'HUD Ligado'])
                            delay()
                            delay()
                            delay()

                        if hud_switch==True:
                            fill_preto()
                            hud_off()
                            pygame.display.update()
                            data = datetime.date.today()
                            hora_hud_desligado = datetime.datetime.now().time()
                            arquivo.gravaDados(jogador_selecionado_detalhado,[sessao, data, hora_hud_desligado, tamanho_sequencia_atual,nivel_sequencia_atual, posicao(), 'HUD Desligado'])
                            delay()
                            delay()
                            delay()

                        hud_switch= not hud_switch



                # SOM ON/OFF (S ou 3)
                    if event.key==pygame.K_s or event.key==pygame.K_3:
                        fill_preto()
                        if som_switch==False:
                            som_ligado()
                            tela_update()
                            data = datetime.date.today()
                            hora_som_ligado = datetime.datetime.now().time()
                            arquivo.gravaDados(jogador_selecionado_detalhado,[sessao, data, hora_som_ligado, tamanho_sequencia_atual,nivel_sequencia_atual, posicao(), 'Som Ligado'])
                            delay()
                            delay()
                            delay()
                        if som_switch==True:
                            som_desligado()
                            tela_update()
                            data = datetime.date.today()
                            hora_som_desligado = datetime.datetime.now().time()
                            arquivo.gravaDados(jogador_selecionado_detalhado,[sessao, data, hora_som_desligado, tamanho_sequencia_atual,nivel_sequencia_atual, posicao(), 'Som Desligado'])
                            delay()
                            delay()
                            delay()

                        som_switch = not som_switch


                #FASE ACIMA (seta UP ou 4)
                    if event.key==pygame.K_UP or event.key==pygame.K_4:
                        fill_preto()
                        fase_acima()
                        data = datetime.date.today()
                        hora_fase_acima = datetime.datetime.now().time()
                        arquivo.gravaDados(jogador_selecionado_detalhado,[sessao, data, hora_fase_acima, tamanho_sequencia_atual,nivel_sequencia_atual, posicao(), 'Fase Acima'])
                        tamanho_sequencia_atual=tamanho_sequencia_atual+1
                        tamanho_sequencia=tamanho_sequencia_atual
                        lista_sorteio=[]
                        game_start=False
                        pygame.display.update()
                        delay()
                        delay()
                        delay()

                # FASE ABAIXO (seta DOWN ou 5)
                    if event.key==pygame.K_DOWN or event.key==pygame.K_5:
                        fill_preto()
                        fase_abaixo()
                        data = datetime.date.today()
                        hora_fase_abaixo = datetime.datetime.now().time()
                        arquivo.gravaDados(jogador_selecionado_detalhado,[sessao, data, hora_fase_abaixo, tamanho_sequencia_atual,nivel_sequencia_atual, posicao(), 'Fase Abaixo'])
                        if tamanho_sequencia_atual>1:
                            tamanho_sequencia_atual=tamanho_sequencia_atual-1
                            tamanho_sequencia=tamanho_sequencia_atual
                            lista_sorteio=[]
                            game_start=False
                        if tamanho_sequencia_atual==1:
                            tamanho_sequencia=tamanho_sequencia_atual
                            lista_sorteio = []
                            game_start=False
                        pygame.display.update()
                        delay()
                        delay()
                        delay()

                # PAUSE (ESPAÇO)
                    if event.key == pygame.K_SPACE:
                        data = datetime.date.today()
                        hora_pausa = datetime.datetime.now().time()
                        arquivo.gravaDados(jogador_selecionado_detalhado,[sessao, data, hora_pausa, tamanho_sequencia_atual, nivel_sequencia_atual,posicao(), 'Pausa'])
                        t0=int(time.time())
                        pausa_switch= not pausa_switch



            # SAIR (ESC)
                    if event.key == pygame.K_ESCAPE:
                        data = datetime.date.today()
                        hora_esc = datetime.datetime.now().time()

                        arquivo.set_R_FASE(jogador_selecionado_config, tamanho_sequencia_atual)
                        arquivo.set_R_NIVEL(jogador_selecionado_config, nivel_sequencia_atual)
                        arquivo.set_R_HUD(jogador_selecionado_config, hud_switch)
                        arquivo.set_R_SOM(jogador_selecionado_config, som_switch)
                        arquivo.set_R_SESSAO(jogador_selecionado_config, sessao)

                        arquivo.gravaDados(jogador_selecionado_detalhado,[sessao, data, hora_esc, tamanho_sequencia_atual, nivel_sequencia_atual, posicao(),'Sair'])
                        arquivo.gravaDados(jogador_selecionado,[sessao, data, hora_inicio, hora_esc, tamanho_sequencia_atual, nivel_sequencia_atual,q_acertos,q_acertos_com_ajuda, q_ajudas, q_erros, q_omissao])

                        gameExit = True
                        print('QUIT')
                        cv2.destroyWindow('tela_de_controle')
                        pygame.quit()
                        camera.release()
                        exit()



