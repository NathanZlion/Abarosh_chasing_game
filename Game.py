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
        self.splash_screen = True
        self.chaser_score = 0
        self.chased_score = 0
        self.splash_animation_frames = []
        self.load_splash_animation_frames()  # Load animation frames

        self.CHASER = Chaser(
            game=self,
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

    def check_collisions(self):
        chaser_rect = self.CHASER.get_rect()
        chased_rect = self.CHASED.get_rect()

        if chaser_rect.colliderect(chased_rect):
            self.chaser_score += 1
            self.CHASER.reset_position()
            self.CHASED.reset_position()

        goal_safe_zone = self.safe_zones[-1]
        if chased_rect.colliderect(goal_safe_zone):
            self.chased_score += 1
            self.CHASED.reset_position()

    def draw(self):
        self.screen.fill((0, 0, 0))  # Clear screen
        for safe_zone in self.safe_zones:
            pygame.draw.rect(self.screen, GREEN, safe_zone)
        self.CHASER.draw(self.screen)
        self.CHASED.draw(self.screen)
        for obstacle in self.obstacles:
            # draw the obstacles so that they look like trees
            pygame.draw.rect(self.screen, BROWN, obstacle, 0, 20, 20, 20, 20)

        # Display scores
        font = pygame.font.SysFont("None", 36)
        chaser_score_text = font.render(
            f"Chaser Score: {self.chaser_score}", True, WHITE
        )
        chased_score_text = font.render(
            f"Chased Score: {self.chased_score}", True, WHITE
        )
        self.screen.blit(chaser_score_text, (10, 10))
        self.screen.blit(chased_score_text, (10, 50))

        pygame.display.flip()

    def load_splash_animation_frames(self):
        for i in range(0, 14):
            if i < 10:
                i = f"0{i}"

            frame = pygame.transform.scale(
                pygame.image.load(f"./images/splash{i}.png").convert_alpha(), (800, 600)
            )
            self.splash_animation_frames.append(frame)

    def show_splash_screen(self):
        frame_index = 0
        animation_delay = 100  # Delay between animation frames (in milliseconds)
        animation_timer = 0

        while self.splash_screen:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    quit()

            self.screen.fill((0, 0, 0))  # Clear screen

            # Display animation frame
            self.screen.blit(self.splash_animation_frames[frame_index], (0, 0))

            pygame.display.flip()

            # Update animation frame
            animation_timer += self.clock.get_time()
            if animation_timer >= animation_delay:
                frame_index += 1
                animation_timer = 0

            # Break out of splash screen after all frames have been displayed
            if frame_index >= len(self.splash_animation_frames):
                break

            self.clock.tick(60)  # Limit frame rate

        pygame.time.wait(2000)  # Wait for 2 seconds after animation
        self.splash_screen = False

    def run(self):
        self.show_splash_screen()

        while self.is_running:
            self.handle_events()

            if not self.splash_screen:
                self.check_collisions()
                self.draw()

            # Limit frame rate
            self.clock.tick(10)

        pygame.quit()
