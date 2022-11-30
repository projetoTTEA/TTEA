import image
import pygame, time, sys, math
from typing import List
from settings import *
from line import Line

roadW = 400 #Tamanho pista
segL = 200 # Tamanho segmento
camD = 3 # camera depth

dark_grass = pygame.Color(0,154,0)
light_grass = pygame.Color(16,200,16)
dark_rumble = pygame.Color(255,0,0)
light_rumble = pygame.Color(255,255,255)
dark_road = pygame.Color(75,75,75)
light_road = pygame.Color(107,107,107)
finish_light = pygame.Color(255,255,255)
finish_dark = pygame.Color(0,0,0)

def drawQuad(
        surface: pygame.Surface,
        color: pygame.Color,
        x1: int,
        y1: int,
        w1: int,
        x2: int,
        y2: int,
        w2: int,
    ):
    pygame.draw.polygon(
        surface, color, [(x1-w1, y1), (x2-w2, y2), (x2+w2, y2), (x1+w1, y1)]
    )

class Background:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.last_time = time.time()
        self.time_left = time.time()
        self.dt = 0

        # sprites
        self.sprite_arv_esq = pygame.image.load("Assets/Kartea/5.png").convert_alpha()
        self.sprite_arv_dir = pygame.image.load("Assets/Kartea/5,1.png").convert_alpha()


        # background
        self.background_image = pygame.image.load("Assets/Kartea/bg.png").convert_alpha()
        self.background_surface = pygame.Surface(
            (self.background_image.get_width() * 2, self.background_image.get_height())
        )
        self.background_surface.blit(self.background_image, (0, 0))
        self.background_surface.blit(self.background_image, (self.background_image.get_width(), 0))
        self.background_rect = self.background_surface.get_rect(topleft=(0, 0))

        #objectives
        self.Objectives = []
        self.distObj = (150, 100, 50)

        self.lines: List[Line] = []
        for i in range(5000):
            line = Line()
            line.z = i * segL + 0.00001

            grass_color = light_grass if (i // 3) % 2 else dark_grass
            rumble_color = light_rumble if (i // 3) % 2 else dark_rumble
            road_color = light_road
            div_color = light_rumble if (i // 3) % 2 else light_road

            line.grass_color = grass_color
            line.rumble_color = rumble_color
            line.road_color = road_color
            line.div_color = div_color

            if i % 70 == 0:
                line.spriteX = -2.5
                line.sprite = self.sprite_arv_esq
                line.sprite2X = 1
                line.sprite2 = self.sprite_arv_dir

            self.lines.append(line)
        self.N = len(self.lines)
        self.pos = 0
        self.playerX = 0
        self.playerY = 1500

        self.speed = 0

    def speed1(self):
        self.speed = segL

    def speed2(self):
        self.speed = 2*segL

    def speed3(self):
        self.speed = 3*segL

    def stop(self):
        self.speed = 0

    def background_menu(self):
        self.image = image.load("Assets/Kartea/Background_Menu.png", size=(SCREEN_WIDTH, SCREEN_HEIGHT),convert="default")

    def get_startPos(self):
        return (self.pos // segL) + 200


    def draw(self, surface):
        surface.blit(self.background_surface, self.background_rect)

        surface.fill("black")
        surface.blit(self.background_surface, self.background_rect)

        self.pos += self.speed

        while self.pos >= self.N * segL:
            self.pos -= self.N * segL
        while self.pos < 0:
            self.pos += self.N * segL

        startPos = self.pos // segL

        x = dx = 0.0

        camH = self.playerY + self.lines[startPos].y

        maxy = SCREEN_HEIGHT * 2

        for n in range(startPos, startPos + 300):
            current = self.lines[n % self.N]
            current.project(self.playerX - x, camH, self.pos - (self.N * segL if n >= self.N else 0))
            x += dx
            dx += current.curve

            current.clip = maxy

            if current.Y >= maxy:
                continue
            maxy = current.Y

            prev = self.lines[(n - 1) % self.N]

            drawQuad(surface, current.grass_color, 0, prev.Y, SCREEN_WIDTH, 0, current.Y, SCREEN_WIDTH)
            drawQuad(surface, current.rumble_color, prev.X, prev.Y, prev.W * 1.2, current.X, current.Y, current.W * 1.2)
            drawQuad(surface, current.road_color, prev.X, prev.Y, prev.W, current.X, current.Y, current.W)
            drawQuad(surface, current.div_color, prev.X, prev.Y, prev.W * 0.35, current.X, current.Y, current.W * 0.35)
            drawQuad(surface, current.road_color, prev.X, prev.Y, prev.W * 0.3, current.X, current.Y, current.W * 0.3)

        #spawn targets

        for n in range(startPos + 300, startPos, -1):
            if self.lines[n % self.N].sprite != None:
                self.lines[n % self.N].drawSprite(surface)
            if self.lines[n % self.N].sprite2 != None:
                self.lines[n % self.N].drawSprite2(surface)
            if self.lines[n % self.N].target != None:
                self.lines[n % self.N].drawTarget(surface)
                self.lines[n % self.N].target.att_current_pos(self.lines[n % self.N].target.current_pos[0], self.lines[n % self.N].Y)
