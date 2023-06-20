import pygame

## directions
UP = (0, -1)
RIGHT = (1, 0)
DOWN = (0, 1)
LEFT = (-1, 0)

## colors
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GRAY = (128, 128, 128)
BROWN = (165, 42, 42)
WHITE = (255, 255, 255)
shade = (0, 0, 0, 1)

## speeds
CHASER_SPEED = 10
CHASED_SPEED = 8

## positions
CHASER_INITIAL_POSITION = (450, 450)
CHASED_INITIAL_POSITION = (100, 120)

# sounds
pygame.mixer.init()
loading_sound = pygame.mixer.Sound("./sounds/loading.mp3")
loading_sound.set_volume(0.2)
game_music = pygame.mixer.Sound("./sounds/conga_loop.mp3")
game_music.set_volume(0.2)
winning_sound = pygame.mixer.Sound("./sounds/truimpth.mp3")
winning_sound.set_volume(0.2)
bump_sound = pygame.mixer.Sound("./sounds/bump_block.wav")
bump_sound.set_volume(0.6)
barrel_collision_sound = pygame.mixer.Sound("./sounds/barrel_collision.mp3")
barrel_collision_sound.set_volume(0.2)


# images
tree = pygame.image.load("./images/tree.png")
house = pygame.image.load("./images/house.png")
fence_wood = pygame.image.load("./images/one_fence.png")
field = pygame.image.load("./images/grass_field.png")
goal = pygame.image.load("./images/target.png")
char1_left = pygame.transform.scale(pygame.image.load("./images/char1_left.png"), (40,40))
char1_right = pygame.transform.scale(pygame.image.load("./images/char1_right.png"), (40,40))
char1_up = pygame.transform.scale(pygame.image.load("./images/char1_up.png"), (40,40))
char1_down = pygame.transform.scale(pygame.image.load("./images/char1_down.png"), (40,40))
char2_left = pygame.transform.scale(pygame.image.load("./images/char2_left.png"), (40,40))
char2_right = pygame.transform.scale(pygame.image.load("./images/char2_right.png"), (40,40))
char2_up = pygame.transform.scale(pygame.image.load("./images/char2_up.png"), (40,40))
char2_down = pygame.transform.scale(pygame.image.load("./images/char2_down.png"), (40,40))



# game settings
fence_gap = 30
top_offset = 50
bottom_offset = 20
left_offset = 30
right_offset = 30

# safe_zones
safe_zones = [
    pygame.Rect(left_offset, top_offset, 150, 150),  # top left
    pygame.Rect(left_offset, 450 - bottom_offset, 150, 150),  # bottom left
    pygame.Rect(650 - right_offset, top_offset, 150, 150),  # top right
    pygame.Rect(650 - right_offset, 450 - bottom_offset, 150, 150),  # bottom right
]

goal_zone = pygame.Rect(700 - right_offset, 500 - bottom_offset, 35, 80)  # bottom right corner goal state

# obstacles meaning trees
obstacles = [
    pygame.Rect(100, 230, 50, 50),
    pygame.Rect(200, 230, 50, 50),
    pygame.Rect(200, 400, 50, 50),
    pygame.Rect(370, 100, 50, 50),
    pygame.Rect(300, 200, 50, 50),
    pygame.Rect(300, 300, 50, 50),
    pygame.Rect(400, 100, 50, 50),
    pygame.Rect(400, 200, 50, 50),
    pygame.Rect(406, 400, 50, 50),
    pygame.Rect(456, 400, 50, 50),
    pygame.Rect(500, 300, 50, 50),
    pygame.Rect(500, 300, 50, 50),
    pygame.Rect(500, 400, 50, 50),
    pygame.Rect(600, 200, 50, 50),
]

# menus count
MAIN_MENU_COUNT = 2
PAUSE_MENU_COUNT = 3
