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


    #variables used to make a hill
    hill_position=0
    hill_velocity=0
    hill_acceleration=-0.001  #-0.001 for a downhill and 0.001 for an uphill
    hill_sharpness=5
    old_y_hill_pos=SCREEN_HEIGHT
    current_y_hill_pos=SCREEN_HEIGHT
    y_hill_pos_difference=0    
    #making a hill map
    hill_map=[]
    for i in range(HALF_SCREEN_HEIGHT):
        hill_velocity+=hill_acceleration
        hill_position+=hill_velocity*hill_sharpness
        #-0.0001 for a sharp downhill or 0.0001 for a sharp uphill
        #hill_acceleration+=0.0001    #uncomment this line if you want a sharper hill
        hill_map.append(hill_position)
    #variables used to traverse the hill
    hill_map_lenght=len(hill_map)
    hill_map_index=-1
    hill_increment=2  #this is the speed at witch we traverse the hill
    hill_direction=1
    
    
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
           hill_map_index+=hill_increment
           #if we reach the hill's end we invert it's incrementation to exit it
           if hill_map_index>=hill_map_lenght:
              hill_map_index=hill_map_lenght
              hill_increment*=-1
           #if we totally exit the hill we invert it's incrementation to enter it again
           #we also invert the hill's direction to change the way
           elif hill_map_index<-1:
              hill_increment*=-1
              hill_direction*=-1


        #draw the road
        texture_position=road_pos
        dz=0
        z=0
        old_y_hill_pos=SCREEN_HEIGHT
        current_y_hill_pos=SCREEN_HEIGHT
        screen.fill(BLUE)
        for i in range(HALF_SCREEN_HEIGHT,0,-1):
            if hill_map_index >= i:
               current_y_hill_pos=int(i+HALF_SCREEN_HEIGHT-hill_map[hill_map_index-i]*hill_direction)
            else:
               current_y_hill_pos=i+HALF_SCREEN_HEIGHT
            if current_y_hill_pos<old_y_hill_pos:
               y_hill_pos_difference=old_y_hill_pos-current_y_hill_pos
               old_y_hill_pos=current_y_hill_pos
               if texture_position<half_texture_position_threshold:
                  if y_hill_pos_difference>1:
                     for j in range(y_hill_pos_difference):
                         screen.blit(light_road,(0,current_y_hill_pos+j),(0,i,SCREEN_WIDTH,1))
                  screen.blit(light_road,(0,current_y_hill_pos),(0,i,SCREEN_WIDTH,1))
               else:
                  if y_hill_pos_difference>1:
                     for j in range(y_hill_pos_difference):
                         screen.blit(dark_road,(0,current_y_hill_pos+j),(0,i,SCREEN_WIDTH,1))
                  screen.blit(dark_road,(0,current_y_hill_pos),(0,i,SCREEN_WIDTH,1))
            dz+=ddz
            z+=dz
            texture_position+=texture_position_acceleration+z
            if texture_position>=texture_position_threshold:
               texture_position=0
        pygame.display.flip()

if __name__ == "__main__":
    main()
