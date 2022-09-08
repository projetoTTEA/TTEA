import pygame
import random
import time
import image
from settings import *

roadW = 400 #Tamanho pista
segL = 200 # Tamanho segmento
camD = 3 # camera depth

class Target:
    def __init__(self):
        #size
        size = TARGETS_SIZES
        # moving
        road ,start_pos = self.define_spawn_pos()

        # sprite
        self.tam = size
        self.rect = pygame.Rect(start_pos[0], start_pos[1], size[0], size[1])
        self.images = [image.load("Assets/Kartea/Star.png", size=size)]
        self.current_frame = 0
        self.current_pos = start_pos
        self.current_road = road
        self.animation_timer = 0
        self.line = None

    def define_spawn_pos(self): # define the start pos and moving vel of the mosquito
        road = random.randint(0,2) # 0 esq, 1 meio, 2 dir
        start_pos = OBJ_POS[road]
        return road, start_pos

    def define_pos(self, x, y): # define the start pos and moving vel of the mosquito
        vx = x + self.images[0].get_width()
        vy = y + self.images[0].get_height()
        self.rect = pygame.Rect(x, y, self.rect.width, self.rect.height)


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
                self.images = [image.load("Assets/Kartea/Star.png", size=self.tam)]
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
                self.images = [image.load("Assets/Kartea/Star.png", size=self.tam)]
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
                self.images = [image.load("Assets/Kartea/Star.png", size=self.tam)]
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
                self.images = [image.load("Assets/Kartea/Star.png", size=self.tam)]
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
                self.images = [image.load("Assets/Kartea/Star.png", size=self.tam)]
                if self.current_road == 0:
                        vel = [-3,ve]
                elif self.current_road == 2:
                        vel = [3,ve]
        self.rect.move_ip(vel)

        self.current_pos = (self.current_pos[0] + vel[0], self.current_pos[1] + vel[1])

    def move(self, x, y):
        vel = [x - self.current_pos[0], y - self.current_pos[1]]
        print("vel: ", vel)
        self.rect.move_ip(vel)
        self.current_pos = (x,y)

    def att_current_pos(self, x, y):
        self.current_pos = (x,y)

    def animate(self): # change the frame of the insect when needed
        t = time.time()
        if t > self.animation_timer:
            self.animation_timer = t + ANIMATION_SPEED
            self.current_frame += 1
            if self.current_frame > len(self.images)-1:
                self.current_frame = 0


    def draw_hitbox(self, surface):
        pygame.draw.rect(surface, (200, 60, 0), self.rect)



    def draw(self, surface):
        self.animate()
        image.draw(surface, self.images[self.current_frame], self.rect.center, pos_mode="center")
        if DRAW_HITBOX:
            self.draw_hitbox(surface)


    def kill(self, surface, targets, sounds): # remove the mosquito from the list
        triste_fig = image.load('Assets/Kartea/triste.png')
        feliz_fig = image.load('Assets/Kartea/feliz.png')
        print(self.current_pos)
        if self.current_pos[1] > (SCREEN_HEIGHT):
            targets.remove(self)
            sounds["screaming"].play()
            image.draw(surface,triste_fig,(0,0))
            return 0
        else:
            targets.remove(self)
            sounds["slap"].play()
            image.draw(surface, feliz_fig, (0, 0))
            return 10
