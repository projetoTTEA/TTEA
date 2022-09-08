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
    light_strip=pygame.Surface((SCREEN_WIDTH,1)).convert()
    dark_strip=pygame.Surface((SCREEN_WIDTH,1)).convert()
    light_strip.fill(light_road.get_at((0,0)))
    dark_strip.fill(dark_road.get_at((0,0)))                 
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


    #variables used to make a curve
    curve_position=0
    curve_velocity=0
    curve_acceleration=0.01  #-0.01 for left curve and 0.01 for right curve
    #making a curve map
    curve_map=[]
    for i in range(HALF_SCREEN_HEIGHT):
        curve_velocity+=curve_acceleration
        curve_position+=curve_velocity
        #-0.0001 for an S-curve and 0.0001 for a sharp curve
        #curve_acceleration+=0.0001    #uncomment this line if you want a sharper curve
        curve_map.append(curve_position)
    #variables used to traverse the curve
    curve_map_lenght=len(curve_map)
    curve_map_index=-1
    curve_increment=2  #this is the speed at witch we traverse the curve
    curve_direction=1
    curve_value=0

    
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
           curve_map_index+=curve_increment
           #if we reach the curve's end we invert it's incrementation to exit it
           if curve_map_index>=curve_map_lenght:
              curve_map_index=curve_map_lenght
              curve_increment*=-1
           #if we totally exit the curve we invert it's incrementation to enter it again
           #we also invert the curve's direction to change the way
           elif curve_map_index<-1:
              curve_increment*=-1
              curve_direction*=-1


        #draw the road
        texture_position=road_pos      
        dz=0
        z=0
        screen.fill(BLUE)
        for i in range(HALF_SCREEN_HEIGHT,0,-1):
            if curve_map_index >= i:
               curve_value=curve_map[curve_map_index-i]*curve_direction
            else:
               curve_value=0
            if texture_position<half_texture_position_threshold:
               screen.blit(light_strip,(0,i+HALF_SCREEN_HEIGHT)) 
               screen.blit(light_road,(curve_value,i+HALF_SCREEN_HEIGHT),(0,i,SCREEN_WIDTH,1))
            else:
               screen.blit(dark_strip,(0,i+HALF_SCREEN_HEIGHT))
               screen.blit(dark_road,(curve_value,i+HALF_SCREEN_HEIGHT),(0,i,SCREEN_WIDTH,1))
            dz+=ddz
            z+=dz
            texture_position+=texture_position_acceleration+z
            if texture_position>=texture_position_threshold:
               texture_position=0
        pygame.display.flip()

if __name__ == "__main__":
    main()
