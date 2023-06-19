import pygame
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
        self.__load_splash_animation_frames()  # Load animation frames

        # creating the players
        self.CHASER = Chaser(game=self, color=RED, speed=CHASER_SPEED)
        self.CHASED = Player(game=self, position=CHASED_INITIAL_POSITION, color=BLUE, speed=CHASED_SPEED)

        # play game_music
        game_music.play()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.is_running = False

        keys_pressed = pygame.key.get_pressed()  # for continuously pressed keys

        if keys_pressed[pygame.K_w]:
            self.CHASED.move(UP)

        if keys_pressed[pygame.K_s]:
            self.CHASED.move(DOWN)

        if keys_pressed[pygame.K_a]:
            self.CHASED.move(LEFT)

        if keys_pressed[pygame.K_d]:
            self.CHASED.move(RIGHT)

        if keys_pressed[pygame.K_UP]:
            self.CHASER.move(UP) 

        if keys_pressed[pygame.K_DOWN]:
            self.CHASER.move(DOWN)

        if keys_pressed[pygame.K_LEFT]:
            self.CHASER.move(LEFT)

        if keys_pressed[pygame.K_RIGHT]:
            self.CHASER.move(RIGHT)

    def check_collisions(self):
        chaser_rect = self.CHASER.get_rect()
        chased_rect = self.CHASED.get_rect()
        

        # chaser wins
        if chaser_rect.colliderect(chased_rect):
            self.chaser_score += 1
            self.CHASER.reset_position()
            self.CHASED.reset_position()
            self.load_winner(chaser_won=True)

        
        if chased_rect.colliderect(goal_zone):
            self.chased_score += 1
            self.CHASED.reset_position()
            self.load_winner(chaser_won=False)

    def __load_splash_animation_frames(self):
        # play music
        loading_sound.play()

        for i in range(0, 14):
            if i < 10:
                i = f"0{i}"

            frame = pygame.transform.scale(
                pygame.image.load(f"./images/splash_images/splash{i}.png").convert_alpha(),(800, 600))
            self.splash_animation_frames.append(frame)

    def show_splash_screen(self):
        frame_index = 0
        animation_delay = 125  # Delay between animation frames (in milliseconds)
        animation_timer = 0

        while self.splash_screen:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

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

        pygame.time.wait(1800)  # Wait for 2 seconds after animation
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

        game_music.stop()
        winning_sound.play()
        pygame.time.wait(4000)

        winning_sound.stop()
        game_music.play()


    def draw(self):
        self.screen.fill((0, 0, 0)) # a fallback color

        self.screen.blit(pygame.transform.scale(field, (800, 600)),(0, 0)) # background field image
        self.__draw_top_fence()
        self.__draw_safe_zones()
        self.__draw_side_fence()


        self.__draw_tree_shadows()
        self.__draw_player_shadow(self.CHASER)
        self.CHASER.draw(self.screen)
        self.__draw_player_shadow(self.CHASED)
        self.CHASED.draw(self.screen)

        # show trees / obstacles
        self.__draw_obstacles()
        self.__draw_bottom_fence()
        self.__dispay_panel()

        pygame.display.flip()

    def __draw_safe_zones(self):
        for index in range(len(safe_zones)-1):
            safe_zone = safe_zones[index]
            # shrink the safe zone by 5 pixels on each side
            safe_zone = safe_zone.inflate(-25, -25)
            pygame.draw.rect(self.screen, BROWN, safe_zone)    # brown background
            pygame.draw.rect(self.screen, BLUE, safe_zone, 5)  # blue border
            self.screen.blit(pygame.transform.scale( house, (100, 100))
                             ,(safe_zone.x, safe_zone.y)) # house
        
        # for the bottom right corner show the goal
        self.screen.blit(pygame.transform.scale( goal, (50, 50)),(700, 500))
        # show text in blue saying "GOAL" on top of the goal
        font = pygame.font.SysFont("comic", 24)
        text = "GOAL"
        text_rect = font.render(text, True, BLUE)
        text_rect_rectangle = pygame.Rect(0, 0, 0, 0)
        text_rect_rectangle.center = (725, 525)
        self.screen.blit(text_rect, text_rect_rectangle)


    def __draw_top_fence(self):
        # around the top and bottom
        for i in range(0, 800 - right_offset, fence_gap):
            self.screen.blit(pygame.transform.scale(fence_wood, (50, 50)),(i, 0))
            # rectangular shadow
            shadow = pygame.Surface((15, 5))
            # rotate the shadow 45 degrees
            shadow = pygame.transform.rotate(shadow, 45)
            shadow.set_alpha(100)
            shadow.fill((0, 0, 0))
            self.screen.blit(shadow, (i, 0))

    def __draw_side_fence(self):
        # aroung the sides
        for i in range(0, 600, fence_gap):
            self.screen.blit(pygame.transform.scale(fence_wood, (50, 50)),(0, i))
            self.screen.blit(pygame.transform.scale(fence_wood, (50, 50)),(750, i))
            # rectangular shadow
            shadow = pygame.Surface((15, 5))
            shadow = pygame.transform.rotate(shadow, 45)
            shadow.set_alpha(100)
            shadow.fill((0, 0, 0))
            self.screen.blit(shadow, (0, i))
            self.screen.blit(shadow, (750, i))

    
    def __draw_bottom_fence(self):
        for i in range(0, 800 - right_offset, fence_gap):
            self.screen.blit(pygame.transform.scale(fence_wood, (50, 50)),(i, 550))
            # rectangular shadow
            shadow = pygame.Surface((15, 5))
            shadow = pygame.transform.rotate(shadow, 45)
            shadow.set_alpha(100)
            shadow.fill((0, 0, 0))
            self.screen.blit(shadow, (i, 550))


    def __dispay_panel(self):
        # Display scores
        font = pygame.font.SysFont("Comic Sans", 30)
        chaser_score_text = font.render(f"Chaser Score: {self.chaser_score}", True, WHITE)
        chased_score_text = font.render(f"Chased Score: {self.chased_score}", True, WHITE)
        self.screen.blit(chaser_score_text, (5, 5))
        self.screen.blit(chased_score_text, (5, 50))

        # display controls
        font = pygame.font.SysFont("Comic Sans", 15)
        controls_text = font.render("Chaser Controls: WASD, Chased Controls: Arrow Keys, ESC to quit", True, WHITE)
        controls_text_area = controls_text.get_rect()
        controls_text_area.center = ( self.screen.get_rect().width //2 + 70 , 25)
        self.screen.blit(controls_text, controls_text_area)


    def __draw_obstacles(self):
        for circular_obstacle in obstacles:
            self.screen.blit(pygame.transform.scale(tree, (60, 80)), (circular_obstacle.centerx - 35, circular_obstacle.centery - 60))

    def __draw_tree_shadows(self):
        for circular_obstacle in obstacles:
            shadow_radius = 25
            shadow = pygame.Surface((shadow_radius * 2, shadow_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(shadow, (0, 0, 0, 100), (shadow_radius, shadow_radius), shadow_radius)
            self.screen.blit(shadow, (circular_obstacle.centerx - shadow_radius, circular_obstacle.centery - shadow_radius))

    def __draw_player_shadow(self, player: Player):
        shadow_radius = 12
        shadow = pygame.Surface((shadow_radius * 2, shadow_radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(shadow, (0, 0, 0, 100), (shadow_radius, shadow_radius), shadow_radius)
        self.screen.blit(shadow, (player.position[0] - shadow_radius, player.position[1] - shadow_radius))
