import pygame,sys
from pygame.locals import *


BLACK=pygame.color.THECOLORS["black"]
WHITE=pygame.color.THECOLORS["white"]
RED=pygame.color.THECOLORS["red"]
GREEN=pygame.color.THECOLORS["green"]
BLUE=pygame.color.THECOLORS["blue"]
YELLOW=pygame.color.THECOLORS["yellow"]
SCREEN_WIDTH=640
SCREEN_HEIGHT=480
HALF_SCREEN_HEIGHT=int(SCREEN_HEIGHT/2)


def main():
    
    pygame.init()

    #Open Pygame window
    screen = pygame.display.set_mode((640, 480),) #add RESIZABLE or FULLSCREEN
    #Title
    pygame.display.set_caption("simple road")
    #font
    font=pygame.font.SysFont('Arial', 30)

    #images
    light_road=pygame.image.load('light_road.png').convert()
    dark_road=pygame.image.load('dark_road.png').convert()
    #variables
    texture_position=0  #this is used to draw the road
    #those variables are used to increment texture_position
    ddz=0.001
    dz=0
    z=0

    road_pos=0  #this is to remember our position on the road
    road_acceleration=80  #this is the speed at witch we traverse the road
    texture_position_acceleration=4  #this determine how much the strips will stretch forward
    texture_position_threshold=300  #this determine how much the road will be divided into strips
    half_texture_position_threshold=int(texture_position_threshold/2) #this is used to know what road to draw from (light or dark road)

    
    #pygame.key.set_repeat(400, 30)

    while True:
        #loop speed limitation
        #30 frames per second is enought
        pygame.time.Clock().tick(30)
        
        for event in pygame.event.get():    #wait for events
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                
        #Movement controls
        keys = pygame.key.get_pressed()
        if keys[K_UP]:
           road_pos+=road_acceleration
           if road_pos>=texture_position_threshold:
              road_pos=0
        

        #draw the road
        texture_position=road_pos
        dz=0
        z=0            
        screen.fill(BLUE)
        for i in range(HALF_SCREEN_HEIGHT-1,-1,-1):
            if texture_position<half_texture_position_threshold:
               screen.blit(light_road,(0,i+HALF_SCREEN_HEIGHT),(0,i,SCREEN_WIDTH,1))   
            else:
               screen.blit(dark_road,(0,i+HALF_SCREEN_HEIGHT),(0,i,SCREEN_WIDTH,1))
            dz+=ddz
            z+=dz
            texture_position+=texture_position_acceleration+z
            if texture_position>=texture_position_threshold:
               texture_position=0
        pygame.display.flip()

if __name__ == "__main__":
    main()
