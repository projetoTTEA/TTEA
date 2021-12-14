#################################################################################
######################### SOFTWARE BASE - PROJETO T-TEA #########################
#################################################################################
################################# VERSÃO 1.0 ####################################
#################################################################################

import cv2
import mediapipe as mp
import numpy as np


#Tamanho das Telas:
largura_projetor = 800 #A ltere este valor de acordo com a resolução da projeção do jogo.
altura_projetor = 600 #A ltere este valor de acordo com a resolução da projeção do jogo.
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
        #tela_de_calibracao = np.zeros((altura_projetor,largura_projetor,3),np.uint8)
        #cv2.circle(tela_de_calibracao,(jogador),50,branco,-1) 
        #cv2.imshow("TELA DE CALIBRACAO",tela_de_calibracao)
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
                game_loop()
          
                
                       
        except:
            pass


        # Atualização das telas            
        cv2.imshow("TELA DE CONTROLE", tela_de_controle)
        cv2.setMouseCallback("TELA DE CONTROLE",mousePoints)
       
      
        #Saída de programa
        if cv2.waitKey (40) == 27:
            break

    camera.release()
    cv2.destroyAllWindows()
