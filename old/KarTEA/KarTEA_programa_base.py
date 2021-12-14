#################################################################################
######################### SOFTWARE BASE - PROJETO T-TEA #########################
#################################################################################
################################# VERSÃO 1.0 ####################################
#################################################################################

import cv2
import mediapipe as mp
import numpy as np
import sys
import pygame
from pygame import mixer
from pygame.locals import *


#Tamanho das Telas:
largura_projetor = SCREEN_WIDTH = 800 #Altere este valor de acordo com a resolução da projeção do jogo.
altura_projetor = SCREEN_HEIGHT = 600 #Altere este valor de acordo com a resolução da projeção do jogo.
HALF_SCREEN_HEIGHT=int(SCREEN_HEIGHT/2)

largura_tela_controle = 640 # Esta tela é usada pelo terapeuta/operador. Altere o valor caso necessário.
altura_tela_controle = 480 # Esta tela é usada pelo terapeuta/operador. Altere o valor caso necessário.
relacao_largura=(largura_projetor/largura_tela_controle) # Esta relação é usada na correção de perspectiva.
relacao_altura=(altura_projetor/altura_tela_controle) # Esta relação é usada na correção de perspectiva.
tela_de_calibracao = np.zeros((altura_projetor,largura_projetor,3),np.uint8) #Tela que será usada para o projetar o jogo.
tela_de_controle = np.zeros((altura_tela_controle,largura_tela_controle,3),np.uint8) #Tela que será usada para o projetar o jogo.

#Escolha da Câmera:
camera = cv2.VideoCapture(0) #O valor entre parênteses indica qual câmera será utilizada. 0=default; 1,2,3...= câmeras externas.


#Fonte para Letras:
fonte = cv2.FONT_HERSHEY_SIMPLEX

#Cores - Valor em BGR (Blue-Green-Red)
azul = 255,0,0 
verde = 0,255,0
vermelho = 0,0,255 
amarelo = 0,255,255 
branco = 255,255,255 
preto = 0,0,0 

BLACK=pygame.color.THECOLORS["black"]
WHITE=pygame.color.THECOLORS["white"]
RED=pygame.color.THECOLORS["red"]
GREEN=pygame.color.THECOLORS["green"]
BLUE=pygame.color.THECOLORS["blue"]
YELLOW=pygame.color.THECOLORS["yellow"]

#Variaveis KarTEA
texture_position=0  #this is used to draw the road
#variables used to increment texture_position
ddz=0.001
dz=0
z=0

road_pos=0  #this is to remember our position on the road
road_acceleration=40  #this is the speed at witch we traverse the road
texture_position_acceleration=4  #this determine how much the strips will stretch forward
texture_position_threshold=500  #this determine how much the road will be divided into strips
half_texture_position_threshold=int(texture_position_threshold/2) #this is used to know what road to draw from (light or dark road)

hill_map=[0]*HALF_SCREEN_HEIGHT
hill_map_lenght=len(hill_map)
top_segment={'position':100,'dy':0.005}  #dy=-0.005 for a downhill and dy=0.005 for an uphill
bottom_segment={'position':100,'dy':0}
current_y=0
dy=0
ddy=0
hill_speed=5  #this is the speed at witch we traverse the hill
old_y_hill_pos=SCREEN_HEIGHT
current_y_hill_pos=SCREEN_HEIGHT
y_hill_pos_difference=0


#Variáveis de Programa:
mp_drawing = mp.solutions.drawing_utils #Configuração do MediaPipe. Ver https://google.github.io/mediapipe/solutions/pose.html para maiores detalhes.
mp_pose = mp.solutions.pose #Configuração do MediaPipe. Ver https://google.github.io/mediapipe/solutions/pose.html para maiores detalhes.
pontos_calibracao = np.zeros((4,2),int) # Matriz para os pontos de calibração de perspectiva - 4 linhas/ 2 colunas
contador = 0 #Contador utilizado nos 4 pontos de calibração


