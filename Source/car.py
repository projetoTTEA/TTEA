import pygame

import arquivo
import image
from settings import *
import cv2

class Car:
    def __init__(self):
        self.orig_image = image.load("Assets/Carro.png", size=(CAR_SIZE, CAR_SIZE))
        self.image = self.orig_image.copy()
        self.image_smaller = image.load("Assets/Carro.png", size=(CAR_SIZE, CAR_SIZE))
        self.rect = pygame.Rect(SCREEN_WIDTH//2, SCREEN_HEIGHT//2, CAR_HITBOX_SIZE[0], CAR_HITBOX_SIZE[1])
        self.left_click = False
        #self.hand_tracking = HandTracking()


    def follow_mouse(self): # change the hand pos center at the mouse pos
        self.rect.center = pygame.mouse.get_pos()
        #self.hand_tracking.display_hand()

    def follow_mediapipe_hand(self, x, y):
        self.rect.center = (x, y)

    def draw_hitbox(self, surface):
        pygame.draw.rect(surface, (200, 60, 0), self.rect)


    def draw(self, surface):
        image.draw(surface, self.image, self.rect.center, pos_mode="center")

        if DRAW_HITBOX:
            self.draw_hitbox(surface)


    def on_target(self, targets): # return a list with all targets that collide with the hand hitbox
        return [target for target in targets if self.rect.colliderect(target.rect)]


    def kill_targets(self, targets, score, sounds): # will kill the targets that collide with the hand when the left mouse button is pressed
        for target in self.on_target(targets):
                target_score = target.kill(targets)
                score += target_score
                sounds["slap"].play()
                if target_score < 0:
                    sounds["screaming"].play()
        return score
