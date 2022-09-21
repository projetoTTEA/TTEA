import pygame
import sys

import image
from settings import *
from background import Background
import ui
from menu import Menu


class Avanca(Menu):
    def __init__(self, surface):
        self.surface = surface
        self.background = Background()
        self.background.background_menu()
        self.click_sound = pygame.mixer.Sound(f"Assets/Kartea/Sounds/point.wav")


    def draw(self):
        self.background.draw(self.surface)
        fundo = image.load("Assets/Kartea/Fundo.png")
        image.draw(self.surface, fundo, (0,0))
        # draw title
        ui.draw_text(self.surface, "Avançando Nível", (SCREEN_WIDTH // 2, 120), COLORS["title"], font=FONTS["big"], shadow=True, shadow_color=(255,255,255), pos_mode="center")

    def update(self):
        self.draw()

        if ui.button(self.surface, 2, 300 + BUTTONS_SIZES[1] * 4, "Jogar", click_sound=self.click_sound):
            return "game"

        if ui.button(self.surface, 1, 300 + BUTTONS_SIZES[1] * 4, "Sair", click_sound=self.click_sound):
            pygame.display.quit()
            sys.exit()
