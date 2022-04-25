import pygame
import random
import image
from settings import *
from target import Target

class Obstacle(Target):
    def __init__(self):
        #size
        size = OBSTACLE_SIZES
        # moving
        road, start_pos = self.define_spawn_pos(size)

        # sprite
        self.tam = size
        self.rect = pygame.Rect(start_pos[0], start_pos[1], size[0]//1.4, size[1]//1.4)
        self.images = [image.load("Assets/Obstaculo.png", size=size)]
        self.current_frame = 0
        self.current_pos = start_pos
        self.current_road = road
        self.animation_timer = 0

    def move(self):
        ve = TARGETS_MOVE_SPEED
        vel = [0, ve]
        print('Road: ', self.current_road, ', Pos:', self.current_pos)
        if self.current_pos[1] % 10 == 0:
            if self.current_road == 0:
                vel = [-3, ve]
            elif self.current_road == 2:
                vel = [3, ve]
        elif self.current_pos[1] % 5 == 0:
            self.rect.inflate_ip(3, 3)
            self.tam = (int(self.tam[0] + 3), int(self.tam[1] + 3))
            self.images = [image.load("Assets/Obstaculo.png", size=self.tam)]
            if self.current_road == 0:
                    vel = [-3,ve]
            elif self.current_road == 2:
                    vel = [3,ve]
        else:
            vel = [0,ve]
        self.rect.move_ip(vel)

        self.current_pos = (self.current_pos[0] + vel[0], self.current_pos[1] + vel[1])

    def kill(self, objects): # remove the mosquito from the list
        if self.current_pos[1] > 600:
            objects.remove(self)
            return 10
        else:
            objects.remove(self)
            return 0



