#Função para capturar cliques do Mouse:
def mousePoints(event,x,y,flags,params):
    global contador
    if event == cv2.EVENT_LBUTTONDOWN:
        pontos_calibracao[contador] = x,y
        contador = contador+1


#Função com os passos para determinar a área de projeçao capturada pela câmera:
def calibracao():
            tela_de_calibracao = np.zeros((altura_projetor,largura_projetor,3),np.uint8)
            cv2.putText(tela_de_calibracao, ' CLIQUE', (int(largura_projetor/4),(int(altura_projetor/2)-20)), fonte, 3, verde, 2, cv2.LINE_AA)
            cv2.circle(tela_de_controle,(pontos_calibracao[0]),5,azul,3)
            cv2.circle(tela_de_controle,(pontos_calibracao[1]),5,azul,3)
            cv2.circle(tela_de_controle,(pontos_calibracao[2]),5,azul,3)
            cv2.circle(tela_de_controle,(pontos_calibracao[3]),5,azul,3)
                
            
            if contador == 0:
                cv2.arrowedLine(tela_de_calibracao, (int(largura_projetor/2),int(altura_projetor/3)), (0,0), azul, 20)

            if contador == 1:
                cv2.arrowedLine(tela_de_calibracao, (int(largura_projetor/2),int(altura_projetor/3)), (largura_projetor,0), azul, 20)

            if contador == 2:
                cv2.arrowedLine(tela_de_calibracao, (int(largura_projetor/2),int(altura_projetor/2)), (0,altura_projetor), azul, 20)

            if contador == 3:
                cv2.arrowedLine(tela_de_calibracao, (int(largura_projetor/2),int(altura_projetor/2)), (largura_projetor,altura_projetor), azul, 20)
                
            if contador == 4:
                game_loop(p_after)

            cv2.imshow("TELA DE CALIBRACAO",tela_de_calibracao)


#Função para determinar a posição do jogador na área de projeçao:
def posicao():

        #Transformação de Perspectiva:        
        pts1 = np.float32([pontos_calibracao[0],pontos_calibracao[1],pontos_calibracao[2],pontos_calibracao[3]])
        pts2 = np.float32([[0,0],[largura_tela_controle,0],[0,altura_tela_controle],[largura_tela_controle,altura_tela_controle]])
        matrix = cv2.getPerspectiveTransform(pts1,pts2)
        perspectiva = cv2.warpPerspective(tela_de_controle, matrix, (largura_tela_controle,altura_tela_controle))

        #Posição do jogador:        
        p = (int(x_pose*largura_tela_controle),int(y_pose*altura_tela_controle))
        position_x = (matrix[0][0]*p[0] + matrix[0][1]*p[1] + matrix[0][2]) / ((matrix[2][0]*p[0] + matrix[2][1]*p[1] + matrix[2][2]))
        position_y = (matrix[1][0]*p[0] + matrix[1][1]*p[1] + matrix[1][2]) / ((matrix[2][0]*p[0] + matrix[2][1]*p[1] + matrix[2][2]))
        p_after = (int((position_x)*(relacao_largura)), int((position_y)*(relacao_altura)))

        return p_after


