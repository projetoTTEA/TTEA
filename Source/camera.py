import cv2
from settings import *

class Camera:
    def __init__(self):
        # Load camera
        self.cap = cv2.VideoCapture(0)
        self.ret, self.frame = self.cap.read()


    def load_camera(self):
        self.ret, self.frame = self.cap.read()
        # Desenha a borda da area de calibração
        cv2.line(self.frame, (pontos_calibracao[0]), (pontos_calibracao[1]), (verde), 2)
        cv2.line(self.frame, (pontos_calibracao[1]), (pontos_calibracao[3]), (verde), 2)
        cv2.line(self.frame, (pontos_calibracao[2]), (pontos_calibracao[0]), (verde), 2)
        cv2.line(self.frame, (pontos_calibracao[2]), (pontos_calibracao[3]), (verde), 2)

        cv2.circle(self.frame, (pontos_calibracao[0]), 5, azul, 3)
        cv2.circle(self.frame, (pontos_calibracao[1]), 5, azul, 3)
        cv2.circle(self.frame, (pontos_calibracao[2]), 5, azul, 3)
        cv2.circle(self.frame, (pontos_calibracao[3]), 5, azul, 3)

        cv2.imshow("Tela de Captura", self.frame)

    def close_camera(self):
        self.cap.release()
        cv2.destroyWindow("Tela de Captura")