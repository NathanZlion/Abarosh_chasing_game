## directions
import pygame


UP = (0, -1)
RIGHT = (1, 0)
DOWN = (0, 1)
LEFT = (-1, 0)

## colors
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GREY = (128, 128, 128)
BROWN = (165, 42, 42)
WHITE = (255, 255, 255)
## speeds
CHASER_SPEED = 10
CHASED_SPEED = 8

## positions
CHASER_INITIAL_POSITION = (450, 450)
CHASED_INITIAL_POSITION = (100, 120)

# rotation
RIGHT_ROTATION = {UP: RIGHT, RIGHT: DOWN, DOWN: LEFT, LEFT: UP}
LEFT_ROTATION = {UP: LEFT, LEFT: DOWN, DOWN: RIGHT, RIGHT: UP}


# sounds
pygame.mixer.init()
loading_sound = pygame.mixer.Sound("./sounds/loading.mp3")
game_music = pygame.mixer.Sound("./sounds/conga_loop.mp3")
win_sound = pygame.mixer.Sound("./sounds/truimpth.mp3")
bump_sound = pygame.mixer.Sound("./sounds/bump_block.wav")
bump_sound.set_volume(0.6)
barrel_collision_sound = pygame.mixer.Sound("./sounds/barrel_collision.mp3")
barrel_collision_sound.set_volume(0.2)