#Função onde o jogo deve ser inserido:
def game_loop():
        jogador = posicao()
        #gameDisplay.fill(branco)
        #loop speed limitation
        #30 frames per second is enought
        pygame.time.Clock().tick(60)
       
        for event in pygame.event.get():    #wait for events
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                    
        #Movement controls
        keys = pygame.key.get_pressed()
        if keys[K_ESCAPE]:
            pygame.quit()
            sys.exit()
        
        global road_pos, top_segment, bottom_segment, texture_position, ddz, dz, z, dy, ddy, current_y, old_y_hill_pos, current_y_hill_pos, gameDisplay

        #Rode animation
        road_pos+=road_acceleration
        if road_pos>=texture_position_threshold:
            road_pos=0
        top_segment['position']=350
        #if we reach the hill's end we invert it's incrementation to exit it
        if top_segment['position']>=hill_map_lenght:
            top_segment['position']=0
            bottom_segment['dy']=top_segment['dy']
            #top_segment['dy']+=0.005  #+0.005 to exit a downhill and -0.005 to exit an uphill
            #top_segment['dy']*=-1


        #draw the road
        texture_position=road_pos
        dz=0
        z=0
        dy=0
        ddy=0
        current_y=0
        old_y_hill_pos=SCREEN_HEIGHT
        current_y_hill_pos=SCREEN_HEIGHT
        gameDisplay.fill(BLUE)
        for i in range(HALF_SCREEN_HEIGHT-1,-1,-1):
            if top_segment['position'] < i:
                dy = bottom_segment['dy']
            else:
                dy = top_segment['dy']
            ddy += dy
            current_y += ddy
            hill_map[i] = current_y
            current_y_hill_pos = int(i+HALF_SCREEN_HEIGHT-hill_map[i])
            if current_y_hill_pos<old_y_hill_pos:
                y_hill_pos_difference=old_y_hill_pos-current_y_hill_pos
                old_y_hill_pos=current_y_hill_pos
                if texture_position<half_texture_position_threshold:
                    if y_hill_pos_difference>1:
                        for j in range(y_hill_pos_difference):
                            gameDisplay.blit(light_road,(0,current_y_hill_pos+j),(0,i,SCREEN_WIDTH,1))
                    gameDisplay.blit(light_road,(0,current_y_hill_pos),(0,i,SCREEN_WIDTH,1))
                else:
                    if y_hill_pos_difference>1:
                        for j in range(y_hill_pos_difference):
                            gameDisplay.blit(dark_road,(0,current_y_hill_pos+j),(0,i,SCREEN_WIDTH,1))
                    gameDisplay.blit(dark_road,(0,current_y_hill_pos),(0,i,SCREEN_WIDTH,1))
            dz+=ddz
            z+=dz
            texture_position+=texture_position_acceleration+z
            if texture_position>=texture_position_threshold:
                texture_position=0
            pygame.display.flip()

        pygame.draw.circle(gameDisplay,(branco),jogador,5)
        pygame.display.update()
        print (jogador)

