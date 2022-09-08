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
    pygame.display.set_caption("simple road")
    #font
    font=pygame.font.SysFont('Arial', 30)

    #images
    light_road=pygame.image.load('light_road.png').convert()
    dark_road=pygame.image.load('dark_road.png').convert()
    palm_tree=pygame.image.load('palm_tree.png').convert()
    bush=pygame.image.load('bush.png').convert()
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


    z_map=[]
    scaling_z_map=[]
    scale_down_factor=1/20
    y_world=-10  #change this value if the sprites moves wrongly
    dist=554.2562584220408  #HALF_SCREEN_WIDTH/tan(radians(fov/2)))
    #making the z map
    for i in range(HALF_SCREEN_HEIGHT-1,-1,-1):
        #Z = Y_world / (Y_screen - (height_screen / 2))
        y_screen = i
        #z=(y_world*dist)/(y_screen - HALF_SCREEN_HEIGHT)                
        z = y_world / (y_screen - HALF_SCREEN_HEIGHT)
        z_map.append(z)
        scaling_z_map.append(1/z*scale_down_factor)
    z_map_lenght=len(z_map)
    speed_z_map=z_map.copy()
    speed_z_map.reverse()

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
    for y in range(HALF_SCREEN_HEIGHT):
        width=road_start_width+((y-road_start_y)*increment)
        road_half_width.append(int(width/2))
        z_map.append(road_start_width/width)
        scaling_z_map.append(width/road_start_width)
        speed_z_map.append((width/road_start_width)/6)
    

    sprites=[{'image':bush, 'scaled_image':None, 'track_pos':10 ,'pos':[0,0],
              'width':bush.get_width(), 'height':bush.get_height(),
              'side':'right', 'scaled_width':0, 'scaled_height':0, 'mirrored':True},
             {'image':palm_tree, 'scaled_image':None, 'track_pos':40 ,'pos':[0,0],
              'width':palm_tree.get_width(), 'height':palm_tree.get_height(),
              'side':'right', 'scaled_width':0, 'scaled_height':0, 'mirrored':True},
             {'image':bush, 'scaled_image':None, 'track_pos':70 ,'pos':[0,0],
              'width':bush.get_width(), 'height':bush.get_height(),
              'side':'right', 'scaled_width':0, 'scaled_height':0, 'mirrored':True},
             {'image':palm_tree, 'scaled_image':None, 'track_pos':100 ,'pos':[0,0],
              'width':palm_tree.get_width(), 'height':palm_tree.get_height(),
              'side':'right', 'scaled_width':0, 'scaled_height':0, 'mirrored':True}]
   
    
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
           for sprite in sprites:
               sprite['track_pos']+=road_acceleration*speed_z_map[int(sprite['track_pos'])]
               if sprite['track_pos'] > z_map_lenght:
                  sprite['track_pos']=10
                  sprites.insert(0, sprites.pop())
        

        #draw the road
        texture_position=road_pos      
        dz=0
        z=0
        screen.fill(BLUE)
        texture_position=road_pos
        for i in range(HALF_SCREEN_HEIGHT-1,-1,-1):
            if texture_position < half_texture_position_threshold:
               screen.blit(light_road,(0,i+HALF_SCREEN_HEIGHT),(0,i,SCREEN_WIDTH,1))
            else:
               screen.blit(dark_road,(0,i+HALF_SCREEN_HEIGHT),(0,i,SCREEN_WIDTH,1))
            for sprite in sprites:
                if int(sprite['track_pos'])==i:
                   sprite['scaled_width']=int(sprite['width']*scaling_z_map[i])
                   sprite['scaled_height']=int(sprite['height']*scaling_z_map[i])
                   sprite['scaled_image']=pygame.transform.scale(sprite['image'], (sprite['scaled_width'], sprite['scaled_height']))
                   if sprite['side']=='right':
                      sprite['pos'][0]=HALF_SCREEN_WIDTH+road_half_width[i]
                      sprite['pos'][1]=i+HALF_SCREEN_HEIGHT-sprite['scaled_height']
                   elif sprite['side']=='left':
                      sprite['scaled_image']=pygame.transform.flip(sprite['scaled_image'], True, False)
                      sprite['pos'][0]=HALF_SCREEN_WIDTH-road_half_width[i]-sprite['scaled_width']
                      sprite['pos'][1]=i+HALF_SCREEN_HEIGHT-sprite['scaled_height']
            dz+=ddz
            z+=dz
            texture_position+=texture_position_acceleration+z
            if texture_position>=texture_position_threshold:
               texture_position=0
        for sprite in sprites:
            screen.blit(sprite['scaled_image'],sprite['pos'])
            if sprite['mirrored']:
               if sprite['side']=='right':
                  sprite['pos'][0]=HALF_SCREEN_WIDTH-road_half_width[int(sprite['track_pos'])]-sprite['scaled_width']
               elif sprite['side']=='left':
                  sprite['pos'][0]=HALF_SCREEN_WIDTH+road_half_width[int(sprite['track_pos'])]
               sprite['scaled_image']=pygame.transform.flip(sprite['scaled_image'], True, False)       
               screen.blit(sprite['scaled_image'],sprite['pos'])
        pygame.display.flip()

if __name__ == "__main__":
    main()
