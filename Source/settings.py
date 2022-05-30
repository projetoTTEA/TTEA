import pygame
import numpy as np
import mediapipe as mp
import cv2
import arquivo

WINDOW_NAME = "KARTEA"
GAME_TITLE = WINDOW_NAME

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

FPS = 60
DRAW_FPS = True

# sizes
BUTTONS_SIZES = (150, 45)
CAR_SIZE = 150
CAR_HITBOX_SIZE = (100, 100)
TARGETS_SIZES = (12, 12)
OBSTACLE_SIZES = (12, 12)

OBJ_POS = [(368, 80), (393, 80),(419, 80)]
"""
OBJ_POS_F = [(104, 600), (337, 600),(570, 600)]

264, 56, 151
0.5, 0.1, 0.3
"""

# drawing
DRAW_HITBOX = False  # will draw all the hitbox

# animation
ANIMATION_SPEED = 0.01 # the frame of the insects will change every X sec

# difficulty
GAME_DURATION = 120  # the game will last X sec

TARGETS_SPAWN_TIME = 8
TARGETS_MOVE_SPEED = 1
OBSTACLE_PENALITY = 0  # will remove X of the score of the player (if he colides with a obstacle)

# colors
COLORS = {"title": (38, 61, 39), "score": (38, 61, 39),
          "timer": (38, 61, 39), "buttons": {"default": (56, 67, 209), "second":  (87, 99, 255), "text": (255, 255, 255), "shadow": (46, 54, 163)}}  # second is the color when the mouse is on the button

# sounds / music
MUSIC_VOLUME = 0  # value between 0 and 1
SOUNDS_VOLUME = 1

# fonts
pygame.font.init()
FONTS = {}
FONTS["small"] = pygame.font.Font(None, 10)
FONTS["medium"] = pygame.font.Font(None, 25)
FONTS["big"] = pygame.font.Font(None, 50)

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
font = pygame.font.SysFont(None, 25)


#################################################################################
#################################### Hardware ###################################
#################################################################################
# Tamanho das Telas:
largura_projetor = SCREEN_WIDTH  # A ltere este valor de acordo com a resolução da projeção do jogo.
altura_projetor = SCREEN_HEIGHT  # A ltere este valor de acordo com a resolução da projeção do jogo.
largura_tela_controle = 640  # Esta tela é usada pelo terapeuta/operador. Altere o valor caso necessário.
altura_tela_controle = 480  # Esta tela é usada pelo terapeuta/operador. Altere o valor caso necessário.
relacao_largura = (largura_projetor / largura_tela_controle)  # Esta relação é usada na correção de perspectiva.
relacao_altura = (altura_projetor / altura_tela_controle)  # Esta relação é usada na correção de perspectiva.
tela_de_controle = np.zeros((altura_tela_controle, largura_tela_controle, 3),
                            np.uint8)  # Tela que será usada para o projetar o jogo.


#################################################################################
############################# VARIÁVEIS DE PROGRAMA #############################
#################################################################################
mp_drawing = mp.solutions.drawing_utils  # Configuração do MediaPipe. Ver https://google.github.io/mediapipe/solutions/pose.html para maiores detalhes.
mp_pose = mp.solutions.pose  # Configuração do MediaPipe. Ver https://google.github.io/mediapipe/solutions/pose.html para maiores detalhes.
pontos_calibracao = np.zeros((4, 2), int)  # Matriz para os pontos de calibração de perspectiva - 4 linhas/ 2 colunas
contador = 0  # Contador utilizado nos 4 pontos de calibração
game_start=False # Coloca na tela iniciar
gameExit=False # Sai do completamente do jogo
figura_selecionada=False # Usada para evitar que o usuário apenas selecione uma vez a figura e não ficar piscando
lista_sorteio=[] #São as figuras sorteadas pelo computador e colocadas nesta lista, para depois fazer a comparação com as escolhas do usuário
pontuacao=0 # Pontos conseguidos em durante a rodada
tempo_ajuda=5 # Tempo até a ajuda aparecer
tempo_total=10 # Tempo máximo da jogada
atencao_memorizar=False
hud_switch=True
pausa_switch=False
tempo_ajuda_switch=False
tentativa=1

#################################################################################
################################## SPRITES ######################################
#################################################################################
icone_fig=pygame.image.load('Assets/Kartea/icone.png')
avisos_fig=pygame.image.load('Assets/Kartea/avisos.png')
ajuda_f1_fig=pygame.image.load('Assets/Kartea/ajuda_F1.png')
instrucao_calibrar_fig=pygame.image.load('Assets/Kartea/calibrar.png')
sem_sinal_fig=pygame.image.load('Assets/Kartea/sem_sinal.png')
triste_fig=pygame.image.load('Assets/Kartea/triste.png')
feliz_fig=pygame.image.load('Assets/Kartea/feliz.png')
som_fig=pygame.image.load('Assets/Kartea/som.png')
hud_on_fig=pygame.image.load('Assets/Kartea/hud_on.png')
hud_off_fig=pygame.image.load('Assets/Kartea/hud_off.png')
fase_abaixo_fig=pygame.image.load('Assets/Kartea/fase_abaixo.png')
fase_acima_fig=pygame.image.load('Assets/Kartea/fase_acima.png')
trofeu_fig=pygame.image.load('Assets/Kartea/trofeu.png')
trofeu_25_fig=pygame.image.load('Assets/Kartea/trofeu_25.png')
trofeu_50_fig=pygame.image.load('Assets/Kartea/trofeu_50.png')
trofeu_75_fig=pygame.image.load('Assets/Kartea/trofeu_75.png')