# Inicialização do MediaPipe e Calibração.
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
            x_pose =landmarks[mp_pose.PoseLandmark.NOSE.value].x #33 Pontos de referência do MediaPipe. Ex: RIGHT_FOOT_INDEX; NOSE; RIGHT_INDEX
            y_pose =landmarks[mp_pose.PoseLandmark.NOSE.value].y #33 Pontos de referência do MediaPipe. Ex: RIGHT_FOOT_INDEX; NOSE; RIGHT_INDEX

            # Desenho dos pontos de referência
            mp_drawing.draw_landmarks(tela_de_controle, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                mp_drawing.DrawingSpec(color=(0,255,0), thickness=2, circle_radius=2), 
                                mp_drawing.DrawingSpec(color=(0,0,255), thickness=2, circle_radius=2)
                                 )
            # Antes da Calibração.
            if contador<=3:
                calibracao()

            # Depois da Calibração.           
            elif contador ==4:
                cv2.line(tela_de_controle,(pontos_calibracao[0]),(pontos_calibracao[1]),(verde),2)
                cv2.line(tela_de_controle,(pontos_calibracao[1]),(pontos_calibracao[3]),(verde),2)
                cv2.line(tela_de_controle,(pontos_calibracao[2]),(pontos_calibracao[0]),(verde),2)
                cv2.line(tela_de_controle,(pontos_calibracao[2]),(pontos_calibracao[3]),(verde),2)

                cv2.circle(tela_de_controle,(pontos_calibracao[0]),5,azul,3)
                cv2.circle(tela_de_controle,(pontos_calibracao[1]),5,azul,3)
                cv2.circle(tela_de_controle,(pontos_calibracao[2]),5,azul,3)
                cv2.circle(tela_de_controle,(pontos_calibracao[3]),5,azul,3)
                cv2. destroyWindow("TELA DE CALIBRACAO")

                pygame.init()
                #flags = pygame.RESIZABLE | pygame.FULLSCREEN

                gameDisplay = pygame.display.set_mode((largura_projetor, altura_projetor)) #add RESIZABLE or FULLSCREEN
                pygame.display.set_caption("KarTEA")
            
                #Imagens da estrada
                light_road=pygame.image.load('light_road(800x300).png').convert()
                dark_road=pygame.image.load('dark_road(800x300).png').convert()

                #game_loop()

        except:
            pass

        jogador = posicao()
        #gameDisplay.fill(branco)
        #loop speed limitation
        #30 frames per second is enought
        pygame.time.Clock().tick(60)
       
        for event in pygame.event.get():    #wait for events
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                    
        #Movement controls
        keys = pygame.key.get_pressed()
        if keys[K_ESCAPE]:
            pygame.quit()
            sys.exit()
        
        #Rode animation
        road_pos+=road_acceleration
        if road_pos>=texture_position_threshold:
            road_pos=0
        top_segment['position']=350
        #if we reach the hill's end we invert it's incrementation to exit it
        if top_segment['position']>=hill_map_lenght:
            top_segment['position']=0
            bottom_segment['dy']=top_segment['dy']
            #top_segment['dy']+=0.005  #+0.005 to exit a downhill and -0.005 to exit an uphill
            #top_segment['dy']*=-1


        #draw the road
        texture_position=road_pos
        dz=0
        z=0
        dy=0
        ddy=0
        current_y=0
        old_y_hill_pos=SCREEN_HEIGHT
        current_y_hill_pos=SCREEN_HEIGHT
        gameDisplay.fill(BLUE)
        for i in range(HALF_SCREEN_HEIGHT-1,-1,-1):
            if top_segment['position'] < i:
                dy = bottom_segment['dy']
            else:
                dy = top_segment['dy']
            ddy += dy
            current_y += ddy
            hill_map[i] = current_y
            current_y_hill_pos = int(i+HALF_SCREEN_HEIGHT-hill_map[i])
            if current_y_hill_pos<old_y_hill_pos:
                y_hill_pos_difference=old_y_hill_pos-current_y_hill_pos
                old_y_hill_pos=current_y_hill_pos
                if texture_position<half_texture_position_threshold:
                    if y_hill_pos_difference>1:
                        for j in range(y_hill_pos_difference):
                            gameDisplay.blit(light_road,(0,current_y_hill_pos+j),(0,i,SCREEN_WIDTH,1))
                    gameDisplay.blit(light_road,(0,current_y_hill_pos),(0,i,SCREEN_WIDTH,1))
                else:
                    if y_hill_pos_difference>1:
                        for j in range(y_hill_pos_difference):
                            gameDisplay.blit(dark_road,(0,current_y_hill_pos+j),(0,i,SCREEN_WIDTH,1))
                    gameDisplay.blit(dark_road,(0,current_y_hill_pos),(0,i,SCREEN_WIDTH,1))
            dz+=ddz
            z+=dz
            texture_position+=texture_position_acceleration+z
            if texture_position>=texture_position_threshold:
                texture_position=0
            pygame.display.flip()

        pygame.draw.circle(gameDisplay,(branco),jogador,5)
        pygame.display.update()
        print (jogador)

        # Atualização das telas
        cv2.imshow("TELA DE CONTROLE", tela_de_controle)
        cv2.setMouseCallback("TELA DE CONTROLE",mousePoints)

        #Saída de programa ESC
        if cv2.waitKey (40) == 27:
            break

    camera.release()
    cv2.destroyAllWindows()
