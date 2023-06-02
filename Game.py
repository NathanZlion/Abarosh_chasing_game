# import pygame

# from player import Player
# from pygame.locals import *
# from utils import *


# class Game:
#     def __init__(self):
#         pygame.init()
#         pygame.display.set_caption("Abarosh")
#         self.screen = pygame.display.set_mode((800, 600))
#         self.clock = pygame.time.Clock()
#         self.is_running = True
#         self.CHASER = Player(
#             position=CHASER_INITIAL_POSITION,
#             color=RED,
#             speed=CHASER_SPEED,
#         )
#         self.CHASED = Player(
#             position=CHASED_INITIAL_POSITION,
#             color=BLUE,
#             speed=CHASED_SPEED,
#         )

#     def handle_events(self, key_pressed):
#         # w key
#         if key_pressed == K_w:
#             self.CHASER.move()
#         # a key
#         if key_pressed == K_a:
#             self.CHASER.rotate("left")
#         # d key
#         if key_pressed == K_d:
#             self.CHASER.rotate("right")
            
#         # up key
#         if key_pressed == K_UP:
#             self.CHASED.move()
#         # left key
#         if key_pressed == K_LEFT:
#             self.CHASED.rotate("left")
#         # right key
#         if key_pressed == K_RIGHT:
#             self.CHASED.rotate("right")

#     def draw(self):
#         self.screen.fill((0, 0, 0))  # Clear screen
#         self.CHASER.draw(self.screen)
#         self.CHASED.draw(self.screen)
#         pygame.display.flip()

#     def run(self):
#         while self.is_running:
#             for event in pygame.event.get():
#                 if event.type == QUIT:
#                     self.is_running = False
#                 elif event.type == KEYDOWN:
#                     self.handle_events(event.key)

#             keys_pressed = pygame.key.get_pressed()
#             self.handle_events(keys_pressed)
#             self.draw()
#             # self.clock.tick(60)  # Limit frame rate



#         pygame.quit()
