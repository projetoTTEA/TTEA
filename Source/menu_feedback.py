import pygame
import sys

import image
import settings
from settings import *
from background import Background
import ui
from menu import Menu


class Feedback(Menu):
    def __init__(self, surface):
        self.surface = surface
        self.background = Background()
        self.background.background_menu()
        self.click_sound = pygame.mixer.Sound(f"Assets/Kartea/Sounds/point.wav")
        self.tipofeed = 0



        


    def draw(self):
        self.background.draw(self.surface)
        fundo = image.load("Assets/Kartea/Fundo.png")
        image.draw(self.surface, fundo, (0,0))
        self.tipofeed = settings.feedback
        trofeu = image.load("Assets/Kartea/trofeu - 25.png")
        if self.tipofeed == 1:
            trofeu = image.load("Assets/Kartea/trofeu")
        elif self.tipofeed == 2:
            trofeu = image.load("Assets/Kartea/trofeu - 50.png")
        elif self.tipofeed == 3:
            trofeu = image.load("Assets/Kartea/trofeu - 75.png")
        image.draw(self.surface, trofeu, (0,0))
        # draw title
        ui.draw_text(self.surface, GAME_TITLE, (SCREEN_WIDTH // 2, 120), COLORS["title"], font=FONTS["big"],
                     shadow=True, shadow_color=(255,255,255), pos_mode="center")

    def update(self):
        self.draw()

        if ui.button(self.surface, 2, 300 + BUTTONS_SIZES[1] * 4, "Jogar", click_sound=self.click_sound):
            return "game"

        if ui.button(self.surface, 1, 300 + BUTTONS_SIZES[1] * 4, "Sair", click_sound=self.click_sound):
            pygame.display.quit()
            sys.exit()
