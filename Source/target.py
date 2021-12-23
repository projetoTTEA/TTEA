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
        moving_direction, start_pos = self.define_spawn_pos(size)
        # sprite
        self.rect = pygame.Rect(start_pos[0], start_pos[1], size[0]//1.4, size[1]//1.4)
        self.images = [image.load("Assets/mosquito/Star.png", size=size, flip=moving_direction == "right")]
        self.current_frame = 0
        self.animation_timer = 0


    def define_spawn_pos(self, size): # define the start pos and moving vel of the mosquito
        vel = random.uniform(TARGETS_MOVE_SPEED["min"], TARGETS_MOVE_SPEED["max"])
        moving_direction = "down"
        start_pos = (random.randint(size[0], SCREEN_WIDTH-size[0]), -size[1])
        self.vel = [0, vel]
        return moving_direction, start_pos


    def move(self):
        self.rect.move_ip(self.vel)


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


    def kill(self, mosquitos): # remove the mosquito from the list
        mosquitos.remove(self)
        return 1
