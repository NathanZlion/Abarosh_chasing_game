import pygame
from pygame.locals import *
from Chaser import Chaser
from player import Player
from utils import *


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Abarosh")
        self.WIDTH = 800
        self.HEIGHT = 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()
        self.is_running = True
        self.CHASER = Chaser(
            game=self,
            position=CHASER_INITIAL_POSITION,
            color=RED,
            speed=CHASER_SPEED,
        )

        self.CHASED = Player(
            game=self,
            position=CHASED_INITIAL_POSITION,
            color=BLUE,
            speed=CHASED_SPEED,
        )

        self.safe_zones = [
            pygame.Rect(0, 0, 150, 150),
            pygame.Rect(0, 450, 150, 150),
            pygame.Rect(650, 0, 150, 150),
            pygame.Rect(650, 450, 150, 150),
        ]

        self.obstacles = [
            pygame.Rect(100, 300, 50, 50),
            pygame.Rect(100, 400, 50, 50),
            # pygame.Rect(200, 100, 50, 50),
            pygame.Rect(200, 200, 50, 50),
            pygame.Rect(200, 300, 50, 50),
            pygame.Rect(200, 400, 50, 50),
            pygame.Rect(300, 100, 50, 50),
            pygame.Rect(300, 200, 50, 50),
            pygame.Rect(300, 300, 50, 50),
            pygame.Rect(300, 400, 50, 50),
            pygame.Rect(400, 100, 50, 50),
            pygame.Rect(400, 200, 50, 50),
            pygame.Rect(400, 300, 50, 50),
            pygame.Rect(400, 400, 50, 50),
            pygame.Rect(500, 100, 50, 50),
            pygame.Rect(500, 200, 50, 50),
            pygame.Rect(500, 300, 50, 50),
            pygame.Rect(500, 400, 50, 50),
            # pygame.Rect(600, 100, 50, 50),
            pygame.Rect(600, 200, 50, 50),
            pygame.Rect(600, 300, 50, 50),
            # pygame.Rect(600, 400, 50, 50),
            # pygame.Rect(700, 100, 50, 50),
            # pygame.Rect(700, 200, 50, 50),
            # pygame.Rect(700, 300, 50, 50),
            # pygame.Rect(700, 400, 50, 50),

        ]

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.is_running = False

        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[K_w]:
            self.CHASER.move()
        if keys_pressed[K_a]:
            self.CHASER.rotate("left")
        if keys_pressed[K_d]:
            self.CHASER.rotate("right")
        if keys_pressed[K_UP]:
            self.CHASED.move()
        if keys_pressed[K_LEFT]:
            self.CHASED.rotate("left")
        if keys_pressed[K_RIGHT]:
            self.CHASED.rotate("right")

    def draw(self):
        self.screen.fill((0, 0, 0))  # Clear screen
        for safe_zone in self.safe_zones:
            pygame.draw.rect(self.screen, GREEN, safe_zone)
        self.CHASER.draw(self.screen)
        self.CHASED.draw(self.screen)
        for obstacle in self.obstacles:
            # draw the obstacles so that they look like trees
            pygame.draw.rect(self.screen, BROWN, obstacle, 0, 20, 20, 20, 20)


        pygame.display.flip()

    def run(self):
        while self.is_running:
            self.handle_events()
            self.draw()
            self.clock.tick(10)  # Limit frame rate

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
