import cv2
import settings

class Camera:
    def __init__(self):
        # Load camera
        self.cap = cv2.VideoCapture(settings.CAMERA, cv2.CAP_DSHOW)
        self.ret, self.frame = self.cap.read()


    def load_camera(self):
        self.ret, self.frame = self.cap.read()
        self.frame = cv2.flip(self.frame, 1)
        # Desenha a borda da area de calibração
        cv2.line(self.frame, (settings.pontos_calibracao[0]), (settings.pontos_calibracao[1]), (settings.verde), 2)
        cv2.line(self.frame, (settings.pontos_calibracao[1]), (settings.pontos_calibracao[3]), (settings.verde), 2)
        cv2.line(self.frame, (settings.pontos_calibracao[2]), (settings.pontos_calibracao[0]), (settings.verde), 2)
        cv2.line(self.frame, (settings.pontos_calibracao[2]), (settings.pontos_calibracao[3]), (settings.verde), 2)

        cv2.circle(self.frame, (settings.pontos_calibracao[0]), 5, settings.azul, 3)
        cv2.circle(self.frame, (settings.pontos_calibracao[1]), 5, settings.azul, 3)
        cv2.circle(self.frame, (settings.pontos_calibracao[2]), 5, settings.azul, 3)
        cv2.circle(self.frame, (settings.pontos_calibracao[3]), 5, settings.azul, 3)

        cv2.imshow("Tela de Captura", self.frame)

    def close_camera(self):
        self.cap.release()
        cv2.destroyWindow("Tela de Captura")