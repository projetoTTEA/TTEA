import pygame
import sys
from settings import *
from background import Background
import ui


class Menu:
    def __init__(self, surface):
        self.surface = surface
        self.background = Background()
        self.click_sound = pygame.mixer.Sound(f"Assets/Sounds/slap.wav")


    def draw(self):
        self.background.draw(self.surface)
        # draw title
        ui.draw_text(self.surface, GAME_TITLE, (SCREEN_WIDTH // 2, 120), COLORS["title"], font=FONTS["big"],
                     shadow=True, shadow_color=(255,255,255), pos_mode="center")


    def update(self):
        self.draw()

        if ui.button(self.surface, 0, 320, "Jogar", click_sound=self.click_sound):
            return "game"

        if ui.button(self.surface, 1, 320 + BUTTONS_SIZES[1] * 2, "Retroceder", click_sound=self.click_sound):
            return "game"

        if ui.button(self.surface, 0, 320 + BUTTONS_SIZES[1] * 2, "Reiniciar", click_sound=self.click_sound):
            return "game"

        if ui.button(self.surface, 2, 320 + BUTTONS_SIZES[1] * 2, "Avançar", click_sound=self.click_sound):
            return "game"

        if ui.button(self.surface, 0, 320 + BUTTONS_SIZES[1] * 4, "Sair", click_sound=self.click_sound):
            pygame.quit()
            sys.exit()
