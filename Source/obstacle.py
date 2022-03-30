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
        moving_direction, start_pos = self.define_spawn_pos(size)
        # sprite
        self.rect = pygame.Rect(start_pos[0], start_pos[1], size[0]//1.4, size[1]//1.4)
        self.images = [image.load("Assets/Obstaculo.png", size=size, flip=moving_direction == "right")] # load the images
        self.current_frame = 0
        self.animation_timer = 0
        

    def kill(self, objects): # remove the mosquito from the list
        objects.remove(self)
        return -OBSTACLE_PENALITY
