import pygame
import time
import random

import arquivo
from settings import *
from background import Background
from car import Car
from pose_tracking import PoseTracking
from target import Target
from obstacle import Obstacle
import cv2
import ui

class Game:
    def __init__(self, surface):
        self.surface = surface
        self.background = Background()

        # Load camera
        self.cap = cv2.VideoCapture(0)

        self.sounds = {}
        self.sounds["slap"] = pygame.mixer.Sound(f"Assets/Kartea/Sounds/point.wav")
        self.sounds["slap"].set_volume(SOUNDS_VOLUME)
        self.sounds["screaming"] = pygame.mixer.Sound(f"Assets/Kartea/Sounds/miss.wav")
        self.sounds["screaming"].set_volume(SOUNDS_VOLUME)
        TARGETS_MOVE_SPEED = arquivo.get_Nivel()


    def reset(self): # reset all the needed variables
        self.pose_tracking = PoseTracking()
        self.car = Car()
        self.targets = []
        self.targets_spawn_timer = 0
        self.score = 0
        self.game_start_time = time.time()


    def spawn_targets(self):
        t = time.time()
        if t > self.targets_spawn_timer:
            self.targets_spawn_timer = t + TARGETS_SPAWN_TIME

            # increase the probability that the insect will be a bee over time
            nb = (GAME_DURATION-self.time_left)/GAME_DURATION * 100  / 2  # increase from 0 to 50 during all  the game (linear)
            fase = arquivo.get_K_FASE('Jogadores/' + arquivo.get_Player() + '_KarTEA_config.csv')
            #print(fase)
            if fase == 1:
                self.targets.append(Target())
            elif fase == 2:
                self.targets.append(Obstacle())
            else:
                if random.randint(0, 100) < 50:
                    self.targets.append(Obstacle())
                else:
                    self.targets.append(Target())

    def load_camera(self):
        _, self.frame = self.cap.read()

    def set_feet_position(self):
        self.frame = self.pose_tracking.scan_feets(self.frame)
        (x, y) = self.pose_tracking.get_feet_center()
        Y = SCREEN_HEIGHT - CAR_SIZE/2
        self.car.rect.center = (x, Y)
        #print("x: ", x ," y: ", y)
        """
        if x < SCREEN_WIDTH/3:
            self.car.rect.center = (200, 550)
        elif x >= SCREEN_WIDTH/3 and x <= 2*SCREEN_WIDTH/3:
            self.car.rect.center = (400, 550)
        else:
            self.car.rect.center = (600, 550)
        """

    def draw(self):
        # draw the background
        self.background.draw(self.surface)
        # draw the targets
        for insect in self.targets:
            insect.draw(self.surface)
        # draw the car
        self.car.draw(self.surface)
        # draw the score
        ui.draw_text(self.surface, f"Pontuação : {self.score}", (650, 5), COLORS["score"], font=FONTS["medium"],
                     shadow=True, shadow_color=(255,255,255))
        # draw the time left
        timer_text_color = (160, 40, 0) if self.time_left < 5 else COLORS["timer"] # change the text color if less than 5 s left
        ui.draw_text(self.surface, f"Tempo : {self.time_left}", (350, 5), timer_text_color, font=FONTS["medium"],
                     shadow=True, shadow_color=(255,255,255))
        # draw the fase e nivel
        timer_text_color = (160, 40, 0) if self.time_left < 5 else COLORS["timer"] # change the text color if less than 5 s left
        ui.draw_text(self.surface, f"Fase : {arquivo.get_Fase()}", (5, 5), timer_text_color, font=FONTS["medium"],
                     shadow=True, shadow_color=(255,255,255))
        timer_text_color = (160, 40, 0) if self.time_left < 5 else COLORS["timer"] # change the text color if less than 5 s left
        ui.draw_text(self.surface, f"Nivel : {arquivo.get_Nivel()}", (5, 25), timer_text_color, font=FONTS["medium"],
                     shadow=True, shadow_color=(255,255,255))


    def game_time_update(self):
        self.time_left = max(round(GAME_DURATION - (time.time() - self.game_start_time), 1), 0)



    def update(self):

        self.load_camera()
        self.set_feet_position()
        self.game_time_update()

        self.draw()

        if self.time_left > 0:
            self.spawn_targets()
            (x, y) = self.pose_tracking.get_feet_center()
            self.car.rect.center = (x, y)
            self.car.left_click = self.pose_tracking.feet_closed
            #print(arquivo.get_Player()) #checando qual é o jogador selecionado
            self.score = self.car.kill_targets(self.surface, self.targets, self.score, self.sounds)
            for alvo in self.targets:
                alvo.move()
                if alvo.current_pos[1] > (SCREEN_HEIGHT-100):
                    self.score += alvo.kill(self.surface, self.targets, self.sounds)

        else: # when the game is over
            if ui.button(self.surface, 540, "Continue", click_sound=self.sounds["slap"]):
                return "menu"

        cv2.line(self.frame, (pontos_calibracao[0]), (pontos_calibracao[1]), (verde), 2)
        cv2.line(self.frame, (pontos_calibracao[1]), (pontos_calibracao[3]), (verde), 2)
        cv2.line(self.frame, (pontos_calibracao[2]), (pontos_calibracao[0]), (verde), 2)
        cv2.line(self.frame, (pontos_calibracao[2]), (pontos_calibracao[3]), (verde), 2)

        cv2.circle(self.frame, (pontos_calibracao[0]), 5, azul, 3)
        cv2.circle(self.frame, (pontos_calibracao[1]), 5, azul, 3)
        cv2.circle(self.frame, (pontos_calibracao[2]), 5, azul, 3)
        cv2.circle(self.frame, (pontos_calibracao[3]), 5, azul, 3)

        cv2.imshow("Tela de Captura", self.frame)
        cv2.waitKey(1)
