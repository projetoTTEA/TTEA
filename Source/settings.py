import pygame

WINDOW_NAME = "KARTEA"
GAME_TITLE = WINDOW_NAME

SCREEN_WIDTH, SCREEN_HEIGHT = 1920, 1000

FPS = 60
DRAW_FPS = True

# sizes
BUTTONS_SIZES = (300, 90)
HAND_SIZE = 350
HAND_HITBOX_SIZE = (200, 200)
TARGETS_SIZES = (300, 300)
TARGETS_SIZE_RANDOMIZE = (1,2)
OBSTACLE_SIZES = (300, 300)
OBSTACLE_SIZE_RANDOMIZE = (1.2, 1.5)

OBJ_POS = [((SCREEN_WIDTH/4)-150, -SCREEN_HEIGHT), ((SCREEN_WIDTH/2)-150, -SCREEN_HEIGHT),(3*(SCREEN_WIDTH/4)-150, -SCREEN_HEIGHT)]

# drawing
DRAW_HITBOX = False  # will draw all the hitbox

# animation
ANIMATION_SPEED = 0.01 # the frame of the insects will change every X sec

# difficulty
GAME_DURATION = 120  # the game will last X sec
TARGETS_SPAWN_TIME = 10
TARGETS_MOVE_SPEED = {"min": 2, "max": 2}
OBSTACLE_PENALITY = 0  # will remove X of the score of the player (if he kills a bee)

# colors
COLORS = {"title": (38, 61, 39), "score": (38, 61, 39), "timer": (38, 61, 39),
            "buttons": {"default": (56, 67, 209), "second":  (87, 99, 255),
                        "text": (255, 255, 255), "shadow": (46, 54, 163)}}  # second is the color when the mouse is on the button

# sounds / music
MUSIC_VOLUME = 0  # value between 0 and 1
SOUNDS_VOLUME = 0

# fonts
pygame.font.init()
FONTS = {}
FONTS["small"] = pygame.font.Font(None, 40)
FONTS["medium"] = pygame.font.Font(None, 72)
FONTS["big"] = pygame.font.Font(None, 120)

