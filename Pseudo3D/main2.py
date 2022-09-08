import pygame, time, sys, math
from typing import List

import arquivo
from settings import *
import cv2
import ui

WINDOW_WIDTH =800
WINDOW_HEIGHT = 600

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
        self.spriteX = 0.0
        self.clip = 0.0
        self.sprite: pygame.Surface = None
        self.sprite_rect: pygame.Rect = None
        self.grass_color: pygame.Color = "black"
        self.rumble_color: pygame.Color = "black"
        self.road_color: pygame.Color = "black"
        self.div_color: pygame.Color = "black"


    def project(self, camX: int, camY: int, camZ: int):
        self.scale = camD / (self.z - camZ)
        self.X = (1 + self.scale * (self.x - camX)) * WINDOW_WIDTH / 2
        self.Y = (1 - self.scale * (self.y - camY)) * WINDOW_HEIGHT / 5
        self.W = self.scale * roadW * WINDOW_WIDTH / 2

    def drawSprite(self, draw_surface: pygame.Surface):
        if self.sprite is None:
            return
        w = self.sprite.get_width()
        h = self.sprite.get_height()
        destX = self.X + self.scale * self.spriteX * WINDOW_WIDTH / 2
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

class Car:
    def __init__(self):
        self.X = self.Y = 0.0
        self.sprite: pygame.Surface = pygame.image.load("Assets/Kartea/Carro2.png").convert_alpha()
        self.sprite_rect: pygame.Rect = None

    def drawCar(self, draw_surface: pygame.Surface, X, Y):
        if self.sprite is None:
            return
        self.X = X
        self.Y = Y

        w = self.sprite.get_width()
        h = self.sprite.get_height()
        destX = self.X - w / 2
        destY = self.Y - h / 2

        draw_surface.blit(self.sprite, (destX, destY))

class GameWindow:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Pseudo 3D")
        self.window_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.last_time = time.time()
        self.time_left = time.time()
        self.dt = 0

        #sprites
        self.sprite_1 = pygame.image.load("images/1.png").convert_alpha()
        self.sprite_2 = pygame.image.load("images/2.png").convert_alpha()
        self.sprite_3 = pygame.image.load("images/3.png").convert_alpha()
        self.sprite_4 = pygame.image.load("images/4.png").convert_alpha()
        self.sprite_5 = pygame.image.load("images/5.png").convert_alpha()
        self.sprite_6 = pygame.image.load("images/6.png").convert_alpha()
        self.sprite_7 = pygame.image.load("images/7.png").convert_alpha()
        self.sprite_star = pygame.image.load("images/Star100.png").convert_alpha()
        self.car = Car()


        #background
        self.background_image = pygame.image.load("images/bg.png").convert_alpha()
        self.background_surface = pygame.Surface(
            (self.background_image.get_width()*2, self.background_image.get_height())
        )
        self.background_surface.blit(self.background_image, (0,0))
        self.background_surface.blit(self.background_image, (self.background_image.get_width(),0))
        self.background_rect = self.background_surface.get_rect(topleft=(0,0))
        self.window_surface.blit(self.background_surface, self.background_rect)

        #game
        self.score = 0


    def run(self):
        lines: List[Line] = []
        for i in range(20000):
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
            lines.append(line)

        N = len(lines)
        pos = 0
        playerX = 0
        playerY = 1500

        carX = WINDOW_WIDTH / 2
        carY = WINDOW_HEIGHT - (self.car.sprite.get_height())/2

        speed = segL
        while True:
            self.window_surface.fill("black")
            self.window_surface.blit(self.background_surface, self.background_rect)

            pos += speed

            while pos>= N * segL:
                pos -= N * segL
            while pos < 0:
                pos += N * segL

            startPos = pos // segL

            x = dx = 0.0

            camH = playerY + lines[startPos].y

            maxy = WINDOW_HEIGHT*2

            for n in range(startPos, startPos + 300):
                current = lines[n % N]
                current.project(playerX - x, camH,pos - (N * segL if n >= N else 0))
                x += dx
                dx += current.curve

                current.clip = maxy

                if current.Y >= maxy:
                    continue
                maxy = current.Y

                prev = lines[(n-1)%N]


                drawQuad(self.window_surface, current.grass_color,  0,      prev.Y, WINDOW_WIDTH,   0,          current.Y, WINDOW_WIDTH     )
                drawQuad(self.window_surface, current.rumble_color, prev.X, prev.Y, prev.W*1.2,     current.X,  current.Y, current.W*1.2    )
                drawQuad(self.window_surface, current.road_color,   prev.X, prev.Y, prev.W,         current.X,  current.Y, current.W        )
                drawQuad(self.window_surface, current.div_color,    prev.X, prev.Y, prev.W*0.35,    current.X,  current.Y, current.W*0.35   )
                drawQuad(self.window_surface, current.road_color,   prev.X, prev.Y, prev.W*0.3,     current.X,  current.Y, current.W*0.3    )

            for n in range(startPos + 300, startPos, -1):
                lines[n%N].drawSprite(self.window_surface)

            pygame.display.update()
            self.clock.tick(40)


if __name__ == '__main__':
    game = GameWindow()
    game.run()
