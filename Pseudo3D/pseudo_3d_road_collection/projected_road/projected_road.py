import pygame,sys
from math import tan,radians,degrees,pi
from pygame.locals import *


BLACK=pygame.color.THECOLORS["black"]
WHITE=pygame.color.THECOLORS["white"]
RED=pygame.color.THECOLORS["red"]
GREEN=pygame.color.THECOLORS["green"]
LIGHT_GREEN=pygame.color.THECOLORS["lightgreen"]
DARK_GREEN=pygame.color.THECOLORS["darkgreen"]
BLUE=pygame.color.THECOLORS["blue"]
YELLOW=pygame.color.THECOLORS["yellow"]
LIGHT_GRAY=pygame.color.THECOLORS['lightgray']
DARK_GRAY=pygame.color.THECOLORS['darkgray']
SCREEN_WIDTH=640
SCREEN_HEIGHT=480
HALF_SCREEN_WIDTH=int(SCREEN_WIDTH/2)
HALF_SCREEN_HEIGHT=int(SCREEN_HEIGHT/2)


def find_segment(z,segments):
  return segments[int(z/segmentLength) % segments_list_length]


class Segment:
    def __init__(self,):
        self.point_1_x=0
        self.point_1_y=0
        self.point_1_z=0
        self.point_1_screen_x=0
        self.point_1_screen_y=0
        self.point_1_screen_scale=0
        self.point_2_x=0
        self.point_2_y=0
        self.point_2_z=0
        self.point_2_screen_x=0
        self.point_2_screen_y=0
        self.point_2_screen_y=0
        self.point_2_screen_scale=0
        self.road_half_width_1=0
        self.road_half_width_2=0
        self.edje_width_1=0
        self.edje_width_2=0
        self.line_half_width_1=0
        self.line_half_width_2=0
        self.color=0
        self.sprites=[]
    def project(self):
        #transforms 3D point1 and point2 to 2D using a perspective projection
        factor = viewing_distance / (self.point_1_z-camera_z)
        self.point_1_screen_scale=factor
        self.point_1_screen_x = int((self.point_1_x-camera_x) * factor + HALF_SCREEN_WIDTH)
        self.point_1_screen_y = int(-(self.point_1_y-camera_y) * factor + HALF_SCREEN_HEIGHT)
        self.road_half_width_1 = int(factor*half_road_width)
        self.edje_width_1=int(self.road_half_width_1/10)
        self.line_half_width_1=int(self.road_half_width_1/40)
        factor = viewing_distance / (self.point_2_z-camera_z)
        self.point_2_screen_scale=factor
        self.point_2_screen_x = int((self.point_2_x-camera_x) * factor + HALF_SCREEN_WIDTH)
        self.point_2_screen_y = int(-(self.point_2_y-camera_y) *factor + HALF_SCREEN_HEIGHT)
        self.road_half_width_2 = int(factor*half_road_width)
        self.edje_width_2=int(self.road_half_width_2/10)
        self.line_half_width_2=int(self.road_half_width_2/40)
    def draw(self,surface):
        #if self.point_1_z - camera_z > 0:
        #if the segment is not behind the camera we draw it
        if self.point_1_z > camera_z:
           x1 = self.point_1_screen_x
           x2 = self.point_2_screen_x
           y1 = self.point_1_screen_y
           y2 = self.point_2_screen_y
           #render the offroad field
           pygame.draw.polygon(surface, self.color['offroad'],
                              [(0, y1), (SCREEN_WIDTH, y1), (SCREEN_WIDTH, y2), (0, y2)], 0)
           #render the road
           w1 = self.road_half_width_1
           w2 = self.road_half_width_2
           polygon_points=[(x1 - w1, y1), (x2 - w2, y2), (x2 + w2, y2), (x1 + w1, y1)]
           pygame.draw.polygon(surface, self.color['road'], polygon_points, 0)
           #render the road's edge
           w1 = self.edje_width_1
           w2 = self.edje_width_2
           pygame.draw.polygon(surface, self.color['road_edge'],
             [polygon_points[0], (polygon_points[0][0] + w1, polygon_points[0][1]),
             (polygon_points[1][0] + w2 , polygon_points[1][1]), polygon_points[1]], 0)
           pygame.draw.polygon(surface, self.color['road_edge'],
             [polygon_points[3], (polygon_points[3][0] - w1, polygon_points[3][1]),
             (polygon_points[2][0] - w2, polygon_points[2][1]), polygon_points[2]], 0)
           #render the road's line
           if self.color['road_line']:
              w1 = self.line_half_width_1
              w2 = self.line_half_width_2
              pygame.draw.polygon(surface, self.color['road_line'],
                [(x1 - w1, y1), (x2 - w2, y2), (x2 + w2, y2), (x1 + w1, y1)], 0)
           #drawing the sprites
           for sprite in self.sprites:
               #if the sprite is not too close we draw it
               if self.point_1_z - camera_z > 50:
                  scaled_width=int(sprite['width'] * self.point_1_screen_scale)
                  scaled_height=int(sprite['height'] * self.point_1_screen_scale)
                  scaled_sprite=right_sprite=pygame.transform.scale(sprite['image'],(scaled_width,scaled_height))
                  #if the sprite is far away make it transparent 
                  if self.point_1_z - camera_z > 400:
                     scaled_sprite.set_alpha(50)
                  flipped_sprite=pygame.transform.flip(scaled_sprite, True, False)
                  x=int((self.point_1_screen_x))
                  screen.blit(scaled_sprite,(x,self.point_1_screen_y-scaled_height))
                  screen.blit(flipped_sprite,(x-scaled_width,self.point_1_screen_y-scaled_height))


