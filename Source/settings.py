import pygame
import arquivo

WINDOW_NAME = "KARTEA"
GAME_TITLE = WINDOW_NAME

SCREEN_WIDTH, SCREEN_HEIGHT = 1920, 1000

FPS = 60
DRAW_FPS = True

# sizes
BUTTONS_SIZES = (240, 90)
HAND_SIZE = 200
HAND_HITBOX_SIZE = (60, 80)
TARGETS_SIZES = (50, 38)
TARGETS_SIZE_RANDOMIZE = (1,2) # for each new mosquito, it will multiply the size with an random value beteewn X and Y
OBSTACLE_SIZES = (50, 50)
OBSTACLE_SIZE_RANDOMIZE = (1.2, 1.5)

# drawing
DRAW_HITBOX = False  # will draw all the hitbox

# animation
ANIMATION_SPEED = 0.2 # the frame of the insects will change every X sec

# difficulty
GAME_DURATION = 120  # the game will last X sec
TARGETS_SPAWN_TIME = 1
TARGETS_MOVE_SPEED = {"min": 1, "max": 5}
OBSTACLE_PENALITY = 0  # will remove X of the score of the player (if he kills a bee)

# colors
COLORS = {"title": (38, 61, 39), "score": (38, 61, 39), "timer": (38, 61, 39),
            "buttons": {"default": (56, 67, 209), "second":  (87, 99, 255),
                        "text": (255, 255, 255), "shadow": (46, 54, 163)}}  # second is the color when the mouse is on the button

# sounds / music
MUSIC_VOLUME = 0  # value between 0 and 1
SOUNDS_VOLUME = 1

# fonts
pygame.font.init()
FONTS = {}
FONTS["small"] = pygame.font.Font(None, 40)
FONTS["medium"] = pygame.font.Font(None, 72)
FONTS["big"] = pygame.font.Font(None, 120)


