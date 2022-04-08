import pygame
import arquivo

WINDOW_NAME = "KARTEA"
GAME_TITLE = WINDOW_NAME

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

FPS = 60
DRAW_FPS = True

# sizes
BUTTONS_SIZES = (150, 45)
CAR_SIZE = 150
CAR_HITBOX_SIZE = (100, 100)
TARGETS_SIZES = (12, 12)
OBSTACLE_SIZES = (12, 12)

OBJ_POS = [(368, 80), (393, 80),(419, 80)]
"""
OBJ_POS_F = [(104, 600), (337, 600),(570, 600)]

264, 56, 151
0.5, 0.1, 0.3
"""

# drawing
DRAW_HITBOX = False  # will draw all the hitbox

# animation
ANIMATION_SPEED = 0.01 # the frame of the insects will change every X sec

# difficulty
GAME_DURATION = 120  # the game will last X sec

TARGETS_SPAWN_TIME = 10
TARGETS_MOVE_SPEED = 1
OBSTACLE_PENALITY = 0  # will remove X of the score of the player (if he kills a bee)

# colors
COLORS = {"title": (38, 61, 39), "score": (38, 61, 39),
          "timer": (38, 61, 39), "buttons": {"default": (56, 67, 209), "second":  (87, 99, 255), "text": (255, 255, 255), "shadow": (46, 54, 163)}}  # second is the color when the mouse is on the button

# sounds / music
MUSIC_VOLUME = 0  # value between 0 and 1
SOUNDS_VOLUME = 0

# fonts
pygame.font.init()
FONTS = {}
FONTS["small"] = pygame.font.Font(None, 10)
FONTS["medium"] = pygame.font.Font(None, 25)
FONTS["big"] = pygame.font.Font(None, 50)

