import pygame
import random
import time
import image
from settings import *

class Target:
    def __init__(self):
        #size
        #random_size_value = random.uniform(MOSQUITO_SIZE_RANDOMIZE[0], MOSQUITO_SIZE_RANDOMIZE[1])
        size = (int(TARGETS_SIZES[0]), int(TARGETS_SIZES[1]))
        # moving
        road ,start_pos = self.define_spawn_pos(size)

        # sprite
        self.tam = size
        self.rect = pygame.Rect(start_pos[0], start_pos[1], size[0]//1.4, size[1]//1.4)
        self.images = [image.load("Assets/Star.png", size=size)]
        self.current_frame = 0
        self.current_pos = start_pos
        self.current_road = road
        self.animation_timer = 0


    def define_spawn_pos(self, size): # define the start pos and moving vel of the mosquito
        road = random.randint(0,2) # 0 esq, 1 meio, 2 dir
        start_pos = OBJ_POS[road]
        return road, start_pos


    def move(self):
        ve = TARGETS_MOVE_SPEED
        vel = [0, ve]
        print('Road: ', self.current_road, ', Pos:', self.current_pos)
        if self.current_pos[1] % 10 == 0:
            if self.current_road == 0:
                vel = [-2, ve]
            elif self.current_road == 2:
                vel = [2, ve]
        elif self.current_pos[1] % 5 == 0:
            self.rect.inflate_ip(3, 3)
            self.tam = (int(self.tam[0] + 3), int(self.tam[1] + 3))
            self.images = [image.load("Assets/Star.png", size=self.tam)]
            if self.current_road == 0:
                    vel = [-2,ve]
            elif self.current_road == 2:
                    vel = [2,ve]
        else:
            vel = [0,ve]
        self.rect.move_ip(vel)

        self.current_pos = (self.current_pos[0] + vel[0], self.current_pos[1] + vel[1])



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


    def kill(self, targets): # remove the mosquito from the list
        targets.remove(self)
        return 1
