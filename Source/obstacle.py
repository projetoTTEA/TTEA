import pygame
import random
import image
import time
from settings import *
from target import Target

class Obstacle(Target):
    def __init__(self):
        #size
        size = OBSTACLE_SIZES
        # moving
        road, start_pos = self.define_spawn_pos()

        # sprite
        self.tam = size
        self.rect = pygame.Rect(start_pos[0], start_pos[1], size[0], size[1])
        self.images = [image.load("Assets/Kartea/Obstaculo.png", size=size)]
        self.current_frame = 0
        self.current_pos = start_pos
        self.current_road = road
        self.animation_timer = 0

    def move(self):
        ve = TARGETS_MOVE_SPEED
        vel = [0, ve]
        #print('Road: ', self.current_road, ', Pos:', self.current_pos)

        if ve == 1:
            if self.current_pos[1] % 10 == 0:
                if self.current_road == 0:
                    vel = [-3, ve]
                elif self.current_road == 2:
                    vel = [3, ve]
            elif self.current_pos[1] % 5 == 0:
                self.rect.inflate_ip(3, 3)
                self.tam = (int(self.tam[0] + 3), int(self.tam[1] + 3))
                self.images = [image.load("Assets/Kartea/Obstaculo.png", size=self.tam)]
                if self.current_road == 0:
                        vel = [-3,ve]
                elif self.current_road == 2:
                        vel = [3,ve]
            else:
                vel = [0,ve]
        elif ve == 2:
            if self.current_pos[1] % 8 == 0:
                if self.current_road == 0:
                    vel = [-2, ve]
                elif self.current_road == 2:
                    vel = [2, ve]
            elif self.current_pos[1] % 4 == 0:
                self.rect.inflate_ip(3, 3)
                self.tam = (int(self.tam[0] + 3), int(self.tam[1] + 3))
                self.images = [image.load("Assets/Kartea/Obstaculo.png", size=self.tam)]
                if self.current_road == 0:
                        vel = [-2,ve]
                elif self.current_road == 2:
                        vel = [2,ve]
            else:
                vel = [0,ve]
        elif ve == 3:
            if self.current_pos[1] % 12 == 0:
                if self.current_road == 0:
                    vel = [-1, ve]
                elif self.current_road == 2:
                    vel = [1, ve]
            elif self.current_pos[1] % 6 == 0:
                self.rect.inflate_ip(3, 3)
                self.tam = (int(self.tam[0] + 3), int(self.tam[1] + 3))
                self.images = [image.load("Assets/Kartea/Obstaculo.png", size=self.tam)]
                if self.current_road == 0:
                        vel = [-1,ve]
                elif self.current_road == 2:
                        vel = [1,ve]
            else:
                vel = [0,ve]
        elif ve == 4:
            if self.current_pos[1] % 16 == 0:
                if self.current_road == 0:
                    vel = [-1, ve]
                elif self.current_road == 2:
                    vel = [1, ve]
            elif self.current_pos[1] % 8 == 0:
                self.rect.inflate_ip(3, 3)
                self.tam = (int(self.tam[0] + 3), int(self.tam[1] + 3))
                self.images = [image.load("Assets/Kartea/Obstaculo.png", size=self.tam)]
                if self.current_road == 0:
                        vel = [-1,ve]
                elif self.current_road == 2:
                        vel = [1,ve]
            else:
                vel = [0,ve]
        else:
            if self.current_pos[1] % 10 == 0:
                if self.current_road == 0:
                    vel = [-3, ve]
                elif self.current_road == 2:
                    vel = [3, ve]
            else:
                self.rect.inflate_ip(3, 3)
                self.tam = (int(self.tam[0] + 3), int(self.tam[1] + 3))
                self.images = [image.load("Assets/Kartea/Obstaculo.png", size=self.tam)]
                if self.current_road == 0:
                        vel = [-3,ve]
                elif self.current_road == 2:
                        vel = [3,ve]
        self.rect.move_ip(vel)

        self.current_pos = (self.current_pos[0] + vel[0], self.current_pos[1] + vel[1])

    def kill(self, surface, objects, sounds): # remove the mosquito from the list
        triste_fig = image.load('Assets/Kartea/triste.png')
        feliz_fig = image.load('Assets/Kartea/feliz.png')
        print(self.current_pos)
        if self.current_pos[1] > (SCREEN_HEIGHT):
            objects.remove(self)
            sounds["slap"].play()
            image.draw(surface, feliz_fig, (0, 0))
            # gravar detalhado obst desviado
            return 10
        else:
            objects.remove(self)
            sounds["screaming"].play()
            image.draw(surface,triste_fig,(0,0))
            # gravar detalhado obst colidido
            return 0



























