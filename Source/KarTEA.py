# Setup Python ----------------------------------------------- #
import pygame
import sys
import os
import cv2
from settings import *
from game import Game
from menu import Menu
from menu_pause import Pause
from menu_feedback import Feedback
from menu_retrocede import Retrocede
from menu_reinicia import Reinicia
from menu_avanca import Avanca

# Setup pygame/window --------------------------------------------- #
# os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (100, 32) # windows position
pygame.init()
pygame.display.set_caption(WINDOW_NAME)
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 0)

mainClock = pygame.time.Clock()

# Fonts ----------------------------------------------------------- #
fps_font = pygame.font.SysFont("coopbl", 22)
"""
# Music ----------------------------------------------------------- #
pygame.mixer.music.load("Assets/Kartea/Sounds/Komiku_-_12_-_Bicycle.mp3")
pygame.mixer.music.set_volume(MUSIC_VOLUME)
pygame.mixer.music.play(-1)
"""


# Creation -------------------------------------------------------- #
pygame.mixer.init()
game = Game(SCREEN)
menu = Menu(SCREEN)
pause = Pause(SCREEN)
feedback = Feedback(SCREEN)
retrocede = Retrocede(SCREEN)
reinicia = Reinicia(SCREEN)
avanca = Avanca(SCREEN)

# Variables ------------------------------------------------------- #
state = "menu"

# Functions ------------------------------------------------------ #
def user_events():
    global state
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.display.quit()


def update():
    global state
    if state == "menu":
        if menu.update() == "game":
            state = "game"


    elif state == "game":
        if game.update() == "menu":
            state = "menu"
        if game.update() == "pause":
            state = "pause"
        if game.update() == "retroceder":
            # Gravar dados da sessao e retroceder nivel
            state = "retroceder"
        if game.update() == "reiniciar":
            # Gravar dados da sessao e reiniciar nivel
            state = "reiniciar"
        if game.update() == "avancar":
            # Gravar dados da sessao e avancar nivel
            state = "avancar"


    elif state == "pause":
        if pause.update() == "game":
            # Continua nivel atual
            state = "game"
        if pause.update() == "retroceder":
            # Gravar dados da sessao e retroceder nivel
            state = "retroceder"
        if pause.update() == "reiniciar":
            # Gravar dados da sessao e reiniciar nivel
            state = "reiniciar"
        if pause.update() == "avancar":
            # Gravar dados da sessao e avancar nivel
            state = "avancar"

    elif state == "feedback":
        if feedback.update() == "game":
            # Continua nivel atual
            state = "game"
        if feedback.update() == "retroceder":
            # Gravar dados da sessao e retroceder nivel
            state = "retroceder"
        if feedback.update() == "reiniciar":
            # Gravar dados da sessao e reiniciar nivel
            state = "reiniciar"
        if feedback.update() == "avancar":
            # Gravar dados da sessao e avancar nivel
            state = "avancar"

    elif state == "retroceder":
        if retrocede.update() == "game":
            # Continua nivel atual
            state = "game"

    elif state == "reiniciar":
        if reinicia.update() == "game":
            # Continua nivel atual
            state = "game"

    elif state == "avancar":
        if avanca.update() == "game":
            # Continua nivel atual
            state = "game"

    #pygame.display.update()
    mainClock.tick(FPS)


def main():
    try:
        pygame.init()
    except:
        print("Erro ao iniciar pygame")

    # Loop ------------------------------------------------------------ #
    while 1:
        # Buttons ----------------------------------------------------- #
        user_events()

        # Update ------------------------------------------------------ #
        update()

        # FPS
        if DRAW_FPS:
            fps_label = fps_font.render(f"FPS: {int(mainClock.get_fps())}", 1, (255, 200, 20))
            SCREEN.blit(fps_label, (5, 5))

        # Teclas de Atalho
        for event in pygame.event.get():
            # SAIR
            if event.type == pygame.QUIT:
                gameExit = True
                pygame.display.quit()
            if event.type == pygame.KEYDOWN:
                # SAIR (Q)
                if event.key == pygame.K_q:
                    gameExit = True
                    cv2.destroyWindow("Tela de Captura")
                    pygame.display.quit()
                # Pausar (Space)
                if event.key == pygame.K_SPACE:
                    print("Space KarTEA.py")

