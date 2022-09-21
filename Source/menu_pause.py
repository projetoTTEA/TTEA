import pygame
import sys

import image
from settings import *
from background import Background
import ui
from menu import Menu


class Pause(Menu):
    def __init__(self, surface):
        self.surface = surface
        self.background = Background()
        self.background.background_menu()
        self.click_sound = pygame.mixer.Sound(f"Assets/Kartea/Sounds/point.wav")

    def update(self):
        self.draw()

        if ui.button(self.surface, 0, 300, "Continuar", click_sound=self.click_sound):
            return "game"

        if ui.button(self.surface, 1, 300 + BUTTONS_SIZES[1] * 2, "Retroceder", click_sound=self.click_sound):
            return "retroceder"

        if ui.button(self.surface, 0, 300 + BUTTONS_SIZES[1] * 2, "Reiniciar", click_sound=self.click_sound):
            return "reiniciar"

        if ui.button(self.surface, 2, 300 + BUTTONS_SIZES[1] * 2, "Avançar", click_sound=self.click_sound):
            return "avancar"

        if ui.button(self.surface, 0, 300 + BUTTONS_SIZES[1] * 4, "Sair", click_sound=self.click_sound):
            pygame.display.quit()
            sys.exit()
