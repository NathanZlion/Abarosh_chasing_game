import pygame
from pygame.locals import *
from Chaser import Chaser
from player import Player
from utils import *
from pygame import mixer


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

        # creating the players
        self.CHASER = Chaser(game=self, color=RED, speed=CHASER_SPEED)
        self.CHASED = Player(game=self, position=CHASED_INITIAL_POSITION, color=BLUE, speed=CHASED_SPEED)

        # play game_music
        mixer.music.load("./sounds/conga_loop.mp3")
        mixer.music.play(-1)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.is_running = False

            if event.type == KEYDOWN:
                if event.key == pygame.K_a:
                    self.CHASED.rotate("left")

                if event.key == pygame.K_d:
                    self.CHASED.rotate("right")

                if event.key == pygame.K_LEFT:
                    self.CHASER.rotate("left")

                if event.key == pygame.K_RIGHT:
                    self.CHASER.rotate("right")

        keys_pressed = pygame.key.get_pressed()  # for continuously pressed keys
        if keys_pressed[K_w]:
            self.CHASED.move()
        if keys_pressed[K_UP]:
            self.CHASER.move()

    def check_collisions(self):
        chaser_rect = self.CHASER.get_rect()
        chased_rect = self.CHASED.get_rect()

        if chaser_rect.colliderect(chased_rect):
            self.chaser_score += 1
            self.CHASER.reset_position()
            self.CHASED.reset_position()
            self.load_winner(chaser_won=True)

        goal_safe_zone = safe_zones[-1]
        if chased_rect.colliderect(goal_safe_zone):
            self.chased_score += 1
            self.CHASED.reset_position()
            self.load_winner(chaser_won=False)

    def load_splash_animation_frames(self):
        # play music
        loading_sound.play()

        for i in range(0, 14):
            if i < 10:
                i = f"0{i}"

            frame = pygame.transform.scale(
                pygame.image.load(
                    f"./images/splash_images/splash{i}.png"
                ).convert_alpha(),
                (800, 600),
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

        pygame.mixer.music.stop()
        pygame.quit()

    def load_winner(self, chaser_won=True):
        # Display winner text
        font = pygame.font.SysFont("comic", 72)
        text = "Chaser Wins!" if chaser_won else "Chased Wins!"
        text_rect = font.render(text, True, BLUE)
        text_rect_rectangle = pygame.Rect(0, 0, 0, 0)
        text_rect_rectangle.center = self.screen.get_rect().center

        # Display winner text
        self.screen.blit(text_rect, text_rect_rectangle)

        pygame.display.flip()
        pygame.mixer.music.load("./sounds/truimpth.mp3")
        pygame.mixer.music.play(start=0.0)
        pygame.time.wait(4000)
        mixer.music.load("./sounds/conga_loop.mp3")
        mixer.music.play(-1)

    def draw(self):
        self.screen.fill((0, 0, 0)) # a fallback color
        # self.screen.blit(pygame.transform.scale(pygame.image.load("./images/background_field.jpg"), (800, 600)), (0, 0))
        self.screen.blit(pygame.transform.scale(field, (800, 600)),(0, 0))
        self.__draw_top_fence()
        for safe_zone in safe_zones:
            pygame.draw.rect(self.screen, GREEN, safe_zone)
            self.screen.blit(pygame.transform.scale( house, (100, 100)),(safe_zone.x, safe_zone.y))

        self.__draw_side_fence()
        self.CHASER.draw(self.screen)
        self.CHASED.draw(self.screen)

        # show trees / obstacles
        self.__draw_obstacles()
        self.__draw_bottom_fence()
        self.__dispay_score()

        pygame.display.flip()

    def __draw_top_fence(self):
        # around the top and bottom
        for i in range(0, 800 - right_offset, fence_gap):
            self.screen.blit(pygame.transform.scale(fence_wood, (50, 50)),(i, 0))

    def __draw_side_fence(self):
        # aroung the sides
        for i in range(0, 600, fence_gap):
            self.screen.blit(pygame.transform.scale(fence_wood, (50, 50)),(0, i))
            self.screen.blit(pygame.transform.scale(fence_wood, (50, 50)),(750, i))
    
    def __draw_bottom_fence(self):
        for i in range(0, 800 - right_offset, fence_gap):
            self.screen.blit(pygame.transform.scale(fence_wood, (50, 50)),(i, 550))


    def __dispay_score(self):
        # Display scores
        font = pygame.font.SysFont("Comic Sans", 36)
        chaser_score_text = font.render(f"Chaser Score: {self.chaser_score}", True, WHITE)
        chased_score_text = font.render(f"Chased Score: {self.chased_score}", True, WHITE)
        self.screen.blit(chaser_score_text, (10, 10))
        self.screen.blit(chased_score_text, (10, 50))


    def __draw_obstacles(self):
        for circular_obstacle in obstacles:
            pygame.draw.circle(self.screen, shade, circular_obstacle.center, 25)
            self.screen.blit(pygame.transform.scale(tree, (60, 80)), (circular_obstacle.centerx - 35, circular_obstacle.centery - 60))


if __name__ == "__main__":
    game : Game = Game()
    game.run()
