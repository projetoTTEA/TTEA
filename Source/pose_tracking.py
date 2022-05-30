import cv2
import mediapipe as mp
from settings import *
import numpy as np
import settings as st
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_poses = mp.solutions.pose



class PoseTracking:
    def __init__(self):
        self.pose_tracking = mp_poses.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.feet_x = 0
        self.feet_y = 0
        self.results = None
        self.pose_closed = False


    def mousePoints(event, x, y, flags, params):
        # Função para capturar cliques do Mouse:
        if event == cv2.EVENT_LBUTTONDOWN:
            st.pontos_calibracao[st.CONTADOR] = x, y
            st.CONTADOR = st.CONTADOR + 1

    def calibracao():
        # Função com os passos para determinar a área de projeçao capturada pela câmera:
        tela_de_calibracao = np.zeros((SCREEN_WIDTH, SCREEN_HEIGHT, 3), np.uint8)
        cv2.putText(tela_de_calibracao, ' CLIQUE', (int(SCREEN_HEIGHT / 4), (int(SCREEN_WIDTH / 2) - 20)), fonte,
                    3,
                    verde, 2, cv2.LINE_AA)
        cv2.circle(tela_de_controle, (st.pontos_calibracao[0]), 5, azul, 3)
        cv2.circle(tela_de_controle, (st.pontos_calibracao[1]), 5, azul, 3)
        cv2.circle(tela_de_controle, (st.pontos_calibracao[2]), 5, azul, 3)
        cv2.circle(tela_de_controle, (st.pontos_calibracao[3]), 5, azul, 3)

        if st.CONTADOR == 0:
            cv2.arrowedLine(tela_de_calibracao, (int(SCREEN_HEIGHT / 2), int(SCREEN_WIDTH / 3)), (0, 0), azul, 20)

        if st.CONTADOR == 1:
            cv2.arrowedLine(tela_de_calibracao, (int(SCREEN_HEIGHT / 2), int(SCREEN_WIDTH / 3)),
                            (SCREEN_HEIGHT, 0), azul, 20)

        if st.CONTADOR == 2:
            cv2.arrowedLine(tela_de_calibracao, (int(SCREEN_HEIGHT / 2), int(SCREEN_WIDTH / 2)),
                            (0, SCREEN_WIDTH),
                            azul, 20)

        if st.CONTADOR == 3:
            cv2.arrowedLine(tela_de_calibracao, (int(SCREEN_HEIGHT / 2), int(SCREEN_WIDTH / 2)),
                            (SCREEN_HEIGHT, SCREEN_WIDTH), azul, 20)

        cv2.imshow("TELA DE CALIBRACAO", tela_de_calibracao)

    def posicao(self, x, y):
        # Função para determinar a posição do jogador na área de projeçao:
        # Transformação de Perspectiva:
        pts1 = np.float32([pontos_calibracao[0], pontos_calibracao[1], pontos_calibracao[2], pontos_calibracao[3]])
        pts2 = np.float32(
            [[0, 0], [largura_tela_controle, 0], [0, altura_tela_controle],
             [largura_tela_controle, altura_tela_controle]])
        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        perspectiva = cv2.warpPerspective(tela_de_controle, matrix, (largura_tela_controle, altura_tela_controle))

        # Posição do jogador:
        p = (x, y)
        position_x = (matrix[0][0] * p[0] + matrix[0][1] * p[1] + matrix[0][2]) / (
            (matrix[2][0] * p[0] + matrix[2][1] * p[1] + matrix[2][2]))
        position_y = (matrix[1][0] * p[0] + matrix[1][1] * p[1] + matrix[1][2]) / (
            (matrix[2][0] * p[0] + matrix[2][1] * p[1] + matrix[2][2]))
        p_after = (int((position_x) * (relacao_largura)), int((position_y) * (relacao_altura)))

        return p_after

    def scan_feets(self, image):
        rows, cols, _ = image.shape

        # Flip the image horizontally for a later selfie-view display, and convert
        # the BGR image to RGB.
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        self.results = self.pose_tracking.process(image)

        # Draw the pose annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        self.feet_closed = False

        if self.results.pose_landmarks:
            """
            x1, y1 = self.results.pose_landmarks.landmark[30].x, self.results.pose_landmarks.landmark[30].y # left_heel
            x2, y2 = self.results.pose_landmarks.landmark[29].x, self.results.pose_landmarks.landmark[29].y # right_heel

            #Ponto medio entre os pes
            x = int((x1+x2)/2)
            y = int((y+y1)/2)
            x, y
            """
            x, y = self.results.pose_landmarks.landmark[0].x, self.results.pose_landmarks.landmark[0].y  # nose

            self.feet_x = int(x * SCREEN_WIDTH)
            #self.feet_y = int(y * SCREEN_HEIGHT) # Caso o jogador mova-se por toda a tela
            self.feet_y = 550 # Jogador deve se mover apenas lateralmente

            mp_drawing.draw_landmarks(
                image,
                self.results.pose_landmarks,
                mp_poses.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
        return image

    def get_feet_center(self):
        return (self.feet_x, self.feet_y)


    def display_feet(self):
        cv2.imshow("image", self.image)
        cv2.waitKey(1)

    def is_feet_closed(self):

        pass


