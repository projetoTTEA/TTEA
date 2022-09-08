import image
import pygame, time, sys, math
from typing import List
from settings import *
from target import Target

roadW = 400 #Tamanho pista
segL = 200 # Tamanho segmento
camD = 3 # camera depth

dark_grass = pygame.Color(0,154,0)
light_grass = pygame.Color(16,200,16)
dark_rumble = pygame.Color(255,0,0)
light_rumble = pygame.Color(255,255,255)
dark_road = pygame.Color(75,75,75)
light_road = pygame.Color(107,107,107)

class Line:
    def __init__(self):
        self.x = self.y = self.z = 0.0 # posição 3D
        self.X = self.Y = self.W = 0.0 # posição 2D
        self.scale = 0.0 # escala de projeção
        self.curve = 0.0
        self.clip = 0.0

        self.spriteX = 0.0
        self.sprite: pygame.Surface = None
        self.sprite_rect: pygame.Rect = None

        self.targetX = 0.0
        self.target: Target() = None
        self.target_rect: pygame.Rect = None

        self.grass_color: pygame.Color = "black"
        self.rumble_color: pygame.Color = "black"
        self.road_color: pygame.Color = "black"
        self.div_color: pygame.Color = "black"

    def project(self, camX: int, camY: int, camZ: int):
        self.scale = camD / (self.z - camZ)
        self.X = (1 + self.scale * (self.x - camX)) * SCREEN_WIDTH / 2
        self.Y = (1 - self.scale * (self.y - camY)) * SCREEN_HEIGHT / 5
        self.W = self.scale * roadW * SCREEN_WIDTH / 2

    def drawSprite(self, draw_surface: pygame.Surface):
        if self.sprite is None:
            return
        w = self.sprite.get_width()
        h = self.sprite.get_height()
        destX = self.X + self.scale * self.spriteX * SCREEN_WIDTH / 2
        destY = self.Y + 4
        destW = w * self.W / 266
        destH = h * self.W / 266

        destX += destW * self.spriteX
        destY += destH * -1

        clipH = destY * self.spriteX
        if clipH < 0:
            clipH = 0
        if clipH >= destH:
            return

        if destW > (2*w):
            return

        scaled_sprite = pygame.transform.scale(self.sprite,(destW, destH))
        draw_surface.blit(scaled_sprite, (destX, destY))

    def drawTarget(self, draw_surface: pygame.Surface):
        if self.target is None:
            return
        w = self.target.images[0].get_width()
        h = self.target.images[0].get_height()

        #self.target.define_spawn_pos()

        if self.target.current_road == 0:
            self.targetX = -2.25
        elif self.target.current_road == 1:
            self.targetX = -0.5
        else:
            self.targetX = 1.25

        destX = self.X + self.scale * self.targetX * SCREEN_WIDTH / 2
        destY = self.Y + 4
        destW = w * self.W / 266
        destH = h * self.W / 266

        destX += destW * self.targetX
        destY += destH * -1

        self.target.define_pos(destX, destY)

        clipH = destY + destH - self.clip
        if clipH < 0:
            clipH = 0
        if clipH >= destH:
            return

        if destW > 1.5*w:
            return

        scaled_sprite = pygame.transform.scale(self.target.images[0],(destW, destH))
        draw_surface.blit(scaled_sprite, (destX, destY))
        #self.target.move(destX, destY)
        if DRAW_HITBOX:
            self.target.draw_hitbox(draw_surface)

