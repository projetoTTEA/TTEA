import pygame
import sys

import image
import settings
from settings import *
from background import Background
import ui


class Menu:
    def __init__(self, surface):
        self.surface = surface
        self.background = Background()
        self.background.background_menu()
        self.click_sound = pygame.mixer.Sound(f"Assets/Kartea/Sounds/point.wav")


    def draw(self):
        self.background.draw(self.surface)
        fundo = pygame.image.load("Assets/Kartea/Fundo.png").convert_alpha()
        image.draw(self.surface, fundo, (0,0))


    def update(self):
        self.draw()

        if settings.MENU == 'Inicial':
            # draw title
            ui.draw_text(self.surface, GAME_TITLE, (SCREEN_WIDTH // 2, 120), COLORS["title"], font=FONTS["big"],
                         shadow=True, shadow_color=(255, 255, 255), pos_mode="center")

            if ui.button(self.surface, 0, 300, "Jogar", click_sound=self.click_sound):
                return "game"

            if ui.button(self.surface, 0, 300 + BUTTONS_SIZES[1] * 4, "Sair", click_sound=self.click_sound):
                pygame.quit()
                sys.exit()

        elif settings.MENU == 'Pause':
            # draw title
            ui.draw_text(self.surface, "Pause", (SCREEN_WIDTH // 2, 120), COLORS["title"], font=FONTS["big"],
                         shadow=True, shadow_color=(255, 255, 255), pos_mode="center")

            if ui.button(self.surface, 0, 300, "Continuar", click_sound=self.click_sound):
                return "game"

            if ui.button(self.surface, 1, 300 + BUTTONS_SIZES[1] * 2, "Retroceder", click_sound=self.click_sound):
                return "prev"

            if ui.button(self.surface, 0, 300 + BUTTONS_SIZES[1] * 2, "Reiniciar", click_sound=self.click_sound):
                return "rest"

            if ui.button(self.surface, 2, 300 + BUTTONS_SIZES[1] * 2, "Avançar", click_sound=self.click_sound):
                return "next"

            if ui.button(self.surface, 0, 300 + BUTTONS_SIZES[1] * 4, "Sair", click_sound=self.click_sound):
                pygame.quit()
                sys.exit()

        elif settings.MENU == 'Feedback_1':

            trofeu = image.load("Assets/Kartea/trofeu - 25.png")
            image.draw(self.surface, trofeu, (0, 0))

            if ui.button(self.surface, 2, 300 + BUTTONS_SIZES[1] * 4, "Jogar", click_sound=self.click_sound):
                return "prev"

            if ui.button(self.surface, 1, 300 + BUTTONS_SIZES[1] * 4, "Sair", click_sound=self.click_sound):
                pygame.quit()
                sys.exit()

        elif settings.MENU == 'Feedback_2':

            trofeu = image.load("Assets/Kartea/trofeu - 50.png")
            image.draw(self.surface, trofeu, (0, 0))

            if ui.button(self.surface, 2, 300 + BUTTONS_SIZES[1] * 4, "Jogar", click_sound=self.click_sound):
                return "rest"

            if ui.button(self.surface, 1, 300 + BUTTONS_SIZES[1] * 4, "Sair", click_sound=self.click_sound):
                pygame.quit()
                sys.exit()

        elif settings.MENU == 'Feedback_3':

            trofeu = image.load("Assets/Kartea/trofeu - 75.png")
            image.draw(self.surface, trofeu, (0, 0))

            if ui.button(self.surface, 2, 300 + BUTTONS_SIZES[1] * 4, "Jogar", click_sound=self.click_sound):
                return "next"

            if ui.button(self.surface, 1, 300 + BUTTONS_SIZES[1] * 4, "Sair", click_sound=self.click_sound):
                pygame.quit()
                sys.exit()