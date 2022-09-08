import pygame,sys
from math import *
from pygame.locals import *

pygame.init()

BLACK=pygame.color.THECOLORS["black"]
WHITE=pygame.color.THECOLORS["white"]
BLUE=(  0,   0, 255)
GREY=(245, 245, 245)
CLOCK=pygame.time.Clock()
#Open pygame window
WIDTH,HEIGHT=640,480
screen = pygame.display.set_mode((WIDTH, HEIGHT),) #add RESIZABLE or FULLSCREEN
#Title
pygame.display.set_caption("floorcasted road")



plane_center_x=WIDTH//2
texture=pygame.image.load('stripes.png').convert()
texture=pygame.transform.scale(texture, (WIDTH,texture.get_height()))
texture2=pygame.image.load('road3.png').convert()
road_width=texture2.get_width()
road_height=texture2.get_height()
player_car=pygame.image.load('player_car.png').convert_alpha()
player_car=pygame.transform.scale(player_car, (160,82))
ground=pygame.Surface((640,240)).convert();ground.fill((0,100,0))
resolution=1
wall_hit=0
#field of view (FOV) 
fov=60
grid_height=64;grid_width=64;wall_height=64;wall_width=64
player_height=wall_height/2
player_pos=[160,224]
view_angle=90
#Dimension of the Projection Plane
projection_plane=[WIDTH, HEIGHT]
#Center of the Projection Plane
plane_center=HEIGHT//2 #[WIDTH/2, HEIGHT/2]
#distance from player to projection plane
to_plane_dist=int((WIDTH/2)/tan(radians(fov/2)))
#Angle between subsequent rays
angle_increment=fov/WIDTH
#angle of the casted ray
ray_angle=90#view_angle+(fov/2)

move_speed=15
x_move=int(move_speed*cos(radians(view_angle)))
y_move=-int(move_speed*sin(radians(view_angle)))
rotation_speed=3

pygame.key.set_repeat(400, 30)


while True:
    
    #loop speed limitation
    #30 frames per second is sufficient enough
    CLOCK.tick(30)
    
    for event in pygame.event.get():    #wait for events
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            
    #Movement controls
    keys = pygame.key.get_pressed()
 
    if keys[K_UP]:
       player_pos[0]+=x_move#;print(player_pos)
       player_pos[1]+=y_move
       if player_pos[1]<0:player_pos[1]=5000
    elif keys[K_DOWN]:
       player_pos[0]-=x_move
       player_pos[1]-=y_move
    if keys[K_LEFT]:
       view_angle+=rotation_speed
       if view_angle>359:view_angle-=360
       x_move=int(move_speed*cos(radians(view_angle)))
       y_move=-int(move_speed*sin(radians(view_angle)))               
    elif keys[K_RIGHT]:
       view_angle-=rotation_speed
       if view_angle<0:view_angle+=360
       x_move=int(move_speed*cos(radians(view_angle)))
       y_move=-int(move_speed*sin(radians(view_angle)))
                 
    """here start raycasting"""
    
    #angle of the first casted ray
    #ray_angle=view_angle+(fov/2)
    
        
    """if ray_angle<0:ray_angle+=360
    if ray_angle>359:ray_angle-=360
    if ray_angle==0:ray_angle+=0.01"""  
  
     
    #now floor-casting and ceilings
    beta=radians(view_angle-ray_angle)
    cos_beta=cos(beta)
    cos_angle=cos(radians(ray_angle))
    sin_angle=-sin(radians(ray_angle))
    #begining of floor
    #wall_bottom=slice_y+slice_height
    #begining of ceilings
    #wall_top=slice_y
    #wall_bottom=plane_center+25
    wall_bottom=HEIGHT
    #wall_top=plane_center-25
    #while wall_bottom<HEIGHT:
    while wall_bottom>plane_center+10:
        wall_bottom-=resolution
        #wall_top-=resolution
        #(row at floor point-row of center)
        row=wall_bottom-plane_center
        #straight distance from player to the intersection with the floor 
        straight_p_dist=(player_height/row*to_plane_dist)
        #true distance from player to floor
        to_floor_dist=(straight_p_dist/cos_beta)
        #coordinates (x,y) of the floor
        ray_x=int(player_pos[0]+(to_floor_dist*cos_angle))
        ray_y=int(player_pos[1]+(to_floor_dist*sin_angle))
        #the texture position
        floor_x=(ray_x%road_width);floor_y=(ray_y%road_height)
        slice_width =int(road_width/to_floor_dist*to_plane_dist)
        slice_x=(plane_center_x)-(slice_width//2);dx=slice_x
        row_slice=texture2.subsurface(0,floor_y,road_width,1)
        row_slice=pygame.transform.scale(row_slice, (slice_width,resolution))
        screen.blit(texture,(0,wall_bottom),(0,floor_y,WIDTH,resolution))
        screen.blit(row_slice,(slice_x,wall_bottom))
        screen.blit(player_car,(240,320))
        
    #measure the framerate   
    #print(CLOCK.get_fps())
    pygame.display.flip()
    screen.fill(BLUE)
    #screen.blit(ground,(0,240))