def main():
    
    pygame.init()
    
    global camera_x, camera_y, camera_z, viewing_distance, half_road_width, screen
    
    #Open Pygame window
    screen = pygame.display.set_mode((640, 480),) #add RESIZABLE or FULLSCREEN
    #Title
    pygame.display.set_caption("projected road")
    #font
    font=pygame.font.SysFont('Arial', 30)

    #images
    right_tree=pygame.image.load('tree.png').convert()#.convert_alpha()
    left_tree=pygame.transform.flip(right_tree, True, False)
    bike=pygame.image.load('hang-on.png').convert()
    bike.set_colorkey(bike.get_at((0,0)))
    bike=bike.subsurface(0, 0, 33, 74)
    bike=pygame.transform.scale(bike, (bike.get_width()*2, bike.get_height()*2))                  
    #variables
    camera_x=0
    camera_y=15
    camera_z=0.1  #-45.1
    field_of_view=60
    viewing_distance=HALF_SCREEN_WIDTH/tan(radians(field_of_view/2))
    light_color={'road':LIGHT_GRAY, 'offroad':LIGHT_GREEN, 'road_edge':RED, 'road_line':WHITE}
    dark_color={'road':DARK_GRAY, 'offroad':DARK_GREEN, 'road_edge':WHITE, 'road_line':None}
    half_road_width=28
    segment_length=20
    
    #making the road segments
    segments=[]
    for i in range(50):
        s=Segment()
        s.point_1_z=i*segment_length
        s.point_2_z=s.point_1_z+segment_length
        s.color=dark_color if i%2 else light_color
        s.project()
        if not i%6:  #change the value after '%' sign if you want more or less sprites
           sprite={'image':right_tree, 'width':int(right_tree.get_width()/4),
                   'height':int(right_tree.get_height()/4), 'offset':2, 'side':1}
           s.sprites.append(sprite)
        segments.append(s)
    segments.sort(key=lambda s:s.point_1_z, reverse=True)
    last_segment_z=segments[int(len(segments)/2)].point_1_z
    draw_distance=int((len(segments)/2)*segment_length)
    

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
           #we move forward
           camera_z+=12
           #if we cross the last segment we go back to the beginning
           if last_segment_z < camera_z:
              camera_z-=last_segment_z
           for s in segments: #projects the segments only if we move the camera
               s.project()
        elif keys[K_DOWN]:
           #move back
           camera_z-=10
           for s in segments:
               s.project()
        if keys[K_d]:
           #move up
           camera_y+=1
           for s in segments:
               s.project()
        elif keys[K_c]:
           #move down
           camera_y-=1
           for s in segments:
               s.project()
        if keys[K_v]:
           #move right
           camera_x+=1
           for s in segments:
               s.project()
        elif keys[K_x]:
           #move left
           camera_x-=1
           for s in segments:
               s.project()               


           
        #draw the road 
        screen.fill(BLUE);k=0      
        for s in segments:
            #if segment within drawing distance we draw it
            distance = s.point_2_z-camera_z
            if distance  < draw_distance and distance > 0:
               s.draw(screen)
        screen.blit(bike,(285, 300))
        pygame.display.flip()
        
if __name__ == "__main__":
    main()
