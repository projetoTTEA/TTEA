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
HALF_SCREEN_WIDTH=int(SCREEN_WIDTH/2)
HALF_SCREEN_HEIGHT=int(SCREEN_HEIGHT/2)


def main():
    
    pygame.init()

    #Open Pygame window
    screen = pygame.display.set_mode((640, 480),) #add RESIZABLE or FULLSCREEN
    #Title
    pygame.display.set_caption("z map road")
    #font
    font=pygame.font.SysFont('Arial', 30)

    #images
    light_road=pygame.image.load('light_road.png').convert()
    dark_road=pygame.image.load('dark_road.png').convert()

    
    #variables
    road_pos=0  #this is to remember our position on the road
    road_acceleration=10  #this is the speed at witch we traverse the road
    strip_stretch=40  #this determine how much the strips will stretch forward
    strip_length=20  #this determine how much the road will be divided into strips
    strip_length_doubled=strip_length*2  #this is used to know which road to draw from (light or dark road)
    

    #linear interpolat the road width for every y position in the road image
    #and calculate the z map with it
    offroad_color=light_road.get_at((0,0))
    road_width=light_road.get_width()
    point_1=[0,0]
    while light_road.get_at(point_1) == offroad_color:
        point_1[0]+=1
        if point_1[0] > road_width:
           break
    point_2=[road_width-1,0]
    while light_road.get_at(point_2) == offroad_color:
        point_2[0]-=1
        if point_2[0] < 0:
           break
    road_end_width=point_2[0]-point_1[0]    
    road_start_width=road_width
    road_start_y=light_road.get_height()
    road_end_y=0
    increment=(road_end_width-road_start_width)/(road_end_y-road_start_y)
    road_half_width=[]
    z_map=[]
    scaling_z_map=[]
    speed_z_map=[]
    speed_factor=(HALF_SCREEN_HEIGHT+40)/strip_stretch
    for y in range(HALF_SCREEN_HEIGHT):
        width=road_start_width+((y-road_start_y)*increment)
        road_half_width.append(int(width/2))
        z_map.append(640/width)
        scaling_z_map.append(width/640)
        speed_z_map.append(speed_factor*(width/640)**2)
    z_map_lenght=len(z_map)
   
    
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
           if road_pos>=strip_length_doubled:
              road_pos=0
        

        #draw the road
        screen.fill(BLUE)
        for i in range(HALF_SCREEN_HEIGHT-1,-1,-1):
            if (road_pos+strip_stretch*z_map[i])%strip_length_doubled>strip_length:
               screen.blit(light_road,(0,i+HALF_SCREEN_HEIGHT),(0,i,SCREEN_WIDTH,1))
            else:
               screen.blit(dark_road,(0,i+HALF_SCREEN_HEIGHT),(0,i,SCREEN_WIDTH,1))
        pygame.display.flip()

if __name__ == "__main__":
    main()
