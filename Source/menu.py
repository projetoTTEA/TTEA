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
        fundo = image.load("Assets/Kartea/Fundo.png", size=(SCREEN_WIDTH,SCREEN_HEIGHT))
        image.draw(self.surface, fundo, (0,0))

    def draw_Feedback(self):
        ui.draw_text(self.surface, "Feedback", ((SCREEN_WIDTH // 2) + 50, 100), COLORS["title"], font=FONTS["medium"],
                         shadow=True, shadow_color=(255, 255, 255))
        ui.draw_text(self.surface, "Quantidade", ((SCREEN_WIDTH // 2) + 250, 100), COLORS["title"], font=FONTS["medium"],
                         shadow=True, shadow_color=(255, 255, 255))

        ui.draw_text(self.surface, "Pontuação", ((SCREEN_WIDTH // 2) + 50, 130), COLORS["title"], font=FONTS["medium"],
                         shadow=True, shadow_color=(255, 255, 255))
        ui.draw_text(self.surface, str(settings.score), ((SCREEN_WIDTH // 2) + 250, 130), COLORS["title"], font=FONTS["medium"],
                         shadow=True, shadow_color=(255, 255, 255))

        ui.draw_text(self.surface, "Movimentos", ((SCREEN_WIDTH // 2) + 50, 160), COLORS["title"], font=FONTS["medium"],
                         shadow=True, shadow_color=(255, 255, 255))
        ui.draw_text(self.surface, str(settings.movimento), ((SCREEN_WIDTH // 2) + 250, 160), COLORS["title"], font=FONTS["medium"],
                         shadow=True, shadow_color=(255, 255, 255))

        ui.draw_text(self.surface, "Alvos Gerados", ((SCREEN_WIDTH // 2) + 50, 190), COLORS["title"], font=FONTS["medium"],
                         shadow=True, shadow_color=(255, 255, 255))
        ui.draw_text(self.surface, str(settings.Alvo), ((SCREEN_WIDTH // 2) + 250, 190), COLORS["title"], font=FONTS["medium"],
                         shadow=True, shadow_color=(255, 255, 255))

        ui.draw_text(self.surface, "Alvos Colididos", ((SCREEN_WIDTH // 2) + 50, 220), COLORS["title"], font=FONTS["medium"],
                         shadow=True, shadow_color=(255, 255, 255))
        ui.draw_text(self.surface, str(settings.Alvo_c), ((SCREEN_WIDTH // 2) + 250, 220), COLORS["title"], font=FONTS["medium"],
                         shadow=True, shadow_color=(255, 255, 255))

        ui.draw_text(self.surface, "Alvos Desviados", ((SCREEN_WIDTH // 2) + 50, 250), COLORS["title"], font=FONTS["medium"],
                         shadow=True, shadow_color=(255, 255, 255))
        ui.draw_text(self.surface, str(settings.Alvo_d), ((SCREEN_WIDTH // 2) + 250, 250), COLORS["title"], font=FONTS["medium"],
                         shadow=True, shadow_color=(255, 255, 255))

        ui.draw_text(self.surface, "Obst. Gerados", ((SCREEN_WIDTH // 2) + 50, 280), COLORS["title"], font=FONTS["medium"],
                         shadow=True, shadow_color=(255, 255, 255))
        ui.draw_text(self.surface, str(settings.Obst), ((SCREEN_WIDTH // 2) + 250, 280), COLORS["title"], font=FONTS["medium"],
                         shadow=True, shadow_color=(255, 255, 255))

        ui.draw_text(self.surface, "Obst. Desviados", ((SCREEN_WIDTH // 2) + 50, 310), COLORS["title"], font=FONTS["medium"],
                         shadow=True, shadow_color=(255, 255, 255))
        ui.draw_text(self.surface, str(settings.Obst_d), ((SCREEN_WIDTH // 2) + 250, 310), COLORS["title"], font=FONTS["medium"],
                         shadow=True, shadow_color=(255, 255, 255))

        ui.draw_text(self.surface, "Obst. Colididos", ((SCREEN_WIDTH // 2) + 50, 340), COLORS["title"], font=FONTS["medium"],
                         shadow=True, shadow_color=(255, 255, 255))
        ui.draw_text(self.surface, str(settings.Obst_c), ((SCREEN_WIDTH // 2) + 250, 340), COLORS["title"], font=FONTS["medium"],
                         shadow=True, shadow_color=(255, 255, 255))



    def update(self):
        self.draw()

        if settings.MENU == 'Inicial':
            # draw title
            ui.draw_text(self.surface, GAME_TITLE, (SCREEN_WIDTH // 2, 120), COLORS["title"], font=FONTS["big"],
                         shadow=True, shadow_color=(255, 255, 255), pos_mode="center")

            if ui.button(self.surface, 0, 300, "Jogar", click_sound=self.click_sound):
                return "game"

            if ui.button(self.surface, 0, 300 + BUTTONS_SIZES[1] * 4, "Sair", click_sound=self.click_sound):
                pygame.display.quit()
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
                pygame.display.quit()
                sys.exit()

        elif settings.MENU == 'Feedback_1':

            trofeu = image.load("Assets/Kartea/trofeu - 25.png")
            image.draw(self.surface, trofeu, (0, 0))

            self.draw_Feedback()

            if ui.button(self.surface, 2, 300 + BUTTONS_SIZES[1] * 4, "Jogar", click_sound=self.click_sound):
                return "prev"

            if ui.button(self.surface, 1, 300 + BUTTONS_SIZES[1] * 4, "Sair", click_sound=self.click_sound):
                pygame.display.quit()
                sys.exit()

        elif settings.MENU == 'Feedback_2':

            trofeu = image.load("Assets/Kartea/trofeu - 50.png")
            image.draw(self.surface, trofeu, (0, 0))

            self.draw_Feedback()

            if ui.button(self.surface, 2, 300 + BUTTONS_SIZES[1] * 4, "Jogar", click_sound=self.click_sound):
                return "rest"

            if ui.button(self.surface, 1, 300 + BUTTONS_SIZES[1] * 4, "Sair", click_sound=self.click_sound):
                pygame.display.quit()
                sys.exit()

        elif settings.MENU == 'Feedback_3':

            trofeu = image.load("Assets/Kartea/trofeu - 75.png")
            image.draw(self.surface, trofeu, (0, 0))

            self.draw_Feedback()

            if ui.button(self.surface, 2, 300 + BUTTONS_SIZES[1] * 4, "Jogar", click_sound=self.click_sound):
                return "next"

            if ui.button(self.surface, 1, 300 + BUTTONS_SIZES[1] * 4, "Sair", click_sound=self.click_sound):
                pygame.display.quit()
                sys.exit